import sys,time
import tftp2_pb2 as p

msg = p.Mensagem()
msg.rrq.fname = b'nome-do-arquivo'
msg.rrq.mode = 1

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
elif copia.WitchOneof('msg') == 'wrq':
    print('msg: ', copia)
    msgDecodificada = (copia.wrq.fname, copia.wrq.mode)

#DATA
elif copia.WitchOneof('msg') == 'data':
    print('msg: ', copia)
    msgDecodificada = (copia.data.message, copia.data.block_n)

#ACK
elif copia.WitchOneof('msg') == 'ack':
    print('msg: ', copia)
    msgDecodificada = (copia.ack.block_n)

#Error
elif copia.WitchOneof('msg') == 'error':
    print('msg: ', copia)
    msgDecodificada = (copia.error.errorcode)

#Path
elif copia.WitchOneof('msg') == 'path':
    print('msg: ', copia)
    msgDecodificada = (copia.path.errorcode)

#ListResponse
elif copia.WitchOneof('msg') == 'list_resp':
    print('msg: ', copia)
    msgDecodificada = (copia.list_resp.items.file.nome, copia.list_resp.items.dir.nome, copia.list_resp.items.file.tamanho, copia.list_resp.items.dir.path)

else:
    print('msg com campo vazio!')

print('msg decodificada: ', msgDecodificada)

