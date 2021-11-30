#建立虚拟环境
#pipenv install
#进入虚拟环境（上一步可省略,因为没有虚拟环境的话会自动建立一个）
pipenv shell
# 打包程序包（自动下载依赖包）
py setup.py package
#打包的模块也要安装
pip install pyinstaller
#开始打包
pyinstaller -Fw 启动入口.py