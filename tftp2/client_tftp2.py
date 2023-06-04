#!/usr/bin/env python3

import socket
import poller
import tftp2 as t

''' Classe Cliente TFTP2

    Classe capaz prover recursos de envio e recepeção de arquivo, bem como listagem, criação e renomeação ou remoção de arquivo.
    Utiliza dos recursos do tftp2 importado no topo desse arquivo.
    Para a solicitação de escrita de um arquivo no servivor faz uso do CallbackSend
    Para a solicitação de leitura de um arquivo do servivor faz uso do CallbackReceived
    Para a solicitação de listagem de um ou mais arquivos do servivor faz uso do CallbackList
    Para a solicitação de criação de uma pasta no servivor faz uso do CallbackCreateDir
    Para a solicitação de renomeação ou remoção de um arquivo do servidor faz uso do CallbackMove'''
class ClientTFTP:
   
    prefixLog = "ClientTFTP2: "
   
    def __init__(self, server, port):
        self._addr = (server, port)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.s.bind(('0.0.0.0', 0))
        print(f"{self.prefixLog} Create socket for address: {self._addr}")

        self.timeout = 5
        self.packet = None

        self.sched = poller.Poller()
        print(f"{self.prefixLog} Start Poller...")
      
    '''Operacao de envio de arquivo
       Metodo capaz de envia um arquivo para o servidor
       filename: nome do arquivo a ser enviado
       mode: define o modo de transferencia de arquivo octet/netascii
    ''' 
    def envia(self, filename:str, mode:str):
        cs = t.CallbackSend(sock=self.s, timeout=self.timeout, address=self._addr, filename=filename, mode=mode)
        self.sched.adiciona(cs)
        self.sched.despache()
   
    '''Operacao de recebimento de arquivo
       Metodo capaz de receber um arquivo do servidor
       filename: nome do arquivo a ser recebido
       mode: define o modo de transferencia de arquivo octet/netascii
    ''' 
    def recebe(self, filename:str, mode:str):
        cr = t.CallbackReceived(sock=self.s, timeout=self.timeout, address=self._addr, filename=filename, mode=mode)
        self.sched.adiciona(cr)
        self.sched.despache()

    '''Operacao de listagem de arquivo(s)
       Metodo capaz de listar um arquivo ou mais do servidor
       dir: nome do diretorio que contem os arquivos a serem listados
    ''' 
    def list(self, dir:str):
        cl = t.CallbackList(sock=self.s, timeout=self.timeout, address=self._addr, dir=dir)
        self.sched.adiciona(cl)
        self.sched.despache()

    '''Operacao de criação de uma pasta
       Metodo capaz de criar uma pasta no servidor
       dir: nome do diretorio a ser criado
    '''
    def mkdir(self, dir:str):
        cmk = t.CallbackCreateDir(sock=self.s, timeout=self.timeout, address=self._addr, dir=dir)
        self.sched.adiciona(cmk)
        self.sched.despache()

    '''Operacao de renomear ou remover um arquivo
       Metodo capaz de nomear/remover um arquivo do servidor
       oldfilename: nome do arquivo original
       newfilename: novo nome do arquivo (obs.: se vazio exlui o original)
    '''
    def move(self, oldfilename:str, newfilename:str):
        cm = t.CallbackMove(sock=self.s, timeout=self.timeout, address=self._addr, oldfilename=oldfilename, newfilename=newfilename)
        self.sched.adiciona(cm)
        self.sched.despache()