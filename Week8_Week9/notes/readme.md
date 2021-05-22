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
   
   # Linux Namespace
   - But on a server, the services has to be isolated in the view of security and stability.
   - A server running multiple services unisolated, then if a single service gets compromised, rest of services can be compromised as they are not isolated.
   ## Process namespace
   - Linux kernel has maintained a single process tree. The tree contains a reference to every process currently running in a parent-child hierarchy.
   - Every time a computer with Linux boots up, it starts with just one process, with process identifier (PID) 1. 
   - This process is the root of the process tree, and it initiates the rest of the system by starting the correct daemons/services. 
   - All the other processes start below this process in the tree. 
   - The PID namespace allows one to spin off a new tree, with its own PID 1 process. The process that does this remains in the parent namespace, in the original tree, but makes the child the root of its own process tree
   - It is possible to create a nested set of child namespaces: one process starts a child process in a new PID namespace, and that child process spawns yet another process in a new PID namespace, and so on.
   ![pid](https://uploads.toptal.io/blog/image/674/toptal-blog-image-1416487554032.png)
   ## Network namespace
   - in Process namespace, though the process were isolated, they still had full access to the resourse of the host i.e if the child process created above were to listen on port 80, it would prevent every other process from lisening on same port
   - A network namespace allows each of these processes to see an entirely different set of networking interfaces. 
   - Even the loopback interface is different for each network namespac
   - These namespaces have their interfaces isolated from the host.
   ![network](https://github.com/Chayank-S/images/blob/main/network%20namespace1.png)
   #### We can create new name spaces using 
   ```bash
   $ ip netns add pink
   $ ip netns add blue
   ```
   - list the namespace
   ```bash
   $ ip netns
   pink
   blue
   ```
   ![network1](https://github.com/Chayank-S/images/blob/main/network%20namespac%202.png)
   - The interfaces are isolat from the host
   ![network2](https://github.com/Chayank-S/images/blob/main/network%20namespac3.png)
   #### We can create communiaction between the name spaces using the virtual pipe/cabl
   - create a virtual cable
   ```bash
   ip link add veth-pink type veth peer name veth-blue
   ```
   ![network3](https://github.com/Chayank-S/images/blob/main/network%20namespac%204.png)
   - assign each end to the pink and blue namespace
   ```bash
   ip link set veth-pink netns pink
   ip link set veth-blue netns blue
   ```
   ![network4](https://github.com/Chayank-S/images/blob/main/network%20namespac%205.png)
   - assign ip address and bring interface up
   ```bash
   ip -n pink addr add <ip.pink> dev veth-pink
   ip -n blue addr add <ip.blue> dev veth-blue
   
   # up
   ip -n pink link set veth-pink up
   ip -n blue link set veth-blue up
   ```
   ![network3](https://github.com/Chayank-S/images/blob/main/network%20namespac%206.png)
   <img src="https://github.com/Chayank-S/images/blob/main/network%20namespac%206.png" width="48>
   - if there are multiple name spaces, to establish connectivity we need to create a virtual switch.
