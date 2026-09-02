#!/usr/bin/python3
import cgi, cgitb, time, string, html
import xml.etree.ElementTree as ET
#below entry allows for online debugging, it should be removed for release:
import cgitb
cgitb.enable(format = "text")

form = cgi.FieldStorage()                 # parse form data
titleString = "<title>Converted Results</title>"
returnlink = 'https://support.microsurvey.com/convert/magnetcleanup.html'
output_text = '#Converted ' + time.strftime('%B %d, %Y -- %I:%M:%S %p %Z') + '\r\n#Magnet Cleanup script by MicroSurvey -- helpdesk@MicroSurvey.com\r\n#Script Version 1.0 -- February 02, 2020\r\n\r\n'

#print("Content-Type: text/plain")
print("Content-type:text/html\r\n\r\n")
print("<html>")
print("<head>")
print(titleString)
print("<style>")
print("body {font-family:Arial, Helvetica, sans-serif; color:#767676; background:#f5f5f5; font-size:12px; line-height:18px; margin:0;}")
print("html, body {height:100%;}")
print("html {min-width:960px; overflow-y:scroll;}")
print(".container {width:960px; margin:0 auto; position:relative; overflow:hidden;}")
print(".button-2 {line-height:29px; font-size:12px; color:#252525; background:#ededed; border:1px solid #c4c4c4; padding:5px 15px 5px 15px;}")
print(".button-2:hover {background-color:#125A5A; color:#fff;}")
print("a {color:#F24C15; outline:none; cursor:pointer; text-decoration:none;}")
print("</style>")
print("</head>")
print("<body>")
print("<div class='container'>")
print("<p style='text-align:center;'><a class='button-2' href='")
print(returnlink)
print("'>Return to the Input Page</a>&nbsp;&nbsp;&nbsp;<a class='button-2' href='https://support.microsurvey.com/converters.html'>Return to the Main Page</a></p>")
print("<textarea style='width:100%; border:1px solid #CCC; height:800px; padding:5px;'>")

# Insert function definitions below:

def dms2dd(dms):
    dms = float(dms)
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
    s = int(s)
    return str(int(dd)) + '.' + mspace + str(int(m)) + (sspace+str(s))

def reverse(horizAngle):
    horizAngle = dms2dd(horizAngle)
    horizAngle = horizAngle-180
    horizAngle = dd2dmsstring(horizAngle)
    return horizAngle
    
def supplement(zenithAngle):
    zenithAngle = dms2dd(zenithAngle)
    zenithAngle = 360 - zenithAngle
    zenithAngle = dd2dmsstring(zenithAngle)
    return zenithAngle

# Checks if input was empty:
if not 'content' in form:
    output_text = 'ERROR: No input provided...'

#Reads form data passed from webpage and stores it as object "content"
else:
    text = form.getvalue('content')
    stripstderr = form.getvalue('stripstderr')
    movec = form.getvalue('movec')
    combear = form.getvalue('combear')
    
#Insert script below:
    lines = text.splitlines()
    output = ""
    points = ""

    #Run through file to rewrite using M Records
    for i in range(len(lines)):
        curLine = lines[i]
        if curLine == "" or curLine[0] == "#":
            output += curLine + "\n"
            skip = True
        else: 
            row = curLine.split(" ")
            skip = False
    #Handles C Records
            if row[0] == "C" and movec == "y":
                desc = ""
                points += "#" + curLine + "\n"
                skip = True
            if row[0] == "C" and movec != "y":
                output += curLine + "\n"
                skip = True
    #Handles B Records
            if row[0] == "B" and combear == "y":
                output += "#" + curLine + "\n"
                skip = True
            if row[0] == "B" and combear != "y":
                output += curLine + "\n"
                skip = True
    #Handles D Records
            if row[0] == "D" and stripstderr == "y":
                output += "D " + row[1] + "\t"  + row[2] + "\t" + row[4] + "\n"
                skip = True
            if row[0] == "D" and stripstderr != "y":
                output += curLine + "\n"
                skip = True

    #Handles M Records
            if row[0] == "M" and stripstderr == "y":
                if row[2] == "?" and row[4] == "?":
                    output += "M " + row[1] + "\t"  + row[2] + "\t"  + row[3] + "\t"  + row[4] + "\t" + "\t" + row[8] + "\t#" + row[5] + " " + row[6] + " " + row[7] + "\n" 
                else:
                    output += "M " + row[1] + "\t"  + row[2] + "\t"  + row[3] + "\t"  + row[4] + "\t" + row[8] + "\t#" + row[5] + " " + row[6] + " " + row[7] + "\n"
                skip = True
            #need to add feature to handle HT problem
            if row[0] == "M" and stripstderr != "y":
                output += curLine + "\n"
                skip = True

    #Handles V Records
            if row[0] == "V" and stripstderr == "y":
                output += "V " + row[1] + "\t"  + row[2] + "\t"  + row[4] + "\n"
                skip = True
            if row[0] == "V" and stripstderr != "y":
                output += curLine + "\n"
                skip = True

    #need to skip this if any above actions were taken
            elif skip != True:
                output += curLine + "\n"

    if movec == "y":
        output_text += points + "\n"
    output_text += output + "\n"

# dO NOT MODIFY BELOW:
print(html.escape(output_text, quote=True))
print("</textarea>")
print("<p>Please contact MicroSurvey at helpdesk@microsurvey.com if results are not as expected or contain errors.</p>")
print("</div>")
print("</body>")
print("</html>")
