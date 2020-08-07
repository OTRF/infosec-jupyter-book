# Creating a Spark SQL View from a Mordor Dataset

* **Author**: Jose Rodriguez (@Cyb3rPandah)
* **Project**: Infosec Jupyter Book
* **Public Organization**: [Open Threat Research](https://github.com/OTRF)
* **License**: [Creative Commons Attribution-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-sa/4.0/)
* **Reference**: https://mordordatasets.com/introduction.html

## Extracting Mordor JSON File

### Get compressed Zip file

We are using the **wget** command and the **-O** (output document file) option to save the file in **datasets** folder

! wget https://raw.githubusercontent.com/hunters-forge/mordor/master/datasets/large/apt29/day1/apt29_evals_day1_manual.zip  -O datasets/apt29_evals_day1_manual.zip

### Extract JSON file

We are using the **unzip** command and **-o** (Overwrite) and **-d** (different directory) options to save the file in **datasets** folder

! unzip -o datasets/apt29_evals_day1_manual.zip -d datasets/

We will store the **path** of the json file in a variable to facilitate our code

apt29Json = 'datasets/apt29_evals_day1_manual_2020-05-01225525.json'

## Creating a SQL View

### Create Spark session

from pyspark.sql import SparkSession

spark = SparkSession \
    .builder \
    .appName("Mordor") \
    .config("spark.sql.caseSensitive","True") \
    .getOrCreate()

### Read JSON file

apt29Df = spark.read.json(apt29Json)

apt29Df.show(n = 5, vertical = True)

### Expose the dataframe as a SQL view

apt29Df.createOrReplaceTempView('apt29')

## Analyzing the APT29 dataset

Filtering on **Sysmon event 1: Process Creation**

sysmon1 = spark.sql(
'''
SELECT Image, ProcessId, ProcessGuid
FROM apt29
WHERE Channel = 'Microsoft-Windows-Sysmon/Operational'
    AND EventID = 1
''')
sysmon1.show(n = 5, truncate = False)

## Thank you! I hope you enjoyed it!