package com.jsw.scala

import com.alibaba.fastjson.JSON
import com.alibaba.fastjson.serializer.SerializerFeature
import org.json4s.DefaultFormats
import org.json4s.jackson.Json
import scala.reflect.ClassTag





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
  def convert()={
    // yaml文件读取/配置读取
    // object转json
    // json转map
    // map转object
    //    JSON.toJSONString(map, SerializerFeature.WriteMapNullValue)
    val person: Person = Person()
    person.name = "Jack"
    person.age = 20
    //    JSON.parseObject(jsonString, classOf[Nothing])
    //    JSON.toJSONString([person], SerializerFeature.BeanToArray)
    val personJson = JSON.toJSONString(person, SerializerFeature.PrettyFormat)
    val personObject = JSON.parseObject(personJson, classOf[Person])
    println(personJson)
    personObject.name = "Tom"
    println(personObject)

    val map = Map("name"-> "Tony", "age"->18)
    val jsonString = Json(DefaultFormats).write(map)
    println(jsonString)
    println(JSON.parseObject(jsonString, classOf[Person]))


  }

  def aa[T: ClassTag](jsonString: String, obj: Class[T]): T={
    JSON.parseObject(jsonString, obj)
  }

  def main(args: Array[String]): Unit = {
    ScalaTest.convert()

    val person: Person = Person()
    person.name = "Tan"
    person.age = 20
    //    JSON.parseObject(jsonString, classOf[Nothing])
    //    JSON.toJSONString([person], SerializerFeature.BeanToArray)
    val personJson = JSON.toJSONString(person, SerializerFeature.PrettyFormat)
    println(aa(personJson, classOf[Person]))
//    val s: ScalaTest = new ScalaTest()
//    val l = s.test()
//    l.foreach((item: String) => println(item))
  }
}
