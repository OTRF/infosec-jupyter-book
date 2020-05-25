# Elasticsearch

* **Author:** Roberto Rodriguez (@Cyb3rWard0g)
* **Notes**: Download this notebook and use it to connect to your own Elasticsearch database. The BinderHub project might not allow direct connections to external entities on port 9092
* **References:**
    * https://medium.com/threat-hunters-forge/jupyter-notebooks-from-sigma-rules-%EF%B8%8F-to-query-elasticsearch-31a74cc59b99
    * https://github.com/target/huntlib

## Using Elasticsearch DSL

Pre-requisites:

* pip install elasticsearch
* pip install pandas
* pip install elasticsearch-dsl

### Import Libraries

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
import pandas as pd

### Initialize an Elasticsearch client

Initialize an Elasticsearch client using a specific Elasticsearch URL. Next, you can pass the client to the Search object that we will use to represent the search request in a little bit.

es = Elasticsearch(['http://<elasticsearch-ip>:9200'])
searchContext = Search(using=es, index='logs-*', doc_type='doc')

### Set the Query Search Context

In addition, we will need to use the query class to pass an Elasticsearch query_string . For example, what if I want to query event_id 1 events?.

s = searchContext.query('query_string', query='event_id:1')

### Run Query & Explore Response

Finally, you can run the query and get the results back as a DataFrame

response = s.execute()

if response.success():
    df = pd.DataFrame((d.to_dict() for d in s.scan()))

df

## Using HuntLib (@DavidJBianco)

Pre-requisites:

* pip install huntlib

### Import Library

from huntlib.elastic import ElasticDF

### Create Connection
Create a plaintext connection to the Elastic server, no authentication

e = ElasticDF(
    url="http://localhost:9200"
)

### Search ES
A more complex example, showing how to set the Elastic document type, use Python-style datetime objects to constrain the search to a certain time period, and a user-defined field against which to do the time comparisons. The result size will be limited to no more than 1500 entries.

df = e.search_df(
  lucene="item:5285 AND color:red",
  index="myindex-*",
  doctype="doc", date_field="mydate",
  start_time=datetime.now() - timedelta(days=8),
  end_time=datetime.now() - timedelta(days=6),
  limit=1500
)