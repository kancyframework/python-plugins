@echo off

rem 1) pip下载速度慢的解决方法
set pipConfigDir=%userprofile%\pip
set pipConfigFile=%pipConfigDir%\pip.ini

if not exist %pipConfigFile%(
	mkdir %userprofile%\pip
	del %pipConfigFile%
	echo [global]>>%pipConfigFile%

	echo #python pip下载速度慢的解决方法 https://amos-x.com/index.php/amos/archives/python-pip/>>%pipConfigFile%
	echo #>>%pipConfigFile%
	echo #清华pypi镜像仓库>>%pipConfigFile%
	echo index-url = https://pypi.tuna.tsinghua.edu.cn/simple>>%pipConfigFile%
	echo #>>%pipConfigFile%
	echo #豆瓣pypi镜像仓库>>%pipConfigFile%
	echo #index-url = http://pypi.douban.com/simple>>%pipConfigFile%
	echo #>>%pipConfigFile%
	echo #阿里镜像仓库>>%pipConfigFile%
	echo #index-url = http://mirrors.aliyun.com/pypi/simple>>%pipConfigFile%
	echo #>>%pipConfigFile%
	echo #国外官方镜像仓库>>%pipConfigFile%
	echo #index-url = https://pypi.python.org/simple>>%pipConfigFile%
)


rem 2) 配置pypi仓库token
set pypircFile=%userprofile%\.pypirc

if not exist %pypircFile%(
	del %pypircFile%

	echo [pypi]>>%pypircFile%
	echo username = __token__>>%pypircFile%
	echo password = pypi-AgEIcHlwaS5vcmcCJDU2Njk5NzczLWU1ZDktNDg5My1hMmMxLTA1Njg3Mjk2ZmM1YQACJXsicGVybWlzc2lvbnMiOiAidXNlciIsICJ2ZXJzaW9uIjogMX0AAAYgppv_-FkdstNmqpBVXZ3o5sXNuo1i2cXgiFM7WD9KKBU>>%pypircFile%
)

@echo on
