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

    @EnclavesHandler.require_login
    def open(self):
        curr_enc = self.get_enclave()
        if curr_enc not in self.clients.keys():
            self.clients[curr_enc] = []
        self.clients[curr_enc].append(self)
        for client in self.clients[curr_enc]:
            client.write_message(u"Socket opened. %s" %client)
        

#    @EnclavesHandler.require_login
    def on_message(self, message):
        curr_enc = self.get_enclave()
        print(message)

        # forwards received message to all other relevant clients
        for client in self.clients[curr_enc]:
            client.write_message({"user":self.get_secure_cookie("userid"),\
                "message":message})
    
    @EnclavesHandler.require_login
    def on_close(self):
        self.clients[self.get_enclave()].remove(self)

