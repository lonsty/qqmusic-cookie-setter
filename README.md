# QQ Music cookie setter

QQ 音乐 https://y.qq.com 定时自动登录，获取 cookie 并通过 API 上传服务器。

# 使用

### 1. 克隆仓库代码到本地

```shell
$ git clone https://github.com/lonsty/qqmusic-cookie-setter
```

### 2. 下载安装依赖

- 下载 `selenium` 依赖

在本机电脑安装 Chrome 浏览器，并从 [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) 下载对应版本的 chromedriver 保存在 `drivers` 目录下，使用时的路径是 `drivers/chromedriver`。

- 安装 Python 运行依赖

```shell
$ cd qqmusic-cookie-setter
$ pipenv install
```

### 3. 首次运行并添加配置

```shell
$ python3 qqmusic_cookie_setter.py

Path of chromedriver(drivers/chromedriver): drivers/chromedriver
Set cookie API(http://cn.lonsty.me:8179/user/setCookie): http://cn.lonsty.me:8179/user/setCookie
Username: 337657561
Password: 
Secret Key: 
Cookies set successfully at Sat May 30 21:44:32 2020
```

设置完成后，会在根目录下生成 `settings.yml` 配置文件，后续运行从该文件读取配置。

```
# settings.yml

webdriver: drivers/chromedriver
set_cookie_api: http://cn.lonsty.me:8179/user/setCookie
username: 337657561
password: '******'
secret_key: '******'
encoded_password: 6NDhyuTe2c_ZzOPe
```

### 4. 开启定时任务

- 每天 `05:00` 设置一次 cookie

```shell
$ python3 scheduler.py 05:00
```

- 使用`nohup` 后台运行定时任务（默认 `05:18`）

```shell
$ nohup python3 scheduler.py &
```

### 5. 关闭后台定时任务

a. 获取任务进程 ID

```shell
$ ps -ef | grep scheduler.py

allen    13159 10698  0 22:00 pts/2    00:00:00 python3 scheduler.py
```
得到进程 ID `13159`

b. 杀掉后台任务

```
$ kill -9 13159
```