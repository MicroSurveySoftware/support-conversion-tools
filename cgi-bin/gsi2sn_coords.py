#!/usr/bin/python
import cgi, cgitb, time, string

def fmtCoord(coordString):
	result = (coordString[0] + coordString[1:distPrec].lstrip('0').rjust(1, '0') + '.' + coordString[distPrec:]).replace('+', '')
	return result

form = cgi.FieldStorage()                 # parse form data
titleString = "<title>Converted Results</title>"
returnlink = 'http://support.microsurvey.com/convert/gsi_coordsms.html'
output_text = '#Converted ' + time.strftime('%B %d, %Y -- %I:%M:%S %p %Z') + '\r\n#GSI to STAR*NET script by Jacob Wall -- helpdesk@microsurvey.com\r\n#Script Version 0.2 -- December 3, 2015\r\n\r\n'

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
print ".button-2:hover {background-color:#C49C00; color:#fff;}"
print "a {color:#F24C15; outline:none; cursor:pointer; text-decoration:none;}"
print "</style"
print "</head>"
print "<body>"
print "<div class='container'>"
print "<p style='text-align:center;'><a class= 'button-2' href='"
print returnlink
print "'>Return to the Input Page</a>&nbsp;&nbsp;&nbsp;<a class='button-2' href='http://helpdesk.microsurvey.com/index.php?/Knowledgebase/Article/View/1456'>Return to the Main Page</a></p>"
print "<textarea style='width:100%; border:1px solid #CCC; height:800px; padding:5px;'>"

if not 'content' in form:
	output_text = 'ERROR: No input provided...'
else:
	text = form.getvalue('content')
	format = form.getvalue('format')
	if format == 'gsi8':
		valoff = 16
	else:
		valoff = 24
	height = form.getvalue('height')
	if height == 'ellip':
		type = 'CH  '
	else:
		type = 'C  '
	StaList = []
	pos = text.find(' 81')
	if pos > 0:
		lines = text.splitlines()
		distUnit = text[pos+6:pos+7]
		if distUnit == '0':
			distUnit = '.UNITS Meters'
			distPrec = -3
		elif distUnit == '1':
			distUnit = '.UNITS FeetInt #FeetUS'
			distPrec = -3
		elif distUnit == '6':
			distUnit = '.UNITS Meters'
			distPrec = -4
		elif distUnit == '7':
			distUnit = '.UNITS FeetInt #FeetUS'
			distPrec = -4
		else:
			distUnit = '.UNITS Meters'
			distPrec = -5
		output_text += '.3D\r\n' + distUnit + '\r\n\r\n'

		for i in range(len(lines) - 1):
			curLine = lines[i]
			ptID = curLine[8:valoff].lstrip('0')
			if ptID not in StaList:
				StaList.append(ptID)
				pos = curLine.find(' 81')
				if pos > 0:
					east = fmtCoord(curLine[pos+7:pos+valoff])
					writeLine_tf = True
					code = ''
					pos = curLine.find(' 82')
					if pos < 0:
						writeLine_tf = False
					else:
						north = fmtCoord(curLine[pos+7:pos+valoff])
					pos = curLine.find(' 83')
					if pos < 0:
						writeLine_tf = False
					else:
						elev = fmtCoord(curLine[pos+7:pos+valoff])
					pos = curLine.find(' 4')
					if pos > 0:
						code = "  '" + curLine[pos+8:pos+valoff].lstrip('0')
					pos = curLine.find(' 7')
					if pos > 0:
						code = "  '" + curLine[pos+8:pos+valoff].lstrip('0')
					if writeLine_tf:
						output_text += type + ptID.ljust(18, ' ') + north.rjust(15, ' ') + east.rjust(15, ' ') + elev.rjust(12, ' ') + "  * * *" + code + '\r\n'
				pos = curLine.find(' 84')
				if pos > 0:
					east = fmtCoord(curLine[pos+7:pos+valoff])
					writeLine_tf = True
					code = ''
					pos = curLine.find(' 85')
					if pos < 0:
						writeLine_tf = False
					else:
						north = fmtCoord(curLine[pos+7:pos+valoff])
					pos = curLine.find(' 86')
					if pos < 0:
						writeLine_tf = False
					else:
						elev = fmtCoord(curLine[pos+7:pos+valoff])
					pos = curLine.find(' 4')
					if pos > 0:
						code = "  '" + curLine[pos+8:pos+valoff].lstrip('0')
					pos = curLine.find(' 7')
					if pos > 0:
						code = "  '" + curLine[pos+8:pos+valoff].lstrip('0')
					if writeLine_tf:
						output_text += type + ptID.ljust(18, ' ') + north.rjust(15, ' ') + east.rjust(15, ' ') + elev.rjust(12, ' ') + "  * * *" + code + '\r\n'
					
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
