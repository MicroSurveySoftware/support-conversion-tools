#!/usr/bin/python
import cgi, cgitb, time, string
import xml.etree.ElementTree as ET
#below entry allows for online debugging, it should be removed for release:
import cgitb
cgitb.enable(format = "text")



form = cgi.FieldStorage()                 # parse form data
titleString = "<title>Converted Results</title>"
returnlink = 'http://support.microsurvey.com/convert/teachable.html'
output_text = '#Created ' + time.strftime('%B %d, %Y -- %I:%M:%S %p %Z') + '\r\n#Template script by MicroSurvey -- helpdesk@MicroSurvey.com\r\n#Script Version 1.0 -- MM DD, YYYY\r\n\r\n'

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
print "'>Return to the Input Page</a>&nbsp;&nbsp;&nbsp;<a class='button-2' href='http://helpdesk.microsurvey.com/index.php?/Knowledgebase/Article/View/1456/242/online-utilities'>Access Converters</a></p>"
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

def makeheader(input):
    if path:
        if  "http" in input:
            line = '<img src="' + header + '"</>\n\n'
        if  "http" not in input:
            line = '<img src="' + path + header + '"</>\n\n'
    else:
        line = '<img src="' + header + '"</>\n\n'
    return(line)

def makeobjective(input):
    line = '<h1><strong>Objective:</strong></h1>\n<p>' + input + '</p>\n\n'
    return(line)

def makenotes(input,path):
    lines = '<h1><strong>NOTES:</strong></h1>\n<ul>\n'
    data = input.splitlines()
    for i in range(len(data)):
        curLine = data[i]
        if "</image>" in curLine and  "https" in curLine:
            lines += '<img src="' + curLine[curLine.find('<image>')+ 7:curLine.rfind('</image>')] + '"</>\n'
        elif "</image>" in curLine and  "http" not in curLine:
            lines += '<img src="' + path + curLine[curLine.find('<image>')+ 7:curLine.rfind('</image>')] + '"</>\n'
        else:
            lines += '   <li>' + curLine + '</li>\n'
    lines += '</ul>\n\n'
    return lines

def makemovies(input,path,industry):
    lines = '<h1><strong>Movie:</strong></h1>\n<table>'
    data = input.splitlines()
    for i in range(len(data)):
        curLine = data[i]
        url = curLine[curLine.find('<file>')+ 6:curLine.rfind('<filetext>')]
        if "http" not in url:
            url = path + url
        text = curLine[curLine.find('<filetext>')+ 10:curLine.rfind('</filetext>')]
        if industry == 'geomatics':
            content = '    <tr>\n    <td><a href="' + url + '" target="_blank">	<img src = "http://assets.microsurvey.com/media/teachable/small-play-icon5.png" ><span style="padding-left: 20px; font-size: 17px;">' + text + '</span></a></td></li>\n    </tr>\n'
        else:
            content = '    <tr>\n    <td><a href="' + url + '" target="_blank">	<img src = "http://assets.microsurvey.com/media/teachable/small-play-icon4.png" ><span style="padding-left: 20px; font-size: 17px;">' + text + '</span></a></td></li>\n    </tr>\n'
        lines += content
    lines += '</table>\n\n'
    return lines

def makereading(input,path):
    lines = '<h1><strong>Further Reading:</strong></h1>\n'
    data = input.splitlines()
    for i in range(len(data)):
        curLine = data[i]
##        url = curLine[curLine.find('<link>')+ 6:curLine.rfind('<linktext>')]
##        if "http" not in url:
##            url = path + url
##        text = curLine[curLine.find('<linktext>')+ 10:curLine.rfind('</linktext>')]
        content = '<p>' + curLine + '</p>\n'
        lines += content
    return lines
    
def makeassignment(input,path):
    lines = '<h1><strong>Assignment:</strong></h1>\n<ol>\n'
    data = input.splitlines()
    for i in range(len(data)):
        curLine = data[i]
        if "</image>" in curLine and  "http" in curLine:
            lines += '<img src="' + curLine[curLine.find('<image>')+ 7:curLine.rfind('</image>')] + '"</>\n'
        elif "</image>" in curLine and  "http" not in curLine:
            lines += '<img src="' + path + curLine[curLine.find('<image>')+ 7:curLine.rfind('</image>')] + '"</>\n'
        else:
            lines += '   <li>' + curLine + '</li>\n'
    lines += '</ol>\n\n'
    return lines   

# Checks if input was empty:

if not 'instructions' in form:
	output_text = 'ERROR: You must input Instructions...'

#Reads form data passed from webpage and stores it as object "content"

else:
    content = form.getvalue('content')
    #content = input.read()

    
#Insert script below:

    #if not 'formvalue_text' in form:
    #    textinput = ""
    #else:
    header = objective = notes = movielinks = reading = assignment = path = ""
    industry = form.getvalue('industry')
    path = form.getvalue('path')
    header = form.getvalue('header')
    objective = form.getvalue('objective')
    notes = form.getvalue('notes')	
    movielinks = form.getvalue('movies')
    reading = form.getvalue('reading')
    assignment = form.getvalue('instructions')
	
    if path == ' ':
        path = ''
    if header == ' ':
        header = ''
    if assignment is None:
        assignment = 'You must enter instructions'

    #output_text += industry + "\n" 
    #output_text += path + "\n"
    #output_text += header + "\n"
    #output_text += objective + "\n"
    #output_text += notes + "\n"
    #output_text += movies + "\n"
    #output_text += reading + "\n"
    #output_text += instructions + "\n"
	

        
        
    

    #Need to check for entries with quotes in them

    output = ""

    if header:
        output += makeheader(header)

    if objective:
        output += makeobjective(objective)

    if notes:
        output += makenotes(notes,path)

    if movielinks:
        output += makemovies(movielinks,path,industry)


    if reading:
        output += makereading(reading,path)

    if assignment:
        output += makeassignment(assignment,path)



# dO NOT MODIFY BELOW:
print cgi.escape(output, quote=True)
print "</textarea>"
print "<p>Please contact MicroSurvey at helpdesk@microsurvey.com if results are not as expected or contain errors.</p>"
print cgi.escape(output, quote=True)
print "</div>"
print "</body>"
print "</html>"


#Add a note to access.dat
import sys, os
ip = cgi.escape(os.environ["REMOTE_ADDR"])
script = str(sys.argv[0])
date = time.strftime('%B %d: %Y -- %I:%M:%S %p %Z')
note = script + "," + date + ",IP V6 address: " + ip + "\n"
fileout = open('access.dat','a')
fileout.write(note)
fileout.close()
