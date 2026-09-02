#!/usr/bin/python
# -*- coding: cp1252 -*-
import cgi, cgitb, time, string
import xml.etree.ElementTree as ET
#below entry allows for online debugging, it should be removed for release:
import cgitb
import math
cgitb.enable()




form = cgi.FieldStorage()                 # parse form data
titleString = "<title>Instrument Settings</title>"
returnlink = 'http://support.microsurvey.com/convert/instrumentsettings.html'
output_text = 'Created ' + time.strftime('%B %d, %Y -- %I:%M:%S %p %Z') + '<br />Instrument Settings script by MicroSurvey -- helpdesk@MicroSurvey.com<br /> Script Version 1.2 -- 5 23, 2025<br />'

#print "Content-Type: text/plain"	
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
print "'>Return to the Input Page</a>&nbsp;&nbsp;&nbsp;<a class='button-2' href='https://helpdesk.microsurvey.com/article/1339'>Return to the Main Page</a></p>"
#print "<textarea style='width:100%; border:1px solid #CCC; height:800px; padding:5px;'>"

# Insert function definitions below:

def dms2dd(dms):
    dms = float (dms)
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
    s = s * 100
    if s - int(s) > .5:
        s = s + 1
    s = int (s)
    return str(int(dd)) + '.' + mspace + str(int(m)) + (sspace+str(s))

def reverse (horizAngle):
    horizAngle = dms2dd(horizAngle)
    horizAngle = horizAngle-180
    horizAngle = dd2dmsstring(horizAngle)
    return horizAngle
    

def supplement (zenithAngle):
    zenithAngle = dms2dd (zenithAngle)
    zenithAngle = 360 - zenithAngle
    zenithAngle = dd2dmsstring (zenithAngle)
    return zenithAngle

def elevdistconstppm (zenith,deviceconstant,ppm):
	zenith = zenith / 3600
	zenith = math.radians(zenith)
	elevdistconst = math.sin(zenith) * deviceconstant
	elevdistppm = math.sin(zenith) * 1000000
	return elevdistconst,elevdistppm
	
def elevdistconstppmgons (zenith,deviceconstant,ppm):
	zenith = zenith / 1000
	zenith = zenith / 63.6619772367581
	elevdistconst = math.sin(zenith) * deviceconstant
	elevdistppm = math.sin(zenith) * 1000000
	return elevdistconst,elevdistppm
	

#Reads form data passed from webpage and stores it as object "content"


content = form.getvalue('content')
#content = input.read()

au = form.getvalue('formvalue_au')
din = form.getvalue('formvalue_din')
sqrtopt = form.getvalue ('formvalue_sqrt')
edm = form.getvalue('formvalue_edm')
ppm = form.getvalue('formvalue_ppm')
sets = form.getvalue('formvalue_pulldown_sets')
azimuth = form.getvalue('formvalue_az')
instctr = form.getvalue('formvalue_instctr')
trgctr = form.getvalue('formvalue_trgctr')
trgatr = form.getvalue('formvalue_trgatr')
vert = form.getvalue('formvalue_vert')

    
#Insert script below:

if sqrtopt == "yes":
    sqrt = 1.414213562
else:
    sqrt = 1

din = float(din)* sqrt
edm = float(edm)
sets = float(sets)
trgctr = float (trgctr)
trgatr = float (trgatr)
deviceconstant = edm / math.sqrt(sets)
distanceppm = float(ppm)
angle = 2*din / math.sqrt(2 * sets)
direction = din / math.sqrt(sets)
azimuth = float(azimuth)
zenith = 2 * din /math.sqrt(sets)
delta_elev_std_err = 1.00
delta_elev_ppm = 1.00
vert = float (vert)

if au == "degrees":
        elevdistconst = elevdistconstppm(zenith,deviceconstant,ppm)
        elevdistppm = elevdistconst[1]
        elevdistconst = elevdistconst[0]
elif au == "gons":
        elevdistconst = elevdistconstppmgons(zenith,deviceconstant,ppm)
        elevdistppm = elevdistconst[1]
        elevdistconst = elevdistconst[0]	
        

horizinst = float(instctr)
horiztarg = math.sqrt(trgctr*trgctr+trgatr*trgatr)



#Round Values before output:

deviceconstant = '%.6f' % round(deviceconstant,6)
distanceppm = '%.3f' % round(distanceppm,3)

angle = '%.6f' % round(angle,6)
direction = '%.6f' % round(direction,6)
azimuth = '%.6f' % round(azimuth,6)
#
zenith = '%.6f' % round(zenith,6)
elevdistconst = '%.6f' % round(elevdistconst,6)
elevdistppm = '%.6f' % round(elevdistppm,3)
#
horizinst = '%.6f' % round(horizinst,6)
horiztarg = '%.6f' % round(horiztarg,6)
vert = '%.6f' % round(vert,6)



output_text += "<br><br><strong>Conventional:</strong><br>\n"
output_text += 'Distance Constant:;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' + str(deviceconstant) + "<br>\n"
output_text += "Distance PPM:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + str(distanceppm) + "<br><br>\n"
output_text += "Angle:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + str(angle) + "<br>\n"
output_text += "Direction:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + str(direction) + "<br>\n"
output_text += "Azimuth/Bearing:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + str(azimuth) + "<br><br>\n"
output_text += "Zenith:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + str(zenith) + "<br>\n"
output_text += "Elevation Diff Constant:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; " + str(elevdistconst) + "<br>\n"
output_text += "Elevation Diff PPM:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + str(elevdistppm) + "<br><br>\n"
output_text += "<strong>Centering Errors:</strong><br>\n"
output_text += "&nbsp;&nbsp;&nbsp;Horiz Instr:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + str(horizinst) + "<br>\n"
output_text += "&nbsp;&nbsp;&nbsp;Horiz Target:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + str(horiztarg) + "<br>\n"
output_text += "&nbsp;&nbsp;&nbsp;Vertical:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + str(vert) + "<br>\n"


output_text += "<br><br><br>If you wish to add this result to your instrument library you may paste the entry below into Company.def file<br>\n"
output_text += "Open the Company.def file found in: C:\ProgramData\MicroSurvey\StarNet\V* with a text editor.<br>\n"
output_text += "Paste the entry at the bottom of the file, modify the instrument_name and azimuth_std_err section and save.<br><br><br>\n"


output_text += '<font face="courier">' + "#<br></font>\n"
output_text += '<font face="courier">' + "instrument_name&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;placeholder name&nbsp;#<strong>#Modify before use</strong><br></font>\n"
output_text += '<font face="courier">' + "distance_std_err&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + str(deviceconstant) + "<br></font>\n"
output_text += '<font face="courier">' + "edm_ppm&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + str(distanceppm) + "<br></font>\n"
output_text += '<font face="courier">' + "angle_std_err&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + str(angle) + "<br></font>\n"
output_text += '<font face="courier">' + "direction_std_err&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + str(direction) + "<br></font>\n"
output_text += '<font face="courier">' + "azimuth_std_err&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + str(azimuth) + "<br></font>\n"
output_text += '<font face="courier">' + "zenith_std_err&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + str(zenith) + "<br></font>\n"
output_text += '<font face="courier">' + "delta_elev_std_err&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + str(elevdistconst) + "<br></font>\n"
output_text += '<font face="courier">' + "delta_elev_ppm&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + str(elevdistppm) + "<br></font>\n"
output_text += '<font face="courier">' + "instrument_centering_error&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + str(horizinst) + "<br></font>\n"
output_text += '<font face="courier">' + "target_centering_error&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + str(horiztarg) + "<br></font>\n"
output_text += '<font face="courier">' + "vertical_centering_error&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + str(vert) + "<br></font>\n"


###
##instrument_name                JJ
##note                           Note goes here
##distance_std_err               0.0091440183
##edm_ppm                        0.0000000000
##angle_std_err                  4.0000000000
##direction_std_err              3.0000000000
##azimuth_std_err                4.0000000000
##zenith_std_err                 10.0000000000
##delta_elev_std_err             0.0152400305
##delta_elev_ppm                 0.0000000000
##instrument_centering_error     0.0000000000
##target_centering_error         0.0000000000
##vertical_centering_error       0.0000000000




# dO NOT MODIFY BELOW:
print cgi.escape(output_text, quote=True)
print "<p>Please contact MicroSurvey at helpdesk@microsurvey.com if results are not as expected or contain errors.</p>\n"
print '<a href="https://helpdesk.microsurvey.com/article/1293">See this article for details of computations made.</a>'  
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




