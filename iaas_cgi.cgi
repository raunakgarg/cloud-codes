#!/usr/bin/python

print "content-type:text/html"
print ""

import os ,commands ,random,cgi,cgitb,subprocess
cgitb.enable()
data=cgi.FieldStorage()
name=data.getvalue('name')
os=data.getvalue('os')
size=data.getvalue('size')
cpu=data.getvalue('cpu')
memory=data.getvalue('memory')
vnc1=random.randint(5910,5940)
vnc= str(vnc1)


print "<br>"
print "your name is  " + name
commands.getstatusoutput('sudo cd /iaas')
commands.getstatusoutput("sudo qemu-img create -f qcow2 /iaas/"+name+".qcow2 "+size+"G")
commands.getstatusoutput('sudo virt-install --name '+name+' --vnc --vncport='+vnc+' --vnclisten=0.0.0.0  --vcpu '+cpu+' --disk path=/iaas/'+name+'.qcow2,size='+size+' --memory '+memory+'  --cdrom /iaas/rhel-server-7.1-x86_64-dvd.iso  --noautoconsole')
commands.getstatusoutput('sudo setenforce 0')
commands.getstatusoutput('sudo iptables -F')
commands.getstatusoutput('sudo vncviewer 192.168.122.1:"+vnc+"')

commands.getstatusoutput('sudo touch /iaas/'+name+'.py')
commands.getstatusoutput('sudo chmod 777 /iaas/'+name+'.py')
f=open('/iaas/'+name+'.py','w')
f.write("#!/usr/bin/python \n")
f.write("import commands,os \n")
f.write("commands.getstatusoutput('sudo vncviewer 192.168.122.1:"+vnc+"') \n")
f.close()
commands.getstatusoutput('sudo tar -cvf /var/www/html/'+name+'.tar  /iaas/'+name+'.py')
print "<META HTTP-EQUIV=refresh CONTENT=\"0;URL=http://192.168.122.1/"+name+".tar\">\n"
