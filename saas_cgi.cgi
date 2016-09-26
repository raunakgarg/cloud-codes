#!/usr/bin/python

print "content-type:text/html"
print ""

import os ,commands ,cgi,cgitb,subprocess
cgitb.enable()
data=cgi.FieldStorage()
name=data.getvalue('name')
password=data.getvalue('password')
apps=data.getvalue('apps')
print "<br>"
print "your name is  " + name

commands.getstatusoutput('sudo useradd   '+name)
commands.getstatusoutput('sudo echo '+password+' | sudo passwd   '+name+'  --stdin')


commands.getstatusoutput('sudo setenforce 0')
commands.getstatusoutput('sudo iptables -F')

commands.getstatusoutput('sudo touch /iaas/'+name+'.py')
commands.getstatusoutput('sudo chmod 777 /iaas/'+name+'.py')
f=open('/iaas/'+name+'.py','w')
f.write("#!/usr/bin/python \n")
f.write("import commands,os \n")
f.write("commands.getstatusoutput('ssh -X "+name+"@192.168.122.1  "+apps+"') \n")
f.close()
commands.getstatusoutput('sudo tar -cvf /var/www/html/'+name+'.tar  /iaas/'+name+'.py')
print "<META HTTP-EQUIV=refresh CONTENT=\"0;URL=http://192.168.122.1/"+name+".tar\">\n"
