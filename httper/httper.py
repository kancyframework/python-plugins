import requests


def get(url: str, params=None, timeout=None, headers=None, **kwargs):
    """发送 GET 请求。
    :param url: 新 Request 对象的 URL。
    :param params: 请求参数
        字典：{k1:v1,k2:v2}
        数组：[(k1,v1),(k2,v2)]
    :param timeout: 超时时间，单位秒
        1.配置读超时 float
        2.配置连接超时，读超时。元组 (connect timeout, readtimeout) .
    :param headers: 请求头参数
        字典：{k1:v1,k2:v2}
        数组：[(k1,v1),(k2,v2)]
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    return requests.get(url, params=params, timeout=timeout, headers=headers, **kwargs)


def post(url: str, params=None, timeout=None, headers=None, **kwargs):
    """发送 POST 请求。
    :param url: 新 Request 对象的 URL。
    :param params: 请求参数
        字典：{k1:v1,k2:v2}
        数组：[(k1,v1),(k2,v2)]
    :param timeout: 超时时间，单位秒
        1.配置读超时 float
        2.配置连接超时，读超时。元组 (connect timeout, readtimeout) .
    :param headers: 请求头参数
        字典：{k1:v1,k2:v2}
        数组：[(k1,v1),(k2,v2)]
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    return requests.post(url, params=params, timeout=timeout, headers=headers, **kwargs)


def postJson(url: str, json=None, timeout=None, headers=None, **kwargs):
    """发送 POST 请求。
    :param url: 新 Request 对象的 URL。
    :param json: json请求体
    :param timeout: 超时时间，单位秒
        1.配置读超时 float
        2.配置连接超时，读超时。元组 (connect timeout, readtimeout) .
    :param headers: 请求头参数
        字典：{k1:v1,k2:v2}
        数组：[(k1,v1),(k2,v2)]
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    return requests.post(url, json=json, timeout=timeout, headers=headers, **kwargs)

def postJsonText(url: str, json=None, timeout=None, headers=None, **kwargs):
    """发送 POST 请求。
    :param url: 新 Request 对象的 URL。
    :param json: json请求体
    :param timeout: 超时时间，单位秒
        1.配置读超时 float
        2.配置连接超时，读超时。元组 (connect timeout, readtimeout) .
    :param headers: 请求头参数
        字典：{k1:v1,k2:v2}
        数组：[(k1,v1),(k2,v2)]
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    res = requests.post(url, json=json, timeout=timeout, headers=headers, **kwargs)
    if res:
        return res.text


def postForm(url: str, form: dict = None, timeout=None, headers=None, **kwargs):
    """发送 POST 请求。
    :param url: 新 Request 对象的 URL。
    :param form: 表单的数据，接收字典类型
    :param timeout: 超时时间，单位秒
        1.配置读超时 float
        2.配置连接超时，读超时。元组 (connect timeout, readtimeout) .
    :param headers: 请求头参数
        字典：{k1:v1,k2:v2}
        数组：[(k1,v1),(k2,v2)]
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    newForm = dict()
    for key in form:
        newForm[key] = (None, form[key])
    return requests.post(url, files=newForm, timeout=timeout, headers=headers, **kwargs)


def put(url: str, params=None, timeout=None, headers=None, **kwargs):
    """发送 PUT 请求。
    :param url: 新 Request 对象的 URL。
    :param params: 请求参数
        字典：{k1:v1,k2:v2}
        数组：[(k1,v1),(k2,v2)]
    :param timeout: 超时时间，单位秒
        1.配置读超时 float
        2.配置连接超时，读超时。元组 (connect timeout, readtimeout) .
    :param headers: 请求头参数
        字典：{k1:v1,k2:v2}
        数组：[(k1,v1),(k2,v2)]
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    return requests.put(url, params=params, timeout=timeout, headers=headers, **kwargs)


def putJson(url: str, json=None, timeout=None, headers=None, **kwargs):
    """发送 PUT 请求。
    :param url: 新 Request 对象的 URL。
    :param json: json请求体
    :param timeout: 超时时间，单位秒
        1.配置读超时 float
        2.配置连接超时，读超时。元组 (connect timeout, readtimeout) .
    :param headers: 请求头参数
        字典：{k1:v1,k2:v2}
        数组：[(k1,v1),(k2,v2)]
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    return requests.put(url, json=json, timeout=timeout, headers=headers, **kwargs)


def putForm(url: str, form: dict = None, timeout=None, headers=None, **kwargs):
    """发送 PUT 请求。
    :param url: 新 Request 对象的 URL。
    :param form: 表单的数据，接收字典类型
    :param timeout: 超时时间，单位秒
        1.配置读超时 float
        2.配置连接超时，读超时。元组 (connect timeout, readtimeout) .
    :param headers: 请求头参数
        字典：{k1:v1,k2:v2}
        数组：[(k1,v1),(k2,v2)]
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    newForm = dict()
    for key in form:
        newForm[key] = (None, form[key])
    return requests.put(url, files=newForm, timeout=timeout, headers=headers, **kwargs)


def delete(url: str, params=None, timeout=None, headers=None, **kwargs):
    """发送 DELETE 请求。
    :param url: 新 Request 对象的 URL。
    :param params: 请求参数
        字典：{k1:v1,k2:v2}
        数组：[(k1,v1),(k2,v2)]
    :param timeout: 超时时间，单位秒
        1.配置读超时 float
        2.配置连接超时，读超时。元组 (connect timeout, readtimeout) .
    :param headers: 请求头参数
        字典：{k1:v1,k2:v2}
        数组：[(k1,v1),(k2,v2)]
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    return requests.delete(url, params=params, timeout=timeout, headers=headers, **kwargs)


def deleteJson(url: str, json=None, timeout=None, headers=None, **kwargs):
    """发送 DELETE 请求。
    :param url: 新 Request 对象的 URL。
    :param json: json请求体
    :param timeout: 超时时间，单位秒
        1.配置读超时 float
        2.配置连接超时，读超时。元组 (connect timeout, readtimeout) .
    :param headers: 请求头参数
        字典：{k1:v1,k2:v2}
        数组：[(k1,v1),(k2,v2)]
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    return requests.put(url, json=json, timeout=timeout, headers=headers, **kwargs)


def deleteForm(url: str, form: dict = None, timeout=None, headers=None, **kwargs):
    """发送 DELETE 请求。
    :param url: 新 Request 对象的 URL。
    :param form: 表单的数据，接收字典类型
    :param timeout: 超时时间，单位秒
        1.配置读超时 float
        2.配置连接超时，读超时。元组 (connect timeout, readtimeout) .
    :param headers: 请求头参数
        字典：{k1:v1,k2:v2}
        数组：[(k1,v1),(k2,v2)]
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    newForm = dict()
    for key in form:
        newForm[key] = (None, form[key])
    return requests.delete(url, files=newForm, timeout=timeout, headers=headers, **kwargs)


def options(url: str, **kwargs):
    """发送 OPTIONS 请求。
    :param url: 地址
    :param kwargs: 其他参数
    :return:
    """
    return requests.options(url, **kwargs)


def request(method: str, url: str, **kwargs):
    """
    发送一个自定义请求
    :param method: 请求方式
    :param url: 地址
    :param kwargs: 其他参数
    :return:
    """
    return requests.request(method=method, url=url, **kwargs)


def getFile(url: str, fpath: str, headers:dict=None, progress:bool=False, **kwargs):
    """
    :param url: 请求地址
    :param fpath: 下载后的文件地址
    :param headers: 请求头
    :param progress: 下载文件进度条开关
    :param kwargs: 其他参数
    :return:
    """
    # 用流stream的方式获取url的数据
    resp = requests.get(url, headers=headers, allow_redirects=True, stream=True, **kwargs)
    # 拿到文件的长度，并把total初始化为0
    total = int(resp.headers.get('content-length', resp.headers.get('Content-Length', 0)))
    # 初始化tqdm，传入总数，文件名等数据，接着就是写入，更新等操作了
    from tqdm import tqdm
    import os
    with open(fpath, 'wb') as file, tqdm(
            disable=not progress and total < 1024 * 512,
            desc=os.path.basename(fpath),
            total=total,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
    ) as bar:
        for data in resp.iter_content(chunk_size=1024):
            size = file.write(data)
            bar.update(size)


def postFile(url: str, fpath: str, headers:dict=None, progress:bool=False, **kwargs):
    """
    :param url: 请求地址
    :param fpath: 下载后的文件地址
    :param headers: 请求头
    :param progress: 下载文件进度条开关
    :param kwargs: 其他参数
    :return:
    """
    # 用流stream的方式获取url的数据
    resp = requests.post(url, headers=headers, allow_redirects=True, stream=True, **kwargs)
    # 拿到文件的长度，并把total初始化为0
    total = int(resp.headers.get('content-length', resp.headers.get('Content-Length', 0)))
    # 初始化tqdm，传入总数，文件名等数据，接着就是写入，更新等操作了
    from tqdm import tqdm
    import os
    with open(fpath, 'wb') as file, tqdm(
            disable=not progress and total < 1024 * 512,
            desc=os.path.basename(fpath),
            total=total,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
    ) as bar:
        for data in resp.iter_content(chunk_size=1024):
            size = file.write(data)
            bar.update(size)


def downloadFile(url: str, fpath: str, headers:dict=None, progress:bool=False, **kwargs):
    """
    :param url: 请求地址
    :param fpath: 下载后的文件地址
    :param headers: 请求头
    :param progress: 下载文件进度条开关
    :param kwargs: 其他参数
    :return:
    """
    return postFile(url=url, fpath=fpath, headers=headers, progress=progress, **kwargs)


def uploadImage(url, name, file, fname=None, timeout=None, headers=None, contentType='image/png', **kwargs):
    """
    :param url: 请求地址
    :param name: 服务端文件参数名称
    :param file: 文件内容：文件路径、文件字节数组、文件对象
                或者 ("filename3", open("filePath4", "rb"), "image/jpeg", {"refer" : "localhost"})
    :param fname: 上传后的文件名称
    :param timeout: 超时时间，单位秒
        1.配置读超时 float
        2.配置连接超时，读超时。元组 (connect timeout, readtimeout) .
    :param headers: 请求头
    :param contentType: 文件内容格式
    :param kwargs: 其他参数
    :return:
    """
    return uploadFile(url, name, file, fname=fname, timeout=timeout, headers=headers, contentType=contentType, **kwargs)


def uploadFile(url, name, file, fname=None, timeout=None, headers=None, contentType=None, **kwargs):
    """
    :param url: 请求地址
    :param name: 服务端文件参数名称
    :param file: 文件内容：文件路径、文件字节数组、文件对象
                或者 ("filename3", open("filePath4", "rb"), "image/jpeg", {"refer" : "localhost"})
    :param fname: 上传后的文件名称
    :param timeout: 超时时间，单位秒
        1.配置读超时 float
        2.配置连接超时，读超时。元组 (connect timeout, readtimeout) .
    :param headers: 请求头
    :param contentType: 文件内容格式
    :param kwargs: 其他参数
    :return:
    """
    files = {}
    if isinstance(file, str):
        import fileer
        assert fileer.existFile(file)
        if fname is None:
            fname = fileer.getFileName(file)
        files[name] = (fname, open(file, 'rb'), contentType)
    elif isinstance(file, tuple):
        files[name] = file
    else:
        # ("filename", "fileobject", "content-type", "headers")
        # ("filename3", open("filePath4", "rb"), "image/jpeg", {"refer" : "localhost"})
        files[name] = (fname, file, contentType)
    return requests.post(url, files=files, timeout=timeout, headers=headers, **kwargs)
