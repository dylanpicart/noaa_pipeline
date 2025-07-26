Here's a structured, chronological, and **step-by-step action plan** to systematically resolve **all** identified issues:

## ✅ **Goal**:

* Ensure all four containers (**NameNode, DataNode, NodeManager, ResourceManager**) run smoothly and healthily.
* Fix container connectivity issues.
* Properly configure memory allocation.
* Set and verify storage directories.
* Confirm and correct Hadoop configuration files (`core-site.xml`, `hdfs-site.xml`, `yarn-site.xml`, `mapred-site.xml`).

---

## 🛠️ Step 1: **Ensure Containers Are Up and Connected**

### 1.1 Check the Running Containers

Confirm each container is running:

```bash
docker-compose ps
```

* Confirm status is "Up" for:

  * `noaa-hadoop-namenode`
  * `noaa-hadoop-datanode`
  * `noaa-yarn-resourcemanager`
  * `noaa-yarn-nodemanager`

### 1.2 Verify Container Networking

Make sure all containers share the same Docker network:

```bash
docker network inspect noaa_network
```

* Check under `"Containers"` to ensure all four container IDs/names are listed.

---

## 🛠️ Step 2: **Resolve Hadoop Container Connectivity**

### 2.1 NameNode Availability

Ensure NameNode is up and listening on the proper ports (`9000` RPC and `9870` WebUI):

```bash
docker exec -it noaa-hadoop-namenode bash
jps
```

You should see:

* `NameNode`
* Optionally: `SecondaryNameNode`, etc.

Check port accessibility (on host browser or curl):

* Web UI:

```bash
curl http://localhost:9870
```

### 2.2 DataNode Connectivity to NameNode

Confirm DataNode can resolve and reach NameNode:

```bash
docker exec -it noaa-hadoop-datanode bash
ping noaa-hadoop-namenode
```

* **Successful**: Proceed.
* **Fail**: Fix Docker network or DNS resolution.

### 2.3 ResourceManager Connectivity

Ensure ResourceManager can resolve NameNode and DataNode:

```bash
docker exec -it noaa-yarn-resourcemanager bash
ping noaa-hadoop-namenode
ping noaa-hadoop-datanode
```

### 2.4 NodeManager Connectivity

Check NodeManager connectivity to ResourceManager:

```bash
docker exec -it noaa-yarn-nodemanager bash
ping noaa-yarn-resourcemanager
```

---

## 🛠️ Step 3: **Memory Management and Allocation Issues**

### 3.1 Check JVM Heap Space Settings

Review your container JVM heap sizes to avoid thrashing and performance warnings:

* Modify `HADOOP_HEAPSIZE` or YARN resource limits via environment variables (`docker-compose.yaml`):

```yaml
environment:
  - HADOOP_HEAPSIZE=2048 # example: 2GB heap
  - YARN_NODEMANAGER_RESOURCE_MEMORY_MB=4096
```

### Recommended Memory Allocation:

* **NameNode**: At least 4 GB heap (production) or 2 GB heap (development).
* **DataNode**: Minimum 1-2 GB heap.
* **ResourceManager**: 2-4 GB heap.
* **NodeManager**: Limit container resource allocation to avoid exceeding total memory.

Update your Docker Compose accordingly.

### 3.2 Restart After Changes

```bash
docker-compose down
docker-compose up -d
```

---

## 🛠️ Step 4: **Storage Directories Verification**

### 4.1 NameNode Directories

Ensure NameNode storage directories (`dfs.namenode.name.dir`) are properly configured and writable:

Inside NameNode container:

```bash
docker exec -it noaa-hadoop-namenode bash
hdfs getconf -confKey dfs.namenode.name.dir
```

Check directory permissions:

```bash
ls -la /path/to/namenode/dir
```

### 4.2 DataNode Directories

Ensure DataNode storage directories (`dfs.datanode.data.dir`) are configured and writable:

```bash
docker exec -it noaa-hadoop-datanode bash
hdfs getconf -confKey dfs.datanode.data.dir
```

Confirm directory permissions similarly.

---

## 🛠️ Step 5: **Configuration File Checks**

### 5.1 Hadoop Config Files

Confirm the following files (`core-site.xml`, `hdfs-site.xml`, `yarn-site.xml`, `mapred-site.xml`) inside each container.

#### core-site.xml (`fs.defaultFS`):

```xml
<property>
  <name>fs.defaultFS</name>
  <value>hdfs://noaa-hadoop-namenode:9000</value>
</property>
```

#### hdfs-site.xml (`dfs.replication`, RPC addresses):

NameNode container:

```xml
<property>
  <name>dfs.namenode.rpc-address</name>
  <value>noaa-hadoop-namenode:9000</value>
</property>
```

DataNode container (ensure matches NameNode's RPC):

```xml
<property>
  <name>dfs.datanode.address</name>
  <value>0.0.0.0:9866</value>
</property>
```

#### yarn-site.xml (`ResourceManager` and `NodeManager` addresses):

```xml
<property>
  <name>yarn.resourcemanager.hostname</name>
  <value>noaa-yarn-resourcemanager</value>
</property>
```

Ensure these configurations match exactly across containers.

---

## 🛠️ Step 6: **Restart and Verify Hadoop Cluster**

### 6.1 Restart Cluster Cleanly

```bash
docker-compose down
docker-compose up -d
```

### 6.2 Check Hadoop Health

Inside NameNode container, confirm HDFS status:

```bash
docker exec -it noaa-hadoop-namenode bash
hdfs dfsadmin -report
```

* Ensure DataNode is registered.

### 6.3 Check YARN Health

Open YARN ResourceManager Web UI (`http://localhost:8088`) to confirm NodeManager registration and resource status.

---

## 🛠️ Step 7: **Final Verification and Testing**

### 7.1 Test HDFS Storage

Inside NameNode or DataNode:

```bash
hdfs dfs -mkdir -p /test_dir
hdfs dfs -put test_file.txt /test_dir/
hdfs dfs -ls /test_dir
```

### 7.2 Run Sample YARN Job (Optional but Recommended)

```bash
yarn jar $HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-examples-*.jar pi 2 10
```

---

## 📌 **Summary of Steps:**

| Step | Task                                |
| ---- | ----------------------------------- |
| 1    | Verify containers and networking    |
| 2    | Ensure inter-container connectivity |
| 3    | Adjust and manage memory allocation |
| 4    | Verify and fix storage directories  |
| 5    | Confirm Hadoop configuration files  |
| 6    | Restart and check Hadoop cluster    |
| 7    | Final verification and run tests    |

---

