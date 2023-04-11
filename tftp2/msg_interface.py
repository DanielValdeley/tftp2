import struct

'''
    class "interface" de Mensagem
'''
class Mensagem:

    def __init__(self, op:int):
        self._opcode = op

    def serialize(self):
        # retorna um valor "bytes"
        return struct.pack('!H', self._opcode)
        #raise NotImplemented('abstrado')

    def deserialize(allmsg: bytes):
        raise NotImplemented('deserialize abstrado')

#######################################################
'''
    2 bytes     2 bytes      n bytes
    ----------------------------------
    | Opcode |   Block #  |   Data     |
    ----------------------------------
    DATA packet
'''
class Data(Mensagem):

    Opcode = 3

    def __init__(self, blocknum:int, body:bytes):

        Mensagem.__init__(self, self.Opcode)
        self.blocknum = blocknum

        if len(body) > 512:
            raise ValueError('Data -> corpo deve ter no max 512 bytes')
        self.body = body

    def serialize(self):
        op_code = Mensagem.serialize(self)
        block = struct.pack('!H', self.blocknum)
        data = self.body # ja esta em bytes
        return op_code + block + data

    @staticmethod
    def deserialize(allmsg:bytes):
        print("Data -> deserialize allmsg (bytes): ", allmsg)

        'Verifica se opcode da msg com data é igual o opcode declarado na class Data'
        opcode, block_num = struct.unpack_from('!HH', allmsg)
        print("Data -> opcode (2 bytes): ", opcode)
        
        if opcode == 3:
            print("Data -> block_num (2 bytes): ", block_num)
            body = allmsg[struct.calcsize('!HH'):]
            print("Data -> body (n bytes): ", body)
            print("Data -> body len: ", len(body))
            return Data(block_num, body)
        else:
            raise ValueError('opcode diferente')

#######################################################

'''
    2 bytes     string    1 byte     string   1 byte
    ------------------------------------------------
    | Opcode |  Filename  |   0  |    Mode    |   0  |
    ------------------------------------------------
    RRQ/WRQ packet
'''
class Rrq(Mensagem):

    Opcode = 1

    def __init__(self, filename:str, mode:str):
        Mensagem.__init__(self, self.Opcode)
        self._filename = filename
        self._byte_zero = 0
        self._mode = mode
    
    def serialize(self):
        op_code = Mensagem.serialize(self)
        filename = struct.pack(f'!{len(self._filename)}s', self._filename.encode())
        byte_zero = b'\x00' # struct.pack('!B', self._byte_zero)
        mode = struct.pack(f'!{len(self._mode)}s', self._mode.encode())
        return op_code + filename + byte_zero + mode + byte_zero

    @staticmethod
    def deserialize(allmsg:bytes):
        print("Rrq -> deserialize allmsg (bytes): ", allmsg)
        opcode, = struct.unpack_from('!H', allmsg)
        print("Rrq -> opcode (2 bytes): ", opcode)
        if opcode == 1:
            pos = allmsg.find(0, 2)
            filename = allmsg[2:pos]
            print("Rrq -> filename (string): ", filename)
            byte_zero = allmsg[pos:pos+1]
            print("Rrq -> byte_zero (byte): ", byte_zero)
            pos2 = allmsg.find(0, pos+1)
            mode = allmsg[pos+1:pos2]
            print("Rrq -> mode (string): ", mode)
            return Rrq(filename.decode(), mode.decode())
            # return opcodeD + filename + byte_zero + mode + byte_zero
        else:
            raise ValueError('opcode diferente')
        
########################################################################

'''
    2 bytes     string    1 byte     string   1 byte
    ------------------------------------------------
    | Opcode |  Filename  |   0  |    Mode    |   0  |
    ------------------------------------------------
    RRQ/WRQ packet
'''
class Wrq(Mensagem):

    Opcode = 2

    def __init__(self, filename:str, mode:str):
        Mensagem.__init__(self, self.Opcode)
        self._filename = filename
        self._mode = mode
    
    def serialize(self):
        op_code = Mensagem.serialize(self)
        filename = struct.pack(f'!{len(self._filename)}s', self._filename.encode())
        byte_zero = b'\x00' 
        mode = struct.pack(f'!{len(self._mode)}s', self._mode.encode())
        return op_code + filename + byte_zero + mode + byte_zero

    @staticmethod
    def deserialize(allmsg:bytes):
        print("Wrq -> deserialize allmsg (bytes): ", allmsg)
        opcode, = struct.unpack_from('!H', allmsg)
        print("Wrq -> opcode (2 bytes): ", opcode)
        if opcode == 2:
            pos = allmsg.find(0, 2)
            filename = allmsg[2:pos]
            print("Wrq -> filename (string): ", filename)
            byte_zero = allmsg[pos:pos+1]
            print("Wrq -> byte_zero (byte): ", byte_zero)
            pos2 = allmsg.find(0, pos+1)
            mode = allmsg[pos+1:pos2]
            print("Wrq -> mode (string): ", mode)
            return Rrq(filename.decode(), mode.decode())
        else:
            raise ValueError('opcode diferente')

###############################################################

'''   
    2 bytes     2 bytes
    ---------------------
    | Opcode |   Block #  |
    ---------------------
        ACK packet
'''
class Ack(Mensagem):

    Opcode = 4

    def __init__(self, block:int):
        Mensagem.__init__(self, self.Opcode)
        self.block = block

    def serialize(self):
        op_code = Mensagem.serialize(self)
        block = struct.pack('!H', self.block)
        return op_code + block

    @staticmethod
    def deserialize(allmsg:bytes):
        print("Ack -> deserialize allmsg (bytes): ", allmsg)
        opcode, block = struct.unpack_from('!HH', allmsg)
        print("Ack opcode (2 bytes): ", opcode)
        if opcode == 4:
            print("block (2 bytes): ", block)
            return Ack(block)
        else:
            raise ValueError('opcode diferente')
        
###############################################################
'''
     2 bytes     2 bytes      string    1 byte
    -----------------------------------------
    | Opcode |  ErrorCode |   ErrMsg   |   0  |
    -----------------------------------------
    ERROR packet
'''

class Error(Mensagem):

    Opcode = 5

    def __init__(self, errorCode:int, errMsg:str):
        Mensagem.__init__(self, self.Opcode)
        self._errorCode = errorCode
        self._errMsg = errMsg
    
    def serialize(self):
        op_code = Mensagem.serialize(self)
        errorCode = struct.pack("!H", self._errorCode)
        errMsg = struct.pack(f'!{len(self._errMsg)}s', self._errMsg.encode())
        byte_zero = b'\x00' 
        return op_code + errorCode + errMsg + byte_zero

    @staticmethod
    def deserialize(allmsg:bytes):
        print("Error -> deserialize allmsg (bytes): ", allmsg)
        opcode, errorCode = struct.unpack_from('!HH', allmsg)
        print("Error -> opcode (2 bytes): ", opcode)
        print("Error -> errorCode (2 bytes): ", errorCode)
        if opcode == 5:
            pos = allmsg.find(0, 4)
            errMsg = allmsg[4:pos]
            print("Error -> errMsg (string): ", errMsg)
            byte_zero = allmsg[pos:]
            print("Error -> byte_zero (byte): ", byte_zero)
            return Error(errorCode, errMsg)
        else:
            raise ValueError('opcode diferente')


TabMensagens = {
    1: Rrq,
    2: Wrq,
    3: Data,
    4: Ack,
    5: Error
}

def cria_instancia(msg:bytes):
    'Decodifica o opcode e verifica qual a classe correspondente ao opcode'
    opcode, = struct.unpack_from('!H', msg)
    return TabMensagens[opcode].deserialize(msg)

