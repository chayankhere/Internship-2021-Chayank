# Dropbox  
> System Design 

**Dropbox** is a file hosting service operated by the American company **Dropbox, Inc.** that offers `cloud storage`, `file synchronization`, `personal cloud`, and `client software`.
 - Dropbox brings files together in one central place by creating a special folder on the user's computer. The contents of these folders are synchronized to Dropbox's servers and to other computers and devices where the user has installed Dropbox  
- When a file in a user's Dropbox folder is changed, Dropbox only uploads the [pieces of the file]([https://en.wikipedia.org/wiki/Block_(data_storage)](https://en.wikipedia.org/wiki/Block_(data_storage)) "Block (data storage)") that have been changed, whenever possible.  
- When a file or folder is deleted, users can recover it within 30 days.  
- Dropbox accounts that are not accessed or emails not replied in a year are automatically deleted.  
- Dropbox uses `SSL` transfers for synchronization and stores the data via `Advanced Encryption Standard(AES)-256` encryption.
## System Design dropbox

### Core / Functional  Features  
-   User should be able to upload/download, update and delete the files  
-   File versioning (History of updates)  
-   File and folder sync
- System should support offline edit
### Non functional features
- Reliability
- Security
- usability
### Traffic  
-   12+ million unique users  
-   100 million request per day with lots of reads and write.

### Problem Statement  
-   **More bandwidth and cloud space utilization:**  To provide a history of the files you need to keep the multiple versions of the files. This requires more bandwidth and more space in the cloud. Even for the small changes in your file, you will have to back up and transfer the whole file into the cloud again and again which is not a good idea.  
-   **Latency or Concurrency Utilization:**  You can't do time optimization as well. It will consume more time to upload a single file as a whole even if you make small changes in your file. It's also not possible to make use of concurrency to upload/download the files using multi threads or multi processes.
### Solution   
- **Break the files into multiple chunks:** There is no need to upload/download the whole single file after making any changes in the file. You just need to save the chunk which is updated (this will take less memory and time). It will be easier to keep the different versions of the files into various chunks.  
- **Create one more file named as a metadata file:** Incase of multiple files with chunks, This file contains the indexes of the chunks (chunk names and order information). You need to mention the hash of the chunks in this metadata file and you need to sync this file into the cloud.
 ![](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20200619214958/System-Design-Dropbox-High-Level-Solution.png)
We can download the metadata file from the cloud whenever we want and we can recreate the file using various chunks.
### Components for the Dropbox system design  
![]( https://media.geeksforgeeks.org/wp-content/cdn-uploads/20200619215231/Complete-System-Design-Solution-of-Dropbox-Service.png)
- Client installed on a computer.  
- 4 basic components of Client : **`Watcher`,`Chunker`, `Indexer`, and `Internal DB`**  
- Can consists of multiple clients belongs to the same user.  
-   The client is responsible for uploading/downloading the files, identifying the file changes in the sync folder, and handling conflicts due to offline or concurrent updates.  
- The client is actively monitoring the folders for all the updates or changes happening in the files  
-   To handle file metadata updates (e.g. file name, size, modification date, etc.) this client interacts with the Messaging services and Synchronization Service.  
-   It also interacts with the remote cloud storage to store the actual files and to provide folder synchronization.
### APIs

The service will expose API for uploading file and downloading file. 

#### Download Chunk

This API would be used to download the chunk of a file.

Request:

```
GET /api/v1/chunks/<chunk_id>
```

#### Upload Chunk

This API would be used to upload the chunk of a file.

Request:

```
POST /api/v1/chunks/<chunk_id>
```

Response:

```
200 OK 
```

On successful upload, the server will return HTTP response code  `200`. Below are some possible failure response codes:

```
401 Unauthorized
400 Bad request
500 Internal server eror
```
### Client Components

-   **Watcher**  
	- responsible for monitoring the sync folder 
	- It gives notification to the indexer and chunker if any action is performed in the files or folders.
-   **Chunker**  
	-  For new file
		- Break the files into multiple small  chunks  
		- upload it to the cloud storage with a unique id or hash of chunks. 
	-	For any changes in the files, 
		-	the chunking algorithm detects the specific chunk which is modified
		-	only saves that specific part/chunks to the cloud storage. 
-   **Indexer**   
	- responsible for updating the internal database when it receives the notification from the watcher  
	- receives the URL of the chunks from the chunker along with the hash and updates the file with modified chunks. 
	- Indexer communicates with the Synchronization Service using the Message Queuing Service.
-   **Internal database**  
	- store all the files and chunks information, their versions, and their location in the file system.

### Discuss The Other Components

#### 1. Metadata Database

- The metadata database maintains the indexes of the various chunks. 
- The information contains files/chunks names, their different versions along with the information of users and workspace.

- Relational databases ( use for consistency ) are difficult to scale so if we are using the MySQL database then you need to use a database sharding technique to scale the application. 
- we need to build an edge wrapper around the sharded databases to scale.
	- This edge wrapper provides the ORM and the client can easily use this edge wrapper’s ORM to interact with the database (instead of interacting with the databases directly).

![System-Design-Dropbox-Metadata-Edge-Wrapper]( https://media.geeksforgeeks.org/wp-content/cdn-uploads/20200619220100/System-Design-Dropbox-Metadata-Edge-Wrapper.png)

#### 2. Message Queuing Service

The messaging service queue will be responsible for the asynchronous communication between the clients and the synchronization service.

![System-Design-Dropbox-Message-Queue-Service]( https://media.geeksforgeeks.org/wp-content/cdn-uploads/20200619220312/System-Design-Dropbox-Message-Queue-Service.png)

Below are the main requirements of the Message Queuing Service.

-   Ability to handle lots of reads and writes requests.
-   Store lots of messages in a highly available and reliable queue.
-   High performance and high scalability.

There will be two types of messaging queues in the service.

-   **Request Queue:**  
-   **Response Queue:**  
 
>The message will never be lost even if the client will be disconnected from the internet (the benefit of using the messaging queue service).
    
    
    

#### 3. Synchronization Service

The client communicates with the synchronization services either to receive the latest update from the cloud storage or to send the latest request/updates to the Cloud Storage to clients.

- receives the request from the request queue of the messaging services and updates the metadata database with the latest changes. 
-  broadcast the latest update to the other clients  through the response queue so that the other client’s indexer can fetch back the chunks from the cloud storage and recreate the files with the latest update.  
- updates the local database with the information stored in the Metadata Database. 

#### 4. Cloud Storage

- The client communicates with the cloud storage for any action performed in the files/folders using the API provided by the cloud provider.




# Root Cause Analysi (RCA)
## **What is** **Root Cause Analysis (RCA)?**

- Approach used to analyze serious problems before trying to solve them 
- RCA helps isolates and identifies the main root cause of a problem . 

**Root cause analysis (****RCA****)**  
- Is effective problem solving method.

- RCA could be done using multiple tools and methods.

 - Root cause analysis is a reactive approach.

- Root cause analysis is a team approach methodology.

- RCA should be applied shortly after adverse events to keep track of all essential details. 

## **Root Cause Analysis (RCA) Tools**

Root cause analysis (RCA) could be applied using a wide variety of tools, there is no perfect method that can be used anywhere, instead, the quality managers would select the suitable approach for organization and team members, typically using brainstorming technique.

-   Fishbone diagram, also known as Ishikawa or cause and effect diagram is one of the classic tools for RCA. 
-   Five whys is another popular tool for RCA, also known as Gemba Gembustu. 
-   A flowchart is mapping the process steps through different sections or departments that could be helpful to identify defects source location.
-   Pareto chart is usually performed during brainstorming sessions to prioritize the given possible cause of the adverse event. 
-   Scatter diagram is another displaying tool that facilitates localizing relations by representing numerical variables on graphs.


 


# Consistant Hashing

- One of the ways hashing can be implemented in a distributed system is by taking hash Modulo of a number of nodes.  
- The hash function can be defined as  
-- **node_number = hash(key)mod_N**  
	- where N is the number of Nodes.

- To add/retrieve a key to/from the node: 
	- the client computes the hash value of that key 
	- uses the result to contact the appropriate node . 
	- If the key is found, it is retrieved else it is added to the pool of the Node.

**For example,**  
>  client wants to add 1. Its hash value = 7739. It will go to Node number (7739%3). So, it will contact node 2. the key is added to the pool
>   ![]( https://media.geeksforgeeks.org/wp-content/uploads/1-259.png )

### **Disadvantage: The Rehashing problem.**

Let’s suppose the number of nodes has changed. 
- As the keys are distributed depending on the number of nodes, 
- since the number of nodes has changed, the value from hashing function will change so the keys will be redistributed in different nod.


**So, the distribution changes whenever we change the number of Nodes.**

> What happens is the more number of redistributions, 
> - the more number of misses, the more number of memory fetches, placing an additional load on the node and thus decreasing the performanc

**Consistent Hashing.**

  

  

The above issue can be solved by  **Consistent Hashing**.

- This method operates  **independently** of the number of nodes as the hash function is not dependent on the number of nodes.   
- The hash value can be computed as  
	- **position_on_chain = hash(key)mod_360**

> (360 is chosen as we are representing things in a circle. And a circle has 360 degrees.)

![]( https://media.geeksforgeeks.org/wp-content/uploads/4-94.png)  
Steps for the arrangement –

1) Find Hash values of the keys and place it on the ring according to the hash value.  
2) Find Hash values of the individual nodes and place it on the ring according to the hash value.  
3) Now map each key with the node which is closest to it in the counter-clockwise direction.  
4) If the position of a node and key is same, assign that key to the node.  

![]( https://media.geeksforgeeks.org/wp-content/uploads/5-69.png)  
### Operations –  
Case 1) 
Adding a node –  
Suppose we add a new node D in the ring by calculating the hash. Only those keys will be redistributed whose values lie between the D and C. Now they will not point towards A, they will point towards D.

![]( https://media.geeksforgeeks.org/wp-content/uploads/6-1-1.png)

Case 2) Removing a node –  
Suppose we remove a node C in the ring. Only those keys will be redistributed whose values lies between C and the B. Now they will not point towards C, they will point towards A.

![]( https://media.geeksforgeeks.org/wp-content/uploads/7-41.png)

This is how consistent hashing solves the rehashing problem. The  **number of keys which needs to be redistributed after rehashing is minimised.**  So, less number of memory fetches. Hence, performance increas is seen





# inverted index

An inverted index is an index data structure storing a mapping from content, such as words or numbers, to its locations in a document or a set of documents.

Documents are normally stored as lists of words, but inverted indexes invert this by storing for each word the list of documents that the word appears in, hence the name “Inverted index"

There are two types of inverted indexes: 
- 
-- A **record-level inverted index** contains a list of references to documents for each word. 
-- A **word-level inverted index** additionally contains the positions of each word in a document

## Techniques used in Inverted Index
#### **Lexing** 
- Lexing refers to the process of converting a document from a list of characters to a list of tokens
- To generate these tokens from the input character stream,  the input is converted to lowercase. 
- Then, each collection of alphanumeric characters separated by non-alphanumeric characters (whitespace, punctuation,etc.) is added to the list to each of which is a single alphanumeric word

#### **Stemming** 
- Stemming means not indexing each word as it appears after lexing, but transforming it to its root (stem) and indexing that instead.

For example, the words “compute”, “computer”, “computation”, “computers”, “computed” and “computing” might all be indexed as “compute"

#### **Stop words**
- Stop words are words like “a”, “the”, “of”, and “to”, which are so common that nearly every document contains them. 
- A stop word list contains list of the words to ignore while indexing document

Example of inverted index
```
Words                 Documentt
ant                   doc1
demo                  doc2
world                 doc1, doc2
```

# Linux boot process :penguin:

Following steps
1. BIOS (Basic input and output system)
2. MBR (Master boot record)
3. GRUB (Grand unified boot loader)
4. Kernel
5. Init
6. Runlevel program



![](https://static.thegeekstuff.com/wp-content/uploads/2011/02/linux-boot-process.png)

### a) SMPS (Switching Mode Power Supply )
- The primary objective of this component is to provide the perfect required voltage level to the motherboard and other computer components.
- SMPS converts AC to DC and maintain the required voltage level so that the computer can work
-  After power is supplied, SMPS checks the voltage level's its providing to the motherboard. If the power signal level is perfect, then SMPS will send a POWER GOOD signal to the motherboard timer.
- On receiving this POWER GOOD signal from SMPS, the motherboard timer will stop sending reset signal to the CPU. Which means the power level is good.

### b) Bootstrapping
- Something has to be programmed by default, so that the CPU knows where to search for instructions.
- This is an address location in the ROM. The address location is FFFF:0000h.
- This address location is the last region of the ROM. It only contains one instruction. The instruction is to jump to another memory address location. This JUMP command will tell the location of the BIOS program.

## 1. BIOS
- BIOS stands for Basic Input Output System. 
- The most important use of BIOS during the booting process is POST. POST stands for Power on Self Test. 
- Its a series of tests conducted by the bios, which confirms the proper functioning of different hardware components attached to the computer.
- POST is very important thing to have before the Operating system is loaded.  if  we have a faulty hard drive or faulty memory, sometimes the fault causes data corruption or data loss.
- After POST, all drivers are activated including the storage drivers, now the BIOS looks for bootloader in the floowing order.
	1. CD ROM
	2. HARD DISK
	3. USB
	4. Floppy Disk
> **How does the BIOS validate if a disk is bootable or not?** :thinking: 
>[reference]( https://superuser.com/questions/420557/mbr-how-does-bios-decide-if-a-drive-is-bootable-or-not#:~:text=The%20BIOS%20decides%20if%20a,at%20the%20446th%20byte)
	- The BIOS decides if a drive is bootable based on the 16-byte partition record, present _after_ the MBR code area (held in a table starting at the 446th byte). 
	- The first byte in each partition record represents the drive's bootable status (and is set to `0x80` if bootable, `0x00` if not)
	- If the flag is set ( the drive is bootable ) then the control is sent back to the start of the MBR code area of the same drive.
	- if the flag is not set, the BIOS checks the other devices in the given order for a valid bootable disk ( set bootable flag )

## 2. MBR
- Assuming no bootloader is found in the above devices, BIOS is programmed to look at a permanent location on the hard disk to complete its task. 
- This location is called a *Boot sector*, called MBR (Master Boot Record) which is the first sector of hard disk
- This is the location that contains the program that will help our computer to load the operating system. 
- As soon as bios finds a valid MBR, it will load the entire content of MBR to RAM, and then further execution is done by the content of MBR.
 
- Quick look at the same
	- MBR stands for Master Boot Record.
	-   It is located in the 1st sector of the bootable disk. Typically /dev/hda, or /dev/sda
	-   MBR is less than 512 bytes in size. This has three components 
		- primary boot loader info in 1st 446 bytes 
		- partition table info in next 64 bytes 
		- mbr validation check in last 2 bytes.
	- It contains information about GRUB (or LILO in old systems).
	-   So, in simple terms MBR loads and executes the GRUB boot loader.

## 3. GRUB :floppy_disk:
- GRUB stands for **Grand Unified Bootloader**.  
- Result of a troubleshooting done by **Erich Boleyn**, to boot `GNU Hurd` - OS which was designed by GNU, as a **free replacement of UNIX**.  
- **Yoshinori K. Okuji** carried further work to advance the initial GRUB, and is called GRUB2.  
- `440 bytes` of MBR will have GRUB first boot stage.  
- Stage 2 GRUB loads the kernel and other `initrd` image files.  
- GRUB is the combined name given to **different stages** of grub.  
- If you have multiple kernel images installed on your system, you can choose which one to be executed.  
- GRUB stages:  
- GRUB Stage 1  
- GRUB Stage 1.5  
- GRUB Stage 2  
- GRUB displays a splash screen, waits for few seconds, if you don’t enter anything, it loads the default kernel image as specified in the grub configuration file.  
- GRUB has the knowledge of the filesystem (the older Linux loader LILO didn’t understand filesystem).  
- Grub configuration file is /boot/grub/grub.conf (/etc/grub.conf is a link to this). The following is sample grub.conf of CentOS.  
	```  
	#boot=/dev/sda  
	default=0  
	timeout=5  
	splashimage=(hd0,0)/boot/grub/splash.xpm.gz  
	hiddenmenu  
	title CentOS (2.6.18-194.el5PAE)  
	root (hd0,0)  
	kernel /boot/vmlinuz-2.6.18-194.el5PAE ro root=LABEL=/  
	initrd /boot/initrd-2.6.18-194.el5PAE.img  
	```  
- As you notice from the above info, it contains kernel and initrd image.  
- So, in simple terms GRUB just loads and executes Kernel and in


## 4. Kernel :penguin:

-   Mounts the root file system as specified in the “root=” in grub.conf
-   Kernel executes the /sbin/init program
-   Since init was the 1st program to be executed by Linux Kernel, it has the process id (PID) of 1.  Do a `ps -ef | grep init` and check the pid.
-   initrd stands for Initial RAM Disk.
-   initrd is used by kernel as temporary root file system until kernel is booted and the real root file system is mounted. It also contains necessary drivers compiled inside, which helps it to access the hard drive partitions, and other hardware.


## 5. Init :one: & 6. Runlevel :runner: :running:
> Pre init process

The **initrd** and **initramfs** are two different methods by which the temporary file system is made available to the kernel.**Initrd** (Initial ramdisk) was the technique used with earlier linux distros where the compressed image of the entire file system (initrd image) is made available as a special block storage device (**`/dev/ram`**) which is then mounted and decompressed.   
The driver software to access this block storage device is compiled into the kernel. The kernel assumes that the actual file system is mounted and starts `/linuxrc` which in turn starts `/sbin/init`.  
- **Linuxrc** is a program used for setting up the kernel for installation purposes. It allows the user to load modules, start an installed system, a rescue system.   
- **Linuxrc** is designed to be as small as possible. Therefore, all needed programs are linked directly into one binary.  
- `/sbin/init` is the executable starting the **SysV** initialization system.  
- `/sbin/init` is a symlink to `/lib/systemd/systemd`  
 ```bash  
stat /sbin/init  
```
With Initramfs the compressed image is made available as a **cpio** archive which is unpacked by the kernel using a temporary instance of **tempfs** which then becomes the **root file system**.   
It is followed by executing **`/init`** as the first process.  
- **cpio** stands for "copy in, copy out".  
- **tmpfs** is intended to be for temporary storage that is very quick to read and write from and does not need to persist across operating system reboots.   
- **tmpfs** is **used in** Linux for /run, /var/run and /var/lock to provide very fast access for runtime data and lock files.
>Init 	Process

**Init**   
Initialization

It is the parent of all processes, executed by the kernel during the booting of a system.   
- Its principle role is to create processes from a script stored in the file **`/etc/inittab`**. The **init** is a daemon process which starts as soon as the computer starts and continue running till, it is shutdown  having "**pid=1**".  
- If somehow **init** daemon could not start, no process will be started and the system will reach a stage called **Kernel Panic**, which is one of the drawback. init is most commonly referred to as **System V init**. 
- System V -> first commercial UNIX Operating System designed.The OS is booted with the desired runlevel or target.Once the actual file system is mounted, the runlevel is identified. 
- There are 7 runlevels associated with Init: 
	0. **Shutdown or halt** -> Shuts down system
	1. **Single user mode** (root user mode) -> Does not configure network interfaces, start daemons,
	2. **Multiuser without network service** -> Does not configure network interfaces or start daemons.
	3. **Multiuser with network service** -> Starts the system normally. `Default`
	4. **Undefined** -> Not used/User-definable ,configured to provide a custom boot state.
	5. **Graphical mode** -> Starts the system normally with GUI.
	6. **Reboot** -> Reboots the system

The main configuration file is `/etc/inittab`. The default runlevel is specified here.  
The scripts required by each runlevel is specified in **`/etc/rc.d/rc*`** directory  
- One could find a list of **kill (K)** scripts and **start (S)** script. The kill scripts are executed followed by start scripts, along with sequence number in which the programs should be started or killed.

**Systemd**  
(System Management Daemon)

It is based on parallel booting concept where processes and services are started in parallel, speed up the booting process.  
In Systemd there are no runlevels involved, instead target unit files come into play. Unit files are configuration files what define any entity in systemd environment  
**Unitfiles** -> services, targets, devices, file system mount points and sockets.

The targets in systemd are : 

   0. **poweroff.target**   
   1. **rescue.target**   
   2. **multi-user.target**   
   3. **graphical.target**    
   4. **reboot.target**

- In Systemd `/sbin/init` is simlinked to **`/etc/systemd/system/default.target`**.  
- The default.target file is empty and is simlinked with the presently chosen target file located at **`/usr/lib/systemd/system/<target name>.target`**.  
- Advantage is that if the main service fails the dependent services are bypassed  
- It uses `wanted`,` requires`,`before`,`after` for adding a specific service in systemd   
	- **`: <target-name>.target.wants`**
### Comparison of Sys V Run Levels with Target 
Unitsrunlevel0.target **<=>** poweroff.target    
runlevel1.target **<=>** rescue.target   
runlevel[234] **<=>** target, multi- user.target  
runlevel5.target **<=>** graphical.target   
runlevel6.target **<=>** reboot.target 

Init works based on serial booting principle, so even if the main service fails the sub-services are also checked unnecessarily. Even if the service becomes up before the booting has completed it will not be detected by init.   
> - For example, network service is essential for NFS or CIFS to function, so there is no meaning in trying to activate dependant services until the main service is up, but Init will still do it.

If due to some reason Init could not start then, no process will be started and the system will reach a state called **Kernal Panic** where booting fails. 
### TELINIT  
**`/sbin/telinit`** is linked to `/sbin/init` which takes a one-character argument and signals `init` to perform the appropriate action.
- 0,1,2,3,4,5 or 6 -> switch to the specified run level.  
- a, b, c -> process only those **`/etc/inittab`** file entries having runlevel **a, b** or **c**  
- Q or q -> re-examine the **`/etc/inittab`** file.  
- S or s -> switch to single user mode

Only by users with appropriate privileges can invoke **telinit**.





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

























# "RAFT" CONSENSUS ALGORITHM

## Introduction

- Raft protocol was developed by Diego Ongaro and John Ousterhout (Stanford University) . 
- Raft was designed for better understandability of how Consensus can be achieved considering that its predecessor, the Paxos Algorithm.
## Consensus
 
- ***Consensus** means multiple servers agreeing on same information, something significant to design fault-tolerant distributed systems.*  
- Definition of the process used when a client interacts with a server to clarify the process.  
**Process**  : The client sends a message to the server and the server responds back with a reply.

  
 A consensus protocol tolerating failures must have the following features :  

-   **Validity**  : If a process decides(read/write) a value, then it must have been proposed by some other correct process
-   **Agreement**  : Every correct process must agree on the same value
-   **Termination**  : Every correct process must terminate after a finite number of steps.
-   **Integrity**  : If all correct processes decide on the same value, then any process has the said value.

Now, there can be **two types** of systems assuming only one client:  

-   **Single Server system**  : The client interacts with a system having only one server with no backup. There is no problem in achieving consensus in such a system.  
    

![raft](https://media.geeksforgeeks.org/wp-content/uploads/single-server-1-raft-visual.png)
-   **Multiple Server system**  : The client interacts with a system having multiple servers. Such systems can be of two types :
    -   *Symmetric* :- Any of the multiple servers can respond to the client, rest of the other servers are supposed to sync up with the server that responded to the client
    -   *Asymmetric* :- Only the elected leader server can respond to the client. All other servers then sync up with the leader server.

Such a system in which all the servers replicate(or maintain) similar data(shared state) across time can for now be referred to as, **replicated state machine**.

We shall now define some terms used to refer individual servers in a distributed system.  

-   **Leader**  – Only the server elected as leader can interact with the client. All other servers sync up themselves with the leader. 
-   **Follower**  – Follower servers sync up their copy of data with that of the leader’s after every regular time intervals. *When the leader server goes down, one of the followers can contest an election and become the leader*.
-   **Candidate**  – At the time of contesting an election to choose the leader server, the servers can ask other servers for votes. Hence, they are called candidates when they have requested votes. Initially, all servers are in the Candidate state.

So, the above system can now be labelled as in the following snap.  

![multiple server labelled raft visual]( https://media.geeksforgeeks.org/wp-content/uploads/multiple-server-labelled-raft-visual.png )

**CAP theorem**  CAP Theorem is a concept that a distributed database system can only have 2 of the 3:

-   **Consistency**  
-   **Availability**  
-   **Partition Tolerance** 

## What is the Raft protocol

- Raft is a consensus algorithm that is designed to be easy to understand. 
- It’s equivalent to Paxos in fault-tolerance and performance. 
- The difference is that it’s decomposed into relatively independent subproblems, and it cleanly addresses all major pieces needed for practical systems. 
  

  

## Raft consensus algorithm explained

Raft states that each node in a replicated state machine(server cluster) can stay in any of the three states, namely, 

 1. Leader
 2. candidate, 
 3. follower.

![]( https://media.geeksforgeeks.org/wp-content/uploads/20201003144908/nodestatustransitions-300x150.png)

>- Only a leader can interact with the client; 
>- any request to the follower node is redirected to the leader node. 
> - leader can only append entries in its log, cannot update delete  or modify. hence before committing, it wait s for the majority of the nodes to acknowledge that the log has been replicated in those nodes also and then the committing is done
>- A candidate can ask for votes to become the leader. 
>- A follower only responds to candidate(s) or the leader.


**Term number**  
- To maintain these server status(es), the Raft algorithm divides time into small terms of arbitrary length. 
- Each term is identified by a monotonically increasing number, called  **term number**.  
- This term number is maintained by every node and is passed while communications between nodes. 
- Every term starts with an election to determine the new leader. The candidates ask for votes from other server nodes(followers) to gather majority. 
- If the majority is gathered, the candidate becomes the leader for the current term. 
- If no majority is established, the situation is called a  **split vote**  and the term ends with no leader. 

**Purpose of maintaining term number**  
Following tasks are executed by observing the term number of each node:  

-   Servers update their term number if their term number is less than the term numbers of other servers in the cluster. 
-   Candidate or Leader demotes to the Follower state if their term number is out of date(less than others). 
-   aa server node will not accept requests from server with lower term number

Raft algorithm uses two types of Remote Procedure Calls(RPCs) to carry out the functions :  

-   **RequestVotes**  RPC is sent by the Candidate nodes to gather votes during an election
-   **AppendEntries**  is used by the Leader node for replicating the log entries and also as a heartbeat mechanism to check if a server is still up. If heartbeat is responded back to, the server is up else, the server is down. Be noted that the heartbeats do not contain any log entries.

Now, lets have a look at the process of leader election.  

## Leader election

In order to maintain authority as a Leader of the cluster, the **Leader node sends heartbea**t to express dominion to other Follower nodes. 
A leader **election takes place when a Follower node times out** while waiting for a heartbeat from the Leader node. 

At this point of time, the timed out node changes it state to Candidate state, votes for itself and issues RequestVotes RPC to establish majority and attempt to become the Leader. 

The election can go the following three ways:  

-   **The Candidate node becomes the Leader by receiving the majority of votes from the cluster nodes**. and starts sending heartbeats to notify other servers of the new Leader.
-   **The Candidate node fails to receive the majority of votes in the election and hence the term ends with no Leader**. The Candidate node returns to the Follower state.
-   I**f the term number of the Candidate node requesting the votes is less than other Candidate nodes in the cluster, the AppendEntries RPC is rejected** and other nodes retain their Candidate status. If the term number is greater, the Candidate node is elected as the new Leader.

![raft leader election](https://media.geeksforgeeks.org/wp-content/uploads/raft-leader-election.png)


> Raft uses randomized election timeouts to ensure that split votes are rare and that they are resolved quickly. To prevent split votes in the first place, election timeouts are chosen randomly from a fixed interval (e.g., 150–300ms). This spreads out the servers so that in most cases only a single server will time out; it wins the election and sends heartbeats before any other servers time out. The same mechanism is used to handle split votes. **Each candidate restarts its randomized election timeout at the start of** an election, and it waits for that timeout to elapse before starting the next election; this reduces the likelihood of another split vote in the new election.  

## Log Replication

Each request made by the client is stored in the Logs of the Leader. 

This log is then replicated to other nodes(Followers). Typically, a log entry contains the following three information :  

-   **Command**  specified by the client to execute
-   **Index**  to identify the position of entry in the log of the node. The index is 1-based(starts from 1).
-   **Term Number**  to ascertain the time of entry of the command.
 
 - [ ] The Leader node fires AppendEntries RPCs to all other servers(Followers) to sync/match up their logs with the current Leader.
 - [ ] The Leader keeps sending the RPCs until all the Followers safely replicate the new entry in their logs.

However, in case the Leader crashes, the logs may become inconsistent. Quoting the Raft paper :  

> In Raft, the leader handles inconsistencies by forcing the followers’ logs to duplicate its own. This means that conflicting entries in follower logs will be overwritten with entries from the leader’s log.  

The Leader node will look for the last matched index number in the Leader and Follower, it will then overwrite any extra entries further that point(index number) with the new entries supplied by the Leader. 

## Safety

In order to maintain consistency and same set of server nodes, it is ensured by the Raft consensus algorithm that the leader will have all the entries from the previous terms committed in its log.

During a leader election, the RequestVote RPC also contains information about the candidate’s log(like term number) to figure out which one is the latest. If the candidate requesting the vote has less updated data than the Follower from which it is requesting vote, the Follower simply doesn’t vote for the said candidate. The following excerpt from the original Raft paper clears it in a similar and profound way.  

> Raft determines which of two logs is more up-to-date by comparing the index and term of the last entries in the logs. If the logs have last entries with different terms, then the log with the later term is more up-to-date. If the logs end with the same term, then whichever log is longer is more up-to-date.  

**Rules for Safety in the Raft protocol**  
The Raft protocol guarantees the following safety against consensus malfunction by virtue of its design :  

-   **Leader election safety**  – At most one leader per term)
-   **Log Matching safety**(If multiple logs have an entry with the same index and term, then those logs are guaranteed to be identical in all entries up through to the given index.
-   **Leader completeness**  – The log entries committed in a given term will always appear in the logs of the leaders following the said term)
-   **State Machine safety**  – If a server has applied a particular log entry to its state machine, then no other server in the server cluster can apply a different command for the same log.
-   **Leader is Append-only**  – A leader node(server) can only append(no other operations like overwrite, delete, update are permitted) new commands to its log
-   **Follower node crash**  – When the follower node crashes, all the requests sent to the crashed node are ignored. Further, the crashed node can’t take part in the leader election for obvious reasons. When the node restarts, it syncs up its log with the leader node

## Cluster membership and Joint Consensus

When the status of nodes in the cluster changes(cluster configuration changes), the system becomes susceptible to faults which can break the system. So, to prevent this, Raft uses what is known as a two phase approach to change the cluster membership. So, in this approach, the cluster first changes to an intermediate state(known as  **joint consensus**) before achieving the new cluster membership configuration. Joint consensus makes the system available to respond to client requests even when the transition between configurations is taking place. Thus, increasing the availability of the distributed system, which is a main aim.

## What are its advantages/Features

-   The Raft protocol is designed to be easily understandable considering that the most popular way to achieve consensus on distributed systems was the Paxos algorithm, which was very hard to understand and implement. Anyoone with basic knowledge and common sense can understand major parts of the protocol and the research paper published by Diego Ongaro and John Ousterhout
-   It is comparatively easy to implement than other alternatives, primarily the Paxos, because of a more targeted use case segment, assumptions about the distributed system. Many open source implementations of the Raft are available on the internet. Some are in  [Go](https://github.com/hashicorp/raft),  [C++](https://raft.github.io/slides/rustdiego2015.pdf),  [Java](https://github.com/hortonworks/ratis)
-   The Raft protocol has been decomposed into smaller subproblems which can be tackled relatively independently for better understanding, implementation, debugging, optimizing performance for a more specific use case
-   The distributed system following the Raft consensus protocol will remain operational even when minority of the servers fail. For example, if we have a 5 server node cluster, if 2 nodes fail, the system can still operate.
-   The leader election mechanism employed in the Raft is so designed that one node will always gain the majority of votes within a maximum of 2 terms.
-   The Raft employs RPC(remote procedure calls) to request votes and sync up the cluster(using AppendEntries). So, the load of the calls does not fall on the leader node in the cluster.
-   Raft was designed recently, so it employs modern concepts which were not yet understood at the time of the formulation of the Paxos and similar protocols.
-   Any node in the cluster can become the leader. So, it has a certain degree of fairness.
-   Many different open source implementations for different use cases are already out there




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
   ![ Replication in Elasticsearch ]( https://codingexplained.com/wp-content/uploads/7-1024x732.png )  
   
## Task 1 : Setup collectd to monitor various metrics for operating system and one of the following datastores ES/RMQ/AS 
[Collectd influxd graphana](http://www.inanzzz.com/index.php/post/ms6c/collectd-influxdb-and-grafana-integration)

### Step1: Installation of collectd 

```bash 
sudo apt-get update
sudo apt-get install collectd collectd-utils
```

### Step2: Configure collectd 

```bash 
sudo nano /etc/collectd/collectd.conf
```
Now uncomment the plugins 
1.  LoadPlugin cpu
2.  LoadPlugin disk
3.  LoadPlugin load
4.  LoadPlugin memory
5.  LoadPlugin processes
6.  LoadPlugin swap
7.  LoadPlugin user

In addition to above, enable  `LoadPlugin network`  then add block below to the bottom of the page. [more about network](https://collectd.org/wiki/index.php/Networking_introduction)
```xml
  <Plugin  "network">    
      Server "ip of influxd" "port"
  </Plugin>    
```
Star service 

```bash
sudo systemctl start collectd
```

## Task2: Setup influxdb on a vm

### Installing influxd
```bash
wget -qO- https://repos.influxdata.com/influxdb.key | sudo apt-key add -
source /etc/lsb-release
echo "deb https://repos.influxdata.com/${DISTRIB_ID,,} ${DISTRIB_CODENAME} stable" | sudo tee /etc/apt/sources.list.d/influxdb.list

sudo apt-get update && sudo apt-get install influxdb
sudo systemctl start influxdb.service
sudo systemctl start influx
```

### Create user along with influxd configuration 

```
1.  infludbVm:~$ influx
2.  Connected to http://localhost:8086 version 1.3.5
3.  InfluxDB shell version:  1.3.5
4.  >
5.  > CREATE USER chayank WITH PASSWORD 'chayank' WITH ALL PRIVILEGES
6.  >
7.  > SHOW USERS
8.  user    admin
9.  ----  -----
10.  chayank true
11.  >
12.  > EXIT

```
  
  #### restart the service

```
1.  influxdVm:~$ sudo systemctl restart influxdb

```
  

#### Verify database

  ```

1.  influxdbVm:~$ influx -username chayank -password chayank 
2.  Connected to http://localhost:8086 version 1.3.5
3.  InfluxDB shell version:  1.3.5
4.  > CREATE DATABASE collectd 
5.  > SHOW DATABASES
6.  name: databases
7.  name
8.  ----
9.  _internal
10.  collectd
11.  >

```  

#### Configuration for collectd

  

Find  `[[collectd]]`  in  `/etc/influxdb/influxdb.conf`  file and make it match settings below.

  ```

1.  [[collectd]]
2.   enabled =  true
3.   bind-address =  ":25826"
4.   database =  "collectd"
5.   retention-policy =  ""
6.   typesdb =  "/usr/local/share/collectd/types.db"
7.   batch-size =  5000
8.   batch-pending =  10
9.   batch-timeout =  "10s"
10.   read-buffer =  0

  ```

#### Download types.db

```  

sudo mkdir /usr/local/share/collectd
sudo wget -P /usr/local/share/collectd https://raw.githubusercontent.com/collectd/collectd/master/src/types.db

```
## Task3: send metrics to influxdb

###  check the metrc in influxdb
```
1.  influxdbVm:~$ influx -username chayank -password chayank
2.  Connected to http://localhost:8086 version 1.3.5
3.  InfluxDB shell version:  1.3.5
4.  >
5.  > USE collectd
6.  Using database collectd
7.  >
8.  > SHOW MEASUREMENTS
9.  name: measurements
10.  name
11.  ----
12.  cpu_value
13.  memory_value
14.  >
15.  >
16.  > SELECT * FROM cpu_value LIMIT 5
17.  name: cpu_value
18.  time host instance type type_instance value
19.  ----  ----  --------  ----  -------------  -----
20.  1504974634305158622 other 0 cpu user 2711
21.  1504974634305164974 other 0 cpu nice 0
22.  1504974634305167452 other 0 cpu system 2448
23.  1504974634305167969 other 0 cpu idle 2227665
24.  1504974634305168533 other 0 cpu wait 372
25.  >
26.  > SELECT * FROM memory_value LIMIT 5
27.  name: memory_value
28.  time host type type_instance value
29.  ----  ----  ----  -------------  -----
30.  1504974634305230505 other memory used 190013440
31.  1504974634305231222 other memory buffered 16171008
32.  1504974634305231662 other memory cached 265412608
33.  1504974634305232101 other memory free 42156032

```

## Task4 : plot these metrics on grafana dashboard 

### Step1: Installing graphan server [reference](https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-grafana-on-ubuntu-18-04) 

```bash
sudo apt-get install -y apt-transport-https
sudo apt-get install -y software-properties-common wget
wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -

```
```bash
echo "deb https://packages.grafana.com/enterprise/deb stable main" | sudo tee -a /etc/apt/sources.list.d/grafana.list
```
```bash
sudo apt-get update
sudo apt-get install grafana-enterprise
```
Run the server
```bash
sudo systemctl start grafana-server
```
### Step2: adding data source
1. Click on configuration
2. Data source
3. Click on add data source and select influxdb
[see here for further configuration of data source](https://drive.google.com/file/d/1mphfLs3hK-Z2DdkXIQcxqP2QHYC16Kht/view?usp=sharing) 

### Step3: adding dashboard 
1. Click '+' and select dashboard 
2. add new panel and select edit
3. select the data source and the select the required measurement to see in the graph


## Task5: Setup riemann on a vm 

### Step1: installation [reference ](https://riemann.io/quickstart.html)

```bash
$ wget https://github.com/riemann/riemann/releases/download/0.3.6/riemann-0.3.6.tar.bz2
$ tar xvfj riemann-0.3.6.tar.bz2
$ cd riemann-0.3.6 
```
Create a file config.rb 
```bash
sudo nano riemann-0.3.6/etc/config.rb
```
now add the followin
```
set :port, 4567
set :bind, "0.0.0.0"
```
Edit the host addres on riemann.config  as shown
```
; Listen on the local interface over TCP (5555), UDP (5555), and websockets
; (5556)
(let [host "ip of riemann-installed machine"]
```

Start the server
```bash
bin/riemann etc/riemann.config
```
install riemann tools
```bash
sudo apt-get install rubygems ruby-dev
sudo gem install riemann-client riemann-tools riemann-dash
```
Start the dashboard with the server running .  
```bash
riemann-dash riemann-0.3.6/etc/config.rb
```
[follow this after running the dash rieman](https://www.betsol.com/blog/build-your-own-monitoring-system/)

## Task6: Write a script to collect the metrics previously collected by collectd and send it to Riemann

### Step1 : install librarie
1. **riemann-client** [reference](https://pypi.org/project/riemann-client/) : to communicate with riemann dash board
```bash
pip install riemann-client
```
2. **elsticsearch** [reference](https://pypi.org/project/elasticsearch/) : to collect metrics of elasticsearch cluster
```bash
pip install elasticsearch
```
3. **psutil** [reference ](https://psutil.readthedocs.io/en/latest/)
```bash
pip install psutil
```
other references
1. Elasticsearch : https://kb.objectrocket.com/elasticsearch/how-to-use-the-cluster-api-in-the-elasticsearch-python-client-library-260
2. Rieman-client : https://github.com/gleicon/pyriemann/blob/master/examples/riemann_health.py
> Run the script with both the server and rieman dashboard borad      running, you should  see the metrics collected showing on dashboard


## Task7: The metrics should go to influxdb from Riemann 

### Configure the riemann.config file
navigate to riemann.config 


```bash
cd riemann-0.3.6/etc
```
edit and add the define a function as shown in lines

```bash
sudo nano riemann.config
```

```bash
(def send-influx
(influxdb {
:version :0.9
:host "<ip of influxdbVm>"
:port 8086
:db "name of db created in influxd"
:username "admin"
:password "admin"
:timeout 1000000})
```
call the same 

```bash
(streams
  (default :ttl 60
    ; Index all events immediately.
    index
    send-influx
    ; Log expired events.
    (expired
      (fn [event] (info "expired" event))))))
```

now stop restart the riemann-serve to load the change made 

## Prometheus

### downloading [Prometheus](https://prometheus.io/docs/prometheus/latest/getting_started/) 
```bash
tar xvfz prometheus-*.tar.gz
cd prometheus-*
./promethues
```
### downloading [node exporter](https://prometheus.io/docs/guides/node-exporter/#installing-and-running-the-node-exporter)
```bash
wget https://github.com/prometheus/node_exporter/releases/download/v*/node_exporter-*.*-amd64.tar.gz
tar xvfz node_exporter-*.*-amd64.tar.gz
cd node_exporter-*.*-amd64
./node_exporter
```

### downloading [elasticsearch-exporter](https://github.com/vvanholl/elasticsearch-prometheus-exporter)

```bash
cd /usr/share/elasticsearch
sudo bin/elasticsearch-plugin install analysis-phonetic
./bin/elasticsearch-plugin install -b https://github.com/vvanholl/elasticsearch-prometheus-exporter/releases/download/7.12.0.0/prometheus-exporter-7.12.0.0.zip
```

### Configure the Prometheus target

On your Prometheus servers, configure a new job as usual, add a new job in prometheus.yml.
For example, if you have a cluster of 2 nodes:
```yml
- job_name: elasticsearch
  scrape_interval: 10s
  metrics_path: "/_prometheus/metrics"
  static_configs:
  - targets:
    - node1:9200
    - node2:9200
```
<!--stackedit_data:
eyJoaXN0b3J5IjpbMjA4MzI1MzM5LC00MDQyMDE1NjAsMTU0Nz
Q2NTI1OCwyMzgwOTMyOTUsMTgyODAxMDAyMCwtMTM0NjEyNTg5
LC0xNTkwOTMxMzA0XX0=
-->
