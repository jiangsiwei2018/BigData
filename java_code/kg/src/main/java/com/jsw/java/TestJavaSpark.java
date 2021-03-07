package com.jsw.java;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

import org.apache.spark.SparkConf;
import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.api.java.JavaSparkContext;


public class TestJavaSpark {
	
	public static Iterator<Object> getValue(Iterator<String> keyListString)
			throws IOException {
		HbaseUtil app = new HbaseUtil();
		app.createConf();
        List<Object> l = new ArrayList<Object>();
        while (keyListString.hasNext()) {
        	String value= keyListString.next();
        	System.out.println(value);
			l.add(app.get(value));
		}
        return l.iterator();
	}

	@SuppressWarnings("resource")
	public static void main(String[] args) {
		
		SparkConf sparkConf = new SparkConf().setAppName("test").setMaster("local");

		JavaSparkContext sparkContext = new JavaSparkContext(sparkConf);
		
		List<String> list = new ArrayList<>();

        list.add("0001");
        list.add("0002");
        list.add("0003");
        list.add("0004");
        
		JavaRDD<Object> rdd = sparkContext.parallelize(list)
				.mapPartitions(iterator -> getValue(iterator));
		
		for (Object object : rdd.collect()) {
			System.out.println(object);
		}
	}
}
