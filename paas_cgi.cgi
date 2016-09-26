#!/usr/bin/python

print "content-type:text/html"
print ""

import os ,commands ,cgi,cgitb,subprocess,random,time
cgitb.enable()
data=cgi.FieldStorage()
user=data.getvalue('name')
passwd=data.getvalue('passwd')
platform=data.getvalue('platform')
vnc1=random.randint(5910,5940)
vnc= str(vnc1)
print "<br>"
print "your name is  " + user

print user

print passwd
m=commands.getstatusoutput("sudo touch /iaas/{}.py".format(user))
print m
g=commands.getstatusoutput("sudo chmod 777 /iaas/{}.py".format(user))
print g

fobj=open('/iaas/{}.py'.format(user), 'w')
fobj.write('#!/usr/bin/python2\nimport commands,os,cgi\n')

fobj.write("commands.getstatusoutput('useradd -s /usr/bin/python {0}')\n".format(user))
fobj.write("commands.getstatusoutput('echo {0} | sudo passwd {1} --stdin')\n".format(passwd,user))
fobj.close()

df=random.randint(7000,8010)

p=commands.getstatusoutput("sudo docker run -itd -p {}:4200 --privileged -v /iaas:/media/ rahul1 bash".format(df))
commands.getstatusoutput("sudo docker exec -t {} touch /media/{}.py".format(p[1],user))
commands.getstatusoutput("sudo docker exec -t {} chmod 777 /media/{}.py".format(p[1],user))
commands.getstatusoutput("sudo docker exec {} service sshd restart".format(p[1]))
m=commands.getstatusoutput("sudo docker exec {} hostname -i".format(p[1]))
commands.getstatusoutput("sudo touch /media/shellinaboxd")
commands.getstatusoutput("sudo chmod 777 /media/shellinaboxd")
fh=open("/media/shellinaboxd","w")
fh.write("USER=shellinabox\nGROUP=shellinabox\nCERTDIR=/var/lib/shellinabox\nPORT=4200\nOPTS=\"-t -s /:SSH:{}\"".format(m[1]))
fh.close()


k=commands.getstatusoutput("sudo docker exec {} cp -rvf /media/shellinaboxd /etc/sysconfig/shellinaboxd".format(p[1]))
print k

commands.getstatusoutput("sudo docker exec -t {} service shellinaboxd restart".format(p[1]))
commands.getstatusoutput("sudo docker exec -t {} service shellinaboxd restart".format(p[1]))
print "<META HTTP-EQUIV=refresh CONTENT=\"0;URL=http://{}:4200\">\n".format(m[1])
