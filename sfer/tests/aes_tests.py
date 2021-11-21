import sfer

password = 'test'
enc = sfer.aes256Encrypt("test",password)
data = sfer.aes256Decrypt(enc, password)

print(f"{data} - {enc}")


password = "1234567812345678"
a = sfer.Aes(password)
print(a.encrypt("test"))
print(a.decrypt(a.encrypt("test"), password))