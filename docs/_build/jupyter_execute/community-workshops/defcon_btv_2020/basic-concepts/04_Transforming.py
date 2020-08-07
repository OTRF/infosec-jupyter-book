# Data Analysis with Spark.SQL: Transforming
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

apt29Json = 'datasets/apt29_evals_day1_manual_2020-05-01225525.json'

apt29Df = spark.read.json(apt29Json)

apt29Df.createOrReplaceTempView('apt29')

## Transforming data with Spark Built-In functions

### Convert ProcessId (String) to Integer format

IntegerProcessId = spark.sql(
'''
SELECT ProcessId, cast(ProcessId as Integer) as IntegerProcessId
FROM apt29
WHERE lower(Channel) LIKE '%sysmon%'
    AND EventID = 1
''')

print('This dataframe has {} records!!'.format(IntegerProcessId.count()))
IntegerProcessId.printSchema()
IntegerProcessId.show(n = 5, truncate = False)

### Convert ProcessId (Integer) to Hexadecimal format

HexadecimalProcessId = spark.sql(
'''
SELECT ProcessId, hex(cast(ProcessId as Integer)) as HexadecimalProcessId
FROM apt29
WHERE lower(Channel) LIKE '%sysmon%'
    AND EventID = 1
''')

print('This dataframe has {} records!!'.format(HexadecimalProcessId.count()))
HexadecimalProcessId.printSchema()
HexadecimalProcessId.show(n = 5, truncate = False)

## Transforming data with Spark User Defined Functions (UDF)

### Calculate the number of characters of Commad Line values in Sysmon 1 (Process Creation) events

* Define function

def LenCommand(value):
    Length = len(value)
    return Length

* Import **pyspark.sql.types**

from pyspark.sql.types import *

* Register **UDF**

spark.udf.register("LengthCommand", LenCommand, IntegerType())

* Use **UDF**

commandLine = spark.sql(
'''
SELECT CommandLine, LengthCommand(CommandLine) as LengthCommandLine
FROM apt29
WHERE Channel LIKE '%Sysmon%'
    AND EventID = 1
''')

print('This dataframe has {} records!!'.format(commandLine.count()))
commandLine.printSchema()
commandLine.show(n = 5, truncate = 80)

## Thank you! I hope you enjoyed it!