package com.jsw.kg;

import java.io.IOException;
import java.util.ArrayList;
//import java.util.Iterator;
import java.util.List;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.hbase.CellUtil;
import org.apache.hadoop.hbase.HBaseConfiguration;
import org.apache.hadoop.hbase.HColumnDescriptor;
import org.apache.hadoop.hbase.HTableDescriptor;
import org.apache.hadoop.hbase.TableName;
import org.apache.hadoop.hbase.client.Admin;
import org.apache.hadoop.hbase.client.Connection;
import org.apache.hadoop.hbase.client.ConnectionFactory;
import org.apache.hadoop.hbase.client.Delete;
import org.apache.hadoop.hbase.client.Get;
import org.apache.hadoop.hbase.client.Put;
import org.apache.hadoop.hbase.client.Result;
import org.apache.hadoop.hbase.client.ResultScanner;
import org.apache.hadoop.hbase.client.Scan;
import org.apache.hadoop.hbase.client.Table;
import org.apache.hadoop.hbase.util.Bytes;

//Scan类常用方法说明
//指定需要的family或column ，如果没有调用任何addFamily或Column，会返回所有的columns；
// scan.addFamily();
// scan.addColumn();
// scan.setMaxVersions(); //指定最大的版本个数。如果不带任何参数调用setMaxVersions，表示取所有的版本。如果不掉用setMaxVersions，只会取到最新的版本.
// scan.setTimeRange(); //指定最大的时间戳和最小的时间戳，只有在此范围内的cell才能被获取.
// scan.setTimeStamp(); //指定时间戳
// scan.setFilter(); //指定Filter来过滤掉不需要的信息
// scan.setStartRow(); //指定开始的行。如果不调用，则从表头开始；
// scan.setStopRow(); //指定结束的行（不含此行）；
// scan.setBatch(); //指定最多返回的Cell数目。用于防止一行中有过多的数据，导致OutofMemory错误。

//过滤器
//1、FilterList代表一个过滤器列表
//FilterList.Operator.MUST_PASS_ALL -->and
//FilterList.Operator.MUST_PASS_ONE -->or
//eg、FilterList list = new FilterList(FilterList.Operator.MUST_PASS_ONE);
//2、SingleColumnValueFilter
//3、ColumnPrefixFilter用于指定列名前缀值相等
//4、MultipleColumnPrefixFilter和ColumnPrefixFilter行为差不多，但可以指定多个前缀。
//5、QualifierFilter是基于列名的过滤器。
//6、RowFilter
//7、RegexStringComparator是支持正则表达式的比较器。
//8、SubstringComparator用于检测一个子串是否存在于值中，大小写不敏感。

//scan.setTimeStamp(NumberUtils.toLong("1370336286283"));
//scan.setTimeRange(NumberUtils.toLong("1370336286283"), NumberUtils.toLong("1370336337163"));
//scan.setStartRow(Bytes.toBytes("quanzhou"));
//scan.setStopRow(Bytes.toBytes("xiamen"));
//scan.addFamily(Bytes.toBytes("info"));
//scan.addColumn(Bytes.toBytes("info"), Bytes.toBytes("id"));

//查询列镞为info，列id值为1的记录
//方法一(单个查询)
// Filter filter = new SingleColumnValueFilter(
//         Bytes.toBytes("info"), Bytes.toBytes("id"), CompareOp.EQUAL, Bytes.toBytes("1"));
// scan.setFilter(filter);

//方法二(组合查询)
//FilterList filterList=new FilterList();
//Filter filter = new SingleColumnValueFilter(
//    Bytes.toBytes("info"), Bytes.toBytes("id"), CompareOp.EQUAL, Bytes.toBytes("1"));
//filterList.addFilter(filter);
//scan.setFilter(filterList);

public class HbaseUtil {
	private Configuration conf = null;
	private Connection conn = null;
	private Admin admin = null;
	private Table table = null;
	
	public void createConf() throws IOException{
//		Java客户端使用的配置信息是被映射在一个HBaseConfiguration 实例中. 
//		HBaseConfiguration有一个工厂方法, HBaseConfiguration.create(); 
//		运行这个方法的时候，他会去CLASSPATH,下找Hbase-site.xml，读他发现的第一个配置文件的内容。 
//		(这个方法还会去找hbase-default.xml ; hbase.X.X.X.jar里面也会有一个an hbase-default.xml). 
//		不使用任何hbase-site.xml文件直接通过Java代码注入配置信息也是可以的。例如，你可以用编程的方式设置ZooKeeper信息，只要这样做:

		//解决异常,可以不用
		conf = HBaseConfiguration.create();
//		conf.addResource("core-site.xml");
//		conf.addResource("hdfs-site.xml");
//		conf.addResource("hbase-site.xml");
		//设置zk集群地址,这里需要修改windows下的hosts文件
		conf.set("hbase.zookeeper.quorum","master:3000,slave1:3000,slave2:3000");
		//建立连接
		System.out.println(String.format("hbase.zookeeper.quorum: %s", conf.get("hbase.zookeeper.quorum")));
		conn = ConnectionFactory.createConnection(conf);
	}
	

	public void createTable() throws IOException{
		//获取表管理类
		admin = conn.getAdmin();
		//定义表
		HTableDescriptor hTableDescriptor = new HTableDescriptor(TableName.valueOf("student"));
		//定义列族
		HColumnDescriptor hColumnDescriptor = new HColumnDescriptor("info");
		//将列族添加到表中
		hTableDescriptor.addFamily(hColumnDescriptor);
		//执行建表操作
		admin.createTable(hTableDescriptor);
	
	}

	public void put() throws IOException{

		//获取表对象
		table = conn.getTable(TableName.valueOf("student"));
		//创建put对象
		Put put = new Put("p1".getBytes());
		//添加列
		put.addColumn("info".getBytes(), "name".getBytes(), "haha".getBytes());
		//向表格中添加put对象
		table.put(put);
		
	}

	public String get(String rowKey) throws IOException{
		//获取表对象
		table = conn.getTable(TableName.valueOf("student"));
		//用行键实例化get
		Get get = new Get(rowKey.getBytes());
		//增加列族名和列名条件
		get.addColumn("info".getBytes(), "name".getBytes());
		//执行,返回结果
		Result result = table.get(get);
		//取出结果
		System.out.println(result);
		String valStr = Bytes.toString(result.getValue("info".getBytes(), "name".getBytes()));
		return valStr;

	}

	public void scan() throws IOException{
		//获取表对象
		table = conn.getTable(TableName.valueOf("student"));
		//初始化scan示例
		Scan scan = new Scan();
		//增加过滤条件
		scan.addColumn("info".getBytes(), "name".getBytes());
		scan.addColumn("info".getBytes(), "sex".getBytes());
		//返回结果
		ResultScanner rss = table.getScanner(scan);
		//迭代取出结果
		for (Result result : rss) {
			String valStr = Bytes.toString(result.getValue("info".getBytes(), "name".getBytes()));
			String valStr2 = Bytes.toString(result.getValue("info".getBytes(), "sex".getBytes()));
			System.out.println(valStr + "\t" + valStr2);
		}
		
	}

	public void del() throws IOException{
		//获取表对象
		table = conn.getTable(TableName.valueOf("student"));
		//用行键实例化Delete实例
		Delete del = new Delete("p1".getBytes());
		//执行删除
		table.delete(del);
	}

	public void close() throws IOException{
		//关闭连接
		if(admin!=null){
			admin.close();
		}
		if(table!=null){
			table.close();
		}
		if(conn!=null){
			conn.close();
		}
	}
	
	public List<List<String>> qurryTableTestBatch(List<String> rowkeyList) throws IOException {
        List<Get> getList = new ArrayList<Get>();
        String tableName = "student";
        Table table = conn.getTable( TableName.valueOf(tableName));// 获取表
        for (String rowkey : rowkeyList){
            Get get = new Get(Bytes.toBytes(rowkey));
            getList.add(get);
        }
        Result[] results = table.get(getList);
        List<List<String>> list = new ArrayList<List<String>>();
        for (Result result : results){
        	List<String> list1 = new ArrayList<String>();
            for (org.apache.hadoop.hbase.Cell kv: result.rawCells()) {
                String value = Bytes.toString(CellUtil.cloneValue(kv));
//                System.out.println(value);
                list1.add(value);
            }
            list.add(list1);
        }
        System.out.println(list);
        return list;
    }

	public static List<Object> getValue(List<String> keyListString)
			throws IOException {
		HbaseUtil hbase = new HbaseUtil();
		hbase.createConf();
        List<Object> l = new ArrayList<Object>();
        for (String string : keyListString) {
			l.add(hbase.get(string));
		}
        hbase.close();
        return l;
	}
	
	public static void main(String[] args) throws Exception {
        List<String> list = new ArrayList<String>();
        list.add("0001");
        list.add("0003");
        System.out.println(HbaseUtil.getValue(list));
//		HbaseUtil app = new HbaseUtil();
//		app.createConf();
//
//        List<List<String>> l = app.qurryTableTestBatch(list);
//		System.out.println(l);
//		System.out.println("OK");
//		System.out.println(app.get("0003"));;
//		HbaseUtil.getValue("0001");
	}
}

