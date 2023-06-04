from enum import Enum
import sys
import client_tftp2 as client_tftp2

'''Program cliente teste

   Este programa é capaz de testar o envio, recepção, listagem, renomeação e remoção de arquivo e mais a criação de uma pasta.
   Para isso é feito foi importado a bibliote client_tftp2'''

IP = "127.0.0.1"
PORT = 6969

'''Classe Request
    
   Define o tipo de mensagem solicitada ao servidor.
   RRQ: leitura de arquivo
   WRQ: escrita de arquivo
   LIST: lista arquivo(s)
   MKDIR: cria uma pasta
   MOVE: renomeia/remove um arquivo'''
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
    request = int(sys.argv[2])
    mode = int(sys.argv[3])
    ip = str(sys.argv[4])
    port = int(sys.argv[5])
    newnamefile = str(sys.argv[6])
 

except:
    print("\nUso: python3 client_test.py file_name [recv=1/send=2 | list=3/mkdir=4/move=5] [octet=1/netascii=2] IP PORT new_filename\n")
    print("ex list: python3 client_test.py . 3 1 127.0.0.1 6969\n")
    print("ex mkdir: python3 client_test.py nova-pasta-criada 4 1 127.0.0.1 6969\n")
    print("ex move: python3 client_test.py arquivo 5 1 127.0.0.1 6969 novo-nome-arquivo\n")
    #namefile = '/etc/hosts'
    #ip = IP
    #port = PORT
    #request = Request.WRQ.value
    #mode = 2


# Cria uma instancia de Cliente TFTP2
c = client_tftp2.ClientTFTP(server=ip, port=port)

# Define o modo octet ou netascii
if mode == Mode.OCTET.value:
    mode = Mode.OCTET.value
else:
    mode = Mode.NETASCII.value

# Solicitacao de leitura de arquivo (ok)
if request == Request.RRQ.value:
    c.recebe(namefile, mode)

# Solicitacao de escrita de arquivo (ok)
elif request == Request.WRQ.value:
    c.envia(namefile, mode)

# Solicitacao de lisgatem de pasta (ok)
elif request == Request.LIST.value:
    c.list(namefile)

# Solicitacao de criação uma pasta (ok)
elif request == Request.MKDIR.value:
    c.mkdir(namefile)

# Solicitacao de renomeação/remoção de um arquivo (renomeação: ok)
elif request == Request.MOVE.value:
    c.move(oldfilename=namefile, newfilename=newnamefile)

##############################
# checklist funcionalidades###
##############################
# [ok] recebimento de arquivo
#     [ok] arquivo pequeno
#     [ok] arquivo grande
#
# [ok] envio de arquivo
#     [ok] arquivo pequeno
#     [ok] arquivo grande
#
# [ok] listar pasta
# [ok] criar ṕasta
# [[ok][*]] renomear ou remover arquivo
# obs.: [*] servidor disponibilizado pelo professor não está removendo quando novo nome do arquivo é vazio