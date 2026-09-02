#!/usr/bin/python
import cgi, cgitb, time, string, math

def fmtCoord(distString):
	result = (distString[0] + distString[1:distPrec].lstrip('0').rjust(1, '0') + '.' + distString[distPrec:]).replace('+', '')
	return result
	
def fmtAng(angString):
	ang = float(angString)/100000
	if convertDMS:
		ang = dms2dd(ang)
	if convertGONS:
		ang = ang / 1.111111111111111
	return dd2dmsstring(ang).rjust(15, ' ')
		
def dms2dd(dms):
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
	return str(int(dd)) + '-' + mspace + str(int(m)) + '-' + (sspace+format(s, '.2f'))

form = cgi.FieldStorage()                 # parse form data
titleString = "<title>Converted Results</title>"
returnlink = 'http://support.microsurvey.com/convert/gsitsms.html'
output_text = '#Converted ' + time.strftime('%B %d, %Y -- %I:%M:%S %p %Z') + '\r\n#GSI to STAR*NET script by Jacob Wall -- helpdesk@microsurvey.com\r\n#Script Version 0.3 -- December 10, 2015\r\n\r\n'

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
	type = form.getvalue('type')
	gsiformat = form.getvalue('format')
	if gsiformat == 'gsi8':
		valoff = 16
	else:
		valoff = 24
	write_coords = form.getvalue('coords')
	pos = text.find(' 21')
	if pos > 0:
		lines = text.splitlines()
		angUnit = text[pos+6]
		if angUnit == '2': # gons
			convertDMS = False
			convertGONS = True
		elif angUnit == '3': # decimal degree
			convertDMS = False
			convertGONS = False
		else:  #4 DMS, not handling 5 which is 6400 mils
			convertDMS = True
			convertGONS = False
		pos = text.find(' 31')
		distUnit = text[pos+6]
		if distUnit == '0':
			distUnit = '.UNITS Meters'
			distPrec = -3
			distDiv = 1000
		elif distUnit == '1':
			distUnit = '.UNITS FeetInt #FeetUS'
			distPrec = -3
			distDiv = 1000
		elif distUnit == '6':
			distUnit = '.UNITS Meters'
			distPrec = -4
			distDiv = 10000
		elif distUnit == '7':
			distUnit = '.UNITS FeetInt #FeetUS'
			distPrec = -4
			distDiv = 10000
		elif distUnit == '8':
			distUnit = '.UNITS Meters'
			distPrec = -5
			distDiv = 100000
		else: # fall back, seen invalid blocks
			distUnit = '.UNITS Meters'
			distPrec = -3
			distDiv = 1000
		output_text += '.' + type + '\r\n' + distUnit + ' DMS\r\n\r\n'
		output_text += "DB #DB and DE information must be inserted where necessary before use...\r\n"
		instHT = 0.0
		targHT = 0.0
		
		for i in range(len(lines) - 1):
			curLine = lines[i]
			ptID = curLine[8:valoff].lstrip('0')
			if write_coords == 'yes':
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
						output_text += '#C  ' + ptID.ljust(18, ' ') + north.rjust(15, ' ') + east.rjust(15, ' ') + elev.rjust(12, ' ') + "  * * *" + code + '\r\n'
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
						output_text += '#C  ' + ptID.ljust(18, ' ') + north.rjust(15, ' ') + east.rjust(15, ' ') + elev.rjust(12, ' ') + "  * * *" + code + '\r\n'
			pos = curLine.find(' 87')
			if pos > 0:
				targHT = float(curLine[pos+8:pos+valoff])/distDiv
			pos = curLine.find(' 88')
			if pos > 0:
				instHT = float(curLine[pos+8:pos+valoff])/distDiv
			writeLine_tf = True
			pos = curLine.find(' 21')
			if pos < 0:
				writeLine_tf = False
			else:
				hzAngle = fmtAng(curLine[pos+8:pos+valoff])
				pos = curLine.find(' 22')
				if pos < 0:
					writeLine_tf = False
				else:
					vtAngle = fmtAng(curLine[pos+8:pos+valoff])
					if type == '2D':
						vtAng = float(curLine[pos+8:pos+valoff])/100000
						if convertDMS:
							vtAng = dms2dd(vtAng)
						if convertGONS:
							vtAng = vtAng / 1.111111111111111
					pos = curLine.find(' 31')
					if pos < 0:
						writeLine_tf = False
					else:
						pos1 = curLine.find('+', pos)+1  # making exception as per example file with missing width in distance field
						pos2 = curLine.find(' ', pos1)
						slDist = float(curLine[pos1:pos2])/distDiv
						if slDist == 0:
							Dist = '?'.rjust(15, ' ')
						else:
							if type == '2D':
								hzDist = math.fabs(slDist * math.sin(math.radians(vtAng)))
								Dist = format(hzDist, '.5f').rjust(15, ' ')
							else:
								Dist = format(slDist, '.5f').rjust(15, ' ')
				if writeLine_tf:
					if type == '2D':
						output_text += 'DN ' + ptID.ljust(12, ' ') + hzAngle + Dist + '\r\n'
					else:
						output_text += 'DM ' + ptID.ljust(12, ' ') + hzAngle + Dist + vtAngle + '  ' + format(instHT, '.4f') + '/' + format(targHT, '.4f') + '\r\n'
		output_text += 'DE #DB and DE information must be inserted where necessary before use...'
			
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
