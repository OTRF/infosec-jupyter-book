# Data Analysis with Spark.SQL: Filtering & Summarizing
* **Author**: Jose Rodriguez (@Cyb3rPandah)
* **Project**: Infosec Jupyter Book
* **Public Organization**: [Open Threat Research](https://github.com/OTRF)
* **License**: [Creative Commons Attribution-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-sa/4.0/)
* **Reference**: https://spark.apache.org/docs/latest/api/python/pyspark.sql.html

## Creating SQL view from Mordor APT29 dataset

### Create Spark session

from pyspark.sql import SparkSession

spark = SparkSession \
    .builder \
    .appName("Spark_Data_Analysis") \
    .config("spark.sql.caseSensitive","True") \
    .getOrCreate()

### Expose the dataframe as a SQL view

apt29Json = '../datasets/apt29_evals_day1_manual_2020-05-01225525.json'

apt29Df = spark.read.json(apt29Json)

apt29Df.createOrReplaceTempView('apt29')

## Filtering & Summarizing data

### Filter Sysmon event 8 (Create Remote Thread) data

sysmon8 = spark.sql(
'''
SELECT SourceImage, TargetImage, StartFunction
FROM apt29
WHERE Channel = 'Microsoft-Windows-Sysmon/Operational' AND EventID = 8
''')

print('This dataframe has {} records!!'.format(sysmon8.count()))
sysmon8.show(n = 5, truncate = False)

### Filter PowerShell processes within Sysmon event 8 (Create Remote Thread) data

sysmon8 = spark.sql(
'''
SELECT SourceImage, TargetImage, StartFunction
FROM apt29
WHERE Channel = 'Microsoft-Windows-Sysmon/Operational'
    AND EventID = 8
    AND SourceImage LIKE '%powershell.exe%'
''')

print('This dataframe has {} records!!'.format(sysmon8.count()))
sysmon8.show(truncate = False)

## SUMMARIZING data

### Stack Count event logs by source of data and event id

eventLogs = spark.sql(
'''
SELECT Channel, EventID, COUNT(*)
FROM apt29
GROUP BY Channel, EventID
ORDER BY COUNT(*) DESC
''')

print('This dataframe has {} records!!'.format(eventLogs.count()))
eventLogs.show(truncate = False)

### Filtering event logs groups with frequency less or equal to 500

eventLogsLess = spark.sql(
'''
SELECT Channel, EventID, COUNT(*) as Count
FROM apt29
GROUP BY Channel, EventID
HAVING Count <= 500
ORDER BY Count DESC
''')

print('This dataframe has {} records!!'.format(eventLogsLess.count()))
eventLogsLess.show(truncate = False)

## Thank you! I hope you enjoyed it!