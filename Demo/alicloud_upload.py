#!/usr/bin/env python
# tary, 14:49 2018/10/18
import os
import sys
import oss2
import time

#oss2_folder = sys.argv[3]
class log_uploader(object):
    def __init__(self):
        self.access_key_id = u"xxxxxxxxxxxxxxxxxxx"
        self.access_key_secret = u"xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
        self.bucket_name = u"fusion-pic"   #Save the file in ali this path
#        self.bucket_name = oss2_folder   
        self.endpoint = u"oss-cn-hangzhou.aliyuncs.com"

    def uploadfile(self, fileName, localFile):
        auth = oss2.Auth(self.access_key_id, self.access_key_secret)
        print "debug1"
        print auth
        bucket = oss2.Bucket(auth, self.endpoint, self.bucket_name)
        print "debug2"
        print bucket
        try:
            oss2.resumable_upload(bucket, fileName, localFile)
            time.sleep(0.1)

            file_exist_check = bucket.object_exists(fileName)
            if file_exist_check != True:
                return False
        except Exception as e:
            print "debug3"
            print(e)
            return False

        return True
        

if __name__ == '__main__':
    # if len(sys.argv) < 2:
        # print("Usage: {} filename filepath")
        # quit(1)

    uploader = log_uploader()
    uploader.uploadfile("aging_test110_T20210517-165240_FAIL.log", "/var/bbb_log/aging_test110_T20210517-165240_FAIL.log")
    #if uploader.uploadfile(sys.argv[1], sys.argv[2]):
        #quit(0)
    quit(2)

