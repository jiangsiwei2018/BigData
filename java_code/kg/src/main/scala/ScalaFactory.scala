package com.jsw.scala

import scala.collection.mutable


class BaseSite {
	//  属性和方法都可以被重写
	val urlPatterns = List[String]()
	def process(url: String, html: String): mutable.Map[String, Any]={
		var map = mutable.HashMap[String, Any]()
		map.put("url", url)
		map.put("html", html)
		map.put("params", "")
		map
	}
}

class BaseBaidu extends BaseSite {

	//  属性和方法都可以被重写
	override val urlPatterns = List[String](".*baidu.*")

	override def process(url: String, html: String): mutable.Map[String, Any] = {
		var map = super.process(url, html)
		map.put("params", "baidu")
		map
	}
}

class BaseSiteFactory {

	// 如果私有属性不想外部访问 可以加[this]
	var siteList = List[BaseSite]()

	def initFactory(): Unit= {
	  siteList :+= new BaseBaidu()
	}

	def getSite(url: String): BaseSite = {
		var tempSite: BaseSite = new BaseSite()
		println(siteList)
		for (site: BaseSite <- siteList) {
			for (urlPattern: String <- site.urlPatterns) {
				if(ScalaRegUtil.search(urlPattern, url)) {
					return site
				}
			}
		}
		tempSite
	}
}

object ScalaFactory {
	//	Ø  首先，需要使用isInstanceOf 判断对象是否为指定类的对象，
	//      	如果是的话，则可以使用 asInstanceOf 将对象转换为指定类型；
	//	Ø  注意：p.isInstanceOf[XX] 判断 p 是否为 XX 对象的实例；
	//      	p.asInstanceOf[XX] 把 p 转换成 XX 对象的实例
	//	Ø  isInstanceOf 只能判断出对象是否为指定类以及其子类的对象，而不能精确的判断出，对象就是指定类的对象；
	//	Ø  如果要求精确地判断出对象就是指定类的对象，那么就只能使用 getClass 和 classOf 了；
	//	Ø  p.getClass 可以精确地获取对象的类，classOf[XX]可以精确的获取类，然后使用 == 操作符即可判断；

	def main(args: Array[String]): Unit = {
		val siteFactory: BaseSiteFactory = new BaseSiteFactory()
		siteFactory.initFactory()
		val url: String = "https://www.baidu.com"
		val site: BaseSite = siteFactory.getSite(url)
		val map = site.process(url, "<html></html>")
		map.foreach(println)
	}
}