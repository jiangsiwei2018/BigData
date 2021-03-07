package com.jsw.java;

import java.util.*;
import java.util.regex.*;

class Site {
    //    静态属性/方法不能被直接重写，实例属性/方法需要在构造函数中才能操作(近似重写)
    List<String> urlPatterns = new ArrayList<String>();
//    初始化时，不要设置值，否则会被继承到子类
//    public Site() {
//        this.urlPatterns.add("https?://www.common.com");
//    }

    public Map<String, Object> process(String url, String html) {
        Map<String, Object> map = new HashMap<String, Object>();
//        map.put("url", url);
//        map.put("html", html);
        return map;
    }
}

class Baidu extends Site {

    //    静态属性/方法不能被直接重写，实例属性/方法需要在构造函数中才能操作(近似重写)
    public Baidu() {
        this.urlPatterns.add(".*baidu.*");
    }
    public Map<String, Object> process(String url, String html) {
        Map<String, Object> map = new HashMap<String, Object>();
        map.put("url", url);
        map.put("html", html);
        map.put("params", "baidu");
        return map;
    }
}

class Tencent extends Site {

    //    静态属性/方法不能被直接重写，实例属性/方法需要在构造函数中才能操作(近似重写)
    public Tencent() {
        this.urlPatterns.add(".*qq.*");

    }
    public Map<String, Object> process(String url, String html) {
        Map<String, Object> map = new HashMap<String, Object>();
        map.put("url", url);
        map.put("html", html);
        map.put("params", "qq");
        return map;
    }
}


class SiteFactory {
    List<Site> siteList = new ArrayList<Site>();

    public void initFactory() {
        siteList.add(new Baidu());
        siteList.add(new Tencent());

    }
    public Site getSite(String url) {
        Site tempSite = new Site();
        for(Site site: this.siteList) {
            for(String urlPattern: site.urlPatterns) {
                if(Pattern.matches(urlPattern, url)) {
                    return site;
                }
            }
        }
        return tempSite;
    }
}


public class JavaFactory {
    //    java 中类属性需要先定义，才能使用！！！; interface 中一般不定义属性，更多的是接口函数
    public static void main(String[] args) {
        SiteFactory siteFactory = new SiteFactory();
        siteFactory.initFactory();
        String url = "https://www.baidu.com";
        Site site = siteFactory.getSite(url);
        System.out.println(site);
        Map<String, Object> map = site.process(url, "<html></html>");
        for(Map.Entry<String, Object> entry : map.entrySet()) {
            System.out.println("Key = " + entry.getKey() + ", Value = " + entry.getValue());
        }
    }

    public void test() {
        Site site = new Site();
        System.out.println(site.urlPatterns);
        Map<String, Object> map = site.process("https://www.baidu.com", "<html></html>");
        for(Map.Entry<String, Object> entry : map.entrySet()) {
            System.out.println("Key = " + entry.getKey() + ", Value = " + entry.getValue());
        }
    }
}
