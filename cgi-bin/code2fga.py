#!/usr/bin/python
import cgi, cgitb, time, string
import xml.etree.ElementTree as ET
#below entry allows for online debugging, it should be removed for release:
import cgitb
cgitb.enable(format = "text")



form = cgi.FieldStorage()                 # parse form data
titleString = "<title>FGA Template Codelist</title>"
returnlink = 'https://support.microsurvey.com/convert/code2fga.html'
output_text = "" #'#Converted ' + time.strftime('%B %d, %Y -- %I:%M:%S %p %Z') + '\r\n#Code to FGA script by MicroSurvey -- helpdesk@MicroSurvey.com\r\n#Script Version 1.0 -- 03 08, 2020\r\n\r\n'

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
print "'>Return to the Input Page</a>&nbsp;&nbsp;&nbsp;<a class='button-2' href='https://support.microsurvey.com/converters.html'>Return to the Main Page</a></p>"
print "<bold>Instructions for Creating an FGA template Codelist:</bold><br>1. Create a new text document using a text editor on a Windows or Android device<br>2. Click in the field below<br>3. CTRL-A to select all<br>4. CTRL-C to copy all<br>5. Click in your new text file"
print "<br>6. CTRL-V to paste<br>7. Save the text file with the name *.ctf<br>8. Transfer the new file to your controller in:<br>(Device Name)\Internal shared storage\FieldGenius\Configurations"
print "<textarea style='width:100%; border:1px solid #CCC; height:800px; padding:5px;'>"

# Insert function definitions below:

def col_to_num(col_str):
    """ Convert base26 column string to number. """
    col_str = col_str.upper()
    expn = 0
    col_num = 0
    for char in reversed(col_str):
        col_num += (ord(char) - ord('A') + 1) * (26 ** expn)
        expn += 1

    return col_num - 1
                    
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

# Checks if input was empty:

if not 'content' in form:
	output_text = 'ERROR: No input provided...'

#Reads form data passed from webpage and stores it as object "content"

else:
    content = form.getvalue('content')
    #content = input.read()

    
#Insert script below:

    if not 'formvalue_text' in form:
        textinput = ""
    else:
        content = form.getvalue('content')
        lines = content.splitlines()
        separator = form.getvalue('formvalue_radio')
        formatstring = form.getvalue('formvalue_pulldown')
        header = form.getvalue('header')
        if formatstring == "custom":
            formatstring = form.getvalue('formvalue_text')
        if formatstring == "automap":
            formatstring = "A,L,0,1"
            separator = ","
            header = "1"
        formatlist = formatstring.split(",")
        header = int(header)
        codes = []
  


        section1 = '''<?xml version="1.0" encoding="utf-8"?>
        <attribute_table_templates version="1.00" xmlns="http://tempuri.org/XMLSchemaAttributes.xsd">
          <table name="Survey_Pnt" alias="Survey_Point" geometry="point">
            <fields>
              <field name="ID" alias="ID" state="editable" unique="yes" required="yes">
                <datatype_text>
                  <default apply="no" value="" />
                  <constraint lengthmin="0" lengthmax="0" />
                  <widget_textbox>
                    <multiline>no</multiline>
                  </widget_textbox>
                </datatype_text>
              </field>\n'''
        pointcodes = '''      <field name="Desc" alias="Desc" state="editable" unique="no" required="no">
                <datatype_text>
                  <default apply="no" value="" />
                  <constraint lengthmin="0" lengthmax="0" />
                  <widget_listbox>
                    <textbox>yes</textbox>
                    <editable>yes</editable>
                    <items>\n'''
        section3 = '''            </items>
                  </widget_listbox>
                </datatype_text>
              </field>
              <field name="Note" alias="Note" state="editable" unique="no" required="no">
                <datatype_text>
                  <default apply="no" value="" />
                  <constraint lengthmin="0" lengthmax="0" />
                  <widget_textbox>
                    <multiline>yes</multiline>
                  </widget_textbox>
                </datatype_text>
              </field>
            </fields>
            <symbol>
              <type name="symbol1" size="1" unit="millimeter" />
              <colour>#FF0000</colour>
              <rotation>0</rotation>
              <opacity>100</opacity>
              <offsetx anchor="center" offset="0" unit="millimeter" />
              <offsety anchor="center" offset="0" unit="millimeter" />
            </symbol>
            <label>
              <field>ID</field>
              <font name="Ariel" style="regular" size="12" unit="points" />
              <colour>#000000</colour>
              <rotation>0</rotation>
              <opacity>100</opacity>
              <typecase>no change</typecase>
              <offsetx anchor="left" offset="0" unit="millimeter" />
              <offsety anchor="center" offset="0" unit="millimeter" />
            </label>
            <popup>
              <field name="ID" />
              <field name="Desc" />
            </popup>
            <cad>
              <plotted_description_field>Desc</plotted_description_field>
              <layer>Points</layer>
            </cad>
          </table>\n'''
        linecodes = '''  <table name="Survey_Line" alias="Survey_Line" geometry="line">
            <fields>
              <field name="ID" alias="ID" state="editable" unique="yes" required="yes">
                <datatype_text>
                  <default apply="no" value="" />
                  <constraint lengthmin="0" lengthmax="0" />
                  <widget_textbox>
                    <multiline>no</multiline>
                  </widget_textbox>
                </datatype_text>
              </field>
              <field name="Desc" alias="Desc" state="editable" unique="no" required="no">
                <datatype_text>
                  <default apply="no" value="" />
                  <constraint lengthmin="0" lengthmax="0" />
                  <widget_listbox>
                    <textbox>yes</textbox>
                    <editable>yes</editable>
                    <items>\n'''

        section5 = '''            </items>
                  </widget_listbox>
                </datatype_text>
              </field>
              <field name="Note" alias="Note" state="editable" unique="no" required="no">
                <datatype_text>
                  <default apply="no" value="" />
                  <constraint lengthmin="0" lengthmax="0" />
                  <widget_textbox>
                    <multiline>yes</multiline>
                  </widget_textbox>
                </datatype_text>
              </field>
            </fields>
            <symbol>
              <type name="symbol1" size="1" unit="millimeter" />
              <colour>#FF0000</colour>
              <rotation>0</rotation>
              <opacity>100</opacity>
              <offsetx anchor="center" offset="0" unit="millimeter" />
              <offsety anchor="center" offset="0" unit="millimeter" />
            </symbol>
            <label>
              <field>ID</field>
              <font name="Ariel" style="regular" size="12" unit="points" />
              <colour>#000000</colour>
              <rotation>0</rotation>
              <opacity>100</opacity>
              <typecase>no change</typecase>
              <offsetx anchor="left" offset="0" unit="millimeter" />
              <offsety anchor="center" offset="0" unit="millimeter" />
            </label>
            <popup>
              <field name="ID" />
              <field name="Desc" />
            </popup>
            <cad>
              <plotted_description_field>Desc</plotted_description_field>
              <layer>Lines</layer>
            </cad>
          </table>
        </attribute_table_templates>'''


        #parse formatlist

        keyposition = col_to_num(formatlist[0])
        lineposition = col_to_num(formatlist[1])
        lineoff = formatlist[2]
        lineon = formatlist[3]


        for i in range(header,len(lines)):
            items = lines[i].split(separator)
            key = items[keyposition].rstrip()
            line = items[lineposition].rstrip()
            if '"' in key:
            #    key = "illegal"
                key = cgi.escape( """& < >""" )   # key = "&amp; &lt; &gt;"
            if key not in codes:
                codes.append(key)
                if line == lineoff:
                    pointcodes += '              <item value="'  + key + '" alias="' + key + '" />\n'
                
                elif line == lineon:
                    linecodes += '              <item value="'  + key + '" alias="' + key + '" />\n'

                else:
                    pointcodes += '              <item value="'  + key + '" alias="' + key + '" />\n'        


        output_text = section1 + pointcodes + section3 + linecodes + section5
        


 



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
