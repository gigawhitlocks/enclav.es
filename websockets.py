from tornado import websocket

class PostSocket(websocket.WebSocketHandler):
    def open(self):
        pass

    def on_message(self):
        pass

    def on_close(self):
        pass

    
class ChatSocket(websocket.WebSocketHandler):
    clients = []

    def open(self):
        self.clients.append(self)
        for client in self.clients:
            client.write_message(u"Socket opened. %s" %client)

        print("Socket opened")
        pass

    def on_message(self):
        pass

    def on_close(self):
        self.clients.remove(self)
        pass


