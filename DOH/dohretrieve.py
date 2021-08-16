class DOH:
    def __init__(self, ident, dfname, where, limit, select, order):
        self.ident = ident
        self.dfname = dfname
        self.where = where
        self.limit = limit
        self.select = select
        self.order = order
    
    def get_data(self):
        import os
        from dotenv import load_dotenv
        import time
        import pandas as pd
        from sodapy import Socrata
        load_dotenv()
        doh_domain = 'data.pa.gov'
        socrata_token = os.getenv('socrata_token')
        client = Socrata (doh_domain, socrata_token)
        datestr = time.strftime("%Y%m%d")
        dfname = self.dfname
        self.dfname = client.get(self.ident, where=self.where, limit=self.limit, select=self.select, order=self.order)
        self.dfname = pd.DataFrame.from_dict(self.dfname)
        self.dfname = self.dfname.dropna()
        self.dfname.to_csv(datestr + "_" + dfname + ".csv", index=False)