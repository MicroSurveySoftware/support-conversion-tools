print (output_text|output)#!/usr/bin/python
import cgi, cgitb, time, string
import xml.etree.ElementTree as ET
import math
#below entry allows for online debugging, it should be removed for release:
#import cgitb
#cgitb.enable(format='text')



form = cgi.FieldStorage()                 # parse form data
titleString = "<title>Converted Results</title>"
returnlink = 'https://support.microsurvey.com/convert/xmlms.html'
output_text = '#Converted ' + time.strftime('%B %d, %Y -- %I:%M:%S %p %Z') + '\r\n#XML to STAR*NET script by MicroSurvey -- helpdesk@microsurvey.com\r\n#Script Version 1.1 -- December 13, 2018\r\n\r\n'

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
print "'>Return to the Input Page</a>&nbsp;&nbsp;&nbsp;<a class='button-2' href='https://helpdesk.microsurvey.com/index.php?/Knowledgebase/Article/View/1456'>Return to the Main Page</a></p>"
print "<textarea style='width:100%; border:1px solid #CCC; height:800px; padding:5px;'>"


hyphenwarn = 0

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
	
##def dd2dmsstring(dd):
##    mspace = ''
##    sspace = ''
##    m = abs((dd-int(dd))) * 60
##    s = (m-int(m)) * 60
##    if m < 10:
##        mspace = '0'
##    if s < 9.995: # which would round up to 10
##        sspace = '0'
##    s = s * 100
##    if s - int(s) > .5:
##        s = s + 1
##    #s = int (s)
##    return str(int(dd)) + '.' + mspace + str(int(m)) + (sspace+str(s))

def dd2dmsstring(dd):
    m = abs((dd-int(dd))) * 60
    s = (m-int(m)) * 60.0
    m = str(int(m))
    m = m.zfill(2)
    s = round(s,2)
    dec,s = math.modf(s)
    s = int(s)
    s = str(s)
    s = s.zfill(2)
    dec = dec * 100
    dec = int(dec)
    dec = str(dec)
    dec = dec.zfill(2)
    return str(int(dd)) + '.' + m + '' + s + '' + dec 

def reverse (horizAngle):
    horizAngle = dms2dd(horizAngle)
    horizAngle = horizAngle-180
    if horizAngle < 0:
        horizAngle = horizAngle+360
    horizAngle = dd2dmsstring(horizAngle)
    return horizAngle
    

def supplement (zenithAngle):
    zenithAngle = dms2dd (zenithAngle)
    zenithAngle = 360 - zenithAngle
    zenithAngle = dd2dmsstring (zenithAngle)
    return zenithAngle

if not 'content' in form:
	output_text = 'ERROR: No input provided...'
if not "</LandXML>" in form.getvalue('content'):
        output_text = 'ERROR: Not a valid XML...'

else:
    XMLtext = form.getvalue('content') 
    #XMLtext = input.read()
    coordorder = form.getvalue('coordorder') 

    pos = XMLtext.find('</LandXML>') # look for ending tag
    if pos<0:
        output_text += "Not a valid XML file"
    else:
        XMLtext = XMLtext[0:pos+10] # get all the text from beginning to end of ending tag
        root = ET.fromstring(XMLtext)

    InstrumentSetupdict = {'placeholder': '1'}
    RawObservationdict = {'placeholder': '1'}
    output = ""
    header = ""
    CgPoints = ""

#Find all necessary Header Information:
    header += ".order " + coordorder + "\n"
##    for headerunits in root.getiterator('{http://www.landxml.org/schema/LandXML-1.1}Metric'):
##        linearUnit = headerunits.attrib["linearUnit"]
##        linearUnit = "undefined"
##        if linearUnit == "meter":
##            linearUnit = "METERS"
##        if linearUnit == "USSurveyFoot":
##            linearUnit = "FEETUS"
##        if linearUnit == "IntFoot":
##            linearUnit = "FEETINT"
##        #stationName = units.attrib["stationName"]        
##        #instrumentHeight = units.attrib["instrumentHeight"]
##    header += ".units " + linearUnit + " DMS" + "\n"

#Find all CgPoints:
    lines=XMLtext.splitlines()
    for i in range(len(lines) - 1):
            curline = lines[i]
            if "</CgPoint>" in curline:
                name = curline[curline.find("<CgPoint name=")+15:curline.find('" ')]
                code = ""
                if 'code="' in curline:
                    code = curline[curline.find('code=')+6:curline.find('" role')]
                if "-" in name:
                    hyphenwarn = 1
                    name = name.replace("-","_",3)
                xyz = curline[curline.find('">')+2:curline.find("</CgPoint>")]
                xyz = xyz.split(" ")
                if len(xyz) == 2:
                    xyzne = xyz[0] +"\t" + xyz[1]
                    xyzen = xyz[1] +"\t" + xyz[0]   
                else:
                    xyzne = xyz[0] +"\t" + xyz[1] +"\t" + xyz[2]
                    xyzen = xyz[1] +"\t" + xyz[0] +"\t" + xyz[2]              
                if coordorder == "ne":
                    CgPoints += "#C" + "\t" + name + "\t" + xyzne +"\t" + "'" + code + "\n"
                if coordorder == "en":
                    CgPoints += "#C" + "\t" + name + "\t" + xyzen +"\t" + "'" + code + "\n"

#<CgPoint name="S2" oID="S2" timeStamp="2016-01-13T15:58:41">2247357.955000 377207.781000 10.000000</CgPoint>
#<CgPoint name="OBS_1" oID="OBS_1" code="ROADLEFT" role="measured" timeStamp="2017-10-16T15:26:12">10003.572386 10000.061750 102.770407</CgPoint>

#Find All Setup Records:
    for setup in root.getiterator('{http://www.landxml.org/schema/LandXML-1.1}InstrumentSetup'):
        InstrumentSetupid = setup.attrib["id"]
        stationName = setup.attrib["stationName"]        
        instrumentHeight = setup.attrib["instrumentHeight"]

        #Add each Setup to a dictionary of all Setups:
        Setupinfo = InstrumentSetupid,stationName,instrumentHeight
        InstrumentSetupdict[InstrumentSetupid] = Setupinfo



    #Find all Raw Observations:
    for rawobs in root.getiterator('{http://www.landxml.org/schema/LandXML-1.1}RawObservation'):
        comment = ""
        if 'horizDistance' in rawobs.attrib:
            horizDistance = rawobs.attrib["horizDistance"]
        targetHeight = rawobs.attrib["targetHeight"]
        horizAngle = rawobs.attrib["horizAngle"]
        zenithAngle = rawobs.attrib["zenithAngle"]
        setupID = rawobs.attrib["setupID"]
        #Need to use this attribute for cases where normalization required
        directFace = rawobs.attrib["directFace"]
        purpose = rawobs.attrib["purpose"]
        timeStamp = rawobs.attrib["timeStamp"]
##        if directFace == "false":
##            horizAngle = reverse(horizAngle)
##            zenithAngle = supplement(zenithAngle)
##            comment = "#F2 observation Normalized"

        #find the TargetPoint which is a child of the rawObservation section
        TargetPoint = rawobs.find('{http://www.landxml.org/schema/LandXML-1.1}TargetPoint')
        TargetPoint = TargetPoint.attrib["name"]
        #if "@" in TargetPoint:
        #   TargetPoint = TargetPoint[0:TargetPoint.find("@")]
        if 'slopeDistance' in rawobs.attrib:
            slopeDistance = rawobs.attrib["slopeDistance"]
        else:
            slopeDistance = "?         "
        HI = InstrumentSetupdict[setupID][2]

        #Add relevant attributes from each rawobservation to a raw observations dictionary:
        #Dictionary uses concatenated setupID and TargetPoint as the key:
        Rawobservationdictentry = TargetPoint,horizAngle,slopeDistance,zenithAngle,HI,targetHeight,comment
        ID = setupID+TargetPoint
        RawObservationdict[ID] = Rawobservationdictentry
        #print Rawobservationdictentry


    #Now create a direction set for each setup record:
    for setup2 in root.getiterator('{http://www.landxml.org/schema/LandXML-1.1}InstrumentSetup'):
        InstrumentSetupid = setup2.attrib["stationName"]
        StationName = setup2.attrib["id"]
        output += "\n" + "\n" + "# InstrumentSetup id= " + StationName + "\n"
        output += "DB" + "\t" + InstrumentSetupid + "\n"

        #iterates through all raw observations and writes a DM line if the setupid matches the Station Name from the setup lines
        for rawobs2 in root.getiterator('{http://www.landxml.org/schema/LandXML-1.1}RawObservation'):
            setupID = rawobs2.attrib["setupID"]
            TargetPoint = rawobs2.find('{http://www.landxml.org/schema/LandXML-1.1}TargetPoint')
            TargetPointname = TargetPoint.attrib["name"]
            #if "@" in TargetPointname:
            #   TargetPointname = TargetPointname[0:TargetPointname.find("@")]

            #Finds raw observation information from Dictionary:
            searchstring = setupID+TargetPointname
            if setupID == StationName:
                DM = RawObservationdict[searchstring]
                TargetPointname = RawObservationdict[searchstring][0]
                if "@" in TargetPointname:
                   TargetPointname = TargetPointname[0:TargetPointname.find("@")]
                DM = "DM " + "\t" + TargetPointname + "\t" + RawObservationdict[searchstring][1] + "\t" + RawObservationdict[searchstring][2] + "\t" + RawObservationdict[searchstring][3] + "\t" + RawObservationdict[searchstring][4] + "/" + RawObservationdict[searchstring][5]+ "\t" + RawObservationdict[searchstring][6]

                output += DM + "\n"


        output += "DE"

    output_text += header + "\n" + "\n"
    output_text += CgPoints + "\n" + "\n"
    if hyphenwarn == 1:
        output_text += "#Warning: hyphens were found in at least one point ID and replaced with '_' in the CgPoints section.\n#The traverse information below will require manual correction."
    output_text += output



# dO NOT MODIFY BELOW:
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
