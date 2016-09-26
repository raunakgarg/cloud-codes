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
commands.getstatusoutput('sudo useradd  -s /sbin/nologin   '+name)
commands.getstatusoutput('sudo echo -e "redhat\nredhat" | sudo smbpasswd -a  '+name)


f=open('/etc/samba/smb.conf','a')
f.write("["+name+"] \n")
f.write("path=/media/"+name+" \n")
f.write("writable = yes  \n")
f.write("valid users = "+name+" \n")
f.write("hosts allow=ALL\n")
f.close()

commands.getstatusoutput('sudo systemctl restart smb')
commands.getstatusoutput('sudo systemctl enable smb.service')
commands.getstatusoutput('sudo setenforce 0')
commands.getstatusoutput('sudo iptables -F')



commands.getstatusoutput('sudo touch /iaas/'+name+'.py')
commands.getstatusoutput('sudo chmod 777 /iaas/'+name+'.py')
f=open('/iaas/'+name+'.py','w')
f.write("#!/usr/bin/python \n")
f.write("import commands,os \n")
f.write("commands.getstatusoutput('mkdir /media/"+name+"') \n")
f.write("commands.getstatusoutput('mount -o username="+name+"  //192.168.122.1/"+name+"  /media/"+name+"') \n")
f.close()
commands.getstatusoutput('sudo tar -cvf /var/www/html/'+name+'.tar  /iaas/'+name+'.py')
print "<META HTTP-EQUIV=refresh CONTENT=\"0;URL=http://192.168.122.1/"+name+".tar\">\n"
