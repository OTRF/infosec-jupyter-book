# Data Analysis with Spark.SQL: Correlating
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

## Correlating data

### Get new Processes created by an Account that Logged On over the network

lateralMovement = spark.sql(
'''
SELECT b.SubjectUserName, b.TargetUserName, b.NewProcessName, b.ParentProcessName, a.IpAddress
FROM apt29 b
INNER JOIN(
    SELECT TargetLogonId, LogonType, IpAddress
    FROM apt29
    WHERE lower(Channel) LIKE '%security%'
        AND EventID = 4624
        AND LogonType = 3
    )a
ON a.TargetLogonId = b.TargetLogonId
WHERE lower(b.Channel) LIKE '%security%'
    AND b.EventID = 4688
''')

print('This dataframe has {} records!!'.format(lateralMovement.count()))
lateralMovement.show(truncate = False)

### Add context (Parent Process) to Network Connection events

parentProcess = spark.sql(
'''
SELECT b.Image, b.SourceIp, b.DestinationIp, a.ParentImage
FROM apt29 b
LEFT JOIN(
    SELECT ProcessGuid, ParentImage
    FROM apt29
    WHERE lower(Channel) LIKE '%sysmon%'
        AND EventID = 1
    )a
ON a.ProcessGuid = b.ProcessGuid
WHERE lower(b.Channel) LIKE '%sysmon%'
    AND b.EventID = 3
''')

print('This dataframe has {} records!!'.format(parentProcess.count()))
parentProcess.show(n = 5, truncate = 25)

### Add context (Parent Process) to Processes that made a  Network Connection and modified a Registry Value

modifyRegistry = spark.sql(
'''
SELECT d.ParentImage, c.Image, c.SourceIp, c.DestinationIp, c.TargetObject
FROM apt29 d
RIGHT JOIN(
    SELECT b.ProcessGuid, b.Image, b.SourceIp, b.DestinationIp, a.TargetObject
    FROM apt29 b
    INNER JOIN(
        SELECT ProcessGuid, TargetObject
        FROM apt29
        WHERE lower(Channel) LIKE '%sysmon%'
            AND EventID = 13
        )a
    ON b.ProcessGuid = a.ProcessGuid
    WHERE lower(b.Channel) LIKE '%sysmon%'
        AND b.EventID = 3
)c
ON d.ProcessGuid = c.ProcessGuid
WHERE lower(d.Channel) LIKE '%sysmon%'
    AND d.EventID = 1
''')

print('This dataframe has {} records!!'.format(modifyRegistry.count()))
modifyRegistry.show(n = 1, vertical = True,truncate = False)

## Thank you! I hope you enjoyed it!