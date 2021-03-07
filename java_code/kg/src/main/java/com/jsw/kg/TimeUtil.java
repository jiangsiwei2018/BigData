package com.jsw.kg;

import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Calendar;

public class TimeUtil {

    public static String UniformFormat = "yyyy-MM-dd HH:mm:SS";

    public static String timeFormat(Date date, String format) {
        DateFormat fm = new SimpleDateFormat(format);
        return fm.format(date);
    }

    public static String timeFormat(Date date) {
        return TimeUtil.timeFormat(date, UniformFormat);
    }

    public static String timeFormat() {
        return TimeUtil.timeFormat(new Date(), UniformFormat);
    }

    public static String timeFormat(Calendar calendar, String format) {
        Date date = calendarToDate(calendar);
        return TimeUtil.timeFormat(date, format);
    }

    public static String timeFormat(Calendar calendar) {
        return TimeUtil.timeFormat(calendar, UniformFormat);
    }

    /**
     * 时间转换： 字符串转Date时间, 然后再转其他时间字符串
     */
    public static String timeFormat(String source, String sourceFormat, String format) {
        Date date = timeStringToDate(source, sourceFormat);
        return timeFormat(date, format);
    }

    /**
     * 时间转换： 字符串转Date时间, 然后再转默认通用时间字符串
     */
    public static String timeFormat(String source, String sourceFormat) {
        return timeFormat(source, sourceFormat, UniformFormat);
    }

    /**
     * 时间转换： 字符串转Date时间
     */
    public static Date timeStringToDate(String source, String sourceFormat) {
        DateFormat fm = new SimpleDateFormat(sourceFormat);
        Date date = null;
        try {
            date = fm.parse(source);
        } catch (ParseException e) {
            e.printStackTrace();
        }
        return date;
    }

    public static Calendar dateToCalendar(Date date) {
        Calendar calendar = Calendar.getInstance();
        calendar.setTime(date);
        return calendar;
    }

    public static Date calendarToDate(Calendar calendar) {
        Date date = calendar.getTime();
        return date;
    }

    public static long timeStamp(Date date) {
        return date.getTime();
    }

    public static long timeStamp(Calendar calendar) {
        //    return calendar.getTimeInMillis();
        return timeStamp(calendarToDate(calendar));
    }

    public static long timeStamp() {
        return timeStamp(new Date());
    }

    public static Date timeStampToDate(long time) {
        return new Date(time);
    }

    public static void main(String[] args) {
        Date date = new Date();
        System.out.println(timeFormat(date));
        System.out.println(timeStamp(date));
        System.out.println(timeStamp(timeStringToDate("2005-06-09", "yyyy-MM-dd")));

        System.out.println("###############");
        System.out.println(new Date().getTime());

        System.out.println(timeStampToDate(1386665666777L));
    }

}
