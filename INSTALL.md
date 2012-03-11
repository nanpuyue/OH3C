openwrt需安装python-pcap，python-mini

首次刷机后，先设置密码：

telnet 192.168.1.1
passwd


然后使用scp上传：

scp -r [本地路径]yah3c root@192.168.1.1:/usr
scp -r [本地路径]root root@192.168.1.1:/


使用ssh登录并运行yah3c：

ssh -l root 192.168.1.1
yah3c (或 python /usr/yah3c/yah3c.py)