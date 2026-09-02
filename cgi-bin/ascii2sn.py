#!/usr/bin/python
import cgi, cgitb, time, string
##import cgitb
##cgitb.enable()

form = cgi.FieldStorage()                 # parse form data
titleString = "<title>Converted Results</title>"
returnlink = 'https://support.microsurvey.com/convert/asciims.html'
output_text = '#Converted ' + time.strftime('%B %d, %Y -- %I:%M:%S %p %Z') + '\r\n#ASCII to STAR*NET script by Jacob Wall -- helpdesk@MicroSurvey.com\r\n#Script Version 0.2 -- December 3, 2015\r\n\r\n'
	
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
print "'>Return to the Input Page</a>&nbsp;&nbsp;&nbsp;<a class='button-2' href='https://helpdesk.microsurvey.com/index.php?/Knowledgebase/Article/View/1456'>Return to the Main Page</a></p>"
print "<textarea style='width:100%; border:1px solid #CCC; height:800px; padding:5px;'>"

if not 'content' in form:
	output_text = 'ERROR: No input provided...'
else:
	delimiter = form.getvalue('delimiter')
	if delimiter == 'comma':
		char = ','
	elif delimiter == 'space':
		char = ' '
	else:
		char = '\t'
	format = form.getvalue('format')
	if format[1] == 'n':
		npos = 1
		epos = 2
	else:
		npos = 2
		epos = 1
	if len(format) == 4:
		if format[3] == 'z':
			writez = True
		else:
			writez = False
		if format[3] == 'd':
			dpos = 3
			writed = True
		else:
			writed = False
	elif len(format) == 5:
		writez = True
		writed = True
		dpos = 4
	else:
		writez = False
		writed = False
	height = form.getvalue('height')
	if writez:
		if height == 'ellip':
			type = 'CH  '
		else:
			type = 'C  '
	else:
		type = 'C  '	
	if writez:
		output_text += '\n.3D\r\n.ORDER NE\r\n\r\n'
	else:
		output_text += '\n.2D\r\n.ORDER NE\r\n\r\n'
	
	text = form.getvalue('content')
	lines = text.splitlines()		
	for i in range(len(lines)):
		curLine = lines[i].split(char)
		output_text += type + curLine[0].ljust(18, ' ') + curLine[npos].ljust(15, ' ') + curLine[epos].ljust(15, ' ')
		if writez:
			output_text += curLine[3].rjust(12, ' ')
			output_text += "  * * *  " 
		else:
			output_text += "  * *  "
		if writed:
			output_text += "'" + curLine[dpos]
		output_text += '\r\n'
		
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
