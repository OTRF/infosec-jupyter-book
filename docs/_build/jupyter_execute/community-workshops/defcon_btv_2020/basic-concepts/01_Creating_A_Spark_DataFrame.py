# Creating a Spark Dataframe

* **Author**: Jose Rodriguez (@Cyb3rPandah)
* **Project**: Infosec Jupyter Book
* **Public Organization**: [Open Threat Research](https://github.com/OTRF)
* **License**: [Creative Commons Attribution-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-sa/4.0/)
* **Reference**: https://mordordatasets.com/introduction.html

## Importing Spark libraries

from pyspark.sql import SparkSession

## Creating Spark session

spark = SparkSession \
    .builder \
    .appName("Spark_example") \
    .config("spark.sql.caseSensitive","True") \
    .getOrCreate()

spark

## Creating a Spark Sample DataFrame

### Create sample data

Security event logs

eventLogs = [('Sysmon',1,'Process creation'),
             ('Sysmon',2,'A process changed a file creation time'),
             ('Sysmon',3,'Network connection'),
             ('Sysmon',4,'Sysmon service state changed'),
             ('Sysmon',5,'Process terminated'),
             ('Security',4688,'A process has been created'),
             ('Security',4697,'A service was installed in the system')]

type(eventLogs)

### Define dataframe schema

from pyspark.sql.types import *

schema = StructType([
   StructField("Channel", StringType(), True),
   StructField("Event_Id", IntegerType(), True),
   StructField("Description", StringType(), True)])

### Create Spark datarame

eventLogsDf = spark.createDataFrame(eventLogs,schema)

eventLogsDf.show(truncate = False)

type(eventLogsDf)

## Exposing Spark DataFrame as a SQL View

eventLogsDf.createOrReplaceTempView('eventLogs')

## Testing a SQL-like Query

Filtering on **Sysmon** event logs

sysmonEvents = spark.sql(
'''
SELECT *
FROM eventLogs
WHERE Channel = 'Sysmon'
''')

sysmonEvents.show(truncate = False)

## Thank you! I hope you enjoyed it!