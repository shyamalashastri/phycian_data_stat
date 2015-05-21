#!/usr/bin/python
import sys, getopt
import json,requests,re, string

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

year = sys.argv[2];
platform = sys.argv[3];
specialty = sys.argv[1];

SIM = {}
ME = {}
FFM_cnt = 0;
PM_cnt = 0;
SB_cnt = 0;
YES_cnt =0;
NO_cnt = 0;
Scount = {}
Sname = {}
missing_count = 0;
total_count = 0;
statecode = ""
with open("crosswalk.txt") as f:
    for line in f:
        #print line;
        #system.exit();
        results = line.split();
        key = results[0];
        SIM[key] = results[1];
        ME[key] = results[2];
        Scount[key] = 0;

with open("state.txt") as f:
    for line in f:
        #print line;
        #system.exit();
        results = line.split();
        key = results[0];
        Sname[key] = results[1];

#print SIM;
#print ME;
#print Sname;
linenum = 0;
fout =  open("results/"+year+"/"+platform+"/csv/"+specialty+".csv",'w');
fres=  open("results/"+year+platform+".csv",'a');

#info files

#aggregate
aFFM = open("results/"+year+"-"+platform+"-"+"aggregate"+"-FFM.txt",'a');
aPM = open("results/"+year+"-"+platform+"-"+"aggregate"+"-PM.txt",'a');
aSB = open("results/"+year+"-"+platform+"-"+"aggregate"+"-SBM.txt",'a');
aYES = open("results/"+year+"-"+platform+"-"+"aggregate"+"-YES.txt",'a');
aNO = open("results/"+year+"-"+platform+"-"+"aggregate"+"-NO.txt",'a');

sFFM = open("results/"+year+"-"+platform+"-"+specialty+"-FFM.txt",'w');
sPM = open("results/"+year+"-"+platform+"-"+specialty+"-PM.txt",'w');
sSB = open("results/"+year+"-"+platform+"-"+specialty+"-SBM.txt",'w');
sYES = open("results/"+year+"-"+platform+"-"+specialty+"-YES.txt",'w');
sNO = open("results/"+year+"-"+platform+"-"+specialty+"-NO.txt",'w');


for line in open(year+"/"+platform+"/csv/"+specialty+".csv",'r').readlines():
    #print line;
    line = filter(lambda x: x in string.printable, line)
    results = line.split(',');
    
    if linenum == 0:
        linenum = linenum + 1;
        continue;

    if platform == "JAMA":
        name = results[1];
        address = results[2];
        description = results[6];
    elif platform == "NCHCR":
        name = results[4];
        address = results[3];
        description = results[11]+results[12];
    elif platform == "NEJM":
        name = results[1];
        address = results[3];
        description = results[7];


    total_count += 1;
    
    if( address != ""):
    #replace " " with "+" in address field
    
        for delim in ' ':
            ad = address.replace(delim, '+');

        api= 'http://gws2.maps.yahoo.com/findlocation?pf=1&location='+ad;
        

#print ad;
#print api;
        response = requests.get(url=api)

        #print response.text;
        statecode = find_between(response.text,"<countrycode>US</countrycode><statecode>","</statecode>")



    if statecode == "":
        #print address
        for delim in ' ':
            ad = name.replace(delim, '+');
        api= 'http://gws2.maps.yahoo.com/findlocation?pf=1&location='+ad;
        #print api;
        try :
            response = requests.get(url=api)
        except Exception:
            continue;

        
        #print response.text;
        statecode = find_between(response.text,"<countrycode>US</countrycode><statecode>","</statecode>")

    if statecode == "":
        #print address
        for eachKey in Sname.keys():
            #print Sname[eachKey];
            if Sname[eachKey] in address:
                statecode = eachKey;
            elif Sname[eachKey] in description:
                statecode = eachKey;
            elif Sname[eachKey] in name:
                statecode = eachKey;
            else:
                statecode = "MISSING/INTERNATIONAL"

#print statecode

    if statecode == "PR" or statecode == "GU":
        statecode = "MISSING/INTERNATIONAL"

    if statecode != "MISSING/INTERNATIONAL":
        
        sim_val = SIM[statecode];
        me_val = ME[statecode];
        Scount[statecode] += 1;

        print >>fout,line,"+",statecode,"+",sim_val,"+",me_val;
        
        if sim_val == "FFM":
            FFM_cnt += 1;
            print >>aFFM,description
            print >>sFFM,description
        elif sim_val == "PM":
            PM_cnt += 1;
            print >>aPM,description
            print >>sPM,description
        elif sim_val == "SBM":
            SB_cnt += 1;
            print >>aSB,description
            print >>sSB,description

        if me_val == "Yes":
            YES_cnt += 1;
            print >>aYES,description
            print >>sYES,description
        elif me_val == "No":
            NO_cnt += 1;
            print >>aNO,description
            print >>sNO,description

    else:
        missing_count += 1;



print >>fres,year,"   ",platform;
print >>fres,"Primary care specialties"+","+"	Total	"+","+"Total in US state locations (i.e. not missing and not international)	 	"+","+"Federally-facilitated [FFM]	"+","+"Partnership marketplace [PM]	"+","+"State-based [SBM]	 	"+","+"Yes	"+","+"No";
print >>fres,specialty,",",total_count,",",(total_count-missing_count),",",FFM_cnt,",",PM_cnt,",",SB_cnt,",",YES_cnt,",",NO_cnt;

sys.exit(0);
