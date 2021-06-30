package com.jsw.scala;
import scala.beans.BeanProperty

case class Person(
                   @BeanProperty var name: String = "",
                   @BeanProperty var age: Int = 0
                 )
