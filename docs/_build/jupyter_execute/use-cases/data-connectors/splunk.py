# Splunk

* **Author:** Roberto Rodriguez (@Cyb3rWard0g)
* **Notes**: Download this notebook and use it to connect to your own Splunk instance. The BinderHub project might not allow direct connections to external entities on not common ports
* **References:**
    * https://github.com/target/huntlib

## Using HuntLib (@DavidJBianco)

Pre-requisites:

* pip install huntlib

### Import Library

from huntlib.splunk import SplunkDF

### Search

df = s.search_df(
  spl="search index=win_events EventCode=4688",
  start_time="-2d@d",
  end_time="@d"
)

