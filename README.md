# test case

**关于其他测试，查看 [other.md](./other.md) 文档**

## 跨事务事务

**需求**

1) 分布式事务读强一致性：相同硬件配置下，通过反复执行插入和删除1000条数据（100次以上），保证数据可平均分配到不同的节点的条件下，通过查询所有节点的数据总数是否是0或1000，验证分布式事务读强一致。

2) 分布式事务写强一致性：相同硬件配置下，通过反复执行插入1000条数据（100次以上），保证数据可平均分配到不同的节点的条件下，通过统计所有节点的记录行数是否是1000的整数倍，验证分布式事务写强一致。

**安装包**
```shell
pip install mysql-connector-python
```

# 测试流程

**创建测试表**

```sql
CREATE TABLE `t3` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cname` varchar(20) DEFAULT NULL,
  `start_time` datetime(3) NOT NULL,
  `cid` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin; 
```

**脚本使用**

```shell
cd Script/

# 查看用法
usage: run_tidb.py [-h] [--host HOST] [-P PORT] [-u USER] [-p PASSWORD]
                   [-b DATABASE] [--thread THREAD_NUM] [--exe RANGE_NUM]
                   [--mode MODE] [--limit LIMIT]

Test case for cq

optional arguments:
  -h, --help           show this help message and exit
  --host HOST          TiDB's host
  -P PORT              TiDB's port
  -u USER              TiDB's user
  -p PASSWORD          TiDB's passwd
  -b DATABASE          TiDB's database
  --thread THREAD_NUM  execute thread
  --exe RANGE_NUM      Execution times
  --mode MODE          Test Case: id is insert and delete,Only test insert by
                       default
  --limit LIMIT        How many rows to delete or insert
[root@centos76_vm Script]# 
```

**说明**

1. --thread 是执行并发
2. --exe 是执行次数
3. --mode 默认是只插入，指定为 id 时，会执行 insert & delete
4. --limit 指定一个事务中 insert 和 delete 的行数