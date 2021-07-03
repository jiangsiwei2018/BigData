package com.jsw.scala

import com.fasterxml.jackson.annotation.JsonProperty
import com.fasterxml.jackson.databind.ObjectMapper
import com.fasterxml.jackson.module.scala.DefaultScalaModule
import com.fasterxml.jackson.dataformat.yaml.YAMLFactory


object ScalaYamlConfigUtil {

  val mapper = new ObjectMapper(new YAMLFactory())
  mapper.registerModule(DefaultScalaModule)
  val fileStream = getClass.getResourceAsStream("config.yaml")
  val config: Config = mapper.readValue(fileStream, classOf[Config])


  case class Config(
                     @JsonProperty("mysql.config") var mysqlConfig: MysqlConfig = null,
                     @JsonProperty("hdfs.config") var hdfsConfig: HDFSConfig = null
                   )


  case class MysqlConfig(
                    @JsonProperty("database") var database: MysqlDataBase = null)


  case class HDFSConfig(@JsonProperty("common.path") var commonPath: String = null)


  case class MysqlDataBase(
                            @JsonProperty var username: String = null,
                            @JsonProperty var password: String = null)


  def main(args: Array[String]): Unit = {
    val username = config.mysqlConfig.database.username
    println(username)


  }
}
