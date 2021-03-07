package com.jsw.kg;

import java.io.{BufferedWriter, File, FileWriter}

import scala.io.Source

object ScalaFileUtil{

	def readFile(path: String): Iterator[String]={
		val f = Source.fromFile(path)
		for (line: String <- f.getLines()) yield line
	}

	def wrieFile(path: String, lines: List[String], append: Boolean=false): Unit = {
		val writer = new BufferedWriter(new FileWriter(path, append))
		writer.write(lines.mkString("\n") + "\n")
		writer.close()
	}

	def getFileListObj(dir: File): Array[File] = {
		val fp = dir.listFiles
		val d = fp.filter(_.isDirectory)
		val f = fp.filter(_.isFile)
		f ++ d.flatMap(getFileListObj(_))
	}

	def getFileList(dir: String): List[String]={
		getFileListObj(new File(dir)).map(_.getPath).toList
	}

	def remove(path: String): Boolean={
		return JavaFileUtil.remove(path)
	}

	def main(args: Array[String]): Unit = {
		val path = "E:\\LocalCode\\allcode"
		getFileList(path).foreach(println)
//		writeFile(path, List("aaa", "bbb", "ccc"))
//		val lines = readFile(path)
//		lines.foreach(println)
	}
}
