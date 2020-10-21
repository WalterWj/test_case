# 数据导出

推荐使用 dumpling

# 数据分片测试

## 分区表 SQL

**Range 分区**

```sql
CREATE TABLE employees (
    id INT NOT NULL,
    fname VARCHAR(30),
    lname VARCHAR(30),
    hired DATE NOT NULL DEFAULT '1970-01-01',
    separated DATE NOT NULL DEFAULT '9999-12-31',
    job_code INT NOT NULL,
    store_id INT NOT NULL
)

PARTITION BY RANGE (store_id) (
    PARTITION p0 VALUES LESS THAN (6),
    PARTITION p1 VALUES LESS THAN (11),
    PARTITION p2 VALUES LESS THAN (16),
    PARTITION p3 VALUES LESS THAN (21)
);
```

**Hash 分区**

```sql
CREATE TABLE employees (
    id INT NOT NULL,
    fname VARCHAR(30),
    lname VARCHAR(30),
    hired DATE NOT NULL DEFAULT '1970-01-01',
    separated DATE NOT NULL DEFAULT '9999-12-31',
    job_code INT,
    store_id INT
)

PARTITION BY HASH(store_id)
PARTITIONS 4;
```

## sql 标准语法

**table schema**

```sql
CREATE TABLE `t1` (
  `id` int(11) NOT NULL,
  `cname` varchar(20) DEFAULT NULL,
  `start_time` datetime(3) NOT NULL,
  `cid` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE `t2` (
  `id` int(11) NOT NULL,
  `cname` varchar(20) DEFAULT NULL,
  `start_time` datetime(3) NOT NULL,
  `cid` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
);

insert into t1 values (1,'a',now(3),1),(2,'b',now(),2),(3,'c',now(),3);
insert into t2 values (1,'aa',now(3),1),(2,'bb',now(),2),(3,'cc',now(),3);

insert into t1 values (4,'a',now(3),1),(5,'b',now(),2),(6,'c',now(),3);
insert into t2 values (4,'aa',now(3),1),(5,'bb',now(),2),(6,'cc',now(),3);
```

**参测产品需支持 SELECT 排序分页，支持一张表或多张表连接的查询操作基础上，进行数据结果集的排序和分页**

```sql
-- 单表
select t1.* from t1 where id <=10 order by id limit 0,10;

-- 多表
select t1.* from t1 join t2 on t1.id=t2.id 
where t1.id <=10 order by id limit 0,10;
```

**参测产品需支持 SELECT 分组计算汇总，支持一张表或多张表连接的查询操作基础上，进行数据结果集的分组、计算和汇总**

```sql
-- 单表
select sum(t1.id) as sumid, count(1) as cnt,t1.cname
from t1 where t1.id <=10 group by t1.cname order by t1.cname limit 0,10;

-- 多表
select sum(t1.id) as sumid, count(1) as cnt,t2.cname
from t1 join t2 on t1.id=t2.id 
where t1.id <=10 group by t2.cname order by t2.cname limit 0,10;
```

**参测产品需支持 UPDATE 子查询，UPDATE 多表关联，支持 UPDATE 子查询和 UPDATE 多表关联**

```sql
-- 单表 update 子查询
update t1 set t1.cname = 'b' where t1.id in (select id from t1 where id = 1);

-- 多表关联 update 子查询
update t1 join t2 on t1.id=t2.id 
set t1.cname = 'a' 
where t2.id in (select t1.id from t1 where t1.id = 1);
```

**参测产品需支持 UPDATE ORDER BY 、SubQuery 等语法，支持一张表或多张表上的数据排序。**

```sql
-- 单表 update 子查询 order by 
update t1 set t1.cname = 'b' where t1.id in (select id from t1 where id = 1 order by id limit 1);

-- 多表关联 update 子查询 order by
update t1 join t2 on t1.id=t2.id 
set t1.cname = 'a' 
where t2.id in (select t1.id from t1 where t1.id = 1 order by t1.id limit 1);
```

**参测产品需支持 group by、union 等语法**

```sql
-- support group by 
select t1.cname ,count(1) as cnt from t1 group by cname;

-- support group by & union
select t1.cname ,count(1) as cnt from t1 group by cname
union all
select t2.cname ,count(1) as cnt from t2 group by cname;
```

**参测产品需支持 DELETE 子查询，DELETE 多表关联等语法。**

```sql
--  单表子查询 delete
delete from t1 where  t1.id in (select id from t1 where id = 10 order by id limit 1);

-- 多表关联子查询 delete
delete from t1 join t2 on t1.id=t2.id 
set t1.cname = 'a' 
where t2.id in (select t1.id from t1 where t1.id = 10 order by t1.id limit 1);
```

**参测产品需支持DELETE ORDER BY等语法。**

```sql
delete from t1 where  t1.id in (select id from t1 where id = 10 order by id limit 1);
```

**参测产品需支持时间函数精确到毫秒、时间函数取值在计算节点实现并做到全局不紊乱**

```sql
MySQL [test]> select * from t1;
+----+-------+-------------------------+------+
| id | cname | start_time              | cid  |
+----+-------+-------------------------+------+
|  1 | a     | 2020-10-20 16:20:34.084 |    1 |
|  2 | b     | 2020-10-20 16:20:34.000 |    2 |
|  3 | c     | 2020-10-20 16:20:34.000 |    3 |
|  4 | a     | 2020-10-20 16:23:52.652 |    1 |
|  5 | b     | 2020-10-20 16:23:52.000 |    2 |
|  6 | c     | 2020-10-20 16:23:52.000 |    3 |
+----+-------+-------------------------+------+
6 rows in set (0.00 sec)
```

**危险SQL操作拦截，对不符合设计规范的SQL语句、涉及数据访问安全的SQL语句进行拦截**

相关 [PR](http://github.com/pingcap/tidb/pull/20184/files) (需要 TIDB master 版本)