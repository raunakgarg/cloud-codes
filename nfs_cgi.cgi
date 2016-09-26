#!/usr/bin/python

print "content-type:text/html"
print ""

import os ,commands ,cgi,cgitb,subprocess
cgitb.enable()
data=cgi.FieldStorage()
name=data.getvalue('name')
size=data.getvalue('size')
print "<br>"
print "your name is  " + name
print "<br>"
print "the size you required is    " + size
t=commands.getstatusoutput('sudo lvcreate --name '+name+' --size +'+size+'M /dev/rgvg')
print "<br>"
s=commands.getstatusoutput('sudo mkfs.ext4 /dev/rgvg/'+name)
print "<br>"
print "<br>"
print "this is mkfs command"
c=commands.getstatusoutput('sudo mkdir /media/'+name)
print "<br>"
print "<br>"
print "this is mkdir command"
mo=commands.getstatusoutput('sudo mount /dev/rgvg/'+name+'  /media/'+name)
print "<br>"
print "<br>"
print "mounted"
print "<br>"
commands.getstatusoutput('sudo echo /media/'+name+'            *\(rw,no_root_squash\)  | cat >> /etc/exports')
commands.getstatusoutput('sudo setenforce 0')
commands.getstatusoutput('sudo systemctl restart nfs-server')
commands.getstatusoutput('sudo systemctl enable nfs-server')
print "<br>"
print "dekh le desktop per"
commands.getstatusoutput('sudo touch /iaas/'+name+'.py')
commands.getstatusoutput('sudo chmod 777 /iaas/'+name+'.py')
f=open('/iaas/'+name+'.py','w')
f.write("#!/usr/bin/python \n")
f.write("import commands,os \n")
f.write("commands.getstatusoutput('mkdir /media/"+name+"') \n")
f.write("commands.getstatusoutput('mount 192.168.122.1:/media/"+name+" /media/"+name+"') \n")
f.close()
commands.getstatusoutput('sudo tar -cvf /var/www/html/'+name+'.tar  /iaas/'+name+'.py')
print "<META HTTP-EQUIV=refresh CONTENT=\"0;URL=http://192.168.122.1/"+name+".tar\">\n"
