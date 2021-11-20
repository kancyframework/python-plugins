import os
import re
import shutil
from typing import Any, IO

__filer_default_charset = 'utf-8'


def formatPath(path: str):
    if path:
        return re.sub("/+", "/", path.replace("\\", "/"))


def fpath(path: str):
    return formatPath(path)


def paths(*path):
    if path:
        return fpath("/".join(path))


def filePaths(*path):
    if path:
        return fpath("/".join(path))


def getUserHome() -> str:
    return fpath(os.path.expanduser('~'))


def getFileName(path: str):
    return os.path.basename(path)


def getFileExtName(path: str):
    fileNamePath, fileExtension = os.path.splitext(path)
    return fileExtension


def fileName(path: str):
    return getFileName(path)


def fileExtName(path: str):
    return getFileExtName(path)


def getParentAbsolutePath(path: str):
    return fpath(os.path.abspath(os.path.dirname(path)))


def getAbsolutePath(path: str):
    return fpath(os.path.abspath(path))


def existFile(file: str) -> bool:
    return os.path.exists(file) and os.path.isfile(file)


def isFile(file: str) -> bool:
    return existFile(file)


def existFolder(folder: str) -> bool:
    return os.path.exists(folder) and not os.path.isfile(folder)


def isFolder(folder: str) -> bool:
    return existFolder(folder)


def createFolder(folder: str):
    if not existFolder(folder):
        return os.makedirs(folder)


def createFile(filePath: str):
    if not existFile(filePath):
        createFolder(getParentAbsolutePath(filePath))
        with openWriteFile(filePath):
            pass


def newFile(filePath: str):
    return createFile(filePath)


def openFile(path: str, mode: str = 'r', encoding: str = None) -> IO[Any]:
    if encoding:
        return open(path, mode, encoding=encoding)
    else:
        return open(path, mode)


def openReadFile(path: str, encoding=__filer_default_charset) -> IO[Any]:
    return openFile(path, "r", encoding)


def openWriteFile(path: str, append: bool = False, encoding=__filer_default_charset) -> IO[Any]:
    if append:
        return openFile(path, "a+", encoding)
    else:
        return openFile(path, "w+", encoding)


def openReadBytesFile(path: str) -> IO[Any]:
    return openFile(path, "rb")


def openWriteBytesFile(path: str, append: bool = False) -> IO[Any]:
    if append:
        return openFile(path, "ab+")
    else:
        return openFile(path, "wb+")


def readFile(path, encoding=__filer_default_charset):
    with openReadFile(path, encoding) as f:
        lines = f.read()
        return lines


def readFileLines(path, encoding=__filer_default_charset):
    with openReadFile(path, encoding) as f:
        lines = f.readlines()
        lines = [row.rstrip("\n") for row in lines]
        return lines


def handleFileLines(path, fun, encoding=__filer_default_charset):
    with openReadFile(path, encoding) as f:
        for row in f:
            fun(row.rstrip("\n"))


def readFileBytes(path) -> bytes:
    with openReadBytesFile(path) as f:
        return f.read()


def writeFile(path, text, append: bool = False, encoding=__filer_default_charset):
    with openWriteFile(path, append, encoding) as f:
        f.write(text)


def writeFileLine(path, line: str, append: bool = False, encoding=__filer_default_charset):
    with openWriteFile(path, append, encoding) as f:
        f.write(line + '\n')


def writeFileLines(path, lines: (list, tuple, str), append: bool = False, encoding=__filer_default_charset):
    with openWriteFile(path, append, encoding) as f:
        if isinstance(lines, str):
            f.write(lines + '\n')
        else:
            for line in lines:
                f.writelines(line + '\n')
                f.flush()


def writeFileBytes(path, byteArray: bytes, append: bool = False):
    with openWriteBytesFile(path, append) as f:
        f.write(byteArray)
        f.flush()


def copyFile(source: str, target: str):
    if existFile(source):
        # 拷贝文件，包括全部信息
        shutil.copy2(source, target)


def copyFolder(source: str, target: str):
    if existFolder(source):
        # 拷贝目录及文件， 新文件不能存在
        shutil.copytree(source, target)


def renameFile(file: str, newFileName: str):
    if isFile(file):
        target = paths(getParentAbsolutePath(file), newFileName)
        shutil.move(file, target)


def moveFile(source: str, target: str):
    if existFile(source):
        shutil.move(source, target)


def moveFolder(source: str, target: str):
    if existFolder(source):
        shutil.move(source, target)


def delete(path: str):
    if existFile(path):
        deleteFile(path)
    if existFolder(path):
        deleteFolder(path)


def deleteFile(file: str):
    if existFile(file):
        os.remove(file)


def deleteFolder(folder: str):
    if existFolder(folder):
        shutil.rmtree(folder)


def rmFile(file: str):
    deleteFile(file)


def rmFolder(folder: str):
    deleteFolder(folder)


def rm(path: str):
    delete(path)


def pack(packFolder: str, packFileName: str = None, mode: str = 'zip'):
    """
    :param packFolder: 需要压缩的目录
    :param packFileName: 压缩文件（路径）名称
    :param mode: "zip", "tar", "gztar","bztar", or "xztar"
    :return: 压缩文件路径
    """
    if existFolder(packFolder):
        if not packFileName:
            packFileName = fileName(packFolder)
        return shutil.make_archive(packFileName, mode, packFolder)


def unpack(packFilePath: str, unpackFolder: str = None, mode: str = None):
    if existFile(packFilePath):
        return shutil.unpack_archive(packFilePath, unpackFolder, mode)


def packZip(packFolder: str, packFileName: str = None):
    return pack(packFolder, packFileName, 'zip')


def unpackZip(packFilePath: str, unpackFolder: str = None):
    return unpack(packFilePath, unpackFolder, 'zip')


def packTar(packFolder: str, packFileName: str = None):
    return pack(packFolder, packFileName, 'tar')


def unpackTar(packFilePath: str, unpackFolder: str = None):
    return unpack(packFilePath, unpackFolder, 'tar')


def packGzTar(packFolder: str, packFileName: str = None):
    return pack(packFolder, packFileName, 'gztar')


def unpackGzTar(packFilePath: str, unpackFolder: str = None):
    return unpack(packFilePath, unpackFolder, 'gztar')


def packXzTar(packFolder: str, packFileName: str = None):
    return pack(packFolder, packFileName, 'xztar')


def unpackXzTar(packFilePath: str, unpackFolder: str = None):
    return unpack(packFilePath, unpackFolder, 'xztar')


def packBzTar(packFolder: str, packFileName: str = None):
    return pack(packFolder, packFileName, 'bztar')


def unpackBzTar(packFilePath: str, unpackFolder: str = None):
    return unpack(packFilePath, unpackFolder, 'bztar')
