# _*_coding:utf-8_*_
#  author:  'lonny'
# dateTime:  '15/9/28'
#   motto:  'Good memory as bad written'


# LocalHost links Files
# Test Tomcat Server
project_front_name = "cybershop-front-0.0.1-SNAPSHOT"
project_back_name = "cybershop-web-0.0.1-SNAPSHOT"
project_dir = "/install/cybershop_project"
Tomcat_webapps_front = "/software/tomcat-front"
Tomcat_webapps_back = "/software/tomcat-back"
Mount_Dir = "/install/upload"
Tomcat_Deploy_Dir_Front = "%s/webapps/cybershop-front-0.0.1-SNAPSHOT" % Tomcat_webapps_front
Front_Link_Dir = "%s/assets/upload" % Tomcat_Deploy_Dir_Front
Tomcat_Deploy_Dir_Back = "%s/webapps/cybershop-web-0.0.1-SNAPSHOT" % Tomcat_webapps_back
Back_Link_Dir = "%s/assets/upload" % Tomcat_Deploy_Dir_Back
Tomcat_FrontTmp_Dir = "%s/work/" % Tomcat_webapps_front
Tomcat_BackTmp_Dir = "%s/work/" % Tomcat_webapps_back
