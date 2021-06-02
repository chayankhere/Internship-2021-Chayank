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
  <img src="https://github.com/Chayank-S/images/blob/main/network%20namespac%204.png" width="760" height="250">
   
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
   - if there are multiple name spaces, to establish connectivity we need to create a virtual switch.
  <img src="https://github.com/Chayank-S/images/blob/main/network%20namespac%206.png" width="500" height="500">
   
   ## mnt namepsace
   - Creating separate mount namespace has an effect similar to doing a chroot().
   - Chroot is does not provide complete isolation, and it isolates at filesystem level only. If ps is excecuted, all the process will be visible.
   - Creating a separate mount namespace allows each of these isolated processes to have a completely different view of the entire system’s mountpoint structure from the original one.
  <img src="https://uploads.toptal.io/blog/image/677/toptal-blog-image-1416545619045.png" width="500" height="500">
  - This allows you to have a different root for each isolated process.
  - For a particular namespace, it is the root of file system.
  - We can mount portions of underlying filesystem like adding commands and libraries to the mount namespace.
  
  #### Use case:
   - mount namespaces is to create environments that are similar to chroot jails.
   - But with the use of the chroot() system call only file system level isolation is provided, namespaces provide isolation for process, network interfcaes, process etc.

## Uts namespace
- it isolates two system identifier *nodename* and *domainname* returned by the uname() systemcall.
- It is much more convinient to carry the communiaction between hosts using their hostname, than using ip address
- Searching through log files, for instance, is much easier when identifying a hostname than ip
- Also, in a dynamic environment, IPs can change which also is the reason to use hostname.
- The term "UTS" is derived from the name of the structure passed to the uname() system call: struct utsname
- In the context of containers, the UTS namespaces feature allows each container to have its own hostname and NIS domain name ( NIS =  Network Information Service, or NIS, is a client–server directory service protocol for distributing system configuration data such as user and host names between computers)


# Docker networking

There are three components in Docker Networking:

-   The Container Network Model (CNM)
-   Libnetwork
-   Drivers

**CNM:**  CNM defines and outline fundamental building blocks of Docker Network.

**Libnetwork:**  It is the real implementation of CNM and is used by Docker, Just like TCP/IP is implementation of OSI layer.

**Drivers:**  With the help of drivers, various Network topologies can be implemented like bridge and host based networking.

> Behind the scenes Docker Engine creates the necessary Linux bridges, internal interfaces, iptables rules, and host routes to make this connectivity possible

**CN M**
CNM is the framework which defines how networking design should be from Docker Network. CNM model is categorised in to three building blocks.

-   Sandboxes
-   Endpoints
-   Networks

**Sandbox:**  It is an isolated network stack, which includes Ethernet interface, DNS, Ports, routing tables.

**Endpoints:**  It is a virtual interface, which is used to provide network connection to make communication successful.

**Networks:**  It is the 802.1d software network bridge or software based switch, on which various endpoints connects to communicate to each other.

![enter image description here](https://www.dclessons.com/uploads/2019/09/Docker-7.2.png)

Basic definitions:

-   **NAT:**   Typically, the NAT gives the kernel the ability to provide private networks to connect to the Internet using a single public IP address. 
-   **Bridge:**  the Network Bridge is a device (can also be a virtual one) that creates a communication surface which connects two or more interfaces to a single flat broadcast network. 

When you run a docker container, 
- default bridge network is created and all the containers in that host are connected to that particular network bridge.
- this network bridge acts as a interface to the host, and as bridge to the containers.
- A respective veth created in order to transfer traffic between the container and the bridge, after a container is created.

![enter image description here](https://argus-sec.com/wp-content/uploads/2020/03/docker6.png)

Host networking

- container’s network stack is not isolated from the Docker host and the container does not get its own IP-address allocated.
- Eg : if we run a container which binds to port 80 and you use host networking, the container’s application is available on port 80 on the host’s IP address
1.  Create and start the container as a detached process.
    
    ```
    docker run --rm -d --network host --name my_nginx nginx
    ```
2. Verify there are no internal interfcaes were created     
	  ```
	  ifconfig
	 ```

3. -   Verify which process is bound to port 80, using the  `netstat`  command. 
    
    ```
    sudo netstat -tulpn | grep :80
    ```
  
  Bridge Networking
  
-   The  **default bridge network**, which allows simple container-to-container communication by IP address, and is created by default.
    
-   A  **user-defined bridge network**, which you create yourself, and allows your containers to communicate with each other, by using their container name as a hostname

1. Default Bridge network:

- **Check that the bridge network is running**
	```
	docker network ls
	```
- **Start container**
		```
		docker run -it --network=bridge ubuntu /bin/bash 
		```
	  
- To find the IP addresses of a container, look at the output of the  `docker inspect`  command:

	```
	$ docker inspect <container_id> | grep IPAddress
	```
- Check containers connected to bridge
	```
	$ sudo docker inspect bridge
	```

2. User defined bridge
Why have a user defined bridge
- In the default bridge network, all the containers were able to see one another, having a user defined bridge can provide a isolation to certain containers added to that network.
- **Create a user-defined bridge network**
	```
	docker network create mynet
	```
- **Start a container and connect it to the bridge**
	```
	docker run --rm -it --net mynet --hostname c1 --name ubuntu ubuntu /bin/bash
	```
- We can connect or disconnect a container from a network
	```
	docker network connect mynet {container_id}
	```
	```
	docker network disconnect mynet {container_id}
	```


# Linux Boot process

Following steps
- 

![](https://static.thegeekstuff.com/wp-content/uploads/2011/02/linux-boot-process.png)
