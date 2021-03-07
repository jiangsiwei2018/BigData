package com.jsw.kg

import scala.util.matching.Regex


object ScalaRegUtil {

	def search(pattern: String, string: String): Boolean={
		val r:Regex = new Regex(pattern)
		r.pattern.matcher(string).matches
	}

	def findAll(pattern: String, string: String): List[String]={
		val r:Regex = new Regex(pattern)
		var list = List[String]()
		if(r.pattern.matcher(string).matches) {
			val m = r.findAllIn(string)
			while(m.hasNext) {
				list = list :+ m.next()
			}
		}
		list
	}

	def replaceAll(string: String, pattern: String, replace: String): String = {
		val r:Regex = new Regex(pattern)
		r.replaceAllIn(string, replace)
	}

	def main(args: Array[String]): Unit = {
		val s = ScalaRegUtil.search("(abc).*", "abcdef")
		println(s)
		val s1 = ScalaRegUtil.replaceAll("abcdef", "(abc).*", "aaa")
		println(s1)
		val s2 = ScalaRegUtil.findAll("(abc).*", "abcdef")
		println(s2)
	}
}
