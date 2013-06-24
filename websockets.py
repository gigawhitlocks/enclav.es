from tornado import websocket
from handlers import EnclavesHandler

class EnclaveSocket(websocket.WebSocketHandler):
    clients = {}    

    def get_enclave(self):
        return self.request.uri.split("/")[1][1:]

    def is_logged_in(self):
        """
        Checks to see if a user is logged in.
        """
        return self.get_secure_cookie("userid") != None 

class PostSocket(websocket.WebSocketHandler):

    @EnclavesHandler.require_login
    def open(self):
        pass

    @EnclavesHandler.require_login
    def on_message(self):
        pass

    @EnclavesHandler.require_login
    def on_close(self):
        pass

    
class ChatSocket(EnclaveSocket):

    def broadcast(self, message):
        """ broadcast <message> to all connected clients """
        for client in self.clients[self.get_enclave()]:
            try:
                client.write_message(message)
            except AttributeError: # wut
                pass

    def open(self):
    #    print(self.clients)
        curr_enc = self.get_enclave()
        if curr_enc not in self.clients.keys():
            self.clients[curr_enc] = []
        self.clients[curr_enc].append(self)
        
        self.broadcast({"type":"join", "user":self.get_secure_cookie("userid")})
        

    def on_message(self, message):
        self.broadcast(\
                {"type":"chat", \
                "user":self.get_secure_cookie("userid"),\
                "message":message})
                
    def on_close(self):
        self.broadcast({"type":"part", "user":self.get_secure_cookie("userid")}) #TODO: %s/self.get_secure_cookie/bound_ID/g
        self.clients[self.get_enclave()].remove(self)

