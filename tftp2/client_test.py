from enum import Enum
import sys
import client_tftp

'''Program cliente teste

   Este programa é capaz de testar o envio e recepçaõ de arquivo.
   Para isso é feito foi importado a bibliote client_tftp'''

IP = "127.0.0.1"
PORT = 6969

'''Classe Request
    
   Define o tipo de mensagem solicitada ao servidor.
   RRQ: leitura de arquivo
   WRQ: escrita de arquivo'''
class Request(Enum):
    RRQ = 1
    WRQ = 2


'''Classe Mode

   Define o modo de transferecia do arquivo
   OCTET: transferencia de arquivo binario
   NETASCII: transferencia de arquivo texto'''
class Mode(Enum):
    OCTET = 1
    NETASCII = 2
        

try:
    namefile = str(sys.argv[1])
    request = int(sys.argv[2])
    mode = int(sys.argv[3])
    ip = str(sys.argv[4])
    port = int(sys.argv[5])
 

except:
    print("\nUso: python3 client_test.py file_name recv=1/send=2 octet=1/netascii=2 IP PORT")
    print("ex: python3 client_test.py file_name 1 1 127.0.0.1 6969\n")
    #namefile = '/etc/hosts'
    #ip = IP
    #port = PORT
    #request = Request.WRQ.value
    #mode = 2


# Cria uma instancia de Cliente TFTP
c = client_tftp.ClientTFTP(server=ip, port=port)

# Define o modo octet ou netascii
if mode == Mode.OCTET.value:
    mode = Mode.OCTET.name.lower()
else:
    mode = Mode.NETASCII.name.lower()

# Solicitacao de leitura de arquivo
if request == Request.RRQ.value:
    #namefile = 'arquivorecebidopequeno' # ok (<=512)
    #namefile = 'arquivorecebidogrande' # ok (>512)
    c.recebe(namefile, mode)

# Solicitacao de escrita de arquivo
elif request == Request.WRQ.value:
    #namefile = 'arquivoenviopequeno' # ok (<=512)
    #namefile = 'arquivoenviogrande' # ok (>512)
    c.envia(namefile, mode)


