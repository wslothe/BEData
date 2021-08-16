import pandas as pd
import numpy as np
import time
from datetime import date, timedelta
import os
#identifying the day (in ISO 8601) so we can read the most recent file, as well as yesterday's date
today = time.strftime("%Y%m%d")
yesterday = date.today() - timedelta(days=1)
yesterday = yesterday.strftime("%Y%m%d")
#putting that into a more readable format
dayofweek = time.strftime("%A, %b. %d, %Y")
#input new data as dataframes
ctycasename = (today + "_county_cases.csv")
ctycases = pd.read_csv(ctycasename)
ctynewvaxname = (today + "_county_daily_vax.csv")
ctynewvax = pd.read_csv(ctynewvaxname)
ctytotvaxname = (today + "_county_cumulative_vax.csv")
ctytotvax = pd.read_csv(ctytotvaxname)
#defining our function
def getnum(file, row, dataname):
    dataname = file.iloc[[0], [row]]
    return dataname.to_string(index = False, header = False)  
#getting county case info from most recent file
newcases = getnum(ctycases, 2, 'newcases')
newcaserate = getnum(ctycases, 3, 'newcaserate')
sevenavg = getnum(ctycases, 4, 'sevenavg')
sevenavgrate = getnum(ctycases, 5, 'sevenavgrate')
cumecases = getnum(ctycases, 6, 'cumecases')
cumerate = getnum(ctycases, 7, 'cumerate')
newptlvax = getnum(ctynewvax, 2, 'newptlvax')
newfullvax = getnum(ctynewvax, 3, 'newfullvax')
totptlvax = getnum(ctytotvax, 2, 'totptlvax')
ptlvaxrate = getnum(ctytotvax, 3, 'ptlvaxrate')
totfullvax = getnum(ctytotvax, 4, 'totfullvax')
fullvaxrate = getnum(ctytotvax, 5, 'fullvaxrate')
#before writing the data to the text files, we should first archive the current ones.
newfilenamecty = (yesterday + "_county_data.txt")
os.rename("new_county_data.txt", newfilenamecty)
#putting county data in text form!
updated = ("Updated: " + dayofweek + "\n" + "\n")
prtnewcase = ("New cases in Butler County: " + newcases + "\n")
prtnewrate = ("New cases per 100k: " + newcaserate + "\n")
prtsevenavg = ("Seven-day average: " + sevenavg + "\n")
prtsevenavgrate = ("Seven-day average per 100k: " + sevenavgrate + "\n")
prtcumecases = ("Total cases in Butler county: " + newcases + "\n")
prtcumecaserate = ("Total cases in Butler County per 100k: " + cumerate + "\n")
prtnewptlvax = ("Newly partially vaccinated individuals: " + newptlvax + "\n")
prttotptlvax = ("Partially vaccinated individuals: " + totptlvax + "\n")
prtptlvaxrate = ("Partially vaccinated individuals per 100k: " + ptlvaxrate + "\n")
prtnewfullvax = ("Newly fully vaccinated individuals: " + newfullvax + "\n")
prtfullvax = ("Fully vaccinated individuals: " + totfullvax + "\n")
prtfullvaxrate = ("Fully vaccinated individuals per 100k: " + fullvaxrate)
prtcounty = (updated + prtnewcase + prtnewrate + prtsevenavg + prtsevenavgrate + prtcumecases + prtcumecaserate + prtnewptlvax + prttotptlvax + prtptlvaxrate +
             prtnewfullvax + prtfullvax + prtfullvaxrate)
#writing the new county data to a file
ctyfile = open("new_county_data.txt", "w")
ctyfile.write(prtcounty)
ctyfile.close()