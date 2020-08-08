# DCSync dcerpc dcerpc
* **Author**: Jose Rodriguez (@Cyb3rPandah)
* **Project**: Infosec Jupyter Book
* **Public Organization**: [Open Threat Research](https://github.com/OTRF)
* **License**: [Creative Commons Attribution-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-sa/4.0/)
* **Reference**: 
    * https://spark.apache.org/docs/latest/api/python/pyspark.sql.html
    * https://threathunterplaybook.com/notebooks/windows/06_credential_access/WIN-180815210510.html

## Creating SQL view from Mordor DCSync dataset

### Create Spark session

from pyspark.sql import SparkSession

spark = SparkSession \
    .builder \
    .appName("Spark_Data_Analysis") \
    .config("spark.sql.caseSensitive","True") \
    .getOrCreate()

### Unzip Mordor Dataset

! unzip -o ../datasets/covenant_dcsync_dcerpc_drsuapi_DsGetNCChanges.zip -d ../datasets/

### Expose the dataframe as a SQL view

dcSyncJson = '../datasets/covenant_dcsync_dcerpc_drsuapi_DsGetNCChanges_2020-08-05020926.json'

dcSyncDf = spark.read.json(dcSyncJson)

dcSyncDf.createOrReplaceTempView('dcSync')

## Technical Description
Active Directory replication is the process by which the changes that originate on one domain controller are automatically transferred to other domain controllers that store the same data.
Active Directory data takes the form of objects that have properties, or attributes. Each object is an instance of an object class, and object classes and their respective attributes are defined in the Active Directory schema.
The values of the attributes define the object, and a change to a value of an attribute must be transferred from the domain controller on which it occurs to every other domain controller that stores a replica of that object.
An adversary can abuse this model and request information about a specific account via the replication request.
This is done from an account with sufficient permissions (usually domain admin level) to perform that request.
Usually the accounts performing replication operations in a domain are computer accounts (i.e dcaccount$).
Therefore, it might be abnormal to see other non-dc-accounts doing it.

The following access rights / permissions are needed for the replication request according to the domain functional level

| Control access right symbol | Identifying GUID used in ACE |
| :-----------------------------| :------------------------------|
| DS-Replication-Get-Changes | 1131f6aa-9c07-11d1-f79f-00c04fc2dcd2 |
| DS-Replication-Get-Changes-All | 1131f6ad-9c07-11d1-f79f-00c04fc2dcd2 |
| DS-Replication-Get-Changes-In-Filtered-Set | 89e95b76-444d-4c62-991a-0facbeda640c |

Additional reading
* https://github.com/hunters-forge/ThreatHunter-Playbook/tree/master/docs/library/active_directory_replication.md

## Filtering & Summarizing data

### What Users used replication request rights

operationObject = spark.sql(
'''
SELECT `@timestamp`, Hostname, SubjectUserName, SubjectLogonId
FROM dcSync
WHERE Channel = "Security"
    AND EventID = 4662
    AND AccessMask = "0x100"
    AND (
        Properties LIKE "%1131f6aa_9c07_11d1_f79f_00c04fc2dcd2%"
        OR Properties LIKE "%1131f6ad_9c07_11d1_f79f_00c04fc2dcd2%"
        OR Properties LIKE "%89e95b76_444d_4c62_991a_0facbeda640c%"
    )
    AND NOT SubjectUserName LIKE "%$"
''')

print('This dataframe has {} records!!'.format(operationObject.count()))
operationObject.show(truncate = False)

## Correlating data

### Get more information about the Endpoint that requested the replication

authentication = spark.sql(
    '''
SELECT o.`@timestamp`, o.Hostname, o.SubjectUserName, o.SubjectLogonId, a.IpAddress
FROM dcSync o
INNER JOIN (
    SELECT Hostname,TargetUserName,TargetLogonId,IpAddress
    FROM dcSync
    WHERE lower(Channel) = "security"
        AND EventID = 4624
        AND LogonType = 3
        AND IpAddress IS NOT NULL
        AND NOT TargetUserName LIKE "%$"
    ) a
ON o.SubjectLogonId = a.TargetLogonId
WHERE lower(o.Channel) = "security"
    AND o.EventID = 4662
    AND o.AccessMask = "0x100"
    AND (
        o.Properties LIKE "%1131f6aa_9c07_11d1_f79f_00c04fc2dcd2%"
        OR o.Properties LIKE "%1131f6ad_9c07_11d1_f79f_00c04fc2dcd2%"
        OR o.Properties LIKE "%89e95b76_444d_4c62_991a_0facbeda640c%"
    )
    AND o.Hostname = a.Hostname
    AND NOT o.SubjectUserName LIKE "%$"
    '''
)

print('This dataframe has {} records!!'.format(authentication.count()))
authentication.show(truncate = False)

## Thank you! I hope you enjoyed it!