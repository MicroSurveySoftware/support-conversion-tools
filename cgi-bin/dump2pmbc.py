#!/usr/bin/python
import cgi, cgitb, time, string, math
import cgitb
cgitb.enable()

def get_point_list(ptstring):
	input_list = ptstring.split(',')
	output_list = []
	for i in range(len(input_list)):
		if len(input_list[i]) > 0:
			output_list.append(input_list[i])
	return output_list

form = cgi.FieldStorage()                 # parse form data
titleString = "<title>Converted Results</title>"
returnlink = 'http://support.microsurvey.com/convert/dumpms.html'
output_text = ''
header_text = 'Converted ' + time.strftime('%B %d, %Y -- %I:%M:%S %p %Z') + '<br>STAR*NET Dump to PMBC script by Jacob Wall -- helpdesk@microsurvey.com<br>Script Version 0.2 -- December 5, 2015'
	
print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<head>"
print titleString
print "<script src='/js/filesaver.js'></script>"
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
	filter_on = False
	if 'filter' in form:
		ptfilter = form.getvalue('filter')
		pt_list = get_point_list(ptfilter)
		if len(pt_list) > 0:
			filter_on = True
	text = form.getvalue('content')
	numFormat = form.getvalue('numDec')
	lines = text.splitlines()		
	for i in range(len(lines)):
		curLine = lines[i].split(',')
		write_line = True
		if curLine[0] == '"Name"':
			pass
		elif curLine[0] == '[Station_Station_Covariances]':
			break
		else:
			name = curLine[0][1:-1]
			x_stddev = float(curLine[12])
			y_stddev = float(curLine[11])
			Qxx = float(curLine[15])
			Qyy = float(curLine[14])
			Qxy = float(curLine[17])
			if x_stddev < 1e-07 and y_stddev < 1e-07 or Qxy == 0:
				output_text += name + ',' + format(float(curLine[2]), numFormat) + ',' + format(float(curLine[3]), numFormat) + ',' + format(float(curLine[4]), numFormat) + ',' + curLine[1][1:-1] + ',' + ',' + ',' + ',' + ',G\r\n'
			else:
				if filter_on:
					if not name in pt_list:
						write_line = False
				if write_line:
					t = math.atan(2*Qxy/(Qyy-Qxx))/2
					if Qxy < 0:
						if (Qyy - Qxx) < 0: # quadrant 3
							t += math.pi*1.5
						else: # quadrant 4
							t += (math.pi)*2
					else:
						if (Qyy - Qxx) < 0: # quadrant 2
							t += (math.pi)/2
						# else quadrant 1
					semi_major = math.sqrt(Qxx*(math.sin(t))**2+2*Qxy*math.cos(t)*math.sin(t)+Qyy*(math.cos(t))**2)*2.4477
					semi_minor = math.sqrt(Qxx*(math.cos(t))**2-2*Qxy*math.cos(t)*math.sin(t)+Qyy*(math.sin(t))**2)*2.4477				
					t = math.degrees(t)
					if t > 180:
						t = t-180
					z_stddev = float(curLine[13])*1.96
					output_text += name + ',' + format(float(curLine[2]), numFormat) + ',' + format(float(curLine[3]), numFormat) + ',' + format(float(curLine[4]), numFormat) + ',' + curLine[1][1:-1] + ',' + format(semi_major, numFormat) + ',' + format(semi_minor, numFormat) + ',' + format(t, '.4f') + ',' + format(z_stddev, numFormat) + ',S\r\n'

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
