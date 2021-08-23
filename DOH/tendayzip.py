import pandas as pd
import numpy as np
import time
from datetime import date, timedelta
import os
#identifying the day (in ISO 8601) so we can read the most recent file, as well as yesterday's date
today = time.strftime("%Y%m%d")
yesterday = date.today() - timedelta(days=1)
yesterday = yesterday.strftime("%Y%m%d")
lastweek = date.today() - timedelta(days=7)
lastweek = lastweek.strftime("%Y%m%d")
lastten = date.today() - timedelta(days=10)
lastten = lastten.strftime("%Y%m%d")
#input data as dataframes
todayzipname = ("C:\\Users\\aweidenhof\\Documents\\GitHub\\BEData\\DOH\\Data\\" + today + "_zip_code_data.csv")
todayzip = pd.read_csv(todayzipname)
yesterdayzipname = ("C:\\Users\\aweidenhof\\Documents\\GitHub\\BEData\\DOH\\Data\\" + yesterday + "_zip_code_data.csv")
yesterdayzip = pd.read_csv(yesterdayzipname)
lastweekzipname = "C:\\Users\\aweidenhof\\Documents\\GitHub\\BEData\\DOH\\Data\\" + (lastweek + "_zip_code_data.csv")
lastweekzip = pd.read_csv(lastweekzipname)
lasttenzipname = ("C:\\Users\\aweidenhof\\Documents\\GitHub\\BEData\\DOH\\Data\\" + lastten + "_zip_code_data.csv")
lasttenzip = pd.read_csv(lasttenzipname)
#defining our function
def getnum(file, row, dataname):
    dataname = file.iloc[:,[row]]
    return dataname
dailypos = getnum(todayzip, 1, 'dailypos')
dailyneg = getnum(todayzip, 2, 'dailyneg')
yesterdaypos = getnum(yesterdayzip, 1, 'yesterdaypos')
yesterdayneg = getnum(yesterdayzip, 2, 'yesterdayneg')
lastweekpos = getnum(lastweekzip, 1, 'lastweekpos')
lastweekneg = getnum(lastweekzip, 2, 'lastweekneg')
lasttenpos = getnum(lasttenzip, 1, 'lasttenpos')
lasttenneg = getnum(lasttenzip, 2, 'lasttenneg')
cumetests = dailypos.values + dailyneg.values
population = todayzip.iloc[:, [8]]
population = population.values
cumepos = dailypos / cumetests * 100
cumepos = cumepos.round(2)
dailychange = dailypos - yesterdaypos
dailychangerate = dailychange / population * 100000
dailychangerate = dailychangerate.round(2)
todaypos = dailypos - yesterdaypos
todayneg = dailyneg - yesterdayneg
todaytests = todaypos.values + todayneg.values
dailypostestrate = todaypos.values / todaytests
dailypostestrate = dailypostestrate * 100
dailypostestrate = dailypostestrate.round(2)
dailypostestrate = pd.DataFrame.from_dict(dailypostestrate)
weeklypos = dailypos - lastweekpos
weeklyposavg = weeklypos / 7
weeklyposavgrate = weeklyposavg / population * 100000
weeklyposavgrate = weeklyposavgrate.round(2)
weeklyposavg = weeklyposavg.round(2)
weeklynewpos = dailypos - lastweekpos
weeklynewneg = dailyneg - lastweekneg
weeklynewtests = weeklynewpos.values + weeklynewneg.values
weeklypostestrate = weeklynewpos.values / weeklynewtests * 100
weeklypostestrate = weeklypostestrate.round(2)
weeklypostestrate = pd.DataFrame.from_dict(weeklypostestrate)
tendaynewpos = dailypos - lasttenpos
tendayposrate = tendaynewpos / population * 100000
tendayposrate = tendayposrate.round(2)
tendaynewneg = dailyneg - lasttenneg
tendaynewtests = tendaynewpos.values + tendaynewneg.values
tendaypostestrate = tendaynewpos.values / tendaynewtests * 100
tendaypostestrate = tendaypostestrate.round(2)
tendaypostestrate = pd.DataFrame.from_dict(tendaypostestrate)
cumetests = pd.DataFrame.from_dict(cumetests)
todaytests = pd.DataFrame.from_dict(todaytests)
weeklynewtests = pd.DataFrame.from_dict(weeklynewtests)
tendaynewtests = pd.DataFrame.from_dict(tendaynewtests)
newstuff = pd.concat([cumetests, cumepos, dailychange, dailychangerate, todayneg, todaytests, dailypostestrate, weeklypos, weeklyposavg, weeklyposavgrate, 
                      weeklynewneg, weeklynewtests, weeklypostestrate, tendaynewpos, tendayposrate, tendaynewneg, tendaynewtests,  tendaypostestrate], 
                    axis = 1)
todayzip = pd.concat([todayzip, newstuff], axis = 1)
todayzip.columns = ['Postcode', 'Positive', 'Negative', 'Cumulative Incidence', 'Partially Vaxxed', 'Partially Vaxxed Rate',
                    'Fully Vaxxed', 'Fully Vaxxed Rate', 'Population', 'Total Tests', 'Positivity Percentage', 'New Positives Today', 
                    'New Positives per 100k', 'New Negatives', 'New Tests', 'Positive Test Rate Today', 'Weekly Positives', 'Average Weekly Positives', 
                    'Weekly Positive Average per 100k', 'Weekly Negatives', 'Weekly Tests', 'Weekly Positive Test Rate', 'Ten-Day Positives', 
                   'Ten-Day Positives per 100k', 'Ten-day Negatives', 'Ten-day Tests', 'Ten-Day Poisitive Test Rate']
todayzip.to_csv(todayzipname)