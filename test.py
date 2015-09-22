import ConfigParser

conf = ConfigParser.ConfigParser()
conf.read('/software/python_works/Linux_script_python/tomcat_deploy/tomcat.conf')
print conf.get('remote', 'remote_web_node1')
