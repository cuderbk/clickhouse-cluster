# ClickHouse Cluster Deployment with Ansible

## Overview
This repository provides an **Ansible-based automation** for deploying a **ClickHouse Cluster with sharding** on a **single server**. This setup is useful for:

- **Development & Testing**: Quickly simulating a distributed ClickHouse setup without needing multiple physical/virtual machines.
- **Performance Benchmarking**: Evaluating ClickHouse cluster sharding capabilities in a local environment.
- **Simplified Management**: Using Ansible to manage, configure, and scale ClickHouse clusters effortlessly.

## Features
- **Automated ClickHouse installation** on a single server.
- **Cluster configuration with multiple shards & replicas**.
- **Replication setup using  Zookeeper** 
- **Configurable number of shards and replicas**.
- **Customizable ClickHouse settings via Ansible variables**.

## Prerequisites
- A **Linux-based server** (Ubuntu, Debian, CentOS, etc.).
- **Python 3** installed.
- **Clickhouse server** installed.
- **Zookeeper 3** installed.
```bash
    sudo apt update
    sudo apt install zookeeper -y
    /usr/share/zookeeper/bin/zkServer.sh start
    echo srvr | nc localhost 2181
  ```
- **Ansible** installed on the control machine:
  ```bash
    sudo apt-add-repository ppa:ansible/ansible
    sudo apt install ansible
  ```
- **SSH access** to the target server. (I'm deploy on current server, so... it no need)

## Installation
### 1. Clone the Repository
```bash
git clone https://github.com/cuderbk/clickhouse-cluster.git
cd clickhouse-cluster
```

### 2. Configure Inventory File
Edit the `vars/shards.yml` file to define the ClickHouse cluster shards metadata. Example:
```ini
    cluster_name: "StationCluster"

    shards:
    - { host: "localhost", port: 9100, user: "default", password: "shard1", instance: 1, existing: false }
    - { host: "localhost", port: 9101, user: "default", password: "shard2", instance: 2, existing: false }
    - { host: "localhost", port: 7100, user: "default", password: "shard3", instance: 3, existing: false }
    - { host: "localhost", port: 7101, user: "default", password: "shard4", instance: 4, existing: false }
```

### 3. Run the Playbook
Execute the Ansible playbook to deploy ClickHouse cluster:
```bash
    make setup-cluster
```

## Usage
### Access ClickHouse Client
Once deployed, you can access the ClickHouse client:
```bash
clickhouse-client --host 127.0.0.1 --user default --password shard1
```
### Verify Cluster Status
Run the following command inside ClickHouse:
```sql
SELECT * FROM system.clusters WHERE cluster='StationCluster';
```

## Configuration
### Sharding Strategy
The playbook sets up **sharded tables** using the Distributed engine. Example table creation:
```sql
CREATE TABLE distributed_table ON CLUSTER 'StationCluster'
AS local_table ENGINE = Distributed('StationCluster', 'default', 'local_table', rand());
```

### Replication Setup
Each shard has a replicated table using `ReplicatedMergeTree`:
```sql
CREATE TABLE local_table ON CLUSTER 'StationCluster' (
    id UInt64,
    name String
) ENGINE = MergeTree()
ORDER BY id;
```
## Troubleshooting
### Check ClickHouse Logs
```bash
sudo journalctl -u clickhouse-server --no-pager | tail -n 50
```
### Restart ClickHouse Service
```bash
sudo systemctl restart clickhouse-<instance-number>
```

## License
MIT License. Feel free to modify and contribute!

## Author
Maintained by cuderbk.

## Contributions
Pull requests are welcome! 🚀

