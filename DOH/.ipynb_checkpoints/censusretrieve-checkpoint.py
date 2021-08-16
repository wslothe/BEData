class Getcensus:
    def __init__(self, name, year, state, geo2, geo2select, tables):
        self.name = name
        self.year = year
        self.state = state
        self.geo2 = geo2
        self.geo2select = geo2select
        self.tables = tables
    def get_census(self):
        import pandas as pd
        import censusdata
        import time
        self.name = censusdata.download('acs5', self.year,
                                        censusdata.censusgeo([('state', self.state), (self.geo2, self.geo2select)]),
                                        [self.tables])
        self.name = pd.DataFrame(self.name)
        name = self.name