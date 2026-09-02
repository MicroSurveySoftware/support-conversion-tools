#!/usr/bin/python
import cgi, cgitb, time, string
import xml.etree.ElementTree as ET
#below entry allows for online debugging, it should be removed for release:
#import cgitb
#cgitb.enable(format = "text")



form = cgi.FieldStorage()                 # parse form data
titleString = "<title>Converted Results</title>"
returnlink = 'http://support.microsurvey.com/convert/JobxmlModifier.html'
output_text = ""
#output_text = '<!-- Converted ' + time.strftime('%B %d, %Y -- %I:%M:%S %p %Z') + '-->\r\n<!--JobxmlModifier script by MicroSurvey -- helpdesk@MicroSurvey.com-->\r\n<!--Script Version 1.0 -- 08 06, 2025-->\r\n\r\n'

#print "Content-Type: text/plain"	
print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<head>"
print titleString
print "<style>"
print "body {font-family:Arial, Helvetica, sans-serif; color:#767676; background:#f5f5f5; font-size:12px; line-height:18px;	margin:0;}"
print "html, body {height:100%;}"
print "html {min-width:960px; overflow-y:scroll;}"
print ".container {width:960px;	margin:0 auto; position:relative; overflow:hidden;}"
print ".button-2 {line-height:29px; font-size:12px;	color:#252525; background:#ededed; border:1px solid #c4c4c4; padding:5px 15px 5px 15px;}"
print ".button-2:hover {background-color:#125A5A; color:#fff;}"
print "a {color:#F24C15; outline:none; cursor:pointer; text-decoration:none;}"
print "</style"
print "</head>"
print "<body>"
print "<div class='container'>"
print "<p style='text-align:center;'><a class='button-2' href='"
print returnlink
print "'>Return to the Input Page</a>&nbsp;&nbsp;&nbsp;<a class='button-2' href='https://helpdesk.microsurvey.com/article/1339'>Return to the Main Page</a></p>"
print "<textarea style='width:100%; border:1px solid #CCC; height:800px; padding:5px;'>"

# Insert function definitions below:


# Checks if input was empty:

if not 'content' in form:
	output_text = 'ERROR: No input provided...'
elif not '<?xml' in form.getvalue('content'):
	output_text = 'ERROR: This does not appear to be a complete jobxml file...'

#Reads form data passed from webpage and stores it as object "content"

else:
        text = form.getvalue('content')

    
#Insert script below:

        output_text = ""
        lines = text.splitlines()
        i = 0
        while i < len(lines):
            if "<TargetRecord " in lines[i]:
                if "<Name" in lines[i+1]:
                    curLine = lines[i]
                    i += 2
                else:
                    curLine = lines[i]
                    i += 1
                
            else:
                curLine = lines[i]
                i += 1
            output_text += curLine + "\n"


# dO NOT MODIFY BELOW:
print cgi.escape(output_text, quote=True)
print "</textarea>"
print "<p>Please contact MicroSurvey at helpdesk@microsurvey.com if results are not as expected or contain errors.</p>"
print "</div>"
print "</body>"
print "</html>"


#Add a note to access.dat
##import sys, os
##ip = cgi.escape(os.environ["REMOTE_ADDR"])
##script = str(sys.argv[0])
##date = time.strftime('%B %d: %Y -- %I:%M:%S %p %Z')
##note = script + "," + date + ",IP V6 address: " + ip + "\n"
##fileout = open('access.dat','a')
##fileout.write(note)
##fileout.close()
