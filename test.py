#!/usr/bin/env python
# _*_coding:utf-8_*_
# Author "Edward.Liu"

# import zipfile
# import contextlib
# import time
# import os
#
# timeStr = time.strftime("%Y-%m-%d-%H:%M")
# source_filename = "/software/cybershop-front-0.0.1-SNAPSHOT.war"
# dest_dir = "/software/upload_project/%s-%s" % (timeStr, source_filename.split('/')[2].split('.war')[0])
# dest_deploy_dir = "/software/deploy-front/%s" % source_filename.split('/')[2].split('.war')[0]
# images_Home = "/software/newupload1"
# static_images_lins = "%s/assets/upload" % dest_dir
# static_Home = "/data/www"
# static_home_link = "%s/www" % dest_dir
#
#
# def unzip(source_filename, dest_dir):
#     with contextlib.closing(zipfile.ZipFile(source_filename)) as zf:
#         if os.path.exists(dest_dir):
#             zf.extractall(dest_dir)
#         else:
#             print "\033[32mPath %s Is Not Exists....Creating....\033[0m" % dest_dir
#             os.makedirs(dest_dir)
#             zf.extractall(dest_dir)
#
#
# def soft_link(source, dest):
#     print "\033[32mCreating Static Files/Images Link "
#     os.symlink(images_Home, static_images_lins)
#     os.symlink(static_Home, static_home_link)
#     os.symlink(source, dest)
#
#
# unzip(source_filename, dest_dir)
# soft_link(dest_dir, dest_deploy_dir)
import time


class Tomcat(object):
    def __init__(self, tomcat_exe):
        self.tomcat_exe = tomcat_exe
        self.Tomcat_Home = "/software/%s" % tomcat_exe
        self.Tomcat_Log_Home = "/software/%s/logs" % tomcat_exe
        self.counnt = 10
        # deploy options
        self.timeStr = time.strftime("%Y-%m-%d-%H")
        self.source_files = "/software/cybershop-front-0.0.1-SNAPSHOT.war"
        self.dest_dir = "/software/upload_project/%s-%s" % (
            self.timeStr, self.source_files.split('/')[2].split('.war')[0])
        self.dest_deploy_dir = "/software/deploy-front/%s" % self.source_files.split('/')[2].split('.war')[0]
        self.images_Home = "/software/newupload1"
        self.static_images_lins = "%s/assets/upload" % self.dest_dir
        self.static_Home = "/data/www"
        self.static_home_link = "%s/www" % self.dest_dir
        # deploy options --->end


a = Tomcat(tomcat_exe="tomcat-test")
print a.timeStr
print a.dest_deploy_dir
print a.source_files
print a.dest_dir
print a.images_Home
print a.static_images_lins
print a.static_Home
print a.static_home_link
