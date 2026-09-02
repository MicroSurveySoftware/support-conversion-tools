#!/usr/bin/python
import cgi, cgitb, time, string

form = cgi.FieldStorage()                 # parse form data
titleString = "<title>Converted Results</title>"
returnlink = 'http://support.microsurvey.com/convert/codingms.html'
output_text = ''
header_text = 'Converted ' + time.strftime('%B %d, %Y -- %I:%M:%S %p %Z') + '<br>Line Coding to XYZ Coding script by Jacob Wall -- helpdesk@microsurvey.com<br>Script Version 0.1 -- December 8, 2015'

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
print "'>Return to the Input Page</a>&nbsp;&nbsp;&nbsp;<a class='button-2' href='http://helpdesk.microsurvey.com/index.php?/Knowledgebase/Article/View/1456'>Return to the Main Page</a></p><p>"
print header_text
print "</p><textarea id='output' style='width:100%; border:1px solid #CCC; height:800px; padding:5px;'>"

if (not 'content' in form or not 'begCode' in form or not 'endCode' in form or not 'closeCode' in form):
	output_text = 'ERROR: Insufficient Input...'
else:
	delimiter = form.getvalue('delimiter')
	if delimiter == 'comma':
		char = ','
	elif delimiter == 'space':
		char = ' '
	else:
		char = '\t'
	code_pos = int(form.getvalue('codePos'))-1
	begLine_code = form.getvalue('begCode')
	begLine_len = len(begLine_code)
	if form.getvalue('begPos') == 'lead1':
		begLine_lead = True
	else:
		begLine_lead = False
	endLine_code = form.getvalue('endCode')
	endLine_len = len(endLine_code)
	if form.getvalue('endPos') == 'lead2':
		endLine_lead = True
	else:
		endLine_lead = False
	clsLine_code = form.getvalue('closeCode')
	clsLine_len = len(clsLine_code)
	if form.getvalue('closePos') == 'lead3':
		clsLine_lead = True
	else:
		clsLine_lead = False
	text = form.getvalue('content')
	lines = text.splitlines()
	activeLineList = []
	for i in range(len(lines)):
		curLine = lines[i].split(char)
		if len(curLine) < code_pos:
			output_text += lines[i] + '\r\n'
		else:
			curCode = curLine[code_pos].rstrip(' ')
			if begLine_lead:
				testString1 = curCode[:begLine_len]
			else:
				testString1 = curCode[-begLine_len:]
			if endLine_lead:
				testString2 = curCode[:endLine_len]
			else:
				testString2 = curCode[-endLine_len:]
			if clsLine_lead:
				testString3 = curCode[:clsLine_len]
			else:
				testString3 = curCode[-clsLine_len:]
			if testString1 == begLine_code:
				if begLine_lead:
					desc = curCode[begLine_len:]
				else:
					desc = curCode[:-begLine_len]
				if not desc in activeLineList:
					activeLineList.append(desc)
				output_text += lines[i].replace(curCode, 'Z' + desc) + '\r\n'		
			elif testString2 == endLine_code:
				if endLine_lead:
					desc = curCode[endLine_len:]
				else:
					desc = curCode[:-endLine_len]
				if desc in activeLineList:
					activeLineList.remove(desc)
				output_text += lines[i].replace(curCode, desc) + '\r\n'
			elif testString3 == clsLine_code:
				if clsLine_lead:
					desc = curCode[clsLine_len:]
				else:
					desc = curCode[:-clsLine_len]
				if desc in activeLineList:
					activeLineList.remove(desc)
				output_text += lines[i].replace(curCode, '.' + desc) + '\r\n'
			else:
				desc = curCode
				if desc in activeLineList:
					output_text += lines[i].replace(curCode, 'Z' + desc) + '\r\n'
				else:
					output_text += lines[i] + '\r\n'

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
