import sys
########Tkinter dialog prompts to select input file###################
#import Tkinter as tk
#import tkFileDialog
#root = tk.Tk()
#root.withdraw()
#!/usr/bin/python
import cgi, time, string
import cgitb
cgitb.enable()
form = cgi.FieldStorage()                 # parse form data
titleString = "<title>Listing</title>"
returnlink = 'http://support.microsurvey.com/convert/list2web.html'
output_text = '#Converted ' + time.strftime('%B %d, %Y -- %I:%M:%S %p %Z') + '\r\n#ASCII to STAR*NET script by Jacob Wall -- helpdesk@MicroSurvey.com\r\nScript Version 0.2 -- December 3, 2015\r\n\r\n'
	

output_text = ""
i = 0


##def replsingl(string):
##    newstring = ""
##    for k in range(len(string)):
##        if string[k] != " ":
##            newstring += string[k]
##            #print "1 " + "|" + string[k] + "|" + newstring
##        elif string[k] == " " and string[k-1] == " " and string[k+1] == " ":
##            newstring += string[k]
##            #print "2 " + "   "  + newstring
##        elif string[k] == " " and string[k-1] == " " and string[k+1] != " ":
##            newstring += string[k]
##            #print  "3 " + "   " + newstring
##        elif string[k] == " " and string[k-1] != " " and string[k+1] != " ":
##            newstring += "_"
##            #print  "4 " + "   " + newstring
##        elif string[k] == " " and string[k-1] != " " and string[k+1] == " ":
##            newstring += string[k]
##            #print "5 " + "   "  + newstring
##    return newstring
##
##            
##    
##
##def tablebuilder(lines,curLine,i,skip):
##    #replaces single spaces with _
##    #to accomdate headers that have single spaces for some column labels:
##    #curLine = replsingl(curLine)
##    #whole file, current line (title), place in file, gap before headers line
##    #create the title
##    table = ""
##
##    #skip to header line
##    count = i + skip
##    line = lines[count]
##    if "Comb Grid" in line:
##        line = line.replace("Comb Grid", "Comb_Grid")
##    if "Ellip Ht" in line:
##        line = line.replace("Ellip Ht", "Ellip_Ht")
##    header = line.split()
##    columns = len(header)
##    #Now that we have the header we can start writing the table html:
##    #First define the column headers:
##    table += "<p>" + curLine.strip('\n') + "</p><p></p>" + '\n'
##    #clean up curLine so we can use it to customize the sorting script:
##    curLine = curLine.strip('\n')
##    curLine = curLine.replace(" ", "")
##    curLine = curLine.replace("(", "")
##    curLine = curLine.replace(")", "")
##    curLine = curLine.replace("=", "")
##    
##    
##    table += '''<style>
##  table {
##    border-collapse: collapse;
##  }
##  th, td {
##    border: 2px solid #4b9b98;
##    padding: 5px;
##    text-align: center;
##  }
##</style>'''
##    table += '<font face="courier" ><table border="1" style="width:100%"  border="collapse" id="' + curLine.strip('\n') + '">' + '\n'
##    table += '  <tr>' + '\n'
##    for j in range(columns):
##        table += '<th onclick="sortTable' + curLine + '(' + str(j) + ')">' + header[j] + '</th>' + '\n'
##    table += '  </tr>' + '\n'
##    #Now define the columns:
##    while '\n' not in lines[count+1][0:2]:
##        count += 1
##        line = lines[count]
##        line = replsingl(line)
##        row = line.split()
##        rows = len(row)
##        table += '  <tr>' + '\n'
##        for k in range (rows):
##            table += '    <td>' + row[k] + '</td>' + '\n'
##        table += '  </tr>' + '\n'        
##        
##    table += '</table></font>' + '\n'
##    #Now write the java script for sorting:
##    table += '''<script>
##function sortTable''' + curLine + '''(n) {
##  var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
##  table = document.getElementById("''' + curLine + '''");
##  switching = true;
##  //Set the sorting direction to ascending:
##  dir = "asc"; 
##  /*Make a loop that will continue until
##  no switching has been done:*/
##  while (switching) {
##    //start by saying: no switching is done:
##    switching = false;
##    rows = table.getElementsByTagName("TR");
##    /*Loop through all table rows (except the
##    first, which contains table headers):*/
##    for (i = 1; i < (rows.length - 1); i++) {
##      //start by saying there should be no switching:
##      shouldSwitch = false;
##      /*Get the two elements you want to compare,
##      one from current row and one from the next:*/
##      x = rows[i].getElementsByTagName("TD")[n];
##      y = rows[i + 1].getElementsByTagName("TD")[n];
##      /*check if the two rows should switch place,
##      based on the direction, asc or desc:*/
##      if (dir == "asc") {
##        if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
##          //if so, mark as a switch and break the loop:
##          shouldSwitch= true;
##          break;
##        }
##      } else if (dir == "desc") {
##        if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
##          //if so, mark as a switch and break the loop:
##          shouldSwitch= true;
##          break;
##        }
##      }
##    }
##    if (shouldSwitch) {
##      /*If a switch has been marked, make the switch
##      and mark that a switch has been done:*/
##      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
##      switching = true;
##      //Each time a switch is done, increase this count by 1:
##      switchcount ++;      
##    } else {
##      /*If no switching has been done AND the direction is "asc",
##      set the direction to "desc" and run the while loop again.*/
##      if (switchcount == 0 && dir == "asc") {
##        dir = "desc";
##        switching = true;
##      }
##    }
##  }
##}
##</script>'''
##    return table,count+1






output_text += "<!DOCTYPE html><html><title>STAR*NET HTML Listing</title><body>"
output_text += "Hello"
###url = form.getvalue("url")
###output_text += '<p><img src="http://microsurvey.com/dealers/files/Logo_STARNET.png" alt="STAR*NET" align="middle"> </p>'
##
###filename = tkFileDialog.askopenfilename(filetypes=[("text file","*.lst")])
###text = open(filename,'r')
##text = form.getvalue('content')
##lines = text.readlines()
###text.close()
###lines = lines.replace('\x0c\n','\n')
##
##
##
##while i < (len(lines)):
##    curLine = lines[i]
##    if "Adjusted Measured Angle Observations" in curLine:
##        table = tablebuilder(lines,curLine,i,2)
##        output_text += table[0]
##        i = table[1]
##
##    elif "Adjusted Measured Distance Observations" in curLine:
##        table = tablebuilder(lines,curLine,i,2)
##        output_text += table[0]
##        i = table[1]
##
##    elif "Adjusted Zenith Observations" in curLine:
##        table = tablebuilder(lines,curLine,i,2)
##        output_text += table[0]
##        i = table[1]
##
##    elif "GPS Vector Residual Summary" in curLine:
##        table = tablebuilder(lines,curLine,i,3)
##        output_text += table[0]
##        i = table[1]
##
##    elif "Coordinate Changes from Entered Provisionals" in curLine:
##        table = tablebuilder(lines,curLine,i,2)
##        output_text += table[0]
##        i = table[1]
##
##    elif "Adjusted Coordinates" in curLine:
##        table = tablebuilder(lines,curLine,i,2)
##        output_text += table[0]
##        i = table[1]
##
##    elif "Adjusted ECEF Coordinates" in curLine:
##        table = tablebuilder(lines,curLine,i,2)
##        output_text += table[0]
##        i = table[1]
##
##
##    elif "Number of Measured Angle Observations" in curLine:
##        table = tablebuilder(lines,curLine,i,2)
##        output_text += table[0]
##        i = table[1]
##
##    elif "Number of Measured Distance Observations" in curLine:
##        table = tablebuilder(lines,curLine,i,2)
##        output_text += table[0]
##        i = table[1]
##
##    elif "Number of Zenith Observations" in curLine:
##        table = tablebuilder(lines,curLine,i,2)
##        output_text += table[0]
##        i = table[1]
##
##    elif "Station Coordinate Standard Deviations" in curLine:
##        table = tablebuilder(lines,curLine,i,2)
##        output_text += table[0]
##        i = table[1]
##
##
##    elif "Adjusted Positions and" in curLine:
##        table = tablebuilder(lines,curLine,i,3)
##        output_text += table[0]
##        i = table[1]
##
####    elif "Iteration #" in curLine:
####        table = tablebuilder(lines,curLine,i,3)
####        output_text += table[0]
####        i = table[1]
##        
##    else:
##        curLine = curLine.replace(' ','&nbsp;')
##        #output_text += '<p style="font-family:courier;">' + curLine + '<br>'
##        output_text += '<font face="courier">' + curLine + '</font><br>'
##        i += 1
##    
###fileout = open('Listing.html','w')
###fileout.write(output_text)
###fileout.close()
print "Content-type:text/html\r\n\r\n"
print cgi.escape(output_text, quote=True)
#print "</textarea>"
#print "<p>Please contact MicroSurvey at helpdesk@microsurvey.com if results are not as expected or contain errors.</p>"
#print "</div>"
#print "</body>"
print "</html>"
    

