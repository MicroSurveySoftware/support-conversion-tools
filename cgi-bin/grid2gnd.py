#!/usr/bin/python
import cgi, cgitb, time, string
import xml.etree.ElementTree as ET
#below entry allows for online debugging, it should be removed for release:
import cgitb
#cgitb.enable(format='text')
import sys
import string



form = cgi.FieldStorage()                 # parse form data
titleString = "<title>Converted Results</title>"
returnlink = 'http://support.microsurvey.com/convert/grid2gnd.html'
#output = '#Converted ' + time.strftime('%B %d, %Y -- %I:%M:%S %p %Z') + '\r\n#Template script by MicroSurvey -- helpdesk@MicroSurvey.com\r\n#Script Version 1.0 -- MM DD, YYYY\r\n\r\n'

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
print "'>Return to the Input Page</a>&nbsp;&nbsp;&nbsp;<a class='button-2' href='http://support.microsurvey.com/converters.html'>Return to the Main Page</a></p>"
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
	output = 'ERROR: No input provided...'


#Reads form data passed from webpage and stores it as object "content"

else:
    text = form.getvalue('content')
    #content = input.read()

    
#Insert script below:

    if not 'input_text' in form:
        textinput = ""
    else:
        text = form.getvalue('input_text')
    skiphead = int(form.getvalue('skiphead'))
    separator = form.getvalue('separator')
    origin = form.getvalue('origin')
    #modify origin so it matches separator of other input
    if separator == " " and "," in origin:
        origin = origin.split(",")[0] + " " + origin.split(",")[1]
    if separator == "," and "," not in origin:
        origin = origin.split(" ")[0] + "," + origin.split(" ")[1]
    
    scale = float(form.getvalue('scale'))




    output = ""


    lines = text.splitlines()

    for i in range(skiphead,len(lines)):
        curLine = lines[i]
        # check if line is missing separator character
        if separator not in curLine:
            output = "Separator missing on line " + str(i+1)
            break
      
        coords = curLine.split(separator)
     
        # build checks here to catch missing x,y or z inputs  or non numeric or missing inputs.
        newline = "error free"

        if len(coords) != 5:
            newline = "Line is not pt,x,y,z,desc"
        if coords[1].isalpha():
            newline = "Column 2 is not a number on line " + str(i+1)
        if coords[2].isalpha():
            newline = "Column 3 is not a number on line " + str(i+1)
        if coords[3].isalpha():
            newline = "Column 4 is not a number on line " + str(i+1)


        # error checks have passed, proceed to transform points:
        elif newline == "error free":
            pt = coords[0]
            x = coords[1]
            y = coords[2]
            z = coords[3]
            desc = coords[4]


            xshift = float(x) - float(origin.split(separator)[0])
            yshift = float(y) - float(origin.split(separator)[1])
            xshift = xshift * float(scale)
            yshift = yshift * float(scale)
            x = str(xshift + float(origin.split(separator)[0]))
            y = str(yshift + float(origin.split(separator)[1]))
            newline = pt + separator + x + separator + y + separator + z + separator + desc
        
        
        output += newline + "\n"
        
     



# dO NOT MODIFY BELOW:
print cgi.escape(output, quote=True)
print "</textarea>"
print "<p>Please contact MicroSurvey at helpdesk@microsurvey.com if results are not as expected or contain errors.</p>"
print "</div>"
print "</body>"
print "</html>"
