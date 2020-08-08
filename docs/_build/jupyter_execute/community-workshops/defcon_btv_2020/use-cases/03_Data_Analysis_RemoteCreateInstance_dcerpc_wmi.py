# Remote Create Instance - dcerpc - wmi
* **Author**: Jose Rodriguez (@Cyb3rPandah)
* **Project**: Infosec Jupyter Book
* **Public Organization**: [Open Threat Research](https://github.com/OTRF)
* **License**: [Creative Commons Attribution-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-sa/4.0/)
* **Reference**: 
    * https://spark.apache.org/docs/latest/api/python/pyspark.sql.html
    * https://threathunterplaybook.com/notebooks/windows/08_lateral_movement/WIN-190810201010.html

## Creating SQL view from Mordor Process Injection dataset

### Create Spark session

from pyspark.sql import SparkSession

spark = SparkSession \
    .builder \
    .appName("Spark_Data_Analysis") \
    .config("spark.sql.caseSensitive","True") \
    .getOrCreate()

### Unzip Mordor Dataset

! unzip -o ../datasets/covenant_sharpwmi_dcerpc_wmi_remotecreateinstance.zip -d ../datasets/

### Expose the dataframe as a SQL view

wmiJson = '../datasets/covenant_sharpwmi_dcerpc_wmi_remotecreateinstance_2020-08-06035621.json'

wmiDf = spark.read.json(wmiJson)

wmiDf.createOrReplaceTempView('wmi')

## Technical Description
WMI is the Microsoft implementation of the Web-Based Enterprise Management (WBEM) and Common Information Model (CIM).
Both standards aim to provide an industry-agnostic means of collecting and transmitting information related to any managed component in an enterprise.
An example of a managed component in WMI would be a running process, registry key, installed service, file information, etc.
At a high level, Microsoft’s implementation of these standards can be summarized as follows > Managed Components Managed components are represented as WMI objects — class instances representing highly structured operating system data. Microsoft provides a wealth of WMI objects that communicate information related to the operating system. E.g. Win32_Process, Win32_Service, AntiVirusProduct, Win32_StartupCommand, etc.

One well known lateral movement technique is performed via the WMI object — class Win32_Process and its method Create.
This is because the Create method allows a user to create a process either locally or remotely.
One thing to notice is that when the Create method is used on a remote system, the method is run under a host process named “Wmiprvse.exe”.

The process WmiprvSE.exe is what spawns the process defined in the CommandLine parameter of the Create method. Therefore, the new process created remotely will have Wmiprvse.exe as a parent. WmiprvSE.exe is a DCOM server and it is spawned underneath the DCOM service host svchost.exe with the following parameters C:\WINDOWS\system32\svchost.exe -k DcomLaunch -p.
From a logon session perspective, on the target, WmiprvSE.exe is spawned in a different logon session by the DCOM service host. However, whatever is executed by WmiprvSE.exe occurs on the new network type (3) logon session created by the user that authenticated from the network.

Additional Reading
* https://github.com/hunters-forge/ThreatHunter-Playbook/tree/master/docs/library/logon_session.md

## Filtering data

### Look for wmiprvse.exe spawning processes that are part of non-system account sessions.

processCreation = spark.sql(
'''
SELECT `@timestamp`, Hostname, SubjectUserName, TargetUserName, NewProcessName, CommandLine
FROM wmi
WHERE lower(Channel) = "security"
    AND EventID = 4688
    AND lower(ParentProcessName) LIKE "%wmiprvse.exe"
    AND NOT TargetLogonId = "0x3e7"
''')

print('This dataframe has {} records!!'.format(processCreation.count()))
processCreation.show(vertical = True, truncate = False)

## Correlating data

### Look for non-system accounts leveraging WMI over the netwotk to execute code

authenticationNetwork = spark.sql(
'''
SELECT o.`@timestamp`, o.Hostname, o.SubjectUserName, o.TargetUserName, o.NewProcessName, o.CommandLine, a.IpAddress
FROM wmi o
INNER JOIN (
    SELECT Hostname,TargetUserName,TargetLogonId,IpAddress
    FROM wmi
    WHERE lower(Channel) = "security"
        AND LogonType = 3
        AND IpAddress IS NOT NULL
        AND NOT TargetUserName LIKE "%$"
    ) a
ON o.TargetLogonId = a.TargetLogonId
WHERE lower(o.Channel) = "security"
    AND o.EventID = 4688
    AND lower(o.ParentProcessName) LIKE "%wmiprvse.exe"
    AND NOT o.TargetLogonId = "0x3e7"
'''
)

print('This dataframe has {} records!!'.format(authenticationNetwork.count()))
authenticationNetwork.show(vertical = True, truncate = False)

## Thank you! I hope you enjoyed it!