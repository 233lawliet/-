import  os
import sys
import  re
import configparser

class Tools():

    localBasicPath=r""   #本地基本路径

    remoteBasicPath=r""  #远程基本路径(ssh)
    remoteRelativePath=r"" #文件存储的相对路径
    remoteRealPath=r""   #存储路径

    remoteSSHBasicPath=r"" #ssh的前缀
    remoteSSHPath=r""      #远程存储文件的路径

    nginxUrl=r""  #文件的访问链接

    # 加载配置
    def __init__(self):

        #加载配置信息
        config = configparser.ConfigParser()
        config.read("sshToolsConfig.txt")

        #加载client配置
        self.localBasicPath=config.get("local","basicPath")
        #加载服务器配置
        self.remoteBasicPath=config.get("remote","basicPath")
        self.remoteRelativePath=config.get("remote","relativePath")
        self.remoteRealPath=self.remoteBasicPath+self.remoteRelativePath
        #加载ssh配置
        self.remoteSSHBasicPath=config.get("ssh","host")
        self.remoteSSHPath=self.remoteSSHBasicPath+":"+self.remoteRealPath
        #加载nginx配置
        self.nginxUrl = config.get("nginx", "url")


    #文件上传
    def upload(self,fileName):
        localFile=self.localBasicPath+"\\"+fileName    #本地路径
        remotePath=self.remoteSSHPath   #远程路径
        localExist=os.path.exists(localFile)
        if localExist:
            os.system("scp "+localFile+" " +remotePath)
        else:
            print("该文件不存在！")

        self.printNginxUrl(fileName)

    # 访问nginx链接
    def printNginxUrl(self, fileName):
        nginxUrl = self.nginxUrl + self.remoteRelativePath + "/" + fileName
        print("访问的链接：" + nginxUrl)

    #文件创建
    def mkdir(self,relativePath):
        remotePath=self.remoteBasicPath+relativePath
        #文件创建
        os.system("ssh "+self.remoteSSHBasicPath+" mkdir -p "+remotePath)
        #权限赋予
        os.system("ssh " + self.remoteSSHBasicPath + " chmod 777 " + remotePath)
        print("成功创建服务器路径："+remotePath)

    #修改本地的配置文件
    def changeConfigRelativePath(self,remoteRelativePath):
        config=configparser.ConfigParser()
        config.read("sshToolsConfig.txt")

        #设置参数，保存
        config.set("remote","relativepath",remoteRelativePath)
        config.write(open('config.txt', "w"))

        #更新默认路径
        self.remoteRelativePath=remoteRelativePath

        print("默认上传路径已修改为：" + self.remoteRelativePath)

if __name__ == '__main__':
    tools=Tools()


    #获取执行的方法
    func=sys.argv[1]

    #执行upload方法
    if func == "upload":
        # 第一个参数：文件名
        fileName = sys.argv[2]

        if len(sys.argv) == 3:
            tools.upload(fileName)

        elif len(sys.argv) == 4:
            relativePath = sys.argv[3]
            tools.remoteRelativePath = relativePath
            tools.remoteRealPath = tools.remoteBasicPath + tools.remoteRelativePath
            tools.remoteSSHPath = tools.remoteSSHBasicPath + ":" + tools.remoteRealPath
            tools.upload(fileName)
        else:
            print("参数错误！")
    #执行mkdir参数
    elif func == "mkdir":
        
        # 第一个参数：服务器相对路径
        relativePath = sys.argv[2]
        if relativePath[0] =="/":
            relativePath=relativePath[1:]

        # 设置默认的文件路径，带参数的设置
        if len(sys.argv) == 3 :
            tools.mkdir(relativePath)
            tools.changeConfigRelativePath(relativePath)
        elif len(sys.argv) == 4:
            #捕获参数 判定是否修改默认路径
            changeRelativePathFlag=sys.argv[3]
            #true-修改
            if changeRelativePathFlag == "true":
                tools.mkdir(relativePath)
                tools.changeConfigRelativePath(relativePath)
            #false-不修改
            elif changeRelativePathFlag == "false":
                result = tools.mkdir(relativePath)
                print("使用原来默认路径："+tools.remoteRelativePath)
            #其他-判错
            else:
                print("参数错误！")
    else:
        print("还未设置该方法！")
