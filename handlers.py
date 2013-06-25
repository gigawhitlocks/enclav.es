import tornado.auth
import tornado.autoreload
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from bulbs.titan import Graph
from bulbs.config import Config

from jinja2 import Environment, FileSystemLoader

from users import Invitee, User, Invited, Identity, Is
from posts import Post, PostedTo, PostedBy
from enclaves import Enclave, Moderates, Owns

from hashing_passwords import make_hash as generate_storable_password,\
        check_hash
import smtplib
from email.parser import Parser

import riak
import uuid
import time

import functools

class EnclavesHandler(tornado.web.RequestHandler):
    # db config
    conf = Config("http://127.0.0.1:8182/graphs/graph")
    graph = Graph(config=conf)
    riak_client = riak.RiakClient(port=8087, \
            transport_class=riak.RiakPbcTransport)



    #indices

    if len(graph.client.get_vertex_keys().content["results"]) == 0:
        # add new indices to this list if you want them created
        # comment them out when you need to add them
        # if they already exist, 
        # and uncomment any commented ones any time you reload the db

        for new_index in ['userid',
                'invitee', 
                'enclave',
                'title',
                'name',
                'handle',
                'email',
                'token',
                'created',
                'element_type']:

            graph.client.create_vertex_key_index(new_index)


    # objects
    graph.add_proxy("invitees", Invitee)
    graph.add_proxy("users",User)
    graph.add_proxy("identities",Identity)
    graph.add_proxy("posts",Post)
    graph.add_proxy("enclaves", Enclave)
  
    #relationships
    graph.add_proxy("posted_by", PostedBy)
    graph.add_proxy("posted_to", PostedTo)
    graph.add_proxy("invited", Invited)
    graph.add_proxy("Is", Is)
    graph.add_proxy("moderates", Moderates)
    graph.add_proxy("owns", Owns)

    # TODO: put first-run setup in its own file that isn't called
    # sofa king much   graph.add_proxy("owns", Owns)

    # create a 'root' dummy user to start the user tree, 
    # so that every user (except this one) will have an Invited relationship
    if (graph.users.index.lookup(userid="root") is None):
        graph.users.create(userid="root",\
                password=generate_storable_password("password"))  

        # create special "all" enclave if it doesn't exist.
        if (graph.enclaves.index.lookup(name="all") is None):
            All = graph.enclaves.create(name="all", tagline="all enclaves")
            graph.owns.create(graph.users.index.lookup(userid="root"),All)
                

    graph.scripts.update("traversals.groovy")
    env = Environment(loader=FileSystemLoader('templates'),\
            extensions=['jinja2.ext.loopcontrols'])


    def render_template(self, template_name, **kwargs):
        """
        Shorthand for rendering templates (pretty self-explanatory)
        **kwargs is used for passing key=value variables to the template for 
        rendering as {{variable}} in jinja2
        """
        args = {}
        for key in kwargs:
            if kwargs[key]:
                args[key] = kwargs[key]

        self.write(self.env.get_template(template_name).render(**args))

    def get_current_user(self):
        """
        Looks up the current user as stored in a cookie in the Graph
        """
        return self.graph.users.get(int(self.get_secure_cookie('eid')))

    def get_identities(self):
      """Returns a generator that will provide 
      all identities for the current user"""
      return self.get_current_user().outV("is")

    def is_logged_in(self):
        """
        Checks to see if a user is logged in.
        """
        return self.get_secure_cookie("userid") != None


    def forbidden(self):
        """
        Use for throwing a 403 when a user does something that is not permitted
        """
        self.clear()
        self.set_status(403)
        self.finish("<html><body><h3>403 That is not \
                permitted</h3></body></html>")

    def get_poster(self, post):
        """ returns the poster of post """
        # .next() is safe here because any post will only have one poster
        return self.graph.gremlin.query(\
                self.graph.scripts.get('getNeighboringVertices'),
                dict(_id=post.eid,relationship="posted_by",\
                        direction="out")).next()

    @staticmethod
    def require_login(function, *args, **kwargs):
        """
        Use as a decorator around functions that require the user be logged in
        """
        @functools.wraps(function)
        def new_function(self, *args, **kwargs):
            if (not self.is_logged_in()):
                self.forbidden()
            function(self, *args, **kwargs)
        return new_function

    @staticmethod
    def int_time(hours_ago=0, minutes_ago=0, hours_ahead=0, minutes_ahead=0):
        """Returns time as an int for use as a timestamp in riak
            Use any combo of keyword args for easy offsets. Returns time as
            millionths of seconds since Unix epoch"""
        return int((time.time()+60*(minutes_ahead-minutes_ago)\
                +3600*(hours_ahead-hours_ago))*10**6) 


class LandingPageHandler(EnclavesHandler):
    """
    LandingPageHandler handles all requests sent to the root of the domain.
    This means displaying a login page when no user is logged in and the home 
    page for logged in users.

    It also handles POST requests sent to the root,
    which is where logins are handled.
    """

    def get(self):
        """
        Handles requests to the root of the site when visiting normally
        (GET requests)
        """
        if(not self.is_logged_in()):
            self.render_template("landingpage.html")

        else:
            posts=[]
            i=0
            try:
                for post in self.graph.posts.get_all():
                    if i > 20:
                        break
                    else:
                        i+=1
                        posts.append([post, self.get_poster(post).handle])
            except TypeError: #happens when self.graph.posts.get_all is None
                pass

            enclaves=[]
            i=0
            for enclave in self.graph.enclaves.get_all():
               enclaves.append(enclave)

            self.render_template('content.html', posts=posts, enclaves=enclaves)

    def post(self):
        """
        # handles POST requests sent to /
        # Generally these are login requests
        """
        if ( not self.is_logged_in() ):
            # open database and look up input username
            self.set_header("Content-Type", "text/html")
            user = self.graph.users.index.lookup(\
                    userid=self.get_argument("username")) 
            if ( user is None ):
                self.render_template("landingpage.html",\
                        error_message="Username or password was incorrect.\n")
            else :
                
                user = user.next()
                # check that password is correct
                if check_hash(self.get_argument("password"),user.password):
                    # save the session cookie
                    self.set_secure_cookie("userid", user.userid)
                    self.set_secure_cookie("eid", str(user.eid))
                    self.redirect("/")
                else:
                  self.render_template("landingpage.html",\
                          error_message="Username or password was incorrect.\n")

class LogoutHandler(EnclavesHandler):
    """
    Destroys existing sessions
    Send a GET to /logout to trigger this Handler
    """
    def get(self):
        self.clear_cookie("userid")
        self.clear_cookie("eid")
        self.redirect("/")

class InviteHandler(EnclavesHandler):
    """
    Handler for sending out invitation emails.
    """
    @EnclavesHandler.require_login  
    def get(self):
        """
        This loads the invitation creation dialog, 
        for existing users to send invitations
        """
        self.render_template("invite.html")


    @EnclavesHandler.require_login  
    def post(self):
        """
        This actually sends out the email when the existing user clicks 'send'
        """

        currentinvitee = self.graph.invitees.index.lookup(\
                email=self.get_argument("email"))

        # check to see if this email has already been invited. 
        # If it has, remove all of its previos occurrences
        if ( currentinvitee is not None ):
            for current in currentinvitee:
                self.graph.invitees.delete(current.eid)


        #creates an Invitee object with the given email and a generated uuid
        currentinvitee = self.graph.invitees.create(
                                            email=self.get_argument("email"), 
                                            token=uuid.uuid4().hex)
                                        #TODO: Does this need to be more secure?

        currentuser = self.graph.users.index.lookup(\
                userid=self.get_secure_cookie("userid")).next()

        self.graph.invited.create(currentuser, currentinvitee)

        ## build the email and send it. SMTP host is localhost for now.
        s = smtplib.SMTP('localhost')
        headers = Parser().parsestr('From: <noreply@enclav.es)\n'
        'To: <'+ self.get_argument("email") +'>\n'
        'Subject: You have been invited to enclav.es\n'
        '\n'
        ## TODO: Write out a better invite email
        'Click here to accept the invitation: http://enclav.es/sign-up?token='\
                +currentinvitee.token+'\n')

        s.sendmail(headers['from'],[headers['to']],headers.as_string())
        self.redirect("/invite")

class SignUpHandler(EnclavesHandler):
    """
    This route handles incoming new users sent from 
    their email to sign-up/?token=[generated token]
    """

    def get(self):
        """This checks to make sure the provided token is valid"""
        currentinvitee = self.graph.invitees.index.lookup(\
                token=self.get_argument("token"))
        if ( currentinvitee is None ) :
            self.redirect("/")
        else:
            ## If the token is valid load the new user form
            self.set_secure_cookie("token",self.get_argument("token"))
            self.render_template("sign-up.html")
            ## TODO: also check expiry on token


    def post(self):
        """This processes the new user form and creates 
        the new user if the username isn't taken already"""
        
        invitee = self.graph.invitees.index.lookup(\
                token=self.get_secure_cookie("token"))

        if (invitee is None):
            self.forbidden()
        else:
            newuser = self.graph.identities.index.lookup(\
                    handle=self.get_argument("userid"))

            if newuser is not None:
                self.render_template(\
                        "sign-up.html", error_message="That handle is taken.")
            else:
                newuser = self.graph.users.create(
                        userid=self.get_argument("userid"),
                        password=generate_storable_password(\
                                self.get_argument("password")))
                

                get_inviter = self.graph.scripts.get('getInviter')
                inviter = self.graph.gremlin.query(\
                        get_inviter, dict(_id=invitee.next().eid)).next()
                self.graph.invited.create(inviter,newuser)

                # creates an Identity with the same name as the initial username
                self.graph.Is.create(newuser,\
                        self.graph.identities.create(handle=newuser.userid))
                
                self.clear_cookie("token")
                self.clear_cookie("userid")
                self.clear_cookie("eid")
                for i in invitee:
                    self.graph.invitees.delete(i.eid)

                self.redirect("/")

class NewPostHandler(EnclavesHandler):
    """Handles creation of new posts"""
    
    @EnclavesHandler.require_login
    def get(self):

        curr_enclave=self.request.uri.split("/")[1][1:] \
                if self.request.uri[0:2] == "/~" else None

        self.render_template("new_post.html",\
                identities=[i.handle for i in self.get_identities()],
                enclave=curr_enclave)

    @EnclavesHandler.require_login
    def post(self):

        
        curr_enclave=self.request.uri.split("/")[1][1:] \
                if self.request.uri[0:2] == "/~" else None

        valid_identities = [i.handle for i in self.get_identities()]

        #protect against identity spoofing
        if self.get_argument("identity") not in valid_identities:
            self.forbidden()
       
        #retrieve actual identity object (this seems kludgy)
        for i in self.get_identities():
            if self.get_argument("identity") == i.handle:
                ident_to_post_with = i
                break
        
        temp = self.get_argument("enclave")
        if temp == "":
            temp = "all"

        post_to = self.graph.enclaves.index.lookup(name=temp)
        if post_to is None:
            print ("post_to is none")
            self.render_template("new_post.html",\
                    error_message="That enclave does \
                    not exist. Please post to an existing \
                    enclave or leave the field blank.",\
                    identities=valid_identities)
            return

        post_type = self.get_argument("post_type")
        if ( post_type == "link" or post_type == "image" ):
            newpost = self.graph.posts.create(
                                    title=self.get_argument("title"),
                                    url=self.get_argument("url"),
                                    post_type=post_type)
        elif (post_type == "text"):
            newpost = self.graph.posts.create(
                                    title=self.get_argument("title"),
                                    body_text=self.get_argument("body"),
                                    post_type=post_type)
        else:
            # hopefully we won't ever see this :)
            print(post_type)
            self.render_template("new_post.html",\
                    error_message="Invalid post type",\
                    identities=valid_identities)
            return

        if newpost:
            post_to = post_to.next()
            self.graph.posted_by.create(newpost,ident_to_post_with)   
            self.graph.posted_to.create(newpost,post_to) 

            self.redirect("/")

class PostHandler(EnclavesHandler):

    @EnclavesHandler.require_login
    def get(self):
        self.write("this is an individual post page")
        
class SettingsHandler(EnclavesHandler):

    @EnclavesHandler.require_login
    def get(self):
        self.render_template("settings.html", identities=self.get_identities())

    @EnclavesHandler.require_login
    def post(self):
        # Creates new Identities
        desired_identity = self.get_argument("new_identity")

        if desired_identity is not None:
            new_identity = self.graph.identities.index.lookup(\
                    handle=desired_identity)  

            if new_identity is not None: #identity is taken
              self.render_template("settings.html",\
                      identities=self.get_identities(),\
                      error_message="This identity is taken.")

            else: #identity is available
                new_identity = self.graph.identities.create(\
                        handle=desired_identity)

                self.graph.Is.create(self.get_current_user(),new_identity)
                self.redirect("/settings")

class ForgotPassHandler(EnclavesHandler):

    def get(self):
        self.write("Sucks.") #TODO: Implement forgot password utility


class NewEnclaveHandler(EnclavesHandler):
    """Handles creation of enclaves"""

    @EnclavesHandler.require_login
    def get(self):
        self.render_template('new_enclave.html')


    @EnclavesHandler.require_login
    def post(self):
        desired_enclave = self.graph.enclaves.index.lookup(\
                name=self.get_argument("name"))

        print(self.get_argument('privacy'))

        if desired_enclave is not None:
            self.write("This enclave already exists. Please choose a new name.")

        else:
            print(self.request.arguments)
            desired_enclave = self.graph.enclaves.create(\
                    name=self.get_argument("name"),\
                    privacy=self.get_argument("privacy"))

            # current user - moderates -> new enclave
            self.graph.moderates.create(self.get_current_user(),desired_enclave)
            # current user - owns -> new enclave
            self.graph.owns.create(self.get_current_user(),desired_enclave)


            self.redirect("/~"+self.get_argument("name"))

class EnclaveHandler(EnclavesHandler):
    """Handles display of a single Enclave"""
    # yes, I know, singluar/plural really isn't a great name difference
    
    @EnclavesHandler.require_login
    def get(self):

        # this is a potential injection point, 
        # since I'm just reading from the URI directly.
        # therefore, TODO: implement santizing of 
        # self.request.uri before passing it to Titan.
        # but don't really care for now

        current_enclave = self.graph.enclaves.index.lookup(\
                name=self.request.uri[2:])
        if not current_enclave:
            self.render_template("new_enclave.html",
                    error_message="This enclave doesn't exist yet.\
                            You can create it if you'd like.")
        else:
            current_enclave = current_enclave.next()
            self.render_template("enclave.html",\
                    enclave_name=current_enclave.name)
            


class UserHandler(EnclavesHandler):
    """Displays a single identity's profile page"""
    
    @EnclavesHandler.require_login
    def get(self):
        self.write(self.request.uri[3:])
        #TODO: implement this
    
