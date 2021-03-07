package com.jsw.scala

import java.util
import scala.collection.mutable

class ScalaTestDataStruct {
	def testList(): Unit={
		var list1:List[String] = List[String]("111", "222")
		list1 = list1 :+ "ddd"
		list1 = list1 :+ "ccc"

		list1 = list1.drop(1)
		list1.foreach(println)
		println(list1.drop(2))

//		Java
		var list:util.List[String] = new util.ArrayList[String]()
		list.add("aaa");
		list.add("bbb");
		list.toArray().foreach(println)
//		println(list)
//		println(list1)
	}

	def testSet(): Unit={
		var set: Set[String] = Set[String]("###", "222")
		set += ("aaa")
		set.foreach((item: String) => println(item))

		var set2:mutable.Set[String] = mutable.Set[String]()
		set2.add("ttt")
		set2.add("####")
		set.foreach((item: String) => println(item))
	}

	def testMap(): Unit={
		var map: Map[String, Any] = Map[String, Any]()
		map += ("zzz" -> "000000")
		map += ("ttt" -> "11111")
		map.foreach(println)

		var map2: mutable.Map[String, Any] = mutable.HashMap[String, Any]()
		map2.put("aaa", "1111111111")
		map2.put("bbb", "2222222222")

		println(map2)
		println(map2.remove("aaa"))
		println(map2)
	}
}

object ScalaTestDataStruct {
	def main(args: Array[String]): Unit = {
		new ScalaTestDataStruct().testList()
		new ScalaTestDataStruct().testSet()
		new ScalaTestDataStruct().testMap()
	}
}