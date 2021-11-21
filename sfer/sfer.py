import hashlib
import rsa
import base64
import aes256


class Rsa:
    """
    公钥加密、签名，私钥解密、验签
    加密，是希望密文只有接收方可以解密，也就只能由接收方用自己的私钥解密，所以发送方用接收方的公钥加密信息后发送给接收方。
    签名，是希望接收方可以肯定信息是由发送方发来的，那么信息就必须用只有发送方知道的密钥加密也就是用发送方的私钥加密，然后接收方用发送方的公钥解密，以判断信息是不是由发送方发来。
    """

    def __init__(self, pub_key: str = None, pri_key: str = None, encoding='utf-8'):
        self.encoding = encoding
        if pub_key or pri_key:
            self.publicKey = rsa.PublicKey.load_pkcs1(pub_key.encode())
            self.privateKey = rsa.PrivateKey.load_pkcs1(pri_key.encode())
        else:
            keys = self.generateRsaKeys()
            self.privateKey = rsa.PrivateKey.load_pkcs1(keys[0].encode())
            self.publicKey = rsa.PublicKey.load_pkcs1(keys[1].encode())

    @staticmethod
    def generateRsaKeys(nbits=2048) -> tuple:
        """
        生成Rsa密钥对
        :param nbits: 默认2048位
        :return: Rsa密钥对（privateKey，publicKey）
        """
        # 生成密钥
        (publicKey, privateKey) = rsa.newkeys(nbits)
        keys = (privateKey.save_pkcs1().decode(), publicKey.save_pkcs1().decode())
        return keys

    def encryptBytes(self, plainData: (bytes, bytearray, str)) -> bytes:
        """
        加密数据
        :param plainData: 明文数据 (明文字节数组/明文字符串)
        :return: 加密数据的字节数组
        """
        if isinstance(plainData, (bytes, bytearray)):
            return rsa.encrypt(plainData, self.publicKey)
        return rsa.encrypt(plainData.encode(self.encoding), self.publicKey)

    def encryptBase64(self, plainData: (bytes, bytearray, str)) -> str:
        """
        加密数据
        :param plainData: 明文数据 (明文字节数组/明文字符串)
        :return: 加密数据的base64
        """
        dataBytes = self.encryptBytes(plainData)
        return base64.b64encode(dataBytes).decode(self.encoding)

    def encrypt(self, plainData: (bytes, bytearray, str)) -> str:
        """
        加密数据 , 同 encryptBase64()
        :param plainData: 明文数据 (明文字节数组/明文字符串)
        :return: 加密数据的base64
        """
        return self.encryptBase64(plainData)

    def decryptBytes(self, encryptData: (bytes, bytearray, str)):
        """
        解密数据
        :param encryptData: 加密数据 加密字节数组/base64(加密字节数组)
        :return: 返回明文字节数组数据
        """
        if isinstance(encryptData, (bytes, bytearray)):
            encryptDataByes = encryptData
        else:
            encryptDataByes = base64.b64decode(encryptData)
        return rsa.decrypt(encryptDataByes, self.privateKey)

    def decryptBase64(self, encryptData: (bytes, bytearray, str)):
        """
        解密数据
        :param encryptData: 加密数据 加密字节数组/base64(加密字节数组)
        :return: 返回明文字符串
        """
        return self.decryptBytes(encryptData).decode(self.encoding)

    def decrypt(self, encryptData: (bytes, bytearray, str)):
        """
        解密数据
        :param encryptData: 加密数据 加密字节数组/base64(加密字节数组)
        :return: 返回明文字符串
        """
        return self.decryptBase64(encryptData)

    def signBytes(self, plainData: (bytes, bytearray, str), signMethod: str = 'SHA-1'):
        """
        获取签名数据
        :param plainData: 解密后的明文数据 (明文字节数组/明文字符串)
        :param signMethod: 签名的算法
        :return: 签名字节数组
        """
        if isinstance(plainData, (bytes, bytearray)):
            return rsa.sign(plainData, self.privateKey, signMethod)
        return rsa.sign(plainData.encode(self.encoding), self.privateKey, signMethod)

    def signBase64(self, plainData: (bytes, bytearray, str), signMethod: str = 'SHA-1'):
        """
        获取签名
        :param plainData: 解密后的明文数据 (明文字节数组/明文字符串)
        :param signMethod: 签名的算法
        :return: 签名base64字符串
        """
        return base64.b64encode(self.signBytes(plainData, signMethod)).decode(self.encoding)

    def sign(self, plainData: (bytes, bytearray, str), signMethod: str = 'SHA-1'):
        """
        获取签名
        :param plainData: 解密后的明文数据 (明文字节数组/明文字符串)
        :param signMethod: 签名的算法
        :return: 签名base64字符串
        """
        return self.signBase64(plainData, signMethod)

    def verifySign(self, plainData: (bytes, bytearray, str), signData: (bytes, bytearray, str)) -> bool:
        """
        验证签名
        :param plainData: 解密后的明文数据 (明文字节数组/明文字符串)
        :param signData: 签名数据 字节数组/base64(字节数组)
        :return: 结果 True/False
        """
        if isinstance(plainData, (bytes, bytearray)):
            dataBytes = signData
        else:
            dataBytes = plainData.encode(self.encoding)
        if isinstance(signData, (bytes, bytearray)):
            signBytes = signData
        else:
            signBytes = base64.b64decode(signData)
        try:
            rsa.verify(dataBytes, signBytes, self.publicKey)
            return True
        except rsa.pkcs1.VerificationError:
            return False


class Aes:

    def __init__(self, password=None, iv=None):
        if not iv:
            iv = "0123456789abcdef"
        self.password = password
        self.iv = iv

    def encrypt(self, data, password=None, iv: str = None, encoding='utf-8') -> str:
        """
        加密
        :param data: 明文字符串数据
        :param password: 密码
        :param iv: 向量
        :param encoding: 编码
        :return: base64编码后的加密数据
        """
        return self.encryptBase64(data, password, iv, encoding).decode()

    def decrypt(self, data, password, iv: str = None, encoding='utf-8') -> str:
        """
        解密数据
        :param data: base64加密数据
        :param password: 密码
        :param iv: 向量
        :param encoding: 编码
        :return: 解密后的字符串
        """
        return self.decryptBase64(data, password, iv, encoding).decode()

    def encryptBase64(self, data, password=None, iv: str = None, encoding='utf-8') -> bytes:
        """
        加密数据
        :param data: 待加密文本数据
        :param password: 密码
        :param iv: 向量
        :param encoding: 编码
        :return: base64后的字节数组
        """
        return base64.b64encode(self.encryptBytes(data, password, iv, encoding))

    def decryptBase64(self, base64Data, password, iv: str = None, encoding='utf-8') -> bytes:
        """
        解密数据
        :param base64Data: 加密后的base64字节数组
        :param password: 密码
        :param iv: 向量
        :param encoding: 编码
        :return: 字节数组
        """
        return self.decryptBytes(base64.b64decode(base64Data), password, iv, encoding)

    def encryptBytes(self, data, password=None, iv: str = None, encoding='utf-8') -> bytes:
        """
        加密文本数据
        :param data: 明文数据
        :param password: 密码
        :param iv: 向量
        :param encoding: 编码
        :return:
        """
        if not password:
            password = self.password
        if not iv:
            iv = self.iv
        from Cryptodome.Cipher import AES
        cipher = AES.new(password.encode(encoding), AES.MODE_CBC, iv.encode(encoding))
        return cipher.encrypt(self.__pkcs7_padding(data, encoding))

    def decryptBytes(self, dataBytes, password, iv: str = None, encoding='utf-8') -> bytes:
        """
        解密字节数组
        :param dataBytes: 加密后的字节数组
        :param password: 密码
        :param iv: 向量
        :param encoding: 编码
        :return:
        """
        if not password:
            password = self.password
        if not iv:
            iv = self.iv
        ct = dataBytes
        from Cryptodome.Cipher import AES
        cipher = AES.new(password.encode(encoding), AES.MODE_CBC, iv.encode(encoding))
        return self.__pkcs7_trimming(cipher.decrypt(ct))

    def __pkcs7_padding(self, s, encoding='utf-8'):
        BLOCK_SIZE = 16
        s_len = len(s.encode(encoding))
        s = s + (BLOCK_SIZE - s_len % BLOCK_SIZE) * chr(BLOCK_SIZE - s_len % BLOCK_SIZE)
        return bytes(s, encoding)

    def __pkcs7_trimming(self, s):
        if len(s) > 0:
            return s[0:-s[-1]]


def aes256Encrypt(raw: str, passphrase: str):
    """
    aes加密
    :param raw: 文本数据
    :param passphrase: 密码（支持任意长度）
    :return: 密文
    """
    return aes256.encrypt(raw, passphrase).decode()


def aes256Decrypt(enc: str, passphrase: str):
    """
    aes解密
    :param enc: 加密数据
    :param passphrase: 密码（支持任意长度）
    :return:
    """
    return aes256.decrypt(enc, passphrase).decode()


def base64EncodeString(data: (bytes, bytearray, str), encoding='utf-8') -> str:
    """
    转换成base64编码字符串
    :param data: 字节数组/明文字符串
    :param encoding: 字符编码
    :return: base64字符串
    """
    if isinstance(data, (bytes, bytearray)):
        return base64EncodeBytes(data).decode(encoding)
    else:
        return base64EncodeBytes(str(data).encode(encoding)).decode(encoding)


def base64EncodeBytes(dataBytes: (bytes, bytearray)) -> bytes:
    """
    base64编码
    :param dataBytes: 字节数组
    :return: base64编码后的字节数组
    """
    return base64.b64encode(dataBytes)


def base64DecodeString(data: (bytes, bytearray, str), encoding='utf-8') -> str:
    """
    base64解码
    :param data: base64字符串/base64字节数组
    :param encoding: 字符编码
    :return: base64解码后的字符串
    """
    if isinstance(data, (bytes, bytearray)):
        return base64DecodeBytes(data).decode(encoding)
    else:
        return base64DecodeBytes(data.encode(encoding)).decode(encoding)


def base64DecodeBytes(dataBytes: (bytes, bytearray)) -> bytes:
    """
    base64解码
    :param dataBytes: 字节数组
    :return: base64解码后的字节数组
    """
    return base64.b64decode(dataBytes)


def getHash(data: (str, bytes, bytearray), hashName: str):
    """
    获取{hashName}算法的hash值
    :param data: 数据内容
    :param hashName: hash算法名称
            'md5',
            'sha1', 'sha224', 'sha256', 'sha384', 'sha512',
            'blake2b', 'blake2s',
            'sha3_224', 'sha3_256', 'sha3_384', 'sha3_512',
            'shake_128', 'shake_256'
    :return: hash值
    """
    return hashlib.new(hashName, data).hexdigest()


def getFileHash(filePath, hashName: str):
    """
    获取文件的{hashName}算法的hash值
    :param filePath: 文件路径
    :param hashName: hash算法名称
            'md5',
            'sha1', 'sha224', 'sha256', 'sha384', 'sha512',
            'blake2b', 'blake2s',
            'sha3_224', 'sha3_256', 'sha3_384', 'sha3_512',
            'shake_128', 'shake_256'
    :return: hash值
    """
    import fileer
    if fileer.existFile(filePath):
        dataBytes = fileer.readFileBytes(filePath)
        return hashlib.new(hashName, dataBytes).hexdigest()


def __hash_salt(hashFun, data: (str, bytes, bytearray), salt: str = "", encoding='utf-8'):
    """
    内部方法，不推荐使用
    """
    if not isinstance(data, (bytes, bytearray)):
        data = str(data).encode(encoding)
    low = hashFun(salt.encode(encoding))
    low.update(data)
    return low.hexdigest()


def md5(data: (str, bytes, bytearray), salt: (str, bytes, bytearray) = None, encoding='utf-8', upper: bool = False):
    """
    获取md5值
    :param data: 源字节数组/源字符串
    :param salt: md5加盐
    :param encoding: 字符编码
    :param upper: 是否大写
    :return: md5值
    """
    md5Value = __hash_salt(hashlib.md5, data, salt, encoding)
    if upper:
        return md5Value.upper()
    else:
        return md5Value


def md5File(filePath: str, salt: str = None, encoding='utf-8', upper: bool = False):
    """
    获取文件的md5值
    :param filePath: 文件路径
    :param salt: md5加盐
    :param encoding: 字符编码
    :param upper: 是否大写
    :return:
    """
    import fileer
    if fileer.existFile(filePath):
        dataBytes = fileer.readFileBytes(filePath)
        return md5(dataBytes, salt, encoding, upper)


def sha1(data: (str, bytes, bytearray), salt: str = None, encoding='utf-8'):
    """
    获取sha1 hash值
    :param data: 需要被hash的字节数组/字符串
    :param salt: hash算法加盐
    :param encoding: 字符编码
    :return: sha1 hash值
    """
    return __hash_salt(hashlib.sha1, data, salt, encoding)


def sha224(data: (str, bytes, bytearray), salt: str = None, encoding='utf-8'):
    """
    获取sha224 hash值
    :param data: 需要被hash的字节数组/字符串
    :param salt: hash算法加盐
    :param encoding: 字符编码
    :return: sha224 hash值
    """
    return __hash_salt(hashlib.sha224, data, salt, encoding)


def sha256(data: (str, bytes, bytearray), salt: str = None, encoding='utf-8'):
    """
    获取sha256 hash值
    :param data: 需要被hash的字节数组/字符串
    :param salt: hash算法加盐
    :param encoding: 字符编码
    :return: sha256 hash值
    """
    return __hash_salt(hashlib.sha256, data, salt, encoding)


def sha384(data: (str, bytes, bytearray), salt: str = None, encoding='utf-8'):
    """
    获取sha384 hash值
    :param data: 需要被hash的字节数组/字符串
    :param salt: hash算法加盐
    :param encoding: 字符编码
    :return: sha384 hash值
    """
    return __hash_salt(hashlib.sha384, data, salt, encoding)


def sha512(data: (str, bytes, bytearray), salt: str = None, encoding='utf-8'):
    """
    获取sha512 hash值
    :param data: 需要被hash的字节数组/字符串
    :param salt: hash算法加盐
    :param encoding: 字符编码
    :return: sha512 hash值
    """
    return __hash_salt(hashlib.sha512, data, salt, encoding)
