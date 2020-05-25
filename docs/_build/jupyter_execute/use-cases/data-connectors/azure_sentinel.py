# Azure Sentinel

* **Author:** Roberto Rodriguez (@Cyb3rWard0g)
* **Notes**: You can run this notebook from BinderHub! On the top right of your screen click on the rocket and then the BinderHub badge.
* **References:**
    * https://github.com/Azure/Azure-Sentinel-Notebooks

## Using MSTICpy

Pre-requisites:

* pip install pandas
* pip install msticpy

### Import Libraries

import os

import pandas as pd
from msticpy.nbtools.wsconfig import WorkspaceConfig
from msticpy.data.data_providers import QueryProvider
os.environ["KQLMAGIC_LOAD_MODE"]="silent"

### Define Connection String
We are going to authenticate to our demo workspace with an AppKey. Therefore, there is no need for you to pass an azure account or authenticate with your credentials! This is a great demo environment to test your notebooks!

connect_str = f"loganalytics://workspace='DEMO_WORKSPACE';appkey='DEMO_KEY';alias='myworkspace'"
qry_prov = QueryProvider("LogAnalytics")
qry_prov.connect(connect_str)

### Native Kqlmagic interface
See https://github.com/Microsoft/jupyter-Kqlmagic

%kql SecurityEvent | take 1

### MSITCPy query interface

alerts_df = qry_prov.exec_query("""
SecurityAlert 
| take 10
""")
print(type(alerts_df))
alerts_df.head(5)

#### Send queries of arbitrary complexity (using `%%kql` or `msticpy`)

events_df = qry_prov.exec_query("""
SecurityEvent
| where TimeGenerated between (ago(1d) .. now())
| summarize EventCount=count() by EventID
""")
display(events_df.head(5))
events_df.plot.bar(x="EventID")

#### Simple parameterization of queries

from datetime import datetime, timedelta
param_query = """
SecurityEvent
| where TimeGenerated between (datetime({start}) .. datetime({end}))
| summarize EventCount=count() by EventID
"""

end = datetime.utcnow()
start = end - timedelta(3)

events_df = qry_prov.exec_query(
    param_query.format(start=start, end=end)
)

display(events_df.head(5))
events_df.plot.scatter(x="EventID", y="EventCount", figsize=(15, 4), s=50, c="EventCount", colormap="viridis")

