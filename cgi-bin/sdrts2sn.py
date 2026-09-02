#!/usr/bin/python
import cgi, cgitb, time, string, math

def dd2dmsstring(dd):
	mspace = ''
	sspace = ''
	m = abs((dd-int(dd))) * 60
	s = (m-int(m)) * 60
	if m < 10:
		mspace = '0'
	if s < 10:
		sspace = '0'
	return str(int(dd)) + '-' + mspace + str(int(m)) + '-' + (sspace+str(s)).ljust(6, '0')[0:6]

def anglein(angstr):
	ang = float(angstr)
	if angleUnit == '2':
		ang = ang / 1.111111111111111
	return ang

form = cgi.FieldStorage()                 # parse form data
titleString = "<title>Converted Results</title>"
returnlink = 'https://support.microsurvey.com/convert/sdrtsms.html'
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
	type = form.getvalue('type')
	sdrformat = form.getvalue('format')
	lines = text.splitlines()
	staID = 'X'
	bsID = 'Y'
	staHI = 0
	targHT = 0
	bsDone = False
	output_text += '.' + type + '\r\n.ORDER NE\r\n'
	
	for i in range(len(lines)):
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
		elif lineCode == '02':
			if sdrformat == 'sdr20':
				staID = curLine[4:8].lstrip('0')
				staHI = float(curLine[38:48])
				output_text += '\r\n#C ' + staID.ljust(18, ' ') + curLine[8:18].lstrip(' ').rjust(15, ' ') + curLine[18:28].lstrip(' ').rjust(15, ' ')
				if type == '3D':
					output_text += curLine[28:38].lstrip(' ').rjust(12, ' ') + '  * * * \''
				else:
					output_text += '  * * \''
				output_text += curLine[48:].lstrip(' ').rstrip(' ') + '\r\n'
			else:
				staID = curLine[4:20].lstrip(' ')
				staHI = float(curLine[68:84])
				output_text += '\r\n#C ' + staID.ljust(18, ' ') + curLine[20:36].lstrip(' ').rjust(15, ' ') + curLine[36:52].lstrip(' ').rjust(15, ' ')
				if type == '3D':
					output_text += curLine[52:68].lstrip(' ').rjust(12, ' ') + '  * * * \''
				else:
					output_text += '  * * \''
				output_text += curLine[84:].lstrip(' ').rstrip(' ') + '\r\n'
		elif lineCode == '03':
			if sdrformat == 'sdr20':
				targHT = float(curLine[4:14])
			else:
				targHT = float(curLine[4:20])
		elif lineCode == '07':
			if sdrformat == 'sdr20':
				staID = curLine[4:8].lstrip('0')
				bsID = curLine[8:12].lstrip(' ')
				bsAZ = anglein(curLine[12:22])
				bsHZobs = anglein(curLine[22:32])
			else:
				staID = curLine[4:20].lstrip(' ')
				bsID = curLine[20:36].lstrip(' ')
				bsAZ = anglein(curLine[36:52])
				bsHZobs = anglein(curLine[52:68])
			bsDone = True
		elif lineCode == '08':
			if sdrformat == 'sdr20':
				output_text += '#C ' + curLine[4:8].lstrip('0').ljust(18, ' ') + curLine[8:18].lstrip(' ').rjust(15, ' ') + curLine[18:28].lstrip(' ').rjust(15, ' ')
				if type == '3D':
					output_text += curLine[28:38].lstrip(' ').rjust(12, ' ') + '  * * * \''
				else:
					output_text += '  * * \''
				output_text += curLine[38:].lstrip(' ').rstrip(' ') + '\r\n'
			else:
				output_text += '#C ' + curLine[4:20].lstrip(' ').ljust(18, ' ') + curLine[20:36].lstrip(' ').rjust(15, ' ') + curLine[36:52].lstrip(' ').rjust(15, ' ')
				if type == '3D':
					output_text += curLine[52:68].lstrip(' ').rjust(12, ' ') + '  * * * \''
				else:
					output_text += '  * * \''
				output_text += curLine[68:].lstrip(' ').rstrip(' ') + '\r\n'
		elif lineCode == '09':
			if bsDone:
				if sdrformat == 'sdr20':
					staID = curLine[4:8].lstrip('0')
					curSta = curLine[8:12].lstrip('0')
					slDist = float(curLine[12:22])
					vtAng = anglein(curLine[22:32])
					if vtAng > 180:
						vtAng = 360 - vtAng
					hzAng = anglein(curLine[32:42])
					staString = staID + '-' + bsID
					desc = '  \'' + curLine[42:].lstrip(' ').rstrip(' ') + '\r\n'
					if curLine[2:4] in ('F1','F2','MD'):
						if curSta == bsID:
							bsAZ = hzAng
							if type == '2D':
								hzDist = math.fabs(slDist * math.sin(math.radians(vtAng)))
								output_text += 'D  ' + staString.ljust(37, ' ') + format(hzDist, '.5f').rjust(15, ' ') + desc
							else:
								output_text += 'DV ' + staString.ljust(37, ' ') + format(slDist, '.5f').rjust(15, ' ') +  dd2dmsstring(vtAng).rjust(15, ' ') + '  ' + format(staHI, '.5f') + '/' + format(targHT, '.5f') + desc
						else:
							angRight = hzAng - bsAZ
							if angRight < 0:
								angRight = angRight+360
							staString += '-' + curSta
							if type == '2D':
								hzDist = math.fabs(slDist * math.sin(math.radians(vtAng)))
								output_text += 'M  ' + staString.ljust(20, ' ') + '  ' + dd2dmsstring(angRight).rjust(15, ' ') + format(hzDist, '.5f').rjust(15, ' ') + desc
							else:
								output_text += 'M  ' + staString.ljust(20, ' ') + '  ' + dd2dmsstring(angRight).rjust(15, ' ') + format(slDist, '.5f').rjust(15, ' ') + dd2dmsstring(vtAng).rjust(15, ' ') + '  ' + format(staHI, '.5f') + '/' + format(targHT, '.5f') + desc
					else:
						if curSta == bsID:
							bsAZ = hzAng
							if type == '2D':
								hzDist = slDist * math.sin(math.radians(vtAng))
								hzDist = "{:.5f}".format(hzDist)
								output_text += 'D  ' + staString.ljust(37, ' ') + format(hzDist, '.5f').rjust(15, ' ') + desc
							else:
								output_text += 'DV ' + staString.ljust(37, ' ') + format(slDist, '.5f').rjust(15, ' ') +  dd2dmsstring(vtAng).rjust(15, ' ') + '  ' + format(staHI, '.5f') + '/' + format(targHT, '.5f') + desc
						else:
							angRight = hzAng - bsAZ
							if angRight < 0:
								angRight = angRight+360
							staString += '-' + curSta
							if type == '2D':
								hzDist = math.fabs(slDist * math.sin(math.radians(vtAng)))
								output_text += 'M  ' + staString.ljust(20, ' ') + '  ' + dd2dmsstring(angRight).rjust(15, ' ') + format(hzDist, '.5f').rjust(15, ' ') + desc
							else:
								output_text += 'M  ' + staString.ljust(20, ' ') + '  ' + dd2dmsstring(angRight).rjust(15, ' ') + format(slDist, '.5f').rjust(15, ' ') + dd2dmsstring(vtAng).rjust(15, ' ') + '  ' + format(staHI, '.5f') + '/' + format(targHT, '.5f') + desc
				else:
					staID = curLine[4:20].lstrip(' ')
					curSta = curLine[20:36].lstrip(' ')
					slDist = float(curLine[36:52])
					vtAng = anglein(curLine[52:68])
					if vtAng > 180:
						vtAng = 360 - vtAng
					hzAng = anglein(curLine[68:84])
					staString = staID + '-' + bsID
					desc = '  \'' + curLine[85:].lstrip(' ').rstrip(' ') + '\r\n'
					if curLine[2:4] in ('F1','F2','MD'):
						if curSta == bsID:
							bsAZ = hzAng
							if type == '2D':
								hzDist = math.fabs(slDist * math.sin(math.radians(vtAng)))
								output_text += 'D  ' + staString.ljust(37, ' ') + format(hzDist, '.5f').rjust(15, ' ') + desc
							else:
								output_text += 'DV ' + staString.ljust(37, ' ') + format(slDist, '.5f').rjust(15, ' ') +  dd2dmsstring(vtAng).rjust(15, ' ') + '  ' + format(staHI, '.5f') + '/' + format(targHT, '.5f') + desc
						else:
							angRight = hzAng - bsAZ
							if angRight < 0:
								angRight = angRight+360
							staString += '-' + curSta
							if type == '2D':
								hzDist = math.fabs(slDist * math.sin(math.radians(vtAng)))
								output_text += 'M  ' + staString.ljust(20, ' ') + '  ' + dd2dmsstring(angRight).rjust(15, ' ') + format(hzDist, '.5f').rjust(15, ' ') + desc
							else:
								output_text += 'M  ' + staString.ljust(20, ' ') + '  ' + dd2dmsstring(angRight).rjust(15, ' ') + format(slDist, '.5f').rjust(15, ' ') + dd2dmsstring(vtAng).rjust(15, ' ') + '  ' + format(staHI, '.5f') + '/' + format(targHT, '.5f') + desc
					else:
						if curSta == bsID:
							bsAZ = hzAng
							if type == '2D':
								hzDist = slDist * math.sin(math.radians(vtAng))
								hzDist = "{:.5f}".format(hzDist)
								output_text += 'D  ' + staString.ljust(37, ' ') + format(hzDist, '.5f').rjust(15, ' ') + desc
							else:
								output_text += 'DV ' + staString.ljust(37, ' ') + format(slDist, '.5f').rjust(15, ' ') +  dd2dmsstring(vtAng).rjust(15, ' ') + '  ' + format(staHI, '.5f') + '/' + format(targHT, '.5f') + desc
						else:
							angRight = hzAng - bsAZ
							if angRight < 0:
								angRight = angRight+360
							staString += '-' + curSta
							if type == '2D':
								hzDist = math.fabs(slDist * math.sin(math.radians(vtAng)))
								output_text += 'M  ' + staString.ljust(20, ' ') + '  ' + dd2dmsstring(angRight).rjust(15, ' ') + format(hzDist, '.5f').rjust(15, ' ') + desc
							else:
								output_text += 'M  ' + staString.ljust(20, ' ') + '  ' + dd2dmsstring(angRight).rjust(15, ' ') + format(slDist, '.5f').rjust(15, ' ') + dd2dmsstring(vtAng).rjust(15, ' ') + '  ' + format(staHI, '.5f') + '/' + format(targHT, '.5f') + desc
			else:
				output_text += '#Missing Back Bearing:\r\n' + curLine + '\r\n'
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
