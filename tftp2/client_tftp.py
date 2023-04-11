#!/usr/bin/env python3

import socket
import poller
import tftp as t

''' Classe Cliente TFTP

    Classe capaz prover recursos de envio e recepeção de arquivo.
    Utiliza dos recursos do tftp importado no topo desse arquivo.
    Para a solicitação de leitura de um arquivo do servivor faz uso do CallbackReceived
    Para a solicitação de escrita de um arquivo no servidor faz uso do CallbackSend'''
class ClientTFTP:
   
    prefixLog = "ClientTFTP: "
   
    def __init__(self, server, port):
        self._addr = (server, port)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.s.bind(('0.0.0.0', 0))
        print(f"{self.prefixLog} Create socket for address: {self._addr}")

        self.timeout = 5
        self.packet = None

        self.sched = poller.Poller()
        print(f"{self.prefixLog} Start Poller...")
      
    def envia(self, filename:str, mode:str):
        cs = t.CallbackSend(sock=self.s, timeout=self.timeout, address=self._addr, filename=filename, mode=mode)
        self.sched.adiciona(cs)
        self.sched.despache()
   
    def recebe(self, filename:str, mode:str):
        cr = t.CallbackReceived(sock=self.s, timeout=self.timeout, address=self._addr, filename=filename, mode=mode)
        self.sched.adiciona(cr)
        self.sched.despache()