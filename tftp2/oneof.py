import sys,time
import oneof_pb2 as o


# msg1: usa o campo nome do oneof
msg1 = o.Ativo()
msg1.nome = 'PETR4'
msg1.valor = 100



#SampleMessage message;

SampleMessage = o.SampleMessage()

SampleMessage.rrq.fname = 'algo'


#CHECK(message.has_name());
#message.mutable_sub_message();   // Will clear name field.
#CHECK(!message.has_name());

#data = msg1.SerializeToString()

#print('Mensagem codificada:', data)
