#!/usr/bin/env python
# tary, 14:49 2018/10/18

import os
import oss2
import time
import sys


#bucket_name = sys.argv[1]
#need_file_prex = sys.argv[2]

bucket_name = "102110561"
#need_file_prex = "BBBVC20200400020"
bucket_name_bk = "102991313"


class log_uploader():
    def __init__(self):
        self.access_key_id = "xxxxxxxxxxxxxxx"
        self.access_key_secret = "xxxxxxxxxxxxxxxxxxxxxxxxxx"
        self.bucket_name = bucket_name
        self.bucket_name_bk = bucket_name_bk
        self.endpoint = "oss-cn-hangzhou.aliyuncs.com"
        self.auth = oss2.Auth(self.access_key_id, self.access_key_secret)
        self.bucket = oss2.Bucket(self.auth, self.endpoint, self.bucket_name)
        #self.put_object()
        self.bucket_bk = oss2.Bucket(self.auth, self.endpoint, self.bucket_name_bk)
        
        
    def uploadfile(self,logfileName, filePath):
#        realfilepath = filePath + "/" + logfileName
        realfilepath = logfileName
        print(realfilepath)
        try:
            oss2.resumable_upload(self.bucket, logfileName, filePath)
            time.sleep(0.1)

            file_exist_check = self.bucket.object_exists(logfileName)
#            print file_exist_check
            if file_exist_check != True:
                return False
        except Exception as e:
            print(e)
            return False

        return True
        
    def uploadfile_bk(self,logfileName, filePath):
        realfilepath = filePath + "/" + logfileName
        try:
            oss2.resumable_upload(self.bucket_bk, logfileName, filePath)
            time.sleep(0.1)

            file_exist_check = self.bucket_bk.object_exists(logfileName)
            if file_exist_check != True:
                return False
        except Exception as e:
            print(e)
            return False

        return True    
    

    def downloadfile(self):
        try:
            for object_info in oss2.ObjectIterator(self.bucket,prefix=need_file_prex):
                print(object_info.key)
                self.bucket.get_object_to_file(object_info.key, object_info.key) 
        except:
            print "Error"

    
    def deletefile(self):
        for obj in oss2.ObjectIterator(self.bucket, prefix="4016"):
            print obj.key
            self.bucket.delete_object(obj.key)        
    
    def download_delete(self):
        try:
            for object_info in oss2.ObjectIterator(self.bucket,prefix=need_file_prex):
                print(object_info.key)
                self.bucket.get_object_to_file(object_info.key, object_info.key)
                self.bucket.delete_object(object_info.key) 
        except:
            print "Error"
        
    
    def search(self):
        for object_info in oss2.ObjectIterator(self.bucket,prefix=need_file_prex):
            print(object_info.key)
            
    def copyfile(self):
        d_bucket = oss2.Bucket(self.auth, "oss-cn-hangzhou.aliyuncs.com", '102991313')
        for object_info in oss2.ObjectIterator(self.bucket,prefix="11399"):
            print(object_info.key)
            d_bucket.copy_object("mestestbak",object_info.key,object_info.key)
            

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: {} filename filepath")
        quit(1)
        
    uploader = log_uploader()
    if uploader.uploadfile(sys.argv[1],sys.argv[2]):
        quit(0)
    quit(2)
    
#    uploader.copyfile()
#    uploader.deletefile()    
#    uploader.downloadfile()
#    uploader.download_delete()
    
    