# Import socket module
from socket import *
import sys  # In order to terminate the program


class Server:
    def __init__(self, port_number):
        self.port_number = port_number

    def run(self):

        # Create server socket

        # Add your code here
        serverSocket = socket(AF_INET, SOCK_STREAM)
        serverSocket.bind(('', self.port_number))
        serverSocket.listen(1)

        # Set up a new connection from the client
        while True:
            print('The server is ready to receive')

            # Server should be up and running and listening to the incoming connections

            # Add your code here
            connectionSocket, addr = serverSocket.accept()
            clientData = 1
            while clientData:
                clientData = connectionSocket.recv(512).decode()
            # if not clientData:
            #	connectionSocket.close()
                print("Message Received: " + clientData)
                connectionSocket.send(clientData.encode())

        serverSocket.close()
        sys.exit()  # Terminate the program after sending the corresponding data


class Client:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port

    def run(self):

        # Create server socket

        # Add your code here
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((self.server_ip, self.server_port))

        # Get input with python raw_input() or input()

        # Add your code here
        # Hint:
        # try:
        #     from_client = raw_input("Enter message: \n")
        # ...
        # ...
        try:
            to_server = input('Enter message: \n')
            while to_server.lower().strip() != 'bye':
                # send and receive message

                # Add your code here
                clientSocket.send(to_server.encode())
                from_server = clientSocket.recv(512).decode()
                print(from_server)   # show in terminal

                # Get input again

                # Add your code here
                try:
                    to_server = input('Enter message: \n')
                except EOFError:
                    clientSocket.close()  # close the connection
                    break
        except EOFError:
            clientSocket.close()


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: python myprog.py c <address> <port> or python myprog.py s <port>')
    elif sys.argv[1] != "s" and sys.argv[1] != "c":
        print('Usage: python myprog.py c <address> <port> or python myprog.py s <port>')
    elif(sys.argv[1] == "s"):
        server = Server(int(sys.argv[2]))
        server.run()
    else:
        client = Client(sys.argv[2], int(sys.argv[3]))
        client.run()
