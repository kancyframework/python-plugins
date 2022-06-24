import httper

params = {
    "a": 1,
    "b": 2
}

# 发送get请求
httper.get("http://localhost:8080/test/get?id=1")
httper.get("http://localhost:8080/test/get?id=1", params)
httper.get("http://localhost:8080/test/get?id=1", params=params, timeout=10, headers={})

# 发送post请求
httper.post("http://localhost:8080/test/post?id=1")
httper.post("http://localhost:8080/test/post?id=1", params)
httper.post("http://localhost:8080/test/post?id=1", params=params, timeout=10, headers={})

# 发送post表单请求
httper.postForm("http://localhost:8080/test/postForm?id=1", params)
httper.postForm("http://localhost:8080/test/postForm?id=1", form=params, timeout=10, headers={})

# 下载文件
httper.getFile("http://localhost:8080/test/getFile?id=1", "test.py")
httper.getFile("http://localhost:8080/test/getFile?id=1", "test.py", progress=True)

httper.postFile("http://localhost:8080/test/postFile?id=1", "test.py")
httper.postFile("http://localhost:8080/test/postFile?id=1", "test.py", progress=True)

httper.downloadFile("http://localhost:8080/test/postFile?id=1", "test.py")
httper.downloadFile("http://localhost:8080/test/postFile?id=1", "test.py", progress=True)

# 上传文件
httper.uploadFile("http://localhost:8080/test/uploadFile?id=1", "file1", "./files/test.py")
httper.uploadFile("http://localhost:8080/test/uploadFile?id=1", "file1", open("./files/test.py"))
httper.uploadFile("http://localhost:8080/test/uploadFile?id=1", name="file1", file="[fileBytes]", fname="test.py")
httper.uploadFile("http://localhost:8080/test/uploadFile?id=1", name="file1",
                  file=("", open("./files/test.py", "rb"), "image/jpeg", {"refer": "localhost"}))
httper.uploadFile("http://localhost:8080/test/uploadFile?id=1", name="file1",
                  file=("new_filename.py", open("./files/test.py", "rb"), "image/jpeg", {"refer": "localhost"}))

httper.uploadImage("http://localhost:8080/test/uploadFile?id=1", "file2", "./files/img1.py")
