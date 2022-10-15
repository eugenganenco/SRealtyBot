import xmlrpc.client

class ClientSauto:
    def __init__(self):
        self.__proxy = xmlrpc.client.ServerProxy('https://import.sauto.cz/RPC2')
        print(self.__proxy.getHash('ganeugen@gmail.com'))
        #self.__proxy.login()

