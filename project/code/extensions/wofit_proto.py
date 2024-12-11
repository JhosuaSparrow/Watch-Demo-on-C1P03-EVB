import binascii

crc16_table = [
    0x0000, 0xC0C1, 0xC181, 0x0140, 0xC301, 0x03C0, 0x0280, 0xC241,
    0xC601, 0x06C0, 0x0780, 0xC741, 0x0500, 0xC5C1, 0xC481, 0x0440,
    0xCC01, 0x0CC0, 0x0D80, 0xCD41, 0x0F00, 0xCFC1, 0xCE81, 0x0E40,
    0x0A00, 0xCAC1, 0xCB81, 0x0B40, 0xC901, 0x09C0, 0x0880, 0xC841,
    0xD801, 0x18C0, 0x1980, 0xD941, 0x1B00, 0xDBC1, 0xDA81, 0x1A40,
    0x1E00, 0xDEC1, 0xDF81, 0x1F40, 0xDD01, 0x1DC0, 0x1C80, 0xDC41,
    0x1400, 0xD4C1, 0xD581, 0x1540, 0xD701, 0x17C0, 0x1680, 0xD641,
    0xD201, 0x12C0, 0x1380, 0xD341, 0x1100, 0xD1C1, 0xD081, 0x1040,
    0xF001, 0x30C0, 0x3180, 0xF141, 0x3300, 0xF3C1, 0xF281, 0x3240,
    0x3600, 0xF6C1, 0xF781, 0x3740, 0xF501, 0x35C0, 0x3480, 0xF441,
    0x3C00, 0xFCC1, 0xFD81, 0x3D40, 0xFF01, 0x3FC0, 0x3E80, 0xFE41,
    0xFA01, 0x3AC0, 0x3B80, 0xFB41, 0x3900, 0xF9C1, 0xF881, 0x3840,
    0x2800, 0xE8C1, 0xE981, 0x2940, 0xEB01, 0x2BC0, 0x2A80, 0xEA41,
    0xEE01, 0x2EC0, 0x2F80, 0xEF41, 0x2D00, 0xEDC1, 0xEC81, 0x2C40,
    0xE401, 0x24C0, 0x2580, 0xE541, 0x2700, 0xE7C1, 0xE681, 0x2640,
    0x2200, 0xE2C1, 0xE381, 0x2340, 0xE101, 0x21C0, 0x2080, 0xE041,
    0xA001, 0x60C0, 0x6180, 0xA141, 0x6300, 0xA3C1, 0xA281, 0x6240,
    0x6600, 0xA6C1, 0xA781, 0x6740, 0xA501, 0x65C0, 0x6480, 0xA441,
    0x6C00, 0xACC1, 0xAD81, 0x6D40, 0xAF01, 0x6FC0, 0x6E80, 0xAE41,
    0xAA01, 0x6AC0, 0x6B80, 0xAB41, 0x6900, 0xA9C1, 0xA881, 0x6840,
    0x7800, 0xB8C1, 0xB981, 0x7940, 0xBB01, 0x7BC0, 0x7A80, 0xBA41,
    0xBE01, 0x7EC0, 0x7F80, 0xBF41, 0x7D00, 0xBDC1, 0xBC81, 0x7C40,
    0xB401, 0x74C0, 0x7580, 0xB541, 0x7700, 0xB7C1, 0xB681, 0x7640,
    0x7200, 0xB2C1, 0xB381, 0x7340, 0xB101, 0x71C0, 0x7080, 0xB041,
    0x5000, 0x90C1, 0x9181, 0x5140, 0x9301, 0x53C0, 0x5280, 0x9241,
    0x9601, 0x56C0, 0x5780, 0x9741, 0x5500, 0x95C1, 0x9481, 0x5440,
    0x9C01, 0x5CC0, 0x5D80, 0x9D41, 0x5F00, 0x9FC1, 0x9E81, 0x5E40,
    0x5A00, 0x9AC1, 0x9B81, 0x5B40, 0x9901, 0x59C0, 0x5880, 0x9841,
    0x8801, 0x48C0, 0x4980, 0x8941, 0x4B00, 0x8BC1, 0x8A81, 0x4A40,
    0x4E00, 0x8EC1, 0x8F81, 0x4F40, 0x8D01, 0x4DC0, 0x4C80, 0x8C41,
    0x4400, 0x84C1, 0x8581, 0x4540, 0x8701, 0x47C0, 0x4680, 0x8641,
    0x8201, 0x42C0, 0x4380, 0x8341, 0x4100, 0x81C1, 0x8081, 0x4040
]


class Base(object):

    def __str__(self):
        return self.to_hex()

    def to_bytes(self):
        raise NotImplementedError

    @classmethod
    def from_bytes(cls, data):
        raise NotImplementedError

    def to_hex(self):
        return binascii.hexlify(self.to_bytes()).decode().upper()

    @classmethod
    def from_hex(cls, string):
        return cls.from_bytes(binascii.unhexlify(string))


class Layer1(Base):
    """
    L1 package(8-512 Bytes):
    +-------------+--------------+
    | L1 header   | L1 payload   |
    +=============+==============+
    | 8 bytes     | 0-504 bytes  |
    +-------------+--------------+

    L1 header(8 Bytes):
    +------------+----------+-------------+----------+----------+----------+----------------+-----------+-------------+
    | 8 bits     | 1 bits   | 1 bits      | 1 bits   | 1 bits   | 4 bits   | 16 bits        | 16 bits   | 16 bits     |
    +============+==========+=============+==========+==========+==========+================+===========+=============+
    | Magic=0xAB | Reserve  | Data no_ack | ERR Flag | ACK Flag | Version  | Payload length | CRC16     | Sequence ID |
    +------------+----------+-------------+----------+----------+----------+----------------+-----------+-------------+
    """
    MAGIC = 0xAB

    def __init__(self, data_no_ack, err_flag, ack_flag, version, payload_length, crc16, sequence_id, payload=b''):
        self.data_no_ack = data_no_ack
        self.err_flag = err_flag
        self.ack_flag = ack_flag
        self.version = version
        self.payload_length = payload_length
        self.crc16 = crc16
        self.sequence_id = sequence_id
        self.payload = payload

    def to_bytes(self):
        data = bytearray(
            [
                self.MAGIC,
                (self.data_no_ack << 2 | self.err_flag << 1 | self.ack_flag) << 4 | (self.version & 0b1111)
            ]
        )
        data += len(self.payload).to_bytes(2, 'big')
        data += self.crc16.to_bytes(2, 'big')
        data += self.sequence_id.to_bytes(2, 'big')
        data += self.payload
        return data

    @classmethod
    def from_bytes(cls, data):
        data_no_ack = bool(data[1] & (1 << 6))
        err_flag = bool(data[1] & (1 << 5))
        ack_flag = bool(data[1] & (1 << 4))
        version = data[1] & 0b1111
        payload_length = int.from_bytes(data[2:4], 'big')
        crc16 = int.from_bytes(data[4:6], 'big')
        sequence_id = int.from_bytes(data[6:8], 'big')
        payload = data[8:]

        if payload_length != len(payload):
            raise ValueError('{} from_bytes got wrong payload_length'.format(cls.__name__))

        return cls(
            data_no_ack,
            err_flag,
            ack_flag,
            version,
            payload_length,
            crc16,
            sequence_id,
            payload=payload
        )


class Layer2(Base):
    """
    L2 package(5-504 Bytes):
    +-------------+--------------+
    | L2 header   | L2 payload   |
    +=============+==============+
    | 2 bytes     | 0-502 bytes  |
    +-------------+--------------+

    L2 header(16 Bits):
    +----------+-----------+-----------+
    | CMD ID   | Version   | Reserve   |
    +==========+===========+===========+
    | 8 bits   | 4 bits    | 4 bits    |
    +----------+-----------+-----------+
    """

    def __init__(self, cmd_id, version, payload=b''):
        self.cmd_id = cmd_id
        self.version = version
        self.payload = payload

    def to_bytes(self):
        return bytearray([self.cmd_id, self.version << 4]) + self.payload

    @classmethod
    def from_bytes(cls, data):
        return cls(
            data[0],
            data[1] >> 4,
            data[2:]
        )


class Key(Base):
    """
     L2 Key(N bits):
    +----------+------------+-----------+
    | 1 byte   | 2 bytes    | N bytes   |
    +==========+============+===========+
    | Key      | Key header | Key value |
    +----------+------------+-----------+

    L2 Key header(16 bits):
    +-----------+--------------------+
    | Reserve   | Key value length   |
    +===========+====================+
    | 7 bits    | 9 bits             |
    +-----------+--------------------+
    """

    def __init__(self, ident, value=b''):
        self.ident = ident
        self.value = value

    def to_bytes(self):
        length = len(self.value)
        if length > (1 << 9) - 1:
            raise ValueError('{} to_bytes got length out of range'.format(type(self).__name__))
        data = bytearray([self.ident])
        data += length.to_bytes(2, 'big')
        data += self.value
        return data


class Payload(Base):
    """
    L2 Payload:
    +----------+------------+-----------+----------+------------+-----------+-------+
    | 1 byte   | 2 bytes    | N bytes   | 1 byte   | 2 bytes    | N bytes   | ...   |
    +==========+============+===========+==========+============+===========+=======+
    | Key      | Key header | Key value | Key      | Key header | Key value | ...   |
    +----------+------------+-----------+----------+------------+-----------+-------+
    """

    def __init__(self, keys=()):
        self.keys = keys

    def __iter__(self):
        return iter(self.keys)

    def to_bytes(self):
        data = bytearray()
        for temp in (k.to_bytes() for k in self.keys):
            data += temp
        return data

    @classmethod
    def from_bytes(cls, data):
        keys = []
        start, end = 0, len(data) - 1
        while start < end:
            ident = data[start]
            key_header = data[start + 1: start + 3]
            length = int.from_bytes(key_header, 'big') & 0x1ff
            value = data[start + 3: start + 3 + length]
            if len(value) != length:
                raise ValueError('{} from_bytes got length not enough'.format(cls.__name__))
            keys.append(Key(ident, value))
            start = start + 3 + length
        return cls(keys=keys)


class Message(Base):

    def __init__(
            self,
            data_no_ack=False,
            err_flag=False,
            ack_flag=False,
            version=0,
            sequence_id=0,
            cmd_id=None,
            cmd_version=0,
            payload=b''
    ):
        self.data_no_ack = data_no_ack
        self.err_flag = err_flag
        self.ack_flag = ack_flag
        self.version = version
        self.sequence_id = sequence_id
        self.cmd_id = cmd_id
        self.cmd_version = cmd_version
        self.payload = payload

    @staticmethod
    def calc_crc16(data):
        crc = 0
        for byte in data:
            crc = (crc >> 8) ^ crc16_table[(crc ^ byte) & 0xff]
        return crc

    def to_bytes(self):
        if not hasattr(self, '__raw__'):
            if self.cmd_id is not None and self.cmd_version is not None:
                layer2 = Layer2(
                    self.cmd_id,
                    self.cmd_version,
                    payload=self.payload
                )
                payload = layer2.to_bytes()
            else:
                payload = b''

            crc16 = self.calc_crc16(payload)
            layer1 = Layer1(
                self.data_no_ack,
                self.err_flag,
                self.ack_flag,
                self.version,
                len(payload),
                crc16,
                self.sequence_id,
                payload=payload
            )
            setattr(self, '__raw__', layer1.to_bytes())
        return getattr(self, '__raw__')

    @classmethod
    def from_bytes(cls, data):
        layer1 = Layer1.from_bytes(data)
        if layer1.payload:
            layer2 = Layer2.from_bytes(layer1.payload)
            self = cls(
                layer1.data_no_ack,
                layer1.err_flag,
                layer1.ack_flag,
                layer1.version,
                layer1.sequence_id,
                layer2.cmd_id,
                layer2.version,
                payload=layer2.payload
            )
        else:
            self = cls(
                layer1.data_no_ack,
                layer1.err_flag,
                layer1.ack_flag,
                layer1.version,
                layer1.sequence_id
            )
        setattr(self, '__raw__', data)
        return self

    def parse(self):
        return Payload.from_bytes(self.payload)

    def make_response(self, cmd_id=None, payload=b'', err_flag=False):
        return type(self)(
            data_no_ack=True,
            err_flag=err_flag,
            ack_flag=False,
            sequence_id=self.sequence_id,
            cmd_id=cmd_id,
            payload=payload
        )


class Parser(object):

    def __init__(self):
        self.__messages = []
        self.__buffer = b''

    def clear(self):
        self.__buffer = b''

    @property
    def messages(self):
        rv, self.__messages = self.__messages, []
        return rv

    def parse(self, buffer):
        self.__buffer += buffer
        while True:
            start = self.__buffer.find(b'\xAB')
            if start == -1:
                self.clear()
                break
            buffer_length = len(self.__buffer)
            if buffer_length - start < 8:
                break
            payload_length = int.from_bytes(self.__buffer[start + 2: start + 4], 'big')
            if payload_length > buffer_length - (start + 8):
                break
            crc16 = int.from_bytes(self.__buffer[start + 4: start + 6], 'big')
            if crc16 == Message.calc_crc16(self.__buffer[start + 8: start + 8 + payload_length]):
                self.__messages.append(Message.from_bytes(self.__buffer[start: start + 8 + payload_length]))
            self.__buffer = self.__buffer[payload_length + 8:]


if __name__ == '__main__':

    # 组包示例
    print('===========组包示例==================')
    request = Message(
        cmd_id=0x02,  # 设置命令(command Id: 0x02)，手机端将参数下发给设备设备端
        payload=Payload(
            # 参数是一个列表，成员是Key对象，每一个Key对象对应协议中的一个key，以下以设备语言设置命令 (0x4E）为例
            [
                Key(0x4E, b'\x00')  # 4E000100  # 设置语言为English
                # Key(0x4E, b'\x01')  # 4E000101  # 设置语言为中文
            ]
        ).to_bytes()
    )
    print('0x4E指令hex: ', request)
    print('data_no_ack: ', request.data_no_ack)
    print('err_flag: ', request.err_flag)
    print('ack_flag: ', request.ack_flag)
    print('version: ', request.version)
    print('sequence_id: ', request.sequence_id)
    print('cmd_id: ', request.cmd_id)
    print('cmd_version: ', request.cmd_version)
    print('payload: ', request.payload)  # L2层的layload，即多个key组成的字节串
    print('================================')

    # 解包示例
    # 1、模拟串口、蓝牙等接受到的数据
    m1 = Message(
        cmd_id=0x02,
        data_no_ack=True,
        ack_flag=True,
        payload=Payload(
            # 参数是一个列表，成员是Key对象，每一个Key对象对应协议中的一个key，以下以设备语言设置命令 (0x4E）为例
            [
                Key(0x50, b'\x00')  # 4E000100  # 设备语言返回命令 (0x50）
            ]
        ).to_bytes()
    )
    m2 = Message(
        cmd_id=0x02,
        data_no_ack=True,
        ack_flag=True,
        payload=Payload(
            # 参数是一个列表，成员是Key对象，每一个Key对象对应协议中的一个key，以下以设备语言设置命令 (0x4E）为例
            [
                Key(0x55, b'\x00\x64')  # 设备背光亮度返回命令 (0x55），背光100
            ]
        ).to_bytes()
    )
    data_from_serial = m1.to_bytes() + m2.to_bytes()  # 模拟串口获取2条来自蓝牙的消息报文
    # 2、对字节流解包
    parser = Parser()  # 单例对象，全局只需要一个就可以了
    parser.parse(data_from_serial)  # 传入读取的任意长度字节流即可
    for i, msg in enumerate(parser.messages):
        print('拆包出来的 {} 个消息: {}'.format(i, msg))
