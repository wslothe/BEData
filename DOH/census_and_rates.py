from censusretrieve import Getcensus
import pandas as pd
import time
#getting population by zip code
#self, name year, state, geo2, geo2select, tables
r1 = 16001
r2 = 16066
ziplist = list(range(r1, r2+1))
zips = ','.join(str(e) for e in ziplist)
zip5 = Getcensus('zipcodes', 2019, '42', 'zip code tabulation area', zips, 'B01001_001E')
Getcensus.get_census(zip5)
zipcodes = zip5.name
zipcodes.index = zipcodes.index.astype('str')
zipcodes.index = zipcodes.index.str[:11]
zipcodes.index = zipcodes.index.str[-5:]
zipcodes = zipcodes.reset_index()
blankZips = [pd.Series([16003, None], index=zipcodes.columns),
             pd.Series([16018, None], index=zipcodes.columns),
             pd.Series([16039, None], index=zipcodes.columns),
             pd.Series([16058, None], index=zipcodes.columns)]
zipcodes = zipcodes.append(blankZips, ignore_index = True)
zipcodes = zipcodes.set_index('index')
zipcodes.index = zipcodes.index.astype('int')
zipcodes = zipcodes.sort_index()
zipcodes = zipcodes.reset_index(drop = True)
datestr = time.strftime("%Y%m%d")
zip_cases_name = ("C:\\users\\aweidenhof\\Documents\\GitHub\\BEData\\DOH\\Data\\" + datestr + "_zip_code_cases.csv")
zip_cases = pd.read_csv(zip_cases_name)
zip_cases['Population'] = zipcodes['B01001_001E']
zip_cases['Cumulative Incidence'] = zip_cases['positive']/zip_cases['Population']*100000
zip_cases['Cumulative Incidence'] = zip_cases['Cumulative Incidence'].round(2)
zip_cases.to_csv(zip_cases_name, index=False)
zip_vax_name = ("C:\\users\\aweidenhof\\Documents\\GitHub\\BEData\\DOH\\Data\\" + datestr + "_zip_cumulative_vax.csv")
zip_vax = pd.read_csv(zip_vax_name)
population = zipcodes['B01001_001E']
zip_vax['Partially Covered Rate'] = zip_vax['partiallycovered']/population*100000
zip_vax['Partially Covered Rate'] = zip_vax['Partially Covered Rate'].round(2)
zip_vax['Fully Covered Rate'] = zip_vax['fullycovered']/population*100000
zip_vax['Fully Covered Rate'] = zip_vax['Fully Covered Rate'].round(2)
zip_vax.to_csv(zip_vax_name, index=False)