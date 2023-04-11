import sys,time
import tftp2_pb2

msg = tftp2_pb2.DATA()
msg.message = b'Alguma coisa!'
msg.block_n = 1

data = msg.SerializeToString()

print('Mensagem codificada:', data)

copia = tftp2_pb2.DATA()
copia.ParseFromString(data)

print('Mensagem decodificada:')
print('message: ', copia.message)
print('block_n: ', copia.block_n)
