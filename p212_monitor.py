#! /usr/bin/env python

import os
import smtplib
warning = 0					#this is the variable that triggers the mail, if it's 0 there are no prob, if it's 1 the we have a problem

#sendmail
def sendemail(from_addr, to_addr_list, cc_addr_list,
              subject, message,
              login, password,
              smtpserver='smtp.gmail.com:587'):
    header  = 'From: %s\n' % from_addr
    header += 'To: %s\n' % ','.join(to_addr_list)
    header += 'Cc: %s\n' % ','.join(cc_addr_list)
    header += 'Subject: %s\n\n' % subject
    message = header + message
    server = smtplib.SMTP(smtpserver)
    server.starttls()
    server.login(login,password)
    problems = server.sendmail(from_addr, to_addr_list, message)
    server.quit()


#prepare logfile
date = str(os.popen("date").read())		#read the time+date from the os
open('/scripts/datafile.txt', 'w').close() 	#open file and erase it's content
file = open("/scripts/datafile.txt", "r+") 	#open file for writing
file.write(date + "\n")				#write the date in the file


#retrieve p212 data from system
p212_vol0_status = str(os.popen("cciss_vol_status /dev/sg0").read())[-5:-3]
p212_disk1_status = str(os.popen("hpacucli ctrl slot=1 pd 1I:0:1 show status").read())[-4:-2]
p212_disk2_status = str(os.popen("hpacucli ctrl slot=1 pd 1I:0:2 show status").read())[-4:-2]
p212_disk3_status = str(os.popen("hpacucli ctrl slot=1 pd 1I:0:3 show status").read())[-4:-2]
p212_disk4_status = str(os.popen("hpacucli ctrl slot=1 pd 1I:0:4 show status").read())[-4:-2]
p212_batt_status = str(os.popen("hpacucli ctrl slot=1 show | grep 'Battery/CapacitorStatus:'").read())[-3:-1]


#false positive:
#p212_vol0_status = "banana"


#routine to check states of the variuos components:
if str(p212_vol0_status) <> "OK":				#if the state is not "OK"
	print "!!! p212_vol0_status : PANIC !!!" 		
	warning = 1						#trigger the warning andthen the alerts
	file.write("vol0:   " + "WARNING!!!" + "\n")		#write the state of the failed component in the logfile 
else:
	file.write("vol0:   " + p212_vol0_status + "\n")	#write the state(OK) of the component in the logfile

if str(p212_disk1_status) <> "OK":     
        print "!!! p212_disk1_status : PANIC !!!"
        warning = 1 
	file.write("disk1:  " + "WARNING!!!" + "\n")
else: 
	file.write("disk1: " + p212_disk1_status + "\n")

if str(p212_disk2_status) <> "OK":     
        print "!!! p212_disk2_status : PANIC !!!"
        warning = 1 
	file.write("disk2:  " + "WARNING!!!" + "\n")
else:
	file.write("disk2: " + p212_disk2_status + "\n")

if str(p212_disk3_status) <> "OK":     
        print "!!! p212_disk3_status : PANIC !!!"
        warning = 1 
	file.write("disk3:  " + "WARNING!!!" + "\n")
else:
	file.write("disk3: " + p212_disk3_status + "\n")	

if str(p212_disk4_status) <> "OK":     
        print "!!! p212_disk4_status : PANIC !!!"
        warning = 1 
	file.write("disk4:  " + "WARNING!!!" + "\n")
else:
	file.write("disk4: " + p212_disk4_status + "\n")

if str(p212_batt_status) <> "OK":     
        print "!!! p212_batt_status : PANIC !!!"
        warning = 1 
	file.write("batt:   " + "WARNING!!!" + "\n")
else:
	file.write("batt:   " + p212_batt_status + "\n")


file.close() 							#close the logfile

with open ("/scripts/datafile.txt", "r") as myfile:		#reopen the logfile
	datafile = myfile.read().replace('\n', ' \r ')		#read the logfile and 
store it in datafile
myfile.close()

#send email:
if warning <> 0:
	sendemail(from_addr    = 'FROM@gmail.com', 
         	to_addr_list = ['TO@gmail.com'],
          	cc_addr_list = [''], 
          	subject      = 'Warning P212!!', 
          	message      = str(datafile), 
          	login        = 'GMAIL_ACCOUNT', 
          	password     = 'GMAIL_PASSWORD')
