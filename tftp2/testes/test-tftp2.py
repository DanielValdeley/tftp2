import sys,time
import tftp2_pb2 as p

msg = p.Mensagem()
#msg.rrq.fname = b'nome-do-arquivo'
#msg.rrq.mode = 1

#msg.list.path = 'arquivo'

msg2 = p.ListItem()
msg2.file.nome = 'nome'
msg2.file.tamanho = 32
msg.list_resp.items.append(msg2)

data = msg.SerializeToString()

print('Mensagem codificada:', data)

copia = p.Mensagem()
copia.ParseFromString(data)

'''
		REQ rrq = 1;
		REQ wrq = 2;
        DATA data = 3;
        ACK ack = 4;
        Error error = 5;
        Path list = 6;
        ListResponse list_resp = 7;
        Path mkdir = 8;
        MOVE move = 9;
'''
msgDecodificada = ''

#RRQ
if copia.WhichOneof('msg') == 'rrq':
    print('msg: ', copia)
    msgDecodificada = (copia.rrq.fname, copia.rrq.mode)

#WRQ
elif copia.WhichOneof('msg') == 'wrq':
    print('msg: ', copia)
    msgDecodificada = (copia.wrq.fname, copia.wrq.mode)

#DATA
elif copia.WhichOneof('msg') == 'data':
    print('msg: ', copia)
    msgDecodificada = (copia.data.message, copia.data.block_n)

#ACK
elif copia.WhichOneof('msg') == 'ack':
    print('msg: ', copia)
    msgDecodificada = (copia.ack.block_n)

#Error
elif copia.WhichOneof('msg') == 'error':
    print('msg: ', copia)
    msgDecodificada = (copia.error.errorcode)

#Path
elif copia.WhichOneof('msg') == 'list':
    print('msg: ', copia)
    msgDecodificada = (copia.list.path)

#ListResponse
elif copia.WhichOneof('msg') == 'list_resp':
    print('msg: ', copia)
    #msgDecodificada = (copia.list_resp.items.file.nome, copia.list_resp.items.dir.nome, copia.list_resp.items.file.tamanho, copia.list_resp.items.dir.path)
    for i in copia.list_resp.items: 
        print(i)
        msgDecodificada += str(i)

else:
    print('msg copia: ', copia)
    print('msg com campo vazio!')

print('msg decodificada: ', msgDecodificada)

