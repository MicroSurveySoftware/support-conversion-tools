#!/usr/bin/python
import cgi, cgitb, time, string
import xml.etree.ElementTree as ET
#below entry allows for online debugging, it should be removed for release:
import cgitb
import sys
import math
import os
import datetime
cgitb.enable(format = "text")
errorstate = "False"



form = cgi.FieldStorage()                 # parse form data
titleString = "<title>Converted Results</title>"
returnlink = 'https://support.microsurvey.com/convert/template.html'
output_text = '#Converted ' + time.strftime('%B %d, %Y -- %I:%M:%S %p %Z') + '\r\n#Listing2trav script by MicroSurvey -- helpdesk@MicroSurvey.com\r\n#Script Version 1.0 -- 01 29, 2023\r\n\r\n'

#print "Content-Type: text/plain"       
print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<head>"
print titleString
print "<style>"
print "body {font-family:Arial, Helvetica, sans-serif; color:#767676; background:#f5f5f5; font-size:12px; line-height:18px;     margin:0;}"
print "html, body {height:100%;}"
print "html {min-width:960px; overflow-y:scroll;}"
print ".container {width:960px; margin:0 auto; position:relative; overflow:hidden;}"
print ".button-2 {line-height:29px; font-size:12px;     color:#252525; background:#ededed; border:1px solid #c4c4c4; padding:5px 15px 5px 15px;}"
print ".button-2:hover {background-color:#125A5A; color:#fff;}"
print "a {color:#F24C15; outline:none; cursor:pointer; text-decoration:none;}"
print "</style"
print "</head>"
print "<body>"
print "<div class='container'>"
print "<p style='text-align:center;'><a class='button-2' href='"
print returnlink
print "'>Return to the Input Page</a>&nbsp;&nbsp;&nbsp;<a class='button-2' href='http://support.microsurvey.com/converters.html'>Return to the Main Page</a></p>"
print "<textarea style='width:100%; border:1px solid #CCC; height:800px; padding:5px;'>"


#Determine Angular units
def angunits(listing):
    for line in listing:
        if "Project Units   " in line:
            if "; GONS" in line:
                return "GONS"
            else:
                return "DMS"

#Determine Distance units
def distunits(listing):
    for line in listing:
        if "Project Units   " in line:
            distunits = str(line.split(";")[0])
            distunits = distunits.split(':')[1]
            return distunits
        

# Insert function definitions below:
#Extract a list of lines from the summary of unadjusted angles and distances
def obslist(listing,liststring,searchstring,offset):
    for i in range(0,len(listing)):
        if searchstring in listing[i]:
            start = i + offset
            for j in range(start,len(listing)):
                if len(listing[j]) <= 2:
                    end = j
                    list = listing[start:end]
                    return list

#Extract a list of lines from the summary of unadjusted directions
def dirlist(listing,liststring,searchstring,offset):
    for i in range(0,len(listing)):
        if searchstring in listing[i]:
            start = i + offset
            for j in range(start,len(listing)):
                if "Number of" in listing[j+1] or "Adjusted" in listing[j+1] or listing[j]=='\x0c\n':
                    end = j
                    list = listing[start:end]
                    return list

#Create a list of lists consisting of [at,to,dist,stdev] for each distance
def distvals(distlist,comments):
    distvals = []
    for i in range(0,len(distlist)):
        parts = distlist[i].rstrip('\n').split()
        fro = parts[0]
        to = parts[1]
        dist = parts[2]
        stdev = parts[3]
        if stdev != "FREE":
            newline = [fro,to,dist,stdev]
            distvals.append(newline)
        else:
             comments += "#Distance  " + fro + "-" + to + "  " + parts[2] + " " + stdev + " excluded\n"
    return distvals,comments

#this routine returns a float radians value from either a DD-MM-SS string or a decimal gons string
def dms2rad(dms):
    if angunits == "GONS":
        rad = float(dms) * 0.015708
        if '*' in dms:
            rad += -3.14159265359
            if rad < 0:
                rad += 6.28318530718
        return rad       
    mult = 1
    if dms[0] == '-':
        dms = dms.lstrip('-')
        mult = -1
    dmsparts = dms.split('-')
    d = float(dmsparts[0])
    if '*' in dms:
        d += -180
        if d < 0:
            d += 360
    m = float(dmsparts[1]) / 60
    s = float(dmsparts[2]) /3600
    dec = d + m + s
    rad = dec  / 180 * math.pi
    rad = rad * mult
    return rad

#this routine outputs a DD-MM-SS string rounded to nearest second, or a gons output that is unrounded
def rad2dmsstring(rad):
    if angunits == "GONS":
        dms = float(rad) / 0.015708
        return str(dms)    
    dd = float(rad) * 180 / math.pi
    d = int(dd)
    mm = (dd-d) * 60.0
    m = int(mm)
    s = (mm-m) * 60.0
    if s - int(s) < 0.5:
        s = int(s)
    else:
        s = int(s+1)
    d = str(d)
    m = str(m).rjust(2,"0")
    s = str(s).rjust(2,"0")
    if s == '60':
        s = "00"
        m = str(int(m) + 1).rjust(2,"0")
    if m == '60':
        m = '00'
        d= str(int(d) + 1)
    if d == "360":
        d = "0"
    return d + "-" + m.lstrip('-') + "-" + s.lstrip('-')

#Create a list of lists consisting of [at,from,to,radianangle,stdev] for each angle
def angvals(angleslist,comments):
    angvals = []
    for i in range(0,len(angleslist)):
        parts = angleslist[i].rstrip('\n').split()
        at = parts[0]
        fro = parts[1]
        to = parts[2]
        ang = dms2rad(parts[3])
        stdev = parts[4]
        if stdev != "FREE":
            newline = [at,fro,to,ang,stdev]
            angvals.append(newline)
        else:
             comments += "#Angle     " + fro + "-" + to + "  " + parts[3] + " " + stdev + " excluded\n"
    return angvals,comments

#Check if a string can be turned into a float:
def isnum(s):
    try:
        float(s)
    except ValueError:
        return False
    else:
        return True

#Iteratively computes all implied angles from a direction set assuming first line to be the backsight,
# ...and then assuming the second line to be the backsight etc...
#Each result is added to angvals
def additlangs(setlist,angvalslist):
    for i in range(len(setlist)):
        for j in range(1,len(setlist)):
            fro = setlist[0][1]
            at = setlist[0][0]
            to = setlist[j][1]
            ang = float(setlist[j][2]) - float(setlist[0][2])
            if ang <0.0:
                ang = ang + 2*math.pi
            if ang > 2*math.pi:
                ang = ang - 2*math.pi
            stdevfro = setlist[0][3]
            stdevto = setlist[j][3]
            if isnum(stdevfro) == True and isnum(stdevto) == True:
                stdev = math.sqrt(float(stdevfro)**2 + float(stdevto)**2)
            else:
                stdev = "FREE"
            newline = [at,fro,to,ang,stdev]
            angvalslist.append(newline)
        shortened = setlist[1:]
        setlist = shortened
    return angvalslist

#Search distvalslist for all possible matches for at,to and return all [dist,stdev]
def alldist(distvalslist, fro, to):
    distall = []
    for i in range(len(distvalslist)):
        if fro == distvalslist[i][0]:
            if to == distvalslist[i][1]:
                distall.append([distvalslist[i][2],distvalslist[i][3]])
    return distall
            

#Receive a list of [dist,stdev] and return [averagedistance,propogated stdev]
def avgdist(distall):
    dist = 0.0
    stdevtot = 0.0
    for i in range(len(distall)):
        dist += float(distall[i][0])
        stdevtot += float((distall[i][1]))
    stdevprop = (stdevtot/len(distall)) / math.sqrt(float(len(distall)))
    stdevpropstring = str(stdevprop)
    distavg = dist/float(len(distall))
    distavg = round(distavg,4)  
    distavgstring = str(distavg)     
    distavg = [fro,to,distavgstring,stdevpropstring,i+1]      
    return distavg

#Search angvalslist for all possible matches for at,from,to and return all [angs,stdev]
def allangs(angvalslist, at, fro, to):
    angsall = []
    for i in range(len(angvalslist)):
        if at == angvalslist[i][0]:
            if fro == angvalslist[i][1]:
                if to == angvalslist[i][2]:
                    angsall.append([angvalslist[i][3],angvalslist[i][4]])
    return angsall

#Receive a list of [dist,stdev] and return [averagedistance,propogated stdev]
def avgangs(angsall):
    angs = 0.0
    stdevtot = 0.0
    for i in range(len(angsall)):
        angs += float(angsall[i][0])
        stdevtot += float((angsall[i][1]))
    stdevprop = (stdevtot/len(angsall)) / math.sqrt(float(len(angsall)))
    stdevpropstring = str(stdevprop)
    angsavg = angs/float(len(angsall))
    angsavgstring = str(angsavg)     
    angsavg = [at,fro,to,angsavgstring,stdevpropstring,i+1]      
    return angsavg

#Search distvals list given "at,to" and returns "dist,stdev"
def finddistval(avgdistvalslist,at,to,rev):
    dist = "?"
    stdev = "&"
    count = 0
    for i in range (len(avgdistvalslist)):
        if at == avgdistvalslist[i][0]:
            if to == avgdistvalslist[i][1]:
                dist = avgdistvalslist[i][2]
                stdev = str(round(float(avgdistvalslist[i][3]),4))
                count = avgdistvalslist[i][4]
                return dist,stdev,count
    #If an at-to match is not found, routine searches for a to-at match:
    if rev == "yes" and dist == '?':
        for i in range (len(avgdistvalslist)):
            if to == avgdistvalslist[i][0]:
                if at == avgdistvalslist[i][1]:
                    dist = avgdistvalslist[i][2]
                    stdev = str(round(float(avgdistvalslist[i][3]),4))
                    count = avgdistvalslist[i][4]
                    return dist,stdev,count
        
    return dist,stdev,count


#Search angvals list given "at,fro,to" and returns "dmsang,stdev"
def findangval(avgangvalslist,at,fro,to,rev):
    #print "at: " + at + " fro: " + fro + " to: " + to
    angdms = "?"
    stdev = "&"
    count = 0
    for i in range (len(avgangvalslist)):
        if at == avgangvalslist[i][0]:
            if fro == avgangvalslist[i][1]:
                if to == avgangvalslist[i][2]:
                    ang = avgangvalslist[i][3]
                    angdms = rad2dmsstring(ang)
                    stdev = str(round(float(avgangvalslist[i][4]),2))
                    count = avgangvalslist[i][5]
                    #print "found direct count = " + str(count)
                    return angdms,stdev,count
    #if at=from-to match is not found, routine searches for a counter clockwise match:
    if rev == "yes" and angdms == "?":
        for i in range (len(avgangvalslist)):
            if at == avgangvalslist[i][0]:
                if to == avgangvalslist[i][1]:
                    if fro == avgangvalslist[i][2]:
                        ang = avgangvalslist[i][3]
                        angdms = rad2dmsstring(ang)
                        angdms = "-" + angdms
                        stdev = str(round(float(avgangvalslist[i][4]),2))
                        count = avgangvalslist[i][5]
                        return angdms,stdev,count

    return angdms,stdev,count



# Checks if input was empty:
#print "hi there"
if not 'content' in form:
        output_text = 'ERROR: No input provided...'
#Reads form data passed from webpage and stores it as object "content"
else:
        content = form.getvalue('content')      
#Insert script below:
        errorstate = "false"
        output = ""
        if not 'travstring' in form:              
                output += "No Traverse string provided"

        else:
                travstring = form.getvalue('travstring')
                rev = form.getvalue('rev')
                text = form.getvalue('content')
                listing = text.splitlines()
                liststring = text
                liststring = liststring.split("Elapsed Time")[0]



        #output = ""
        comments = "\n#Comments:\n"
        comments += "#Traverse String = " + travstring + "\n"
        comments += "#Allow Reverse Matches option = "  + rev + "\n"
        # Checks if input is valid:
        errorstate = "False"
        if travstring[0:4] == "ie: ":
            output += "Traverse string must be input in the format:\nBacksight point 1,Occupy point 1,Occupy point 2 ... Occupy point n, Foresight point n"   
        if "Adjustment Statistical Summary" not in liststring:
            errorstate = "true"
            output += "Error with Input: Listing does not appear to be a Listing from a STAR*NET Adjustment\n"
        if "Summary of Unadjusted Input Observations" not in liststring:
            errorstate = "true"
            output += "Error with Input: Copy of Input File(s) must be disabled in Project Listing Options\n"
        if travstring.count(',') < 2:
            errorstate = "true"
            output += "Error with Traverse definition: Traverse list must include 3 or more station names\n" 
        if ": 2D" not in liststring:
            errorstate = "true"
            output += "Error with Input: Project must be 2D\n"
        if ": At-From-To" not in liststring:
            errorstate = "true"
            output += "Error with Input: Project input order must be At-From-To\n"
        if not text:
            errorstate = "true"    
            output += 'ERROR: No input provided...'
        if not travstring:
            errorstate = "true"    
            output += 'ERROR: No Traverse String entered...'
  


####################################################       
#Routine begins if contents of listing are suitable:
if errorstate == "False":
    angunits = angunits(listing)
    angleslist = obslist(listing,liststring,"Number of Angle Observations",3)
    distlist = obslist(listing,liststring,"Number of Distance Observations",3)
    dirlist = dirlist(listing,liststring,"Number of Direction Observations",4)

    #Create a list of lists consisting of [at,to,dist,stdev] for each distance
    if distlist:
        distvalslist,comments = distvals(distlist,comments)

    #Create a list of lists consisting of [at,from,to,radianangle,stdev] for each angle
    if angleslist:
        angvalslist,comments = angvals(angleslist,comments)
    #Start of a series of steps to extract data from direction sets
    #Create a list-of-lists-of-lists or list of sets containing a list of each [at,to,radiandirection,stdev]
    if dirlist:
        #dirlist.append("")        
        #dirlist.append("Set")
        dirvals = []       
        setlist = []
        j = 0
        #print dirlist
        while j < len(dirlist)-1:
            #print dirlist[j] + str(j) + "\n"
            if "Set" in dirlist[j+1]:
                dirvals.append(setlist)
                setlist = []
                j += 1
            else:
                parts = dirlist[j].rstrip('\n').split()
                try:
                    fro = parts[0]
                    to = parts[1]
                    dirt = dms2rad(parts[2])
                    stdev = parts[3]
                    if "FREE" not in dirlist[j]:
                        newline = [fro,to,dirt,stdev]
                        setlist.append(newline)
                    else:
                        comments += "#Direction " + fro + "-" + to + "  " + parts[2] + " " + stdev + " excluded\n"
                        j += 1
                #exception catches cases where end of directions in listing is not caught
                except:
                    #print "exception"
                    j += 0
                j += 1
    if not angleslist:
        angvalslist = []

    #Shrinks directions list down to zero, adding all implied angles to the angles list

    if dirlist:
        dirvalsbefore = dirvals
        for i in range(0,len(dirvals)):
            angvalslist = additlangs(dirvals[0],angvalslist)
            shortened = dirvals[1:]
            dirvals = shortened

#Loop through distvalslist and find all repeated entries of the same distance.
#Add averaged distances and propogated stdev to new avgdistvalslist
    at,fro,to = "","",""
    donedist = []
    avgdistvalslist = []
    for i in range (len(distvalslist)):
        pair = ""
        fro = distvalslist[i][0]
        to = distvalslist[i][1]
        check = fro + "-" + to
        if check not in donedist:
            distall = alldist(distvalslist, fro, to)
            distavg = avgdist(distall)
            avgdistvalslist.append(distavg)
            pair = fro + "-" + to
            donedist.append(pair)
            
        

#Loop through angvalslist and find all repeated entries of the same angle
#Add averaged angles and propogated stdev to new avgangvalslist
    doneangs = []
    avgangvalslist = []
    for i in range (len(angvalslist)):
        triple = ""
        at = angvalslist[i][0]
        fro = angvalslist[i][1]
        to = angvalslist[i][2]
        check = at + "-" + fro + "-" + to
        if check not in doneangs:
            angsall = allangs(angvalslist, at, fro, to)
            angsavg = avgangs(angsall)
            avgangvalslist.append(angsavg)
            triple = at + "-" + fro + "-" + to
            doneangs.append(triple)

            
    
        
    travlist = travstring.split(',')
    traverse = ""
    setdist,stdev,count = finddistval(avgdistvalslist,travlist[1],travlist[0],rev)
    traverse += "D  " + travlist[1] + '-' + travlist[0] + "  " + setdist.rjust(10, " ") + "  " + stdev +"\n" + "TB " + travlist[0] + "\n"
    for i in range(1,len(travlist)-1):
        at = travlist[i]
        fro = travlist[i-1]
        to = travlist[i+1]
        dist,diststdev,distcount = finddistval(avgdistvalslist,at,to,rev)
        ang,angstdev,distcount = findangval(avgangvalslist,at,fro,to,rev)
        traverse += "T  " + at.ljust(6, " ") + " " + ang.ljust(12, " ") + " " + dist.ljust(12, " ") + " " + angstdev.ljust(6, " ") + " " + diststdev + "\n"
    traverse += "TE " + to + "\n"
        
    


        

    ct = datetime.datetime.now()
    #Add source file name and timestamp to output:
    output += '#Listing2trav Ver 1.0 Converter Output:\n#Timestamp: ' + str(ct) + "\n"+ comments + "\n"
    output += '.2D\n.UNITS ' + angunits + distunits(listing) + "\n\n"
    output += traverse


# dO NOT MODIFY BELOW:
output_text = output
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
