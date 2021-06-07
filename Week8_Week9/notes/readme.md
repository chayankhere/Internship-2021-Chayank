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

[reference]( https://superuser.com/questions/420557/mbr-how-does-bios-decide-if-a-drive-is-bootable-or-not#:~:text=The%20BIOS%20decides%20if%20a,at%20the%20446th%20byte)

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

![GRUB stages](https://www.linuxnix.com/wp-content/uploads/2013/04/Linux-Booting-process.png) 
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
Words                 Document
ant                   doc1
demo                  doc2
world                 doc1, doc2
```

<img src="https://github.com/Chayank-S/images/blob/main/forwar.png" width="500" height="500">
<img src="https://github.com/Chayank-S/images/blob/main/inwar.png" width="500" height="500">
<img src="https://github.com/Chayank-S/images/blob/main/spars.png" width="860" height="860">
<img src="https://github.com/Chayank-S/images/blob/main/lm1.png" width="860" height="360">
<img src="https://github.com/Chayank-S/images/blob/main/lm2.png" width="860" height="360">
<img src="https://github.com/Chayank-S/images/blob/main/lm3.png" width="860" height="360">
<img src="https://github.com/Chayank-S/images/blob/main/lm4.png" width="860" height="360">

