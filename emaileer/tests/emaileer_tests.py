
import emaileer

if __name__ == '__main__':
    mailer = emaileer.QQMailer("1727949032@qq.com", "kafnedgotjsgjbhg", fromName="kancy")
    mailer.sendText("测试", "demo", "793272861@qq.com", [("file1.txt", "f1"),("file2.txt")])
