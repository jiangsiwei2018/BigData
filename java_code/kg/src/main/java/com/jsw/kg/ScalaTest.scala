package com.jsw.kg

class ScalaTest {

  def test(): List[String]={
    var list1:List[String] = List[String]("111", "222")
    list1 = list1 :+ "ddd"
    list1 = list1 :+ "ccc"
    list1

//    list1 = list1.drop(1)
//    list1.foreach((item: String) => println(item))
//    println(list1.drop(2))
  }
}

object ScalaTest {
  def main(args: Array[String]): Unit = {
    val s: ScalaTest = new ScalaTest()
    val l = s.test()
    l.foreach((item: String) => println(item))
  }
}
