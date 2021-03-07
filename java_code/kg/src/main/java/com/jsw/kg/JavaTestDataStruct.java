package com.jsw.kg;

import java.util.*;

class NewList<T> {
	
	List<T> list = new ArrayList<>();
	
	public List<T> add(T item) {
		list.add(item);
		return list;
	}
}


public class JavaTestDataStruct {
    //    List<T>, ArrayList<T>;
    //    Set<E>, HashSet<T>
    //    Map<String, T>, HashMap<String, T>
    public void testList() {
        List<String> list = new ArrayList<String>();
        list.add("aaa");
        list.add("bbb");
        list.add("ccc");
        System.out.println(list);
        for(String sss: list) {
            System.out.println(sss);
        }
        System.out.println(list.contains("aaa"));
//        Boolean s1 = list.remove("aaa");
//        String s2 = list.remove(0);
//        System.out.println(list);
    }

    public void testSet() {
        Set<String> set = new HashSet<String>();
        set.add("aaa");
        set.remove("aaa");
        set.add("bbb");
        for(String sss: set) {
            System.out.println(sss);
        }
    }

    public void testMap() {
        Map<String, Object> map = new HashMap<String, Object>();
        map.put("aaa", "111");
        map.put("bbb", "222");
        map.remove("aaa");
//        for(Map.Entry entry: map.entrySet()) {
//            System.out.println("Key = " + entry.getKey() + ", Value = " + entry.getValue());
//        }
    }

    public static void main(String[] args) {
        new JavaTestDataStruct().testList();
        new JavaTestDataStruct().testSet();
        new JavaTestDataStruct().testMap();

    }
}
