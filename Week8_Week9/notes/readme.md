# Sharding in Elasticsearch 
- Elasticsearch is scalable due to its distributed architecture, which means data present in different nodes are synced through the communication between the nodes. 
- Sharding is breaking up of a large data into smaller shards and distributing the same to various nodes in a cluster.
### Need for sharding 
- Helps to  scale the data, by splitting the data to shards.
- Increases the performance in search queries
### Varying the number of shards
- During the creation of index   
```json
PUT index_name
{
  "settings" : {
	  "index" : {
		  "number_of shards" : 5,
		  "number_of_replica" : 1
		  }
	}
}
```
- After creation of index : we cant change the number of shards, since it affects the routing. if there is a need then we can 
-- take a snapshot of the existing index, 
-- create the new index of required shards
-- restore it to the new index

### How are Documents stored in particular shards
- Here Routing is used to place or search for any document in a given shard.
- Routing is done by a formula
![Routing]( https://codingexplained.com/wp-content/uploads/Routing-1024x863.png )
- The value of 'routing' in formula by default is the document Id
- Earlier as said, the change in number of shards affects the routing. As seen, the routing formula is dependent on the number of shards, due to which the after changing the shard number, it leads to incorrect routing.            
# Replication in Elasticsearch

- Hardware can fail any time, there is a need for fault tolerance mechanism.
-  Replication helps and serves the same purpose. 

### Two main purposes
- To provide backup for the data
- Increases the query search performance 
### Primary and replica shards
- The shards from which the replication takes place is called primary shards
- The shards resulting after replication is called replica
- The number of replica and shards is mentioned at the time of creation of the index.
- Syntax:
```json
PUT index_name
{
  "settings" : {
	  "index" : {
		  "number_of shards" : 5,
		  "number_of_replica" : 1
		  }
	}
}
```	
   
   - These replicas are stored in different nodes, and are never stored within the same node as the primary shard
   - This is one of the reason  to have more than one node in a cluster. 
![Cluster]( https://www.elastic.co/guide/en/elasticsearch/guide/master/images/elas_0401.png )
   ### Keeping the replica shards updated and in sync with primary shards
   - There would be a problem in case of data inconsistencies within the replication group ( primary shard + its replica shards  ).
   - Here, to address the sync the model used is *Primary backup* for replication .
   - This means any index operation like adding removing and updation of documents is first done in primary shards and then changes are communicated to the replicas in the replication group.
   ![ Replication in Elasticsearch ]( https://codingexplained.com/wp-content/uploads/7-1024x732.png)