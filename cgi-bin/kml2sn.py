#!/usr/bin/python
import cgi, cgitb, time, string

def dd2dms(dd):
	mspace = ''
	sspace = ''
	dd = float(dd)
	m = abs((dd-int(dd))) * 60
	s = (m-int(m)) * 60
	if m < 10:
		mspace = '0'
	if s < 10:
		sspace = '0'
	return str(int(dd)) + '-' + mspace + str(int(m)) + '-' + (sspace+str(s)).ljust(9, '0')[0:9]

form = cgi.FieldStorage()                 # parse form data
titleString = "<title>Converted Results</title>"
returnlink = 'http://support.microsurvey.com/convert/kmlms.html'
output_text = '#Converted ' + time.strftime('%B %d, %Y -- %I:%M:%S %p %Z') + '\r\n#KML to STAR*NET script by Jacob Wall -- helpdesk@microsurvey.com\r\n#Script Version 0.2 -- December 3, 2015\r\n\r\n'
	
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
	height = form.getvalue('height')
	if height == 'ellip':
		type = 'PH  '
	else:
		type = 'P  '
	desctags = form.getvalue('desctags')
	if desctags == 'yes':
		desctags = True
	else:
		desctags = False
	output_text += '.long neg\r\n\r\n'
	pos1 = 0
	pos2 = 0
	nullName = 0
	pos1 = text.find('<Placemark>', pos1)
	pos2 = text.find('</Placemark>', pos1)
	while pos1 > 0 and pos2 > 0:
		placeString = text[pos1:pos2]
		pos3 = placeString.find('<coordinates>')
		if pos3 > 0:
			pos4 = placeString.find('</coordinates>', pos3)
			coords = placeString[pos3+13:pos4].split(',')
			long = dd2dms(coords[0]).ljust(19, ' ')
			lat = dd2dms(coords[1]).ljust(18, ' ')
			elev = 'elev'
			elev = format(float(coords[2]), '.5f').rjust(12, ' ')
			pos3 = placeString.find('<name>')
			if pos3 > 0:
				pos4 = placeString.find('</name>', pos3)
				name = placeString[pos3+6:pos4]
			else:
				nullName += 1
				name = str(nullName)
			if desctags:
				pos3 = placeString.find('<description>')
				if pos3 > 0:
					pos4 = placeString.find('</description>', pos3)
					desc = "  '" + placeString[pos3+13:pos4]
				else:
					desc = ''
			else:
				desc = ''
			output_text += type + name.ljust(18, ' ') + lat + long + elev + "  * * *" + desc + '\r\n'
		pos1 = text.find('<Placemark>', pos1+1)
		pos2 = text.find('</Placemark>', pos1)	
		
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
