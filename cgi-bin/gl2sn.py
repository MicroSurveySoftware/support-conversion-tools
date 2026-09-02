#!/usr/bin/python
import cgi, cgitb, time, string

def fmtlatlng(latlng):
	result = latlng[0:1].replace('N', '').replace('S', '-').replace('W', '-').replace('E', '') + latlng[1:].lstrip(' ').rstrip(' ').replace('  ', '-0').replace(' ', '-')
	return result

form = cgi.FieldStorage()                 # parse form data
titleString = "<title>Converted Results</title>"
returnlink = 'http://support.microsurvey.com/convert/geolabms.html'
output_text = '#Converted ' + time.strftime('%B %d, %Y -- %I:%M:%S %p %Z') + '\r\n#GeoLab to STAR*NET script by Jacob Wall -- helpdesk@microsurvey.com\r\n#Script Version 0.2 -- December 3, 2015\r\n\r\n'

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
	output_text += '.3D\r\n.UNITS Meters\r\n.long neg\r\n.GPS WEIGHT COVARIANCE\r\n\r\n'
	lines = text.splitlines()
	vectorID = 1
	for i in range(len(lines)):
		curLine = lines[i]
		rectype = curLine[0:5].rstrip(' ')
		if rectype == ' PLH':
			floatfix = ' ' + curLine[6:9].replace('0', ' *').replace('1', ' !')
			offset = curLine.find(' ', 22)
			Sta = curLine[10:offset].lstrip(' ').ljust(20)
			latValue = fmtlatlng(curLine[offset+1:offset+18]).rjust(20)
			longValue = fmtlatlng(curLine[offset+19:offset+36]).rjust(20)
			height = curLine[offset+37:offset+49].rjust(12)
			output_text += 'PH  ' + Sta + latValue + longValue + height + floatfix + '\r\n'
		elif rectype == ' GRP':
			output_text += '\r\nG0 \'V' + str(vectorID) + ' [' + curLine[10:40].rstrip(' ') + ']\r\n'
			vectorID += 1
		elif rectype == ' 3DD':
			pass
		elif rectype == ' DXYZ':
			offset1 = curLine.find(' ', 22)
			offset2 = curLine.find(' ', 35)
			stations = curLine[10:offset1].lstrip(' ').rstrip(' ').replace('-', '_') + '-' + curLine[offset1:offset2].lstrip(' ').rstrip(' ').replace('-', '_')
			output_text += 'G1 ' + stations.ljust(32) + curLine[offset2:] + '\r\n'
		elif rectype == ' COV':
			output_text += 'G2 ' + lines[i+1][7:30].lstrip(' ') + lines[i+2][7:30] + lines[i+3][7:30] + '\r\nG3 ' + lines[i+1][31:54].lstrip(' ') + lines[i+1][55:] + ' ' + lines[i+2][31:54] + '\r\n'
		elif rectype == ' ELEM':
			pass
		else:
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
