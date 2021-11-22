import datetime
import os
import smtplib
import uuid
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.utils import formataddr
import fileer


class Mailer(object):
    def __init__(self, host: str, port: int, username: str, password: str, fromName=None, encoding: str = 'utf-8',
                 debug=False):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.encoding = encoding
        self.debug = debug
        self.fromName = fromName
        if not fromName:
            self.fromName = username
        self.smtpObj = smtplib.SMTP()
        self.smtpObj.connect(self.host, port)
        self.smtpObj.login(self.username, self.password)

    def sendHtmlFile(self, title: str, htmlFilePath: str, receivers: (str, list, set, tuple),
                     files: (str, list, set, tuple) = None,
                     encoding=None, **templateVariables):
        """
        发送Html邮件（模板文件）
        :param title: 邮件标题
        :param htmlFilePath: html模板路径
        :param receivers: 接收人（数组、字符串）
            为字符串时，使用逗号分割
        :param files: 附件（数组、字符串）
            1.为字符串时，使用逗号分割，例如："file1.txt,file2.txt,通话.mp3,美女.jpg"
            2.列表元组：[("file1.txt", "f1.txt"),("file2.txt")]
            3.列表字典：[{"filePath:'file1.txt',"fileName:'file1.txt'"},{"filePath:'file2.docx',"fileName:'读书笔记.docx'"}]
        :param encoding: 字符编码
        :param templateVariables: 模板文件变量
        :return:
        """
        if fileer.existFile(htmlFilePath):
            htmlFileData = fileer.readFile(htmlFilePath)
            if len(htmlFileData.strip()) > 0:
                newTemplateVariables = dict(templateVariables)
                newTemplateVariables['__title'] = title
                newTemplateVariables['__filePath'] = os.path.abspath(htmlFilePath)
                newTemplateVariables['__receivers'] = receivers
                newTemplateVariables['__files'] = files
                newTemplateVariables['__encoding'] = encoding
                newTemplateVariables['__today'] = datetime.date.today().strftime("%Y-%m-%d")
                message = htmlFileData.format_map(newTemplateVariables)
                del newTemplateVariables
                self.sendEmail(title, message, receivers, files, 'html', encoding)

    def sendHtml(self, title: str, html: str, receivers: (str, list, set, tuple), files: (str, list, set, tuple) = None,
                 encoding: str = None):
        """
        发送Html邮件
        :param title: 邮件标题
        :param html: html内容
        :param receivers: 接收人（数组、字符串）
            为字符串时，使用逗号分割
        :param files: 附件（数组、字符串）
            1.为字符串时，使用逗号分割，例如："file1.txt,file2.txt,通话.mp3,美女.jpg"
            2.列表元组：[("file1.txt", "f1.txt"),("file2.txt")]
            3.列表字典：[{"filePath:'file1.txt',"fileName:'file1.txt'"},{"filePath:'file2.docx',"fileName:'读书笔记.docx'"}]
        :param encoding: 字符编码
        :return:
        """
        return self.sendEmail(title, html, receivers, files, 'html', encoding)

    def sendText(self, title: str, text: str, receivers: (str, list, set, tuple), files: (str, list, set, tuple) = None,
                 encoding: str = None):
        """
        发送Html邮件
        :param title: 邮件标题
        :param text: 文本内容
        :param receivers: 接收人（数组、字符串）
            为字符串时，使用逗号分割
        :param files: 附件（数组、字符串）
            1.为字符串时，使用逗号分割，例如："file1.txt,file2.txt,通话.mp3,美女.jpg"
            2.列表元组：[("file1.txt", "f1.txt"),("file2.txt")]
            3.列表字典：[{"filePath:'file1.txt',"fileName:'file1.txt'"},{"filePath:'file2.docx',"fileName:'读书笔记.docx'"}]
        :param encoding: 字符编码
        :return:
        """
        return self.sendEmail(title, text, receivers, files, 'plain', encoding)

    def sendEmail(self, title: str, emailContent: str, receivers: (str, list, set, tuple),
                  files: (str, list, set, tuple) = None, type: str = "plain", encoding: str = None):

        """
        发送邮件
        :param title: 邮件标题
        :param emailContent: 邮件内容
        :param receivers: 接收人（数组、字符串）
            为字符串时，使用逗号分割
        :param files: 附件（数组、字符串）
            1.为字符串时，使用逗号分割，例如："file1.txt,file2.txt,通话.mp3,美女.jpg"
            2.列表元组：[("file1.txt", "f1.txt"),("file2.txt")]
            3.列表字典：[{"filePath:'file1.txt',"fileName:'file1.txt'"},{"filePath:'file2.docx',"fileName:'读书笔记.docx'"}]
        :param type: 文件内容类型 （“plain” , "html"）
        :param encoding: 字符编码
        :return:
        """
        if not encoding:
            encoding = self.encoding

        msg = MIMEMultipart()
        msg["Subject"] = Header(title, encoding)
        msg['From'] = formataddr((self.fromName, self.username), encoding)
        if isinstance(receivers, str):
            receivers = receivers.split(",")
        msg["To"] = Header(",".join(receivers), encoding)

        # 邮件正文内容
        msg.attach(MIMEText(emailContent, type, encoding))

        # 添加附件
        if files and len(files) > 0:
            if isinstance(files, str):
                files = files.split(",")
            # 循环添加附件
            for file in files:
                fileData = None
                fileName = None
                if isinstance(file, str) and fileer.existFile(file):
                    fileData = fileer.readFileBytes(file)
                    fileName = fileer.getFileName(file)
                if isinstance(file, (bytes, bytearray)):
                    fileData = file
                    fileName = str(uuid.uuid3(uuid.uuid4(), str(uuid.uuid1())))
                if isinstance(file, tuple) and len(file) > 0 and fileer.existFile(file[0]):
                    fileData = fileer.readFileBytes(file[0])
                    if len(file) >= 2:
                        fileName = file[1]
                    else:
                        fileName = fileer.getFileName(file[0])
                if isinstance(file, dict) and file['filePath'] and fileer.existFile(file['filePath']):
                    fileData = fileer.readFileBytes(file['filePath'])
                    if file['fileName']:
                        fileName = file['fileName']
                    else:
                        fileName = fileer.getFileName(file['filePath'])
                if fileData:
                    if fileName.endswith(("bmp", "jpg", "png", "tif", "gif", "svg", "psd", "webp",
                                          "BMP", "JPG", "PNG", "TIF", "GIF", "SVG", "PSD", "WEBP")):
                        attFile = MIMEImage(fileData)
                        attFile["Content-Type"] = 'application/octet-stream'
                    else:
                        attFile = MIMEApplication(fileData)
                    attFile.add_header('Content-Disposition', 'attachment', filename=(encoding, '', fileName))
                    msg.attach(attFile)

        self.smtpObj.sendmail(self.username, receivers, msg.as_string())

    def __del__(self):
        self.smtpObj.quit()


class QQMailer(Mailer):
    """
    QQ邮箱
    """

    def __init__(self, username: str, password: str, port: int = 25, fromName=None, encoding: str = 'utf-8',
                 debug=False):
        super().__init__("smtp.qq.com", port, username, password, fromName, encoding, debug)


class NeteaseMailer(Mailer):
    """
    网易邮箱
    """

    def __init__(self, username: str, password: str, port: int = 25, fromName=None, encoding: str = 'utf-8',
                 debug=False):
        super().__init__("smtp.163.com", port, username, password, fromName, encoding, debug)


class GoogleMailer(Mailer):
    """
    Google邮箱
    """

    def __init__(self, username: str, password: str, port: int = 25, fromName=None, encoding: str = 'utf-8',
                 debug=False):
        super().__init__("smtp.gmail.com", port, username, password, fromName, encoding, debug)


class GMailer(GoogleMailer):
    """
    Google邮箱
    """

    def __init__(self, username: str, password: str, port: int = 25, fromName=None, encoding: str = 'utf-8',
                 debug=False):
        super().__init__("smtp.gmail.com", port, username, password, fromName, encoding, debug)
