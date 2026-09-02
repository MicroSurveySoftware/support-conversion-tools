#!/usr/bin/python
import cgi, cgitb, time, string,sys
#import xml.etree.ElementTree as ET
#below entry allows for online debugging, it should be removed for release:
import cgitb
#cgitb.enable(format='text')



form = cgi.FieldStorage()                 # parse form data
titleString = "<title>Converted Results</title>"
returnlink = 'http://helpdesk.microsurvey.com/index.php?/Knowledgebase/Article/View/1456'
errorstate = False
errortext = "No Errors found\n"
output_text = '#Modified ' + time.strftime('%B %d, %Y -- %I:%M:%S %p %Z') + '\r\n#vectors script by MicroSurvey -- helpdesk@MicroSurvey.com\r\n#Script Version 1.0 -- 07 08, 2018\r\n\r\n'
output = ""

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
print "'>Return to the Input Page</a>&nbsp;&nbsp;&nbsp;<a class='button-2' href='http://helpdesk.microsurvey.com/index.php?/Knowledgebase/Article/View/1456'>Return to the Main Page</a></p>"
print "<textarea style='width:100%; border:1px solid #CCC; height:800px; padding:5px;'>"

# Insert function definitions below:

def dms2dd(dms):
    dms = float (dms)
    d = float(int(dms))
    m = float(int((dms-d)*100))
    s = ((dms-d)*100-m)*100
    if s > 60:
        m = m+1
        s = abs(s-100)
        if m == 60:
            d = d+1
            m = 0
    return d + (m/60) + (s/3600)
	
def dd2dmsstring(dd):
    mspace = ''
    sspace = ''
    m = abs((dd-int(dd))) * 60
    s = (m-int(m)) * 60
    if m < 10:
        mspace = '0'
    if s < 9.995: # which would round up to 10
        sspace = '0'
    s = s * 100
    if s - int(s) > .5:
        s = s + 1
    s = int (s)
    return str(int(dd)) + '.' + mspace + str(int(m)) + (sspace+str(s))

def reverse (horizAngle):
    horizAngle = dms2dd(horizAngle)
    horizAngle = horizAngle-180
    horizAngle = dd2dmsstring(horizAngle)
    return horizAngle
    

def supplement (zenithAngle):
    zenithAngle = dms2dd (zenithAngle)
    zenithAngle = 360 - zenithAngle
    zenithAngle = dd2dmsstring (zenithAngle)
    return zenithAngle

# Checks if input was empty:

if not 'content' in form:
	output_text = 'ERROR: No input provided...\n'

#Reads form data passed from webpage and stores it as object "content"

else:
    text = form.getvalue('content')
   
#Insert script below:

    output = "# Antenna Heights were removed by vectors utility http://support.microsurvey.com/convert/vectors.html\n"


    lines = text.splitlines()

    for i in range(0,len(lines)):
        curLine = lines[i]
        # simply re write any non-G1 line
        if "G1" not in curLine:
            output += curLine + "\n"
        # simply re write line if it does not contain any antenna heights
        elif "/" not in curLine:
            output += curLine + "\n"
        # Otherwise extract the antenna height section and rewrite the G1 line:
        else:
            ba=curLine.split('/')
            before = ba[0]
            after=ba[1]
            #Handle cases where there is no description
            if not " " in after:
                a = after
            #Handle cases where there is a description
            else:
                a = after[0:after.find(" ")]
            
            b = before[before.rfind(" ")+1:]

            ah = b + "/" + a
        
            gps = curLine.replace(ah,"")
            output += gps + "    #" + ah +"\n"









output_text += output


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
