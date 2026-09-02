#!/usr/bin/python
import cgi, cgitb, time, string
import xml.etree.ElementTree as ET
import sets
#below entry allows for online debugging, it should be removed for release:
import cgitb
import sys
#cgitb.enable(format='text')



form = cgi.FieldStorage()                 # parse form data
titleString = "<title>Converted Results</title>"
returnlink = 'https://support.microsurvey.com/convert/tdef2sn.html'
output_text = '#Converted ' + time.strftime('%B %d, %Y -- %I:%M:%S %p %Z') + '\r\n#TDEF to STAR*NET (Conventional) by MicroSurvey -- helpdesk@MicroSurvey.com\r\n#Script Version 1.3 -- January 16, 2021\r\n\r\n'

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

# Checks if input was empty:

if not 'content' in form:
	output_text = 'ERROR: No input provided...'

#Reads form data passed from webpage and stores it as object "content"

else:
    TDEF = form.getvalue('content')
    linunit = form.getvalue('formvalue_linear')
    record = form.getvalue('formvalue_record')
    ss = form.getvalue('formvalue_pulldown')
    
    #content = input.read()

    
#Insert script below:


########Tkinter dialog prompts to select input file###################

#import tkFileDialog

# Section below quells the extra Tkinter dialog:
##from Tkinter import Tk
##root = Tk()
##root.withdraw()

def dd2dmsstring(dd):
    dd = float(dd)
    mspace = ''
    sspace = ''
    d = int(dd)
    m = abs((dd-d)) * 60.0
    s = (m-int(m)) * 60.0
    if m < 10:
        mspace = '0'
    if s < 10:
        sspace = '0'
    s = '{0:.2f}'.format(s)
    if s == '60.00':
        s = 59.99
    return str(d) + '-' + mspace + str(int(m)) + '-' + sspace + str(s)


def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False


def dirset(TDEF,i,setupid,sep,unit,points):
    cont = True
    count = 0
    #extract at for DB line:
    at = TDEF[i].split(sep)[2]
    at = at.replace ("-","_")
    at = at.replace (" ","_")
    dset = "\n# Setup ID: " + setupid + "\n" + "DB " + at + "\n"
    while cont:
        count +=1
        curLine = TDEF[i]
        TerrObs = curLine.split(sep)
        at = TerrObs[2].replace ("-","_")
        at = at.replace (" ","_")
        fromto = TerrObs[4].replace ("-","_")
        fromto = fromto.replace (" ","_")
        if fromto in points.keys():
            desc = points[fromto]
        if TerrObs[5] != "?":
            ha = dd2dmsstring(TerrObs[5])
        else:
            ha = TerrObs[5]
        if TerrObs[7] != "?":
            ze = dd2dmsstring(TerrObs[7])
        else:
            ze = TerrObs[7]
        rawdist = TerrObs[9]
        offset = TerrObs[11]   
        if isfloat(rawdist):
            dist = str((float(rawdist) + (float(offset))*.001)*unit)
                        
        else:
            #print "rawdist " + rawdist + "   offset" + offset
            dist = "?" + rawdist + "dist or offset missing"

        hi = TerrObs[12]
        if isfloat(hi):
            hi = str(float(hi) * unit)
        ht = TerrObs[13]
        if isfloat(ht):
            ht = str(float(ht) * unit)
        newline = "DM " + fromto.ljust(12) + " " + ha.ljust(18)  + " " + dist.ljust(18) + " " +  ze.ljust(18) + " " + hi + "/" + ht + "   '" + desc + "\n"
        if "?" in newline:
            newline = "#" + newline
            count = count -1
        dset += newline
        i +=1
        curLine = TDEF[i]
        #The test below must be for "\r" for online version
        if curLine == "\r":
            break
        TerrObs = curLine.split(sep)
        nextsetupid = TerrObs[16]
        if nextsetupid != setupid:
            cont = False

    if count == 1:
        dset = "\n# Setup ID: " + setupid + "\n" + "DV " + at + "-" + fromto.ljust(12) + "\t" + dist + "\t" +  ze + "\t" + hi + "/" + ht + "   '" + desc + "\n"
    if count > 1:
        dset += "DE\n\n"
    return(dset,i-1)

def mline(TDEF,i,setupid,sep,unit,ss,redundants,points):
    cont = True
    count = 0
    #extract at for M lines for this setup:
    at = TDEF[i].split(sep)[2]
    at = at.replace ("-","_")
    at = at.replace (" ","_")
    mlines = "\n# Setup ID: " + setupid + "\n"
    while cont:
        count +=1
        curLine = TDEF[i]
        TerrObs = curLine.split(sep)
        at = TerrObs[2].replace ("-","_")
        at = at.replace (" ","_")
        fromfrom = TerrObs[3].replace ("-","_")
        fromfrom = fromfrom.replace (" ","_")
        fromto = TerrObs[4].replace ("-","_")
        fromto = fromto.replace (" ","_")
        if fromto in points.keys():
            desc = points[fromto]
        else:
            desc = ""
        if TerrObs[5] != "?":
            ha = dd2dmsstring(TerrObs[5])
        else:
            ha = TerrObs[5]
        if TerrObs[7] != "?":
            ze = dd2dmsstring(TerrObs[7])
        else:
            ze = TerrObs[7]
        rawdist = TerrObs[9]
        offset = TerrObs[11]   
        if isfloat(rawdist):
            dist = str((float(rawdist) + (float(offset))*.001)*unit)
                        
        else:
            #print "rawdist " + rawdist + "   offset" + offset
            dist = "?" + rawdist + "dist or offset missing"

        hi = TerrObs[12]
        if isfloat(hi):
            hi = str(float(hi) * unit)
        ht = TerrObs[13]
        if isfloat(ht):
            ht = str(float(ht) * unit)
        if ss == "y" and fromto not in redundants:
            newline = "SS " + at + "-" + fromfrom + "-" + fromto + "      " + ha.ljust(18)  + " " + dist.ljust(18) + " " +  ze.ljust(18) + " " + hi + "/" + ht + "   '" + desc + "\n"
        else:
            newline = "M  " + at + "-" + fromfrom + "-" + fromto + "      " + ha.ljust(18)  + " " + dist.ljust(18) + " " +  ze.ljust(18) + " " + hi + "/" + ht + "   '" + desc + "\n"
        if fromfrom == fromto:
            newline = "DV " + at + "-" + fromto + "            " + dist.ljust(18) + " " +  ze.ljust(18) + " " + hi + "/" + ht + "   '" + desc + "\n"
        if "?" in newline:
            newline = "#" + newline
            count = count -1
        mlines += newline
        i +=1
        curLine = TDEF[i]
        #The test below must be for "\r" for online version
        if curLine == "\r":
            break
        TerrObs = curLine.split(sep)
        nextsetupid = TerrObs[16]
        if nextsetupid != setupid:
            cont = False

    if count == 1:
        dset = "\n# Setup ID: " + setupid + "\n" + "DV " + at + "-" + fromto.ljust(12) + "\t" + dist + "\t" +  ze + "\t" + hi + "/" + ht  + "   '" + desc +  "\n"
        #print mlines
    if count > 1:
        mlines += "\n"
    return(mlines,i-1)
            
#Scans all Terrestrial observations and adds all points that were
#backsighted, occupied or foresighted more than once to
#a list named "redundants"
def redundant(TDEF,i,sep,redundants):
    cont = True
    sslist = [""]
    while cont:
        curLine = TDEF[i]
        TerrObs = curLine.split(sep)
        at = TerrObs[2].replace ("-","_")
        at = at.replace (" ","_")
        fromfrom = TerrObs[3].replace ("-","_")
        fromfrom = fromfrom.replace (" ","_")
        fromto = TerrObs[4].replace ("-","_")
        fromto = fromto.replace (" ","_")
        if at not in redundants:
            redundants.append(at)
        if fromfrom not in redundants:
            redundants.append(fromfrom)
        if fromto in sslist:
            if fromto not in redundants:
                redundants.append(fromto)
        sslist.append(fromto)
        i += 1
        curLine = TDEF[i]
        #The test below must be for "\r" for online version
        if curLine == "\r":
            cont = False
    return(redundants)

#initialize variables    

header = '''#NOTE: Station names with spaces or "-" have been replaced with "_"\n'''
output = "\n"
sep = ':'
i = 0
azimuths = "#Azimuths listed in TDEF file:\n\n"
redundants = [""]



#options from html (placeholder):
#linunit = "FeetUS"
if linunit == "FeetUS":
    unit = 3.2808333333333337
    unitstring = "FeetUS"
if linunit == "Meters":
    unit = 1
    unitstring = "Meters"
if linunit == "Feet":
    unit = 3.280839895
    unitstring = "FeetInt"
header += "\n#User Options\n.Units " + unitstring
header += "\n.Units DMS\n.Order AtFromTo\n.Sep -\n.Delta Off\n.3D"
header += "\n\n#Header Notes"

#Browse to Trimble data Exchange File

##filename = tkFileDialog.askopenfilename(filetypes=[("TDEF file","*.asc")])
##text = open(filename,'r')
##
###Creates a list of each line in the TDEF file
###TDEF = text.readlines()
##text.close()

TDEF=TDEF.split("\n")
points = {"ID":"desc"}

while i < len(TDEF):
    #output += str(i)
    curLine = TDEF[i]
    #output += curLine

    

#Populate variables from header
    ProjName = ProjCoordinateSystem = ProjCoordinateZone = ProjGeoidModel = "?"
    #if curLine[:10] == "Separator=":
        #sep = curLine[10:].strip("\n")
        #output += "\n.Sep " + sep
    if curLine[:9] == "ProjName=":
        ProjName = curLine[9:].strip("\n")
        header += "\n#TBC Project Name: " + ProjName
    if curLine[:21] == "ProjCoordinateSystem=":
        ProjCoordinateSystem = curLine[21:].strip("\n")
        header += "\n#TBC Project Coordinate System: " + ProjCoordinateSystem
    if curLine[:19] == "ProjCoordinateZone=":
        ProjCoordinateZone = curLine[19:].strip("\n")
        header += "\n#TBC Project Coordinate Zone: " + ProjCoordinateZone
    if curLine[:15] == "ProjGeoidModel=":
        ProjGeoidModel = curLine[15:].strip("\n")
        header += "\n#TBC Project Geoid Model: " + ProjGeoidModel + "\n\n"

#Populate from coordinates section and add to output
    if curLine [:8] == "Station=":
        Station = curLine.split(sep)
        Stat = Station[2]
        Stat = Stat.replace ("-","_")
        Stat = Stat.replace (" ","_")
        Statprint = Stat.ljust(12)
        prefix = ""
        if Station[6] == "?":
            prefix = "#"
            Y = "0.0"
        else:
            Y = str(float(Station[6])*unit)
        Yprint = Y.ljust(16)
        if Station[7] == "?":
            prefix = "#"
            X = "0.0"
        else:
            X = str(float(Station[7])*unit)
        Xprint = X.ljust(16)
        if Station[8] == "?":
            prefix = "#"
            Z = "0.0"
        else:
            Z = str(float(Station[8])*unit)
        Zprint = Z.ljust(16)
        desc = Station[12]
        if desc == "?":
            desc = ""
        Stat = Statprint.rstrip()
        points[Stat] = desc
        
        output += prefix + "C " + Statprint + " " + Yprint + " " + Xprint + " " + Zprint + " '" + desc + "\n"

#Identify all redundant stations in a list named redundants
    if curLine[:8] == "TerrObs=" and len(redundants) == 1:
        redundants = redundant(TDEF,i,sep,redundants)
     
#Populate direction sets or mlines from Terrestrial observations section
    if curLine[:8] == "TerrObs=":
        TerrObs = curLine.split(sep)
        setupid = TerrObs[16]
        #send line to dirset function whenever a new Setup ID is encountered
        if record == "dsets":
            dset = dirset(TDEF,i,setupid,sep,unit,points)
            output += dset[0]
        #send line to mlines function whenever a new Setup ID is encountered
        if record == "mlines":
            mlines = mline(TDEF,i,setupid,sep,unit,ss,redundants,points)
            output += mlines[0]
            dset  = mlines
        i = dset[1]
    i = i+1
    
#Populate azimuths list from Azimuth section

    if curLine[:8] == "Azimuth=":
        Azimuth = curLine.split(sep)
        azfrom = Azimuth[2]
        azto = Azimuth[3]
        fromto = "#B " + azfrom + "-" + azto
        fromto = fromto.ljust(20)
        az = dd2dmsstring(Azimuth[4])
        azimuths += fromto + az + "\n"       






#Loops through each item in list starting at 0 and ending at the last item
#Copies each line, then adds it to "output" line by line



#Closes the document
#Create a STAR*NET dat file of contents
#diagnostics = "\n\n\nSee below for redundants:\n" + str(redundants) + "\n\n\n"

output_text += header + azimuths + output
##fileout = open('output.dat','w')
##fileout.write(output)
##fileout.close()  
    



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
