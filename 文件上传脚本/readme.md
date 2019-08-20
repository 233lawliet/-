### 简介 ###

    该脚本工具主要用于本地文件上传到服务器。
    
### 安装环境 ###
    
    本地和服务器配置了ssh的免密登录
    服务器搭建了nginx用于文件的访问

### 基本语法 ###

#### upload ####


- F1 

        python tools upload 文件名

        #本地指定路径下的文件--->>>服务器默认的路径下

- F2

        python tools upload 文件名 相对路径名

        #本地指定路径下的文件--->>>服务器相对路径下


#### mkdir ####


- F1 

        python tools mkdir 路径名
        
        或 python tools mkdir 路径名 true

        #在服务器创建相应的路径名，并chmod赋权限，并设置为默认相对路径

- F2

        python tools mkdir 路径名 false
         #在服务器创建相应的路径名，并chmod赋权限，并不设置为默认相对路径