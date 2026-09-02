#!/usr/bin/python
import cgi, cgitb, time, string, math

form = cgi.FieldStorage()                 # parse form data
titleString = "<title>Converted Results</title>"
returnlink = 'http://support.microsurvey.com/convert/geolabtsms.html'
output_text = '#Converted ' + time.strftime('%B %d, %Y -- %I:%M:%S %p %Z') + '\r\n#Geolab to STAR*NET script by Jacob Wall -- helpdesk@microsurvey.com\r\n#Script Version 0.2 -- December 3, 2015\r\n\r\n'

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

if not 'content' in form:
	output_text = 'ERROR: No input provided...'
else:
	text = form.getvalue('content')
	comment = form.getvalue('comment')
	lines = text.splitlines()
	output_text += '.3D\r\n.ORDER AtFromTo\r\n.ORDER NE\r\n\r\n'
	for i in range(len(lines) - 1):
		curLine = lines[i]
		rectype = curLine[0:5].rstrip(' ')
		if rectype == ' NEO':
			nfix = curLine[6:7]
			if nfix == '1':
				nfix = '!'
			else:
				nfix = '*'
			efix = curLine[7:8]
			if efix == '1':
				efix = '!'
			else:
				efix = '*'
			zfix = curLine[8:9]
			if zfix == '1':
				zfix = '!'
			else:
				zfix = '*'
			Sta = curLine[10:22]
			north = curLine[23:39].lstrip(' ')
			east = curLine[40:56].lstrip(' ')
			elev = curLine[57:67].lstrip(' ')
			output_text += 'C ' + Sta + ' ' + north + '  ' + east + '  ' + elev + '  ' + nfix + ' ' + efix + ' ' + zfix + '\r\n'
		elif rectype == ' DIST':
			staString = curLine[10:22].rstrip(' ') + '-' + curLine[23:35].rstrip(' ')
			dist = curLine[49:64].lstrip(' ')
			output_text += 'D  ' + staString.ljust(30, ' ') + dist.rjust(18, ' ') + '  0.00/0.00\r\n'
		elif rectype == ' ANGL':
			staString = curLine[10:22].rstrip(' ') + '-' + curLine[23:35].rstrip(' ') + '-' + curLine[36:48].rstrip(' ')
			angString = curLine[50:53].lstrip(' ') + '-' + curLine[54:56].lstrip(' ').rjust(2, '0') + '-'
			secString = curLine[57:64].lstrip(' ')
			if secString[1] == '.':
				angString += '0'
			angString += secString
			output_text +='A  ' + staString.ljust(30, ' ') + angString.rjust(18, ' ') + '\r\n'
		else:
			if comment == 'yes':
				output_text += '#' + curLine + '\r\n'

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
