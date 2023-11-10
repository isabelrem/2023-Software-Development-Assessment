from PanelApp_API_Request import *
from PanelApp_Request_Parse import *

import sys
sys.path.append('../')


RQ = PanelAppRequest()

### For testing purposes ###
PK = 'Fetal anomalies with a likely genetic cause'
response = RQ.pk_search(PK)

print(f"Status Code: {response.status_code}")

# PanelApp_Request_Parse.pk_search_parse(response.json(), 'GRch37')

### For testing purposes ###
R_code = 'R140'
response_R = RQ.R_search(R_code)

PanelApp_Request_Parse.search_parse(response_R.json(), 'GRch37')







