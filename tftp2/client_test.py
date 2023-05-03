from enum import Enum
import sys
import client_tftp2 as client_tftp2

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
    LIST = 3
    MKDIR = 4
    MOVE = 5


'''Classe Mode

   Define o modo de transferecia do arquivo
   OCTET: transferencia de arquivo binario
   NETASCII: transferencia de arquivo texto'''
class Mode(Enum):
    OCTET = 1
    NETASCII = 2
        
try:
    namefile = str(sys.argv[1])
    newnamefile = str(sys.argv[2])
    request = int(sys.argv[3])
    mode = int(sys.argv[4])
    ip = str(sys.argv[5])
    port = int(sys.argv[6])
 

except:
    print("\nUso: python3 client_test.py file_name new_filename [recv=1/send=2] [list=3/mkdir=4/move=5] [octet=1/netascii=2] IP PORT")
    print("ex: python3 client_test.py file_name new_namefile 1 1 127.0.0.1 6969\n")
    #namefile = '/etc/hosts'
    #ip = IP
    #port = PORT
    #request = Request.WRQ.value
    #mode = 2


# Cria uma instancia de Cliente TFTP
c = client_tftp2.ClientTFTP(server=ip, port=port)

# Define o modo octet ou netascii
if mode == Mode.OCTET.value:
    mode = Mode.OCTET.value
else:
    mode = Mode.NETASCII.value

# Solicitacao de leitura de arquivo
if request == Request.RRQ.value:
    c.recebe(namefile, mode)

# Solicitacao de escrita de arquivo
elif request == Request.WRQ.value:
    c.envia(namefile, mode)

# Lisgatem de pasta
elif request == Request.LIST.value:
    c.list(namefile)

# Cria uma pasta
elif request == Request.MKDIR.value:
    c.mkdir(namefile)

elif request == Request.MOVE.value:
    c.move(oldfilename=namefile, newfilename=newnamefile)