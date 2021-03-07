package com.jsw.kg;

import java.io.*;
import java.util.ArrayList;
import java.util.List;


public class JavaFileUtil {

    public static List<String> readFile(String path) throws IOException {
        List<String> lines = new ArrayList<String>();
        if(!exists(path)) {
            return lines;
        }
        BufferedReader reader = new BufferedReader(new FileReader(path));
        String line = reader.readLine();
        while (line != null) {
            line = reader.readLine();
            lines.add(line);
        }
        reader.close();
        return lines;
    }

    public static void writeFile(String path, List<String> lines) throws IOException {
        if(!exists(path)) {
            return;
        }
        BufferedWriter writer = new BufferedWriter(new FileWriter(path));
        for (String line: lines){
            writer.write(line);
        }
        writer.close();
    }

    public static Boolean exists(String path) {
        File file = new File(path);		//获取其file对象
        return file.exists();
    }

    public static List<String> getFileList(String path, List<String> files) {
        if (!exists(path)) {
            return files;
        }
        File file = new File(path);		//获取其file对象
        File[] fs = file.listFiles();	//遍历path下的文件和目录，放在File数组中
        for(File f: fs) {				//遍历File[]数组
            if(f.isDirectory())
                getFileList(f.getPath(), files);
            else {
                files.add(f.getPath());
            }
        }
        return files;
    }

    public static void mkdir(String path) {
        File file = new File(path);
        // 现在创建目录
        file.mkdirs();
    }

    public static boolean remove(String path) {
        if(!exists(path)) {
            return false;
        }
        File file = new File(path);
        // 现在创建目录
        if(file.isFile()) {
            System.out.println("delete file: " + file.getPath());
            return file.delete();
        } else {
            for(File f: file.listFiles()) {
                remove(f.getPath());
            }
            System.out.println("delete dir: " + file.getPath());
            return file.delete();
        }
    }

    public static void main(String[] args) {
    	JavaFileUtil jFileUtil = new JavaFileUtil();
    	System.out.println(jFileUtil.getClass().getResource("/hadoop"));
        String path = "src/main/resources/";
        List<String> files = new ArrayList<String>();
        System.out.println(files);
        JavaFileUtil.getFileList(path, files);
        for (String file: files) {
            System.out.println(file);
        }
    }
}
