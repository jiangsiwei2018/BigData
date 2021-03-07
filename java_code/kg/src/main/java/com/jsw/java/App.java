package com.jsw.java;
	

public class App {

	public Site SiteList(String url) {
		 System.out.println( "Hello World! Jiansiwei, kg, Welcome! Hei, Hei" );
		 SiteFactory siteFactory = new SiteFactory();
		 siteFactory.initFactory();
		 Site site = siteFactory.getSite(url);
		 return site;
	}
	
	public static void main( String[] args ) {
		 App app = new App();
		 String url = "https://www.baidu.com";
		 Site site = app.SiteList(url);
		 System.out.println(site.process(url, "<html></html>"));
	}
	
}

