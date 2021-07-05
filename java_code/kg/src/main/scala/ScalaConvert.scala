package com.jsw.scala

import com.alibaba.fastjson.JSON
import com.alibaba.fastjson.serializer.SerializerFeature
import com.fasterxml.jackson.databind.ObjectMapper
import com.fasterxml.jackson.module.scala.DefaultScalaModule
import org.json4s.DefaultFormats
import org.json4s.jackson.Json

import scala.reflect.ClassTag
//通过反射我们可以做到，即通过类名获取对应的类：
//  获取运行时类型信息
//  通过类型信息实例化新对象
//  访问或调用对象的方法和属性等

object ScalaConvert {

  val objectMapper = new ObjectMapper()
  objectMapper.registerModule(DefaultScalaModule)

  // T 代表一个类型 ，而 Class[T]代表这个类型所对应的类, classOf[T]返回Class[T]
  // ClassTag 是隐式的类型上届，获得擦除后的类型信息; ClassTag[T]保存着在运行时被JVM擦除的类型T的信息。当我们在运行时想获得被实例化的Array的类型信息的时候，这个特性会比较有
  // T 定义函数使用的变量类型
  def jsonStr2Object[T: ClassTag](jsonString: String, objClass: Class[T]): T={
    JSON.parseObject(jsonString, objClass)
  }

  def jsonStr2Object2[T: ClassTag](jsonString: String, objClass: Class[T]): T={
    objectMapper.readValue(jsonString, objClass)
  }

  def object2JsonStr[T: ClassTag](obj: T): String = {
    JSON.toJSONString(obj, SerializerFeature.PrettyFormat)
  }

  def object2JsonStr2[T: ClassTag](obj: T): String = {
    objectMapper.writeValueAsString(obj)
  }

  def map2JsonStr(map: Map[String, Any]) = {
    Json(DefaultFormats).write(map)
  }

  def map2Object[T: ClassTag](map: Map[String, Any], objClass: Class[T]) = {
    val jsonStr = map2JsonStr(map)
    jsonStr2Object(jsonStr, objClass)
  }

  def main(args: Array[String]) = {
//    val map = Map("name"-> "Tony", "age"->18)
//    println(map2JsonStr(map))
//    println(map2Object(map, classOf[Person]))



    val map = Map("name"-> "Tony", "age"->18)
    val jsonStr = ScalaConvert.map2JsonStr(map)
    println(jsonStr)
    println(jsonStr2Object2(jsonStr, classOf[Person]))

    println(object2JsonStr2(jsonStr2Object2(jsonStr, classOf[Person])))
  }
}
