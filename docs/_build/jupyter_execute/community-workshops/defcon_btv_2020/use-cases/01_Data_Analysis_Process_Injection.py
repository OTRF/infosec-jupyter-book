# Process Injection - CreatRemoteThread
* **Author**: Jose Rodriguez (@Cyb3rPandah)
* **Project**: Infosec Jupyter Book
* **Public Organization**: [Open Threat Research](https://github.com/OTRF)
* **License**: [Creative Commons Attribution-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-sa/4.0/)
* **Reference**: 
    * https://spark.apache.org/docs/latest/api/python/pyspark.sql.html
    * https://docs.microsoft.com/en-us/windows/win32/procthread/process-security-and-access-rights

## Creating SQL view from Mordor Process Injection dataset

### Create Spark session

from pyspark.sql import SparkSession

spark = SparkSession \
    .builder \
    .appName("Spark_Data_Analysis") \
    .config("spark.sql.caseSensitive","True") \
    .getOrCreate()

### Unzip Mordor Dataset

! unzip -o ../datasets/empire_psinject.zip -d ../datasets/

### Expose the dataframe as a SQL view

processInjectionJson = '../datasets/empire_psinject_2020-08-07143205.json'

processInjectionDf = spark.read.json(processInjectionJson)

processInjectionDf.createOrReplaceTempView('processInjection')

## Filtering & Summarizing data

### Get most frecuent Access Flags (Bitmask) of Processes accessing other Processes

* Create dataframe

processAccess = spark.sql(
'''
SELECT GrantedAccess, count(*) as Count
FROM processInjection
WHERE lower(Channel) LIKE '%sysmon%'
    AND EventID = 10
GROUP BY GrantedAccess
ORDER BY Count DESC
''')

print('This dataframe has {} records!!'.format(processAccess.count()))
processAccess.show()

## Transforming data

### Create a Spark UDF to get the specific Access Rights related to every Bitmask

* Define a function

def getSpecificAccessRights(bitmask):
    bitmask = int(bitmask,16)
    specificAccessRights = {'PROCESS_CREATE_PROCESS' : 0x0080,
            'PROCESS_CREATE_THREAD' : 0x0002,
            'PROCESS_DUP_HANDLE' : 0x0040,
            'PROCESS_QUERY_INFORMATION' : 0x0400,
            'PROCESS_QUERY_LIMITED_INFORMATION' : 0x1000,
            'PROCESS_SET_INFORMATION' : 0x0200,
            'PROCESS_SET_QUOTA' : 0x0100,
            'PROCESS_SUSPEND_RESUME' : 0x0800,
            'PROCESS_TERMINATE' : 0x0001,
            'PROCESS_VM_OPERATION' : 0x0008,
            'PROCESS_VM_READ' : 0x0010,
            'PROCESS_VM_WRITE' : 0x0020,
            'SYNCHRONIZE' : 0x00100000,
            'PROCESS_SET_LIMITED_INFORMATION' : 0x2000}
    
    rights = [ ]
    
    for key,value in specificAccessRights.items():
        if value & bitmask != 0:
            rights.append(key)
    
    return rights

* Register Spark UDF

from pyspark.sql.types import *
spark.udf.register("getAccessRights", getSpecificAccessRights,ArrayType(StringType()))

* Apply the Spark UDF

processAccessRights = spark.sql(
'''
SELECT GrantedAccess, getAccessRights(GrantedAccess) as RightsRequested, count(*) as Count
FROM processInjection
WHERE lower(Channel) LIKE '%sysmon%'
    AND EventID = 10
GROUP BY GrantedAccess, RightsRequested
ORDER BY Count DESC
''')

print('This dataframe has {} records!!'.format(processAccessRights.count()))
processAccessRights.show(truncate = 80)

### Filter events that requested "Creation of Thread" rights

* Filter **PROCESS_CREATE_THREAD (0x0002)**: Required to create a thread.

createThread = spark.sql(
'''
SELECT GrantedAccess, SourceImage, TargetImage
FROM processInjection
WHERE lower(Channel) LIKE '%sysmon%'
    AND EventID = 10
    AND array_contains(getAccessRights(GrantedAccess),'PROCESS_CREATE_THREAD')
''')

print('This dataframe has {} records!!'.format(createThread.count()))
createThread.show(truncate = 80)

## Correlating data

### Find Source Processes that used CreateRemoteThread APIs

networkConnection = spark.sql(
'''
SELECT b. SourceImage, b.TargetImage, a.NewThreadId
FROM processInjection b
INNER JOIN(
    SELECT SourceProcessGuid, NewThreadId
    FROM processInjection
    WHERE lower(Channel) LIKE '%sysmon%'
        AND EventID = 8
)a
ON b.SourceProcessGUID = a.SourceProcessGuid
WHERE lower(Channel) LIKE '%sysmon%'
    AND b.EventID = 10
    AND array_contains(getAccessRights(GrantedAccess),'PROCESS_CREATE_THREAD')
''')

print('This dataframe has {} records!!'.format(networkConnection.count()))
networkConnection.show(truncate = 40)

### Find Target Processes that made Network Connections 

networkConnection = spark.sql(
'''
SELECT b.TargetImage, a.SourceIp, a.DestinationIp
FROM processInjection b
INNER JOIN(
    SELECT ProcessGuid, SourceIp, DestinationIp
    FROM processInjection
    WHERE lower(Channel) LIKE '%sysmon%'
        AND EventID = 3
)a
ON b.TargetProcessGUID = a.ProcessGuid
WHERE lower(Channel) LIKE '%sysmon%'
    AND b.EventID = 10
    AND array_contains(getAccessRights(GrantedAccess),'PROCESS_CREATE_THREAD')
''')

print('This dataframe has {} records!!'.format(networkConnection.count()))
networkConnection.show(truncate = 40)

## Thank you! I hope you enjoyed it!

