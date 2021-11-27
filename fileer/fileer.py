import os

__filer_default_charset = 'utf-8'


def formatPath(path: str):
    """
    格式化路径，统一转换成 "/"
    :param path: 路径
    :return: 格式化路径
    """
    if path:
        import re
        return re.sub("/+", "/", path.replace("\\", "/"))


def fpath(path: str):
    """
    格式化路径，统一转换成 "/"
    :param path: 路径
    :return: 格式化路径
    """
    return formatPath(path)


def getParentAbsolutePath(path: str):
    """
    获取父目录的绝对路径
    :param path: 路径
    :return: 父目录的绝对路径
    """
    return fpath(os.path.abspath(os.path.dirname(path)))


def getAbsolutePath(path: str):
    """
    获取绝对路径
    :param path: 路径
    :return: 获取绝对路径
    """
    return fpath(os.path.abspath(path))


def paths(*path):
    """
    拼接路径
    :param path: 路径
    :return: 路径
    """
    if path:
        return fpath("/".join(path))


def filePaths(*path):
    """
    拼接路径
    :param path: 路径
    :return: 路径
    """
    if path:
        return fpath("/".join(path))


def existFile(filePath: str) -> bool:
    """
    文件是否存在
    :param filePath: 文件路径
    :return: 存在/不存在
    """
    return os.path.exists(filePath) and os.path.isfile(filePath)


def isFile(filePath: str) -> bool:
    """
    文件是否存在
    :param filePath: 文件路径
    :return: 存在/不存在
    """
    return existFile(filePath)


def existFolder(folder: str) -> bool:
    """
    文件夹是否存在
    :param folder: 文件夹路径
    :return:
    """
    return os.path.exists(folder) and os.path.isdir(folder)


def isFolder(folder: str) -> bool:
    """
    文件夹是否存在
    :param folder: 文件夹路径
    :return:
    """
    return existFolder(folder)


def getUserHome() -> str:
    """
    获取用户家目录
    :return: 用户家目录
    """
    return fpath(os.path.expanduser('~'))


def getUserWorkspace(workspace: str) -> str:
    """
    获取用户指定工作空间
    :param workspace 工作空间
    :return: 用户家目录工作空间
    """
    return paths(getUserHome(), workspace)


def getDesktop() -> str:
    """
    获取桌面路径
    :return:
    """
    return fpath(os.path.join(os.path.expanduser('~'), "Desktop"))


def getDesktopWorkspace(workspace: str) -> str:
    """
    获取桌面指定工作空间
    :return:
    """
    return paths(getDesktop(), workspace)


def getCurrentDir() -> str:
    """
    获取当前目录
    :return: 当前目录
    """
    return fpath(os.getcwd())


def getFolderName(path: str):
    """
    获取文件夹名称
    :param path: 文件夹路径
    :return: 文件夹名称
    """
    return os.path.basename(path)


def getFileName(path: str):
    """
    获取文件名称
    :param path: 文件路径
    :return: 文件名称
    """
    return os.path.basename(path)


def getFileExtName(filePath: str):
    """
    获取文件扩展名称
    :param filePath: 文件路径
    :return: 文件扩展名称
    """
    fileNamePath, fileExtension = os.path.splitext(filePath)
    return fileExtension


def fileName(path: str):
    """
    获取文件名称
    :param path: 文件路径
    :return: 文件名称
    """
    return getFileName(path)


def fileExtName(filePath: str):
    """
    获取文件扩展名称
    :param filePath: 文件路径
    :return: 文件扩展名称
    """
    return getFileExtName(filePath)


def createFolder(folder: str):
    """
    创建文件夹
    :param folder: 文件夹路径
    :return:
    """
    if not existFolder(folder):
        return os.makedirs(folder)


def createFile(filePath: str):
    """
    创建文件
    :param filePath: 文件路径
    :return:
    """
    if not existFile(filePath):
        createFolder(getParentAbsolutePath(filePath))
        with openWriteFile(filePath):
            pass


def newFile(filePath: str):
    """
    创建文件
    :param filePath: 文件路径
    :return:
    """
    return createFile(filePath)


def openFile(path: str, mode: str = 'r', encoding: str = None):
    """
    打开一个文件
    :param path: 文件路径
    :param mode: 打开模式
        t	文本模式 (默认)。
        x	写模式，新建一个文件，如果该文件已存在则会报错。
        b	二进制模式。
        +	打开一个文件进行更新(可读可写)。
        U	通用换行模式（不推荐）。
        r	以只读方式打开文件。文件的指针将会放在文件的开头。这是默认模式。
        rb	以二进制格式打开一个文件用于只读。文件指针将会放在文件的开头。这是默认模式。一般用于非文本文件如图片等。
        r+	打开一个文件用于读写。文件指针将会放在文件的开头。
        rb+	以二进制格式打开一个文件用于读写。文件指针将会放在文件的开头。一般用于非文本文件如图片等。
        w	打开一个文件只用于写入。如果该文件已存在则打开文件，并从开头开始编辑，即原有内容会被删除。如果该文件不存在，创建新文件。
        wb	以二进制格式打开一个文件只用于写入。如果该文件已存在则打开文件，并从开头开始编辑，即原有内容会被删除。如果该文件不存在，创建新文件。一般用于非文本文件如图片等。
        w+	打开一个文件用于读写。如果该文件已存在则打开文件，并从开头开始编辑，即原有内容会被删除。如果该文件不存在，创建新文件。
        wb+	以二进制格式打开一个文件用于读写。如果该文件已存在则打开文件，并从开头开始编辑，即原有内容会被删除。如果该文件不存在，创建新文件。一般用于非文本文件如图片等。
        a	打开一个文件用于追加。如果该文件已存在，文件指针将会放在文件的结尾。也就是说，新的内容将会被写入到已有内容之后。如果该文件不存在，创建新文件进行写入。
        ab	以二进制格式打开一个文件用于追加。如果该文件已存在，文件指针将会放在文件的结尾。也就是说，新的内容将会被写入到已有内容之后。如果该文件不存在，创建新文件进行写入。
        a+	打开一个文件用于读写。如果该文件已存在，文件指针将会放在文件的结尾。文件打开时会是追加模式。如果该文件不存在，创建新文件用于读写。
        ab+	以二进制格式打开一个文件用于追加。如果该文件已存在，文件指针将会放在文件的结尾。如果该文件不存在，创建新文件用于读写。
    :param encoding: 编码
    :return: IO文件对象
    """
    if encoding:
        return open(path, mode, encoding=encoding)
    else:
        return open(path, mode)


def openReadFile(path: str, encoding=__filer_default_charset):
    """
    以只读模式打开文件
    :param path: 文件路径
    :param encoding: 编码
    :return: IO文件对象
    """
    return openFile(path, "r", encoding)


def openWriteFile(path: str, append: bool = False, encoding=__filer_default_charset):
    """
    以写入模式打开文件
    :param path: 文件路径
    :param append: 是否追加数据（True/False）
    :param encoding: 编码
    :return: IO文件对象
    """
    createFolder(getParentAbsolutePath(path))
    if append:
        return openFile(path, "a+", encoding)
    else:
        return openFile(path, "w+", encoding)


def openReadBytesFile(path: str):
    """
    以只读模式打开二进制文件
    :param path: 文件路径
    :return: IO文件对象
    """
    return openFile(path, "rb")


def openWriteBytesFile(path: str, append: bool = False):
    """
    以写入模式打开二进制文件
    :param path: 文件路径
    :param append: 是否追加数据（True/False）
    :return: IO文件对象
    """
    createFolder(getParentAbsolutePath(path))
    if append:
        return openFile(path, "ab+")
    else:
        return openFile(path, "wb+")


def readFile(path, encoding=__filer_default_charset):
    """
    读取文件内容
    :param path: 文件内容
    :param encoding: 编码
    :return: 文件内容
    """
    with openReadFile(path, encoding) as f:
        lines = f.read()
        return lines


def readFileLines(path, encoding=__filer_default_charset):
    """
    读取文件数据行
    :param path: 文件路径
    :param encoding: 编码
    :return: 数据行列表
    """
    with openReadFile(path, encoding) as f:
        lines = f.readlines()
        lines = [row.rstrip("\n") for row in lines]
        return lines


def handleFileLines(path, fun, encoding=__filer_default_charset):
    """
    使用回调函数fun 处理每一行数据
    :param path: 文件路径
    :param fun: 回调函数
    :param encoding: 编码
    :return:
    """
    with openReadFile(path, encoding) as f:
        for row in f:
            fun(row.rstrip("\n"))


def readFileBytes(path) -> bytes:
    """
    读取文件字节数据
    :param path: 文件路径
    :return: 字节数组
    """
    with openReadBytesFile(path) as f:
        return f.read()


def writeFile(path, text, append: bool = False, encoding=__filer_default_charset):
    """
    写入数据到文件
    :param path: 文件路径
    :param text: 写入文本数据
    :param append: 是否追加数据（True/False）
    :param encoding: 编码
    :return:
    """
    with openWriteFile(path, append, encoding) as f:
        f.write(text)


def writeFileLine(path, line: str, append: bool = False, encoding=__filer_default_charset):
    """
    写入一行数据到文件
    :param path: 文件路径
    :param line: 一行文本数据
    :param append: 是否追加数据（True/False）
    :param encoding: 编码
    :return:
    """
    with openWriteFile(path, append, encoding) as f:
        f.write(line + '\n')


def writeFileLines(path, lines: (list, tuple, str), append: bool = False, encoding=__filer_default_charset):
    """
    批量写入数据行到文件
    :param path: 文件路径
    :param lines: 数据行
    :param append: 是否追加数据（True/False）
    :param encoding: 编码
    :return:
    """
    with openWriteFile(path, append, encoding) as f:
        if isinstance(lines, str):
            f.write(lines + '\n')
        else:
            for line in lines:
                f.writelines(line + '\n')
                f.flush()


def writeFileBytes(path, byteArray: bytes, append: bool = False):
    """
    写入字节数组到二进制文件
    :param path: 文件内容
    :param byteArray: 字节数组
    :param append: 是否追加数据（True/False）
    :return:
    """
    with openWriteBytesFile(path, append) as f:
        f.write(byteArray)
        f.flush()


def copyFile(source: str, target: str):
    """
    复制文件
    :param source: 源文件路径
    :param target: 目标文件路径
    :return:
    """
    if existFile(source):
        import shutil
        # 拷贝文件，包括全部信息
        shutil.copy2(source, target)


def copyFolder(source: str, target: str):
    """
    复制文件夹
    :param source: 源文件夹路径
    :param target: 目标文件夹路径
    :return:
    """
    if existFolder(source):
        import shutil
        # 拷贝目录及文件， 新文件不能存在
        shutil.copytree(source, target)


def renameFile(path: str, newFileName: str) -> str:
    """
    文件重命名
    :param path: 文件/目录路径
    :param newFileName: 新文件名称
    :return: 新文件绝对路径
    """
    if os.path.exists(path):
        target = paths(getParentAbsolutePath(path), newFileName)
        os.rename(path, target)
        return target


def moveFile(source: str, target: str):
    """
    移动文件
        moveFile("test.txt", "data")
        moveFile("test.txt", "data/new_test.txt")
    :param source: 源文件
    :param target: 文件/目录
    :return:
    """
    if existFile(source):
        import shutil
        shutil.move(source, target)


def moveFolder(source: str, target: str):
    """
    移动整个目录
    :param source:源目录
    :param target:目标目录
    :return:
    """
    if existFolder(source):
        import shutil
        shutil.move(source, target)


def delete(path: str):
    """
    删除文件或目录
    :param path: 文件/文件夹路径
    :return:
    """
    if existFile(path):
        deleteFile(path)
    if existFolder(path):
        deleteFolder(path)


def deleteFile(file: str):
    """
    删除文件
    :param file: 文件路径
    :return:
    """
    if existFile(file):
        os.remove(file)


def deleteFolder(folder: str):
    """
    删除文件夹所有内容
    :param folder: 文件夹路径
    :return:
    """
    if existFolder(folder):
        import shutil
        shutil.rmtree(folder)


def rmFile(file: str):
    """
    删除文件
    :param file: 文件路径
    :return:
    """
    deleteFile(file)


def rmFolder(folder: str):
    """
    删除文件夹所有内容
    :param folder: 文件夹路径
    :return:
    """
    deleteFolder(folder)


def rm(path: str):
    """
    删除文件或目录
    :param path: 文件/文件夹路径
    :return:
    """
    delete(path)


def listFiles(folder: str, includeFolder: bool = False) -> list[str]:
    """
    列出目录下所有文件
    :param folder: 文件夹路径
    :param includeFolder: 是否包含文件夹 (True/False)
    :return:
    """
    files = []
    for fileDir, dirs, fs in os.walk(folder):
        if includeFolder:
            files.append(getAbsolutePath(fileDir))
        for fn in fs:
            files.append(paths(getAbsolutePath(fileDir), fn))
    return files


def handleFiles(folder: str, fun, includeFolder: bool = False):
    """
    回调函数处理文件
    :param folder:文件夹
    :param fun: 回调函数
    :param includeFolder: 是否包含文件夹 (True/False)
    :return:
    """
    for fileDir, dirs, fs in os.walk(folder):
        if includeFolder:
            fun(getAbsolutePath(fileDir))
        for fn in fs:
            fun(paths(getAbsolutePath(fileDir), fn))


def pack(packFolder: str, packFileName: str = None, mode: str = 'zip'):
    """
    压缩目录
    :param packFolder: 需要压缩的目录（必须是存在的目录）
    :param packFileName: 压缩文件（路径）名称
    :param mode: 压缩模式
        "zip", "tar", "gztar","bztar", or "xztar"
    :return: 压缩文件路径
    """
    if existFolder(packFolder):
        import shutil
        if not packFileName:
            packFileName = fileName(packFolder)
        return shutil.make_archive(packFileName, mode, packFolder)


def unpack(packFilePath: str, unpackFolder: str = None, mode: str = None):
    """
    解压文件
    :param packFilePath: 压缩文件路径
    :param unpackFolder: 解压后的目录
    :param mode: 解压模式
        "zip", "tar", "gztar","bztar", or "xztar"
    :return:
    """
    if existFile(packFilePath):
        import shutil
        return shutil.unpack_archive(packFilePath, unpackFolder, mode)


def packZip(packFolder: str, packFileName: str = None):
    """
    zip压缩目录
    :param packFolder: 需要压缩的目录（必须是存在的目录）
    :param packFileName: 压缩文件（路径）名称
    :return: zip压缩文件路径
    """
    return pack(packFolder, packFileName, 'zip')


def unpackZip(packFilePath: str, unpackFolder: str = None):
    """
    解压zip文件
    :param packFilePath: zip压缩文件路径
    :param unpackFolder: 解压后的目录
    :return:
    """
    return unpack(packFilePath, unpackFolder, 'zip')


def packTar(packFolder: str, packFileName: str = None):
    """
    tar压缩目录
    :param packFolder: 需要压缩的目录（必须是存在的目录）
    :param packFileName: tar压缩文件（路径）名称
    :return: tar压缩文件路径
    """
    return pack(packFolder, packFileName, 'tar')


def unpackTar(packFilePath: str, unpackFolder: str = None):
    """
    解压tar文件
    :param packFilePath: tar压缩文件路径
    :param unpackFolder: 解压后的目录
    :return:
    """
    return unpack(packFilePath, unpackFolder, 'tar')


def packGzTar(packFolder: str, packFileName: str = None):
    """
    tar.gz压缩目录
    :param packFolder: 需要压缩的目录（必须是存在的目录）
    :param packFileName: tar.gz压缩文件（路径）名称
    :return:  tar.gz压缩文件路径
    """
    return pack(packFolder, packFileName, 'gztar')


def unpackGzTar(packFilePath: str, unpackFolder: str = None):
    """
    解压tar.gz文件
    :param packFilePath: tar.gz压缩文件路径
    :param unpackFolder: 解压后的目录
    :return:
    """
    return unpack(packFilePath, unpackFolder, 'gztar')


def packXzTar(packFolder: str, packFileName: str = None):
    """
    tar.xz压缩目录
    :param packFolder: 需要压缩的目录（必须是存在的目录）
    :param packFileName: tar.xz压缩文件（路径）名称
    :return:  tar.xz压缩文件路径
    """
    return pack(packFolder, packFileName, 'xztar')


def unpackXzTar(packFilePath: str, unpackFolder: str = None):
    """
    解压tar.xz文件
    :param packFilePath: tar.xz压缩文件路径
    :param unpackFolder: 解压后的目录
    :return:
    """
    return unpack(packFilePath, unpackFolder, 'xztar')


def packBzTar(packFolder: str, packFileName: str = None):
    """
    tar.bz2压缩目录
    :param packFolder: 需要压缩的目录（必须是存在的目录）
    :param packFileName: tar.bz2压缩文件（路径）名称
    :return: tar.bz2压缩文件路径
    """
    return pack(packFolder, packFileName, 'bztar')


def unpackBzTar(packFilePath: str, unpackFolder: str = None):
    """
    解压tar.bz2文件
    :param packFilePath: tar.bz2压缩文件路径
    :param unpackFolder: 解压后的目录
    :return:
    """
    return unpack(packFilePath, unpackFolder, 'bztar')
