import sfer

rsa = sfer.Rsa()

plainData = "你好！"

# 加密
encryptBase64 = rsa.encrypt(plainData)
# 签名
signBase64 = rsa.sign(plainData)

# 解密
decryptBase64 = rsa.decrypt(encryptBase64)

# 验证签名
verifySignResult = rsa.verifySign(decryptBase64, signBase64)

print(f"{encryptBase64},{signBase64},{decryptBase64},{verifySignResult}")
