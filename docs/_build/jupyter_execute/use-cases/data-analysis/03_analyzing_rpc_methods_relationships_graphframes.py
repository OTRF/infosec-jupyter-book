# Analyzing Windows RPC Methods and Other Functions Via GraphFrames

* **Author:** Roberto Rodriguez (@Cyb3rWard0g)
* **Project:** Infosec Jupyter Book
* **Public Organization:** Open Threat Research
* **License:** Creative Commons Attribution-ShareAlike 4.0 International
* **Reference:**

## Import Libraries

from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from graphframes import *

## Initialize Spark Session

spark = SparkSession \
    .builder \
    .appName("WinRPC") \
    .config("spark.sql.caseSensitive","True") \
    .config("spark.driver.memory", "4g") \
    .getOrCreate()

spark

## Download and Decompress JSON File

! wget https://github.com/Cyb3rWard0g/WinRpcFunctions/blob/master/win10_1909/AllRpcFuncMaps.zip

! unzip AllRpcFuncMaps.zip

## Read JSON File as Spark DataFrame

%%time
df = spark.read.json('AllRpcFuncMaps.json')

## Create Temporary SQL View

df.createOrReplaceTempView('RPCMaps')

## Create GraphFrame

vertices = spark.sql(
'''
SELECT FunctionName AS id, FunctionType, Module
FROM RPCMaps
GROUP BY FunctionName, FunctionType, Module
'''
)

edges = spark.sql(
'''
SELECT CalledBy AS src, FunctionName AS dst
FROM RPCMaps
'''
).dropDuplicates()

g = GraphFrame(vertices, edges)

g

## Motif Finding

Motif finding refers to searching for structural patterns in a graph.

GraphFrame motif finding uses a simple Domain-Specific Language (DSL) for expressing structural queries. For example, graph.find("(a)-[e]->(b); (b)-[e2]->(a)") will search for pairs of vertices a,b connected by edges in both directions. It will return a DataFrame of all such structures in the graph, with columns for each of the named elements (vertices or edges) in the motif

## Basic Motif Queries

What about a chain of 3 vertices where the first one is an RPC function and the last one is an external function named LoadLibraryExW?

loadLibrary = g.find("(a)-[]->(b); (b)-[]->(c)")\
  .filter("a.FunctionType = 'RPCFunction'")\
  .filter("c.FunctionType = 'ExtFunction'")\
  .filter("c.id = 'LoadLibraryExW'").dropDuplicates()

%%time
loadLibrary.select("a.Module","a.id","b.id","c.id").show(10,truncate=False)

What if we also filter our graph query by a specific module? What about Lsasrv.dll?

loadLibrary = g.find("(a)-[]->(b); (b)-[]->(c)")\
  .filter("a.FunctionType = 'RPCFunction'")\
  .filter("lower(a.Module) LIKE '%lsasrv.dll'")\
  .filter("c.FunctionType = 'ExtFunction'")\
  .filter("c.id = 'LoadLibraryExW'").dropDuplicates()

%%time
loadLibrary.select("a.Module","a.id","b.id","c.id").show(10,truncate=False)

## Breadth-first search (BFS)

Breadth-first search (BFS) finds the shortest path(s) from one vertex (or a set of vertices) to another vertex (or a set of vertices). The beginning and end vertices are specified as Spark DataFrame expressions.

### Shortest Path from an RPC Method to LoadLibraryExW

loadLibraryBFS = g.bfs(
  fromExpr = "FunctionType = 'RPCFunction'",
  toExpr = "id = 'LoadLibraryExW' and FunctionType = 'ExtFunction'",
  maxPathLength = 3).dropDuplicates()

%%time
loadLibraryBFS.select("from.Module", "e0").show(10,truncate=False)

