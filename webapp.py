#!/usr/bin/python3

"""
webApp class
 Root for hierarchy of classes implementing web applications

 Copyright Jesus M. Gonzalez-Barahona and Gregorio Robles (2009-2015)
 jgb @ gsyc.es
 TSAI, SAT and SARO subjects (Universidad Rey Juan Carlos)
 October 2009 - February 2015
"""

import socket


class webApp:
    """Root of a hierarchy of classes implementing web applications

    This class does almost nothing. Usually, new classes will
    inherit from it, and by redefining "parse" and "process" methods
    will implement the logic of a web application in particular.
    """

    def parse(self, request):
        """Parse the received request, extracting the relevant information."""

        return None

    def process(self, parsedRequest):
        """Process the relevant elements of the request.

        Returns the HTTP code for the reply, and an HTML page.
        """

        return ("200 OK", "<html><body><h1>It works!</h1></body></html>")

    def __init__(self, hostname, port): #Todos las clases tienen un _init_, que es como un constructor
        """Initialize the web application."""

        # Create a TCP objet socket and bind it to a port
        mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        mySocket.bind((hostname, port))

        # Queue a maximum of 5 TCP connection requests
        mySocket.listen(5)

        # Accept connections, read incoming data, and call
        # parse and process methods (in a loop)

        while True:
            print('Waiting for connections')
            (recvSocket, address) = mySocket.accept()
            print('HTTP request received (going to parse and process):')
            request = recvSocket.recv(2048)
            print(request.decode('utf-8'))
            parsedRequest = self.parse(request)
            (returnCode, htmlAnswer) = self.process(parsedRequest)
            print('Answering back...')
            recvSocket.send(bytes("HTTP/1.1 " + returnCode + " \r\n\r\n"
                            + htmlAnswer + "\r\n", 'utf-8'))
            recvSocket.close()
#Vamos a definir la clase holaAPP
class holaApp(webApp):
    def parse (self, request):
        return None

    def process (self, parsedRequest):

        return("200 Ok", "<!DOCTYPE html><html><body><h1> HOLA MUNDO </h1> </boody></html>")

    def __init__ (self, hostname, port):
        webApp.__init__(self, hostname, port)

#Vamos a definir la clase adiosApp
class adiosApp(webApp):
    def parse (self, request):
        return None

    def process (self, parsedRequest):

        return ("200 Ok" , "<!DOCTYPE html><html> ADIOS, MUNDO CRUEL </html>")

    def __init__ (self, hostname, port):
        webApp.__init__(self, hostname,port)


#if __name__ == "__main__":
#    testHolaApp = holaApp(socket.gethostname(),1231)




#if __name__ == "__main__": #__name__ -> Indica que esto es el programa principal
#    testWebApp = webApp("localhost", 1234)


    #Para hererdar una clase de otra es --> class [nombre de clase nueva]([clase de la que se hereda]):
    #Para usar la clase definida en otro modulo:
    #   import webaap
    #   classe [nombre_clase]([modulo].[clase])
