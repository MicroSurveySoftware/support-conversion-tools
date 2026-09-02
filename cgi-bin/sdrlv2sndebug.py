#!/usr/bin/python
import cgi, cgitb, time, string, math

#below entry allows for online debugging, it should be removed for release:
import cgitb
cgitb.enable(format='text')

form = cgi.FieldStorage()                 # parse form data
titleString = "<title>Converted Results</title>"
returnlink = 'https://support.microsurvey.com/convert/sdrlvms.html'
output_text = '#Converted ' + time.strftime('%B %d, %Y -- %I:%M:%S %p %Z') + '\r\n#SDR to STAR*NET script by Jacob Wall -- helpdesk@microsurvey.com\r\n#Script Version 0.2 -- December 3, 2015\r\n\r\n'

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
	text = form.getvalue('content')
	sdrformat = form.getvalue('format')
	lines = text.splitlines()
	i = 0
	while (i < len(lines)):
		curLine = lines[i]
		lineCode = curLine[0:2]
		if lineCode == '00':
			angleUnit = curLine[40]
			distUnit = curLine[41]
			if distUnit == '1':
				output_text += '.UNITS Meters\r\n\r\n'
			elif distUnit == '2':
				output_text += '.UNITS FeetInt\r\n\r\n'
			else:
				output_text += '.UNITS FeetUS\r\n\r\n'
			i += 1
		elif lineCode == '61':
			if sdrformat == 'sdr20':
				staID = curLine[4:8].lstrip(' ')
				staElev = float(curLine[24:34])
				desc = '  *  \'' + curLine[8:24].lstrip(' ').rstrip(' ') + '\r\n\r\n'
				output_text += '\r\n#E  ' + staID.ljust(8, ' ') + format(staElev, '.5f').rjust(15, ' ') + desc
			else:
				staID = curLine[4:20].lstrip(' ')
				staElev = float(curLine[36:52])
				desc = '  *  \'' + curLine[20:36].lstrip(' ').rstrip(' ') + '\r\n\r\n'
				output_text += '\r\n#E  ' + staID.ljust(18, ' ') + format(staElev, '.5f').rjust(15, ' ') + desc
			i += 1
		elif lineCode == '62':
			if sdrformat == 'sdr20':
				staNum = curLine[4:9]
				bsID = curLine[9:13].lstrip('0')
				TPcount = curLine[13:18]
			else:
				staNum = curLine[4:9]
				bsID = curLine[9:25].lstrip(' ')
				TPcount = curLine[25:30]
			i += 1
		elif lineCode == '63':
			if (i+2) < len(lines):
				if lines[i+1][0:2] == '63' and lines[i+2][0:2] == '63' and lines[i+3][0:2] == '63':
					if sdrformat == 'sdr20':
						desc = '  \'' + curLine[28:44].lstrip(' ').rstrip(' ') + '\r\n'
						staNum = curLine[44:49]
						IsABs = curLine[49:54]
						IsATP = curLine[54:59]
						offset = float(curLine[59:69])
						bsID = curLine[4:8].lstrip('0')
						bsdist = float(curLine[8:18])
						bsread = float(curLine[18:28])
						staString = bsID + '-' + lines[i+2][4:8].lstrip('0')
						dist = float(lines[i+2][8:18])+bsdist
						read = bsread-float(lines[i+2][18:28])
						output_text += 'L  ' + staString.ljust(20, ' ') + format(read, '.5f').rjust(15, ' ') + format(dist, '.1f').rjust(12, ' ') + '\r\n'
						
						desc = '  \'' + curLine[28:44].lstrip(' ').rstrip(' ') + '\r\n'
						staNum = lines[i+1][44:49]
						IsABs = lines[i+1][49:54]
						IsATP = lines[i+1][54:59]
						offset = float(lines[i+1][59:69])
						bsID = lines[i+1][4:8].lstrip('0')
						bsdist = float(lines[i+1][8:18])
						bsread = float(lines[i+1][18:28])
						staString = bsID + '-' + lines[i+3][4:8].lstrip('0')
						dist = float(lines[i+3][8:18])+bsdist
						read = bsread-float(lines[i+3][18:28])
						output_text += 'L  ' + staString.ljust(20, ' ') + format(read, '.5f').rjust(15, ' ') + format(dist, '.1f').rjust(12, ' ') + '\r\n'
					else:
						desc = '  \'' + curLine[52:68].lstrip(' ').rstrip(' ') + '\r\n'
						staNum = curLine[68:73]
						IsABs = curLine[73:78]
						IsATP = curLine[78:83]
						offset = float(curLine[83:99])
						bsID = curLine[4:20].lstrip('0')
						bsdist = float(curLine[20:36])
						bsread = float(curLine[36:52])
						staString = bsID + '-' + lines[i+2][4:20].lstrip('0')
						dist = float(lines[i+2][20:36])+bsdist
						read = bsread-float(lines[i+2][36:52])
						output_text += 'L  ' + staString.ljust(20, ' ') + format(read, '.5f').rjust(15, ' ') + format(dist, '.1f').rjust(12, ' ') + '\r\n'
						
						desc = '  \'' + curLine[52:68].lstrip(' ').rstrip(' ') + '\r\n'
						staNum = lines[i+1][68:73]
						IsABs = lines[i+1][73:78]
						IsATP = lines[i+1][78:83]
						offset = float(lines[i+1][83:99])
						bsID = lines[i+1][4:20].lstrip(' ')
						bsdist = float(lines[i+1][20:36])
						bsread = float(lines[i+1][36:52])
						staString = bsID + '-' + lines[i+3][4:20].lstrip(' ')
						dist = float(lines[i+3][20:36])+bsdist
						read = bsread-float(lines[i+3][36:52])
						output_text += 'L  ' + staString.ljust(20, ' ') + format(read, '.5f').rjust(15, ' ') + format(dist, '.1f').rjust(12, ' ') + '\r\n'
					i += 4
				elif lines[i+1][0:2] == '63':
					if sdrformat == 'sdr20':
						desc = '  \'' + curLine[28:44].lstrip(' ').rstrip(' ') + '\r\n'
						staNum = curLine[44:49]
						IsABs = curLine[49:54]
						IsATP = curLine[54:59]
						offset = float(curLine[59:69])
						bsID = curLine[4:8].lstrip('0')
						bsdist = float(curLine[8:18])
						bsread = float(curLine[18:28])
						staString = bsID + '-' + lines[i+1][4:8].lstrip('0')
						dist = float(lines[i+1][8:18])+bsdist
						read = bsread-float(lines[i+1][18:28])
						output_text += 'L  ' + staString.ljust(20, ' ') + format(read, '.5f').rjust(15, ' ') + format(dist, '.1f').rjust(12, ' ') + '\r\n'
					else:
						desc = '  \'' + curLine[52:68].lstrip(' ').rstrip(' ') + '\r\n'
						staNum = curLine[68:73]
						IsABs = curLine[73:78]
						IsATP = curLine[78:83]
						offset = float(curLine[83:99])
						bsID = curLine[4:20].lstrip(' ')
						bsdist = float(curLine[20:36])
						bsread = float(curLine[36:52])
						staString = bsID + '-' + lines[i+1][4:20].lstrip(' ')
						dist = float(lines[i+1][20:36])+bsdist
						read = bsread-float(lines[i+1][36:52])
						output_text += 'L  ' + staString.ljust(20, ' ') + format(read, '.5f').rjust(15, ' ') + format(dist, '.1f').rjust(12, ' ') + '\r\n'
					i += 2
				else:
					i += 1
			elif i < len(lines):
				if lines[i+1][0:2] == '63':
					if sdrformat == 'sdr20':
						desc = '  \'' + curLine[28:44].lstrip(' ').rstrip(' ') + '\r\n'
						staNum = curLine[44:49]
						IsABs = curLine[49:54]
						IsATP = curLine[54:59]
						offset = float(curLine[59:69])
						bsID = curLine[4:8].lstrip('0')
						bsdist = float(curLine[8:18])
						bsread = float(curLine[18:28])
						staString = bsID + '-' + lines[i+1][4:8].lstrip('0')
						dist = float(lines[i+1][8:18])+bsdist
						read = bsread-float(lines[i+1][18:28])
						output_text += 'L  ' + staString.ljust(20, ' ') + format(read, '.5f').rjust(15, ' ') + format(dist, '.1f').rjust(12, ' ') + '\r\n'
					else:
						desc = '  \'' + curLine[52:68].lstrip(' ').rstrip(' ') + '\r\n'
						staNum = curLine[68:73]
						IsABs = curLine[73:78]
						IsATP = curLine[78:83]
						offset = float(curLine[83:99])
						bsID = curLine[4:20].lstrip(' ')
						bsdist = float(curLine[20:36])
						bsread = float(curLine[36:52])
						staString = bsID + '-' + lines[i+1][4:20].lstrip(' ')
						dist = float(lines[i+1][20:36])+bsdist
						read = bsread-float(lines[i+1][36:52])
						output_text += 'L  ' + staString.ljust(20, ' ') + format(read, '.5f').rjust(15, ' ') + format(dist, '.1f').rjust(12, ' ') + '\r\n'
					i += 2
				else:
					i += 1
			else:
				i += 1
		else:
			i += 1

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
