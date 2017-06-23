import os;
def rename():
    path="/Users/niumingyi/Downloads/data";
    filelist=os.listdir(path)#该文件夹下所有的文件（包括文件夹）
    for i,files in enumerate(filelist):#遍历所有文件
        Olddir=os.path.join(path,files);#原来的文件路径
        if os.path.isdir(Olddir):#如果是文件夹则跳过
            continue;
        filename= str(i)
        filetype=os.path.splitext(files)[1];#文件扩展名
        Newdir=os.path.join(path,filename+filetype);#新的文件路径
        os.rename(Olddir,Newdir);#重命名

rename()