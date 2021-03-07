package com.jsw.java;

import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class JavaRegUtil {

    public static Matcher getMatcher(String pattern, String string) {
        Pattern r = Pattern.compile(pattern);
        Matcher m = r.matcher(string);
        return m;
    }

    public static Boolean search(String pattern, String string) {
        return JavaRegUtil.getMatcher(pattern, string).find();
    }

    public static List<String> findAll(String pattern, String string) {
        List<String> items = new ArrayList<String>();
        Matcher m = JavaRegUtil.getMatcher(pattern, string);
//        if(m.matches()) {
//            int count = m.groupCount();
//            for(int i=1; i<=count; i++) {
//                items.add(m.group(i));
//            }
//        }
        while (m.find()) {
			items.add(m.group());
		}
//        System.out.println(items);
        return items;
    }

    public static String replaceAll(String string, String pattern, String replace) {
        Matcher m = JavaRegUtil.getMatcher(pattern, string);
        if(m.find()) {
            return m.replaceAll(replace);
        }
        return "";
    }

    public static void main(String[] args) {
        String line = "This order was placed for QT3000! OK?";
        String pattern = "order.*placed";
        System.out.println(JavaRegUtil.search(pattern, line));
        System.out.println(JavaRegUtil.findAll(pattern, line));
    }

}