# Explore Kerberoastable Users with BloodHound
----------------------------------------------
* **Author**: Roberto Rodriguez (@Cyb3rWard0g)
* **Project**: Infosec Jupyter Book
* **Public Organization**: [Open Threat Research](https://github.com/OTRF)
* **License**: [Creative Commons Attribution-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-sa/4.0/)
* **Reference**: https://youtu.be/fqYoOoghqdE?t=1218

## Importing Libraries
Pre-requisites:

* pip install py2neo

from py2neo import Graph

## Count Users with Service Principal Name Set 

When sharphound finds a user with a Service Principal Name set, it property named `hasspn` in the User node to `True`. Therefore, if we want to count the number users with that property set, we just need to query for users with `hasspn = True`.

g = Graph("bolt://206.189.85.93:7687", auth=("neo4j", "BloodHound"))

users_hasspn_count = g.run("""
MATCH (u:User {hasspn:true})
RETURN COUNT(u)
""").to_data_frame()

users_hasspn_count

g.run("""
MATCH (u:User {hasspn:true})
RETURN u.name
""").to_data_frame()

## Retrieve Kerberoastable Users with Path to DA 

We can limit our results and return only Kereberoastable users with paths to DA. We can find Kerberoastable users with a path to DA and also see the length of the path to see which one is the closest.

krb_users_path_to_DA = g.run("""
MATCH (u:User {hasspn:true})
MATCH (g:Group {name:'DOMAIN ADMINS@JAPAN.LOCAL'})
MATCH p = shortestPath(
  (u)-[*1..]->(g)
)
RETURN u.name,LENGTH(p)
ORDER BY LENGTH(p) ASC
""").to_data_frame()

krb_users_path_to_DA

## Return Most Privileged Kerberoastable users

What if we do not have kerberoastable users with a path to DA? We can still look for most privileged Kerberoastable users based on how many computers they have local admins rights on.  

privileged_kerberoastable_users = g.run("""
MATCH (u:User {hasspn:true})
OPTIONAL MATCH (u)-[:AdminTo]->(c1:Computer)
OPTIONAL MATCH (u)-[:MemberOf*1..]->(:Group)-[:AdminTo]->(c2:Computer)
WITH u,COLLECT(c1) + COLLECT(c2) AS tempVar
UNWIND tempVar AS comps
RETURN u.name,COUNT(DISTINCT(comps))
ORDER BY COUNT(DISTINCT(comps)) DESC
""").to_data_frame()

privileged_kerberoastable_users

