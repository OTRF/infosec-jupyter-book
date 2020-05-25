# SQL to Pandas with Windows Events 101
* **Author**: Jose Rodriguez (@Cyb3rPandah)
* **Project**: Infosec Jupyter Book
* **Public Organization**: [Open Threat Research](https://github.com/OTRF)
* **License**: [Creative Commons Attribution-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-sa/4.0/)
* **Reference**: https://pandas.pydata.org/docs/getting_started/comparison/comparison_with_sql.html

## Description

This notebook was created as part of the Open Threat Research (OTR) initiative to empower others in the InfoSec community around the world.

With more security analysts getting into data analysis with Python and Jupyter Notebooks, I figured it would be a good idea to create a notebook and share some of my experience with Pandas. Since many analysts in our community are familiar with SQL syntax to craft detection rules, I used it in this notebook to show how easy it is to translate SQL logic to pandas statements. I leveraged this doc "[Comparison with SQL](https://pandas.pydata.org/docs/getting_started/comparison/comparison_with_sql.html)" to organize the notebook and make sure I align my queries and descriptions to official pandas resources.

### Pre-requisites - Reading
* [Intro to Pandas](https://infosecjupyterbook.com/introduction.html)

## Importing Libraries
Pre-requisites:

* pip install pandas
* pip install openhunt

import pandas as pd
import numpy as np

from openhunt import mordorutils as mu

# Do not truncate Pandas output
pd.set_option('display.max_colwidth', None)

## Importing Mordor Demo Dataset

* Every time I practice or learn something new, I make sure I work on examples that are related to the field where I would implement what I learn to. Therefore, for this notebook, I used a dataset from the [Mordor Project](https://mordordatasets.com/introduction.html) to show you how you can use Pandas to explore a few techniques that were emulated following the [ATT&CK Evals Emulation Plans](https://github.com/hunters-forge/mordor/blob/master/datasets/large/apt29/emulationplans/apt29.xlsx).
* This dataset is a subset of the [Mordor ATT&CK Evals APT29 - Day 1](https://github.com/hunters-forge/mordor/tree/master/datasets/large/apt29). It includes only a few events for the purpose of this notebook. Feel free to download the full dataset on your own. Make sure you allocate enough memory to your local Jupyter Notebooks server since we are using pandas to read the JSON file (dataset).

Let's start by using the `getMordorZipFile` method from the `mordorutils` module to download and decompress the dataset:

mordorUrl = 'https://github.com/OTRF/infosec-jupyter-book/blob/master/datasets/apt29_evals_day1_manual_demo.zip'
mordorFilePath= mu.getMordorZipFile(mordorUrl)

## Reading JSON Mordor File

Next, we use the `read_json` method from `pandas` to read the JSON file (Decompressed dataset) that returns a DataFrame. We are going to use that variable throughout the notebook.

apt29 = pd.read_json("apt29_evals_day1_manual_2020-05-01225525_demo.json")

apt29.head()

## Leveraging Pandas for Security from a SQL perspective

## SELECT 

In SQL, selection is done using a **comma-separated list** of columns you'd like to select. You can use the `*` character to select all the available columnsin the SQL table.

```
SELECT Hostname, Channel, EventTime, EventID
FROM apt29
LIMIT 5;
```

With pandas, column selection is done by passing a list of column names to your DataFrame. We can select a few columns from the APT29 dataset as shown below:

(
apt29[['Hostname','Channel','EventTime','EventID']]
.head(5)
)

Calling the DataFrame **without the list of column** names would **display all columns** (Similar to SQL's *).

### Calculated Column

In SQL, you can add a **calculated column** or **computed column**. A computed column is a virtual column that is not physically stored in the table and can use data from other columns to calculate a new value.

```
SELECT Hostname, Channel, EventTime, EventID,
       len(Hostname) as Hostname_Length
FROM apt29
LIMIT 5;
```

With pandas, you can use the **DataFrame.assign()** method of a DataFrame to append a new column. As a proof of concept, we can add a new column named **Hostname_Length** to the right of our DataFrame to calculate the number of characters in the Hostname field. We are going to show another example that could provide more context to our data analysis.

(
apt29[['Hostname','Channel','EventTime','EventID']]

.assign(Hostname_Length = apt29['Hostname'].str.len())

.head(5)
)

## WHERE

Filtering in SQL is done via a WHERE clause.

```
SELECT Hostname, Channel, EventTime, EventID,
       len(Hostname) as Hostname_Length
FROM apt29
WHERE Channel = 'Windows PowerShell'
LIMIT 5;
```

DataFrames can be **filtered** in multiple ways. According to pandas docs, the most intuitive way is by using **boolean indexing**. We can filter our APT29 DataFrame and show only Windows events from the **Microsoft-Windows-Sysmon/Operational** provider.

(
apt29[['Hostname','Channel','EventTime','EventID']]

.assign(Hostname_Length = apt29['Hostname'].str.len())
    
[apt29['Channel'] == 'Microsoft-Windows-Sysmon/Operational']
    
.head(5)
)

### OR & AND Boolean Operators
Just like SQL’s **OR** and **AND**, multiple conditions can be passed to a DataFrame using | (OR) and & (AND). We can use an **AND** operator in our APT29 DataFrame and only show Sysmon events of ID 1. In this example, I also show you how to use the **calculated columns** concept, that we learnerd earlier, to the **CommandLine** field to calculate the lenght of the command line used by the new process created.

```
SELECT Hostname, Channel, EventTime, EventID, CommandLine
       len(CommandLine) as CommandLineLength
FROM apt29
WHERE Channel = 'Microsoft-Windows-Sysmon/Operational' AND EventID = 1
LIMIT 5;
```

(
apt29[['Hostname','Channel','EventTime','EventID','CommandLine']]

.assign(CommandLineLength = apt29['CommandLine'].str.len())
    
[(apt29['Channel'] == 'Microsoft-Windows-Sysmon/Operational') & (apt29['EventID'] == 1)]

.head(5)
)

We can practice also combinations of **AND** and **OR** boolean operators with Sysmon registry events. Let's use Event ID 12 (Object create and delete) and 13 (Value Set).

```
SELECT Channel, EventID, ProcessGuid, ProcessId, Image, TargetObject, NewName
FROM apt29
WHERE Channel = 'Microsoft-Windows-Sysmon/Operational' AND (EventID = 12 OR eventID = 13)
LIMIT 5;
```

(
apt29[['Channel','EventID','ProcessGuid','ProcessId','Image','TargetObject']]
    
[(apt29['Channel'] == 'Microsoft-Windows-Sysmon/Operational') 
 
     & ((apt29['EventID'] == 12) | (apt29['EventID'] == 13))]

.head()
)

#### Looking for new applications being executed for the first time

We can use what we have learned so far and look for new application in the AppCompat registery keys. This is an indicator of applications executing for the first time.

(
apt29[['EventID','ProcessId','Image','TargetObject']]
    
[(apt29['Channel'] == 'Microsoft-Windows-Sysmon/Operational') 
 
     & ((apt29['EventID'] == 12) | (apt29['EventID'] == 13))
     
     & ((apt29['TargetObject'].str.contains('.*AppCompatFlags\\\\Compatibility Assistant.*', regex=True)))]

.head(10)
)

### NULL Checking

NULL checking is done using the **notna()** and **isna()** methods.

We can show records where **CommandLine** field **IS NULL** with the following query. This query is built on the top of previous ones.

```
SELECT Hostname, Channel, EventTime, EventID, CommandLine
       len(CommandLine) as CommandLineLength
FROM apt29
WHERE Channel = 'Microsoft-Windows-Sysmon/Operational' AND EventID = 1 AND CommandLine IS NULL
LIMIT 5;
```

(
apt29[['Hostname','Channel','EventTime','EventID','CommandLine']]

.assign(CommandLineLength = apt29['CommandLine'].str.len())
    
[(apt29['Channel'] == 'Microsoft-Windows-Sysmon/Operational') 
     & (apt29['EventID'] == 1) & (apt29['CommandLine'].isna())]
    
.head(5)
)

Getting items where **CommandLine** field **IS NOT NULL** can be done with notna().

```
SELECT Hostname, Channel, EventTime, EventID, CommandLine
       len(CommandLine) as CommandLineLength
FROM apt29
WHERE Channel = 'Microsoft-Windows-Sysmon/Operational' AND EventID = 1 AND CommandLine IS NOT NULL
LIMIT 5;
```

(
apt29[['Hostname','Channel','EventTime','EventID','CommandLine']]

.assign(CommandLineLength = apt29['CommandLine'].str.len())
    
[(apt29['Channel'] == 'Microsoft-Windows-Sysmon/Operational') 
     & (apt29['EventID'] == 1) & (apt29['CommandLine'].notna())]
    
.head(5)
)

## GROUP BY

In pandas, SQL’s **GROUP BY** operations are performed using the similarly named **groupby()** method. groupby() typically refers to a process where we’d like to split a dataset into groups, apply some function (typically aggregation) , and then combine the groups together.

We can count and group our APT29 DataFrame by the **Hostname** field.

```
SELECT Hostname, Channel, EventTime, EventID, CommandLine, Image,
       len(CommandLine) as CommandLineLength, count(*)
FROM apt29
GROUP BY Hostname
WHERE Channel = 'Microsoft-Windows-Sysmon/Operational' AND EventID = 1;
```

The pandas equvalent would be:

(
apt29[['Hostname','Channel','EventTime','EventID','CommandLine','Image']]

.assign(CommandLineLength = apt29['CommandLine'].str.len())
    
[(apt29['Channel'] == 'Microsoft-Windows-Sysmon/Operational') & (apt29['EventID'] == 1)]
    
.groupby('Hostname').size()
)

We can use this technique and group Sysmon Event ID 1 events by the process name.

(
apt29[['Hostname','Channel','EventTime','EventID','CommandLine','Image']]

.assign(CommandLineLength = apt29['CommandLine'].str.len())
    
[(apt29['Channel'] == 'Microsoft-Windows-Sysmon/Operational') & (apt29['EventID'] == 1)]
    
.groupby('Image').size()
).to_frame()

In the previous example, I used **size()** and not **count()**. This is because **count()** applies the function to every column and the result does not consider **null records**.

(
apt29[['Hostname','Channel','EventTime','EventID','CommandLine','Image']]

.assign(CommandLineLength = apt29['CommandLine'].str.len())
    
[(apt29['Channel'] == 'Microsoft-Windows-Sysmon/Operational') & (apt29['EventID'] == 1)]
    
.groupby('Hostname').count()
)

Alternatively, we can also use the **count()** method to a specific column. In the example below, we are doing it on the **CommandLine** column.

(
apt29[['Hostname','Channel','EventTime','EventID','CommandLine','Image']]

.assign(CommandLineLength = apt29['CommandLine'].str.len())
    
[(apt29['Channel'] == 'Microsoft-Windows-Sysmon/Operational') & (apt29['EventID'] == 1)]
    
.groupby('Hostname')['CommandLine'].count()
)

### Multiple Functions

We can use multiple functions at once for a specific column. For instance, we can apply the **len()** and **avg()** functions to the field **CommandLineLength**. Then, we can group the results by the **Hostname** field.

```
SELECT Hostname, Channel, EventTime, EventID, CommandLine, Image,
       len(CommandLine) as CommandLineLength, AVG(CommandLine_Length), COUNT(*)
FROM apt29
GROUP BY Hostname
WHERE Channel = 'Microsoft-Windows-Sysmon/Operational' AND EventID = 1;
```

(
apt29[['Hostname','Channel','EventTime','EventID','CommandLine','Image']]

.assign(CommandLineLength = apt29['CommandLine'].str.len())
    
[(apt29['Channel'] == 'Microsoft-Windows-Sysmon/Operational') & (apt29['EventID'] == 1)]
    
.groupby('Hostname').agg({'CommandLineLength': np.mean, 'Channel': np.size})
)

### Grouping By more than one column

Grouping by more than one column is done by passing a list of columns to the **groupby()** method.

```
SELECT Hostname, Channel, EventTime, EventID, CommandLine, Image,
       len(CommandLine) as CommandLineLength, COUNT(*), AVG(CommandLine_Length)
FROM apt29
GROUP BY Hostname, Image
WHERE Channel = 'Microsoft-Windows-Sysmon/Operational' AND EventID = 1
LIMIT 20;
```

(
apt29[['Hostname','Channel','EventTime','EventID','CommandLine','Image']]

.assign(CommandLineLength = apt29['CommandLine'].str.len())
    
[(apt29['Channel'] == 'Microsoft-Windows-Sysmon/Operational') & (apt29['EventID'] == 1)]
    
.groupby(['Hostname','Image']).agg({'CommandLineLength': [np.mean, np.size]})

.head(20)
)

## JOIN

JOINs can be performed with **join()** or **merge()**. By default, join() will join the DataFrames on their indices if a type of join is not specified. Each method has parameters allowing you to specify the type of join to perform **(LEFT, RIGHT, INNER, FULL)** or the columns to join on **(column names or indices)**.

# Creating a dataframe with information of Security event 4624: An account was successfully logged on
Security4624 = apt29[(apt29['Channel'].str.lower() == 'security') & (apt29['EventID'] == 4624)].dropna(axis = 1, how = 'all')
Security4624.shape

# Creating a dataframe with information of Security event 4688: A new process has been created
Security4688 = apt29[(apt29['Channel'].str.lower() == 'security') & (apt29['EventID'] == 4688)].dropna(axis = 1, how = 'all')
Security4688.shape

# Creating a dataframe with information of Security event 4697: A service was installed in the system
Security4697 = apt29[(apt29['Channel'].str.lower() == 'security') & (apt29['EventID'] == 4697)].dropna(axis = 1, how = 'all')
Security4697.shape

### INNER JOIN

In the example below, we are looking for **New Processes** being created by accounts that were authenticated over the network (Logon Type 3). This query looks for potential **Lateral Movement** techniques. Without looking for **"wsmprovhost.exe"** which is an indication of **PSRemoting**, I was able to get there by focusing on the behavior of accounts authenticating over the network and creating new processes.

SELECT x.NewProcessId,x.NewProcessName,x.ProcessId,x.ParentProcessName,y.TargetUserName, y.IpAddress
FROM Security4688 x
INNER JOIN (FROM Security4624 WHERE LogonType = 3) y
  ON x.TargetLogonId = y.TargetLogonId;

# merge performs an INNER JOIN by default
(
pd.merge(Security4688, Security4624[Security4624['LogonType'] == 3],
         on = 'TargetLogonId', how = 'inner')
[['NewProcessId','NewProcessName','ProcessId_x','ParentProcessName','TargetUserName_y','IpAddress']]
)

When the column names where we are performing the join on are different, we need to use the **left_on** and **right_on** parameters as shown below. In this example, we are looking for **New Services** being installed by accounts that were authenticated over the network (Logon Type 3). This query looks for potential **Lateral Movement** techniques. I was able to identify the use pf PSEXEC in the dataset. Once again, I was not looking for the specific service name. I was focusing on the behavior of accounts that authenticate over the network and installing new services.

```
SELECT x.ServiceName, x.ServiceFileName, y.IpAddress
FROM Security4697 x
INNER JOIN (FROM Security4624 WHERE LogonType = 3) y
  ON x.SubjectLogonId = y.TargetLogonId;
```

# merge performs an INNER JOIN by default
(
pd.merge(Security4697, Security4624[Security4624['LogonType'] == 3],
         left_on = 'SubjectLogonId', right_on = 'TargetLogonId', how = 'inner')
[['ServiceName', 'ServiceFileName','IpAddress']]
)

### LEFT OUTER JOIN

Same query as before, but in the example below we use the **LEFT** join type for the **how** parameter. We can see a new service installed named **javamtsup**. If you look at the emulation plan for Day 1, we know tha the javamtsup service was installed locally and not over the network. That service was used for persistence.

(
pd.merge(Security4697, Security4624[Security4624['LogonType'] == 3],
         left_on = 'SubjectLogonId', right_on = 'TargetLogonId', how = 'left')
[['ServiceName', 'ServiceFileName','IpAddress']]
)

### RIGHT JOIN

Same query as before, but in the example below we use the **RIGHT** join type for the **how** parameter. We can see also a new service installing

(
pd.merge(Security4697, Security4624[Security4624['LogonType'] == 3],
         left_on = 'SubjectLogonId', right_on = 'TargetLogonId', how = 'right')
[['ServiceName', 'ServiceFileName','IpAddress']]
)

### FULL JOIN

pandas also allows for FULL JOINs, which display both sides of the dataset, whether or not the joined columns find a match. As of writing, FULL JOINs are not supported in all RDBMS (MySQL).

(
pd.merge(Security4697, Security4624[Security4624['LogonType'] == 3],
         left_on = 'SubjectLogonId', right_on = 'TargetLogonId', how = 'outer')
[['ServiceName', 'ServiceFileName','IpAddress']]
)

## Thank you! I hope you enjoyed it!

