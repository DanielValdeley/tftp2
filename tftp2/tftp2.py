#!/usr/bin/env python3

import sys, time
import socket
import poller
import tftp2_pb2 as p
import traceback

'''Classe CallbackSend:

        Declara um Callback capaz de enviar pacotes 
        definidos do protocolo TFTP2 via socket.
        Implementa a máquina de estados finitos (MEF).'''
class CallbackSend(poller.Callback):

    prefixLog = "CallbackSend: "
   
    def __init__(self, sock:socket, timeout:float, address, filename:str, mode:str):
        poller.Callback.__init__(self, sock, timeout)

        self._sock = sock
        self._address = address

        f = filename.rsplit('/', 1)[-1]

        # WRQ: Pacote para Escrita de arquivo
        self._packet = p.Mensagem()
        self._packet.wrq.fname = f
        self._packet.wrq.mode = mode
        self.path = filename if filename[0] == '/' else "./" + filename # caminho para leitura
        
        # Arquivo de leitura
        self.file = open(self.path, 'rb')
        self._n = 0
    
        # Solicita ao servidor escrita de arquivo
        self._sock.sendto(self._packet.SerializeToString(), self._address)
        print(f"{self.prefixLog} init() sendto packet WRQ: {self._packet}, serialized: {self._packet.SerializeToString()}")

        self.enable_timeout()

        # Estado atual
        self._current_handler = self.handle_init_tx 
        

    def handle_init_tx(self, packet):

        # Cria uma instancia do pacote recebido (deserializar)
        obj = p.Mensagem()
        obj.ParseFromString(packet)

        print(f'{self.prefixLog} obj: {obj}')

        if obj.WhichOneof('msg') == 'ack':
            print('msg: ', obj)
            ack_n = obj.ack.block_n # obtem o ack_n
            print(f"{self.prefixLog} handle_init_tx() obj: {obj} ack_n = {ack_n}")

        if ack_n == 0:
            body = self.file.read(512) 
            buffer = len(body)

            print(f"{self.prefixLog} handle_init_tx() body: {body}, buffer = {buffer}")
            self._n = self._n + 1
            blocknum = self._n
            print(f"{self.prefixLog} handle_init_tx() blocknum = {blocknum}")
            
            #data = m.Data(blocknum=blocknum,body=body)
            d = p.Mensagem()
            d.data.block_n = blocknum
            d.data.message = body
            data = d.SerializeToString()

            print(f"{self.prefixLog} send data: {data}")
            self._sock.sendto(data, self._address)

            if buffer == 512:
                self._current_handler = self.handle_tx

            elif buffer < 512: 
                self._current_handler = self.handle_finish
            

    def handle_tx(self, packet):
        # Cria uma instancia do pacote recebido (deserializar)
        obj = p.Mensagem()
        obj.ParseFromString(packet)

        print(f'{self.prefixLog} obj: {obj}')

        if obj.WhichOneof('msg') == 'ack':
            ack_n = obj.ack.block_n # obtem o ack_n
            print(f"{self.prefixLog} handle_tx() ack_n = {ack_n}")

        body = self.file.read(512)
        buffer = len(body)

        if ack_n == self._n:

            print(f"{self.prefixLog} handle_tx() body: {body}, buffer = {buffer}")
            self._n += 1
            blocknum = self._n
            print(f"{self.prefixLog} handle_tx() blocknum: {blocknum}")
            d = p.Mensagem()
            d.data.block_n = blocknum
            d.data.message = body
            data = d.SerializeToString()
            print(f"{self.prefixLog} handle_tx() send data: {data}")
        
            if buffer >= 512:
                self._sock.sendto(data, self._address)
            
            elif buffer < 512:
                self._sock.sendto(data, self._address)
                self._current_handler = self.handle_finish

        # Timeout
        else: 
            print(f"{self.prefixLog} handle_tx() Timeout, body: {body}, blocknum = {self.n} ack_n ={ack_n}")
            blocknum = self._n

            d = p.Mensagem()
            d.data.block_n = blocknum
            d.data.message = body
            data = d.SerializeToString()

            print(f"{self.prefixLog} handle_tx() Timeout send data: {data}")
            self._sock.sendto(data, self._address)
            

    def handle_finish(self, packet):
        # Cria uma instacia do pacote recebido (deserializar)
        obj = p.Mensagem()
        obj.ParseFromString(packet)

        print(f'{self.prefixLog} obj: {obj}')

        if obj.WhichOneof('msg') == 'ack':
            ack_n = obj.ack.block_n # obtem o ack_n
            print(f"{self.prefixLog} handle_finish() ack_n = {ack_n}")
        
            if (ack_n == self._n):
                print(f"{self.prefixLog} handle_finish() Finish...")
                self.disable_timeout()
                self.disable()

        # Recebe pacote de Error
        elif obj.WhichOneof('msg') == 'error':
            print(f"{self.prefixLog} handle_finish() Error... :)")
            self.disable_timeout()
            self.disable()

        # Timeout
        else:
            print(f"{self.prefixLog} handle_finish() ack_n = {ack_n}")
            body = self.file.read(512)
            blocknum = self._n

            #data = m.Data(blocknum=blocknum,body=body)            
            d = p.Mensagem()
            d.data.block_n = blocknum
            d.data.message = body
            data = d.SerializeToString()

            self._sock.sendto(data, self._address)

    def handle(self):
        'Recebe pacote via socket'
        try:
            packet, addr = self._sock.recvfrom(1024)
            print(f"{self.prefixLog} Received packet: handle() {packet}, address -> ip:{addr[0]} | port: {addr[1]}")
            self._address = (addr[0], addr[1])
            self._current_handler(packet=packet)

        except:
            'Se ocorrer algum erro na recpecao chama handle_timeout'
            print(f"{self.prefixLog} fail received packet!")
            self._current_handler = self.handle_timeout


    def handle_timeout(self):
        'O tratador de evento timeout'
        'Desativa o timeout deste callback, e também o evento de envio de pacote!'
        self.disable_timeout()         
        self.disable() 
        

####################################################################################    


'''Classe CallbackReceived:

        Declara um Callback capaz de receber pacotes 
        definidos do protocolo TFTP2 via socket.
        Implementa a máquina de estados finitos (MEF).'''
class CallbackReceived(poller.Callback):
    
    prefixLog = "CallbackReceived: "
   
    def __init__(self, sock:socket, timeout:float, address, filename:str, mode:str):
        poller.Callback.__init__(self, sock, timeout)

        self._sock = sock
        self._address = address

        # RRQ: Pacote para Leitura de arquivo
        self._packet = p.Mensagem()
        self._packet.rrq.fname = filename
        self._packet.rrq.mode = mode

        self.path = "./" + filename # caminho para escrita
        # Arquivo para escrita
        self.file = open(self.path, 'wb')
        self._n = 1
    
        # Solicita ao servidor leitura de arquivo
        self._sock.sendto(self._packet.SerializeToString(), self._address) 
        print(f"{self.prefixLog} init() sendto packet RRQ: {self._packet}, serialized: {self._packet.SerializeToString()}")

        self.enable_timeout()

        # Estado atual
        self._current_handler = self.handle_rx 
        
        
    def handle_rx(self, packet):
        # Verifica se pacote e' valido
        if (packet == None):
            print(f"{self.prefixLog} packet is None!")
            blocknum = None

            #ack = m.Ack(blocknum)            
            a = p.Mensagem()
            a.ack.block_n = blocknum
            ack = a.SerializeToString()

            self._sock.sendto(ack, self._address)

        else: 
            # Cria uma instacia do pacote recebido (deserializar)
            obj = p.Mensagem()
            obj.ParseFromString(packet)

            print(f'{self.prefixLog} obj: {obj}')

            if obj.WhichOneof('msg') == 'data':  
                data_body = obj.data.message
                data_n = obj.data.block_n
                print(f"{self.prefixLog} handle_rx() obj: {obj} data_body: {data_body}")
                print(f"{self.prefixLog} handle_rx() data_n: {data_n}")

                buffer = len(data_body)
                print(f"{self.prefixLog} handle_rx() buffer: {buffer}")

                if data_n == self._n and buffer == 512:
                    blocknum = self._n

                    #ack = m.Ack(blocknum)
                    a = p.Mensagem()
                    a.ack.block_n = blocknum
                    ack = a.SerializeToString()
                    
                    print(f"{self.prefixLog} handle_rx() send ack: {ack}")
                    self._sock.sendto(ack, self._address)
                    self._n = self._n + 1
                    self.file.write(data_body)

                elif data_n == self._n and buffer < 512: 
                    blocknum = self._n
                    
                    #ack = m.Ack(blocknum)
                    a = p.Mensagem()
                    a.ack.block_n = blocknum
                    ack = a.SerializeToString()

                    print(f"{self.prefixLog} handle_rx() send ack: {ack}")

                    self._sock.sendto(ack, self._address)

                    self.file.write(data_body)
                    print(f"{self.prefixLog} handle_rx() Finish...")
                    self.disable()
                    self.disable_timeout()


    def handle(self):
        'Recebe pacote via socket'
        try:
            packet, addr = self._sock.recvfrom(1024)
            print(f"{self.prefixLog} Received packet: {packet}, address: {addr}")
            self._address = (addr[0], addr[1])
            self._current_handler(packet=packet)

        except Exception as e:
            'Se ocorrer algum erro seja de recepcao do pacote ou seja no estato atual mostra o erro'
            print(f"{self.prefixLog} error: {e}")
            traceback.print_exc()
            sys.exit()
            

    def handle_timeout(self):
        'O tratador de evento timeout'
        'Desativa o timeout deste callback, e também o evento de envio de pacote!'
        self.disable_timeout()         
        self.disable()   


#######################################
##### Novas mensagens do TFTP2 ########
#######################################

'''Classe CallbackList:

        Declara um Callback capaz de fazer a listagem de uma pasta.
        definidos do protocolo TFTP2 via socket.
        Implementa a máquina de estados finitos (MEF).'''
class CallbackList(poller.Callback):
        
    prefixLog = "CallbackList: "
   
    def __init__(self, sock:socket, timeout:float, address, dir:str):
        poller.Callback.__init__(self, sock, timeout)

        self._sock = sock
        self._address = address

        # LIST: fazer listagem de uma pasta
        self._packet = p.Mensagem()
        self._packet.list.path = dir

        # Solicita ao servidor listagem de uma pasta
        self._sock.sendto(self._packet.SerializeToString(), self._address) 
        print(f"{self.prefixLog} init() sendto packet LIST: {self._packet}, serialized: {self._packet.SerializeToString()}")

        self.enable_timeout()

        # Estado atual
        self._current_handler = self.handle_list

    def handle_list(self, packet):
         # Cria uma instancia do pacote recebido (deserializar)
        obj = p.Mensagem()
        obj.ParseFromString(packet)

        print(f'{self.prefixLog} obj: {obj}')

        l = []
        if obj.WhichOneof('msg') == 'list_resp':
            for i in obj.list_resp.items: 
                l.append(i) # obtem listagem de pasta
            
            print(f"{self.prefixLog} handle_list() obj: {l}")


    def handle(self):
        'Recebe pacote via socket'
        try:
            packet, addr = self._sock.recvfrom(1024)
            print(f"{self.prefixLog} Received packet: {packet}, address: {addr}")
            self._address = (addr[0], addr[1])
            self._current_handler(packet=packet)

        except:
            'Se ocorrer algum erro na recpecao chama handle_timeout'
            print(f"{self.prefixLog} fail received packet!")
            self._current_handler = self.handle_timeout
            

    def handle_timeout(self):
        'O tratador de evento timeout'
        self.disable_timeout()         
        self.disable()   


####################################################################################


'''Classe CallbackCreateDir:

        Declara um Callback capaz de criar uma pasta.
        definidos do protocolo TFTP2 via socket.
        Implementa a máquina de estados finitos (MEF).'''
class CallbackCreateDir(poller.Callback):
        
    prefixLog = "CallbackCreateDir: "
   
    def __init__(self, sock:socket, timeout:float, address, dir:str):
        poller.Callback.__init__(self, sock, timeout)

        self._sock = sock
        self._address = address

        # MKDIR: criar uma pasta
        self._packet = p.Mensagem()
        self._packet.mkdir.path = dir

        # Solicita ao servidor a criacao de uma pasta
        self._sock.sendto(self._packet.SerializeToString(), self._address) 
        print(f"{self.prefixLog} init() sendto packet MKDIR: {self._packet}, serialized: {self._packet.SerializeToString()}")

        self.enable_timeout()

        # Estado atual
        self._current_handler = self.handle_create_dir

    def handle_create_dir(self, packet):
         # Cria uma instancia do pacote recebido (deserializar)
        obj = p.Mensagem()
        obj.ParseFromString(packet)

        print(f'{self.prefixLog} obj: {obj}')

        if obj.WhichOneof('msg') == 'ack':
            ack = obj.ack.block_n # obtem ack com bumero de bloco 0
            print(f"{self.prefixLog} handle_create_dir() success ack: {ack}")
        else:
            err = obj.errorcode
            print(f"{self.prefixLog} handle_create_dir() error: {err}")


    def handle(self):
        'Recebe pacote via socket'
        try:
            packet, addr = self._sock.recvfrom(1024)
            print(f"{self.prefixLog} Received packet: {packet}, address: {addr}")
            self._address = (addr[0], addr[1])
            self._current_handler(packet=packet)

        except:
            'Se ocorrer algum erro na recpecao chama handle_timeout'
            print(f"{self.prefixLog} fail received packet!")
            self._current_handler = self.handle_timeout
            

    def handle_timeout(self):
        'O tratador de evento timeout'
        self.disable_timeout()         
        self.disable()   

        
####################################################################################


'''Classe CallbackMove:

        Declara um Callback capaz de renomear ou remover arquivos.
        definidos do protocolo TFTP2 via socket.
        Implementa a máquina de estados finitos (MEF).'''
class CallbackMove(poller.Callback):
        
    prefixLog = "CallbackMove: "
   
    def __init__(self, sock:socket, timeout:float, address, oldfilename:str, newfilename:str):
        poller.Callback.__init__(self, sock, timeout)

        self._sock = sock
        self._address = address

        # MOVE: renomear ou remover um arquivo
        self._packet = p.Mensagem()
        self._packet.move.nome_orig = oldfilename
        self._packet.move.nome_novo = newfilename

        # Solicita ao servidor a remocao ou renomeacao do arquivo
        self._sock.sendto(self._packet.SerializeToString(), self._address) 
        print(f"{self.prefixLog} init() sendto packet MOVE: {self._packet}, serialized: {self._packet.SerializeToString()}")

        self.enable_timeout()

        # Estado atual
        self._current_handler = self.handle_move

    def handle_move(self, packet):
         # Cria uma instancia do pacote recebido (deserializar)
        obj = p.Mensagem()
        obj.ParseFromString(packet)

        print(f'{self.prefixLog} obj: {obj}')

        if obj.WhichOneof('msg') == 'ack':
            ack = obj.ack.block_n # obtem ack com bumero de bloco 0
            print(f"{self.prefixLog} handle_move() success ack: {ack}")
        else:
            err = obj.errorcode
            print(f"{self.prefixLog} handle_move() error: {err}")


    def handle(self):
        'Recebe pacote via socket'
        try:
            packet, addr = self._sock.recvfrom(1024)
            print(f"{self.prefixLog} Received packet: {packet}, address: {addr}")
            self._address = (addr[0], addr[1])
            self._current_handler(packet=packet)

        except:
            'Se ocorrer algum erro na recpecao chama handle_timeout'
            print(f"{self.prefixLog} fail received packet!")
            self._current_handler = self.handle_timeout
            

    def handle_timeout(self):
        'O tratador de evento timeout'
        self.disable_timeout()         
        self.disable()   
