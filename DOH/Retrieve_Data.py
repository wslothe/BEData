import os
import pandas as pd
import numpy as np
import time
import datetime
from dohretrieve import DOH
#Identifying the variables
#ident, dfname, where, limit, select, sort
zipcases = DOH('tsf6-pnaf', 'zip_code_cases', 
               'postcode between "16001" and "16066"', 42, 'postcode, positive, negative', 'postcode ASC')
countycases = DOH('j72v-r42c', 'county_cases', 
               'county = "Butler"', '', 'date, county, cases, cases_rate, cases_avg_new, cases_avg_new_rate, cases_cume, cases_cume_rate', 'date DESC')
countydailyvax = DOH('bicw-3gwi', 'county_daily_vax', 
                'county = "Butler"', '', 'date, county, partiallycovered, fullycovered', 'date DESC')
countycumevax = DOH('gcnb-epac', 'county_cumulative_vax', 
                'county = "Butler"', '', 'county, county_population, partiallycovered, ratepartiallycovered, fullycovered, ratefullycovered', 'county ASC')
zipcumevax = DOH('d63n-ygar', 'zip_cumulative_vax', 
                 'patient_zip_code between "16001" and "16066"', '', 'patient_zip_code, partiallycovered, fullycovered', 'patient_zip_code ASC')
#Running the functions, saving them to new files
DOH.get_data(zipcases)
DOH.get_data(countycases)
DOH.get_data(countydailyvax)
DOH.get_data(countycumevax)
DOH.get_data(zipcumevax)
datestr = time.strftime("%Y%m%d")
zcumevax = pd.read_csv("C:\\users\\aweidenhof\\Documents\\GitHub\\BEData\\DOH\\Data\\" + datestr + "_zip_cumulative_vax.csv")
blankZips = [pd.Series([16018, None, None], index=['patient_zip_code', 'partiallycovered', 'fullycovered']),
             pd.Series([16035, None, None], index=['patient_zip_code', 'partiallycovered', 'fullycovered']),
             pd.Series([16036, None, None], index=['patient_zip_code', 'partiallycovered', 'fullycovered']),
             pd.Series([16039, None, None], index=['patient_zip_code', 'partiallycovered', 'fullycovered']),
             pd.Series([16058, None, None], index=['patient_zip_code', 'partiallycovered', 'fullycovered'])]
zcumevax = zcumevax.append(blankZips, ignore_index = True)
zcumevax = zcumevax.sort_values('patient_zip_code')
zcumevax = zcumevax.set_index('patient_zip_code')
zcumevax.to_csv("C:\\users\\aweidenhof\\Documents\\GitHub\\BEData\\DOH\\Data\\" + datestr + "_zip_cumulative_vax.csv")
#writing population and rates to main zip files
def execfile(filepath, globals=None, locals=None):
    if globals is None:
        globals = {}
    globals.update({
        "__file__": filepath,
        "__name__": "__main__",
    })
    with open(filepath, 'rb') as file:
        exec(compile(file.read(), filepath, 'exec'), globals, locals)
#execute the file
execfile("census_and_rates.py")
#combining zip files
datestr = time.strftime("%Y%m%d")
main_zip_name = ("C:\\users\\aweidenhof\\Documents\\GitHub\\BEData\\DOH\\Data\\" + datestr + "_zip_code_cases.csv")
zip_vax_name = ("C:\\users\\aweidenhof\\Documents\\GitHub\\BEData\\DOH\\Data\\" + datestr + "_zip_cumulative_vax.csv")
main_zip = pd.read_csv(main_zip_name)
zip_vax = pd.read_csv(zip_vax_name)
main_zip['Partially Covered'] = zip_vax['partiallycovered'].round(0)
main_zip['Partially Covered Rate'] = zip_vax['Partially Covered Rate']
main_zip['Fully Covered'] = zip_vax['fullycovered'].round(0)
main_zip['Fully Covered Rate'] = zip_vax['Fully Covered Rate']
#reordering and renaming columns
main_zip = main_zip.set_index('postcode')
main_zip = main_zip[['positive', 'negative', 'Cumulative Incidence', 'Partially Covered', 
                    'Partially Covered Rate', 'Fully Covered', 'Fully Covered Rate', 'Population']]
main_zip = main_zip.rename(columns={'positive' : 'Positive', 'negative' : 'Negative'})
#saving new zip file
newzip_name = ("C:\\users\\aweidenhof\\Documents\\GitHub\\BEData\\DOH\\Data\\" + datestr + "_zip_code_data.csv")
main_zip.to_csv(newzip_name, index = True)
#writing new information to our files
def execfile(filepath, globals=None, locals=None):
    if globals is None:
        globals = {}
    globals.update({
        "__file__": filepath,
        "__name__": "__main__",
    })
    with open(filepath, 'rb') as file:
        exec(compile(file.read(), filepath, 'exec'), globals, locals)
#execute the file
execfile("tendayzip.py")
#deleting old files
os.remove(main_zip_name)
os.remove(zip_vax_name)