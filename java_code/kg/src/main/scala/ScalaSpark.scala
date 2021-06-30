package com.jsw.scala

import org.apache.spark.SparkContext

class ScalaSpark {

}

object ScalaSpark {
	def main(args: Array[String]): Unit = {
		val sc = new SparkContext("local", "spark")
		val arr = Array.range(1, 10)
		val rdd = sc.parallelize(arr).map(item => item * 10)
		rdd.take(10).foreach(println)
		sc.stop()


	}
}
