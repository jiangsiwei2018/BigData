package com.jsw.java;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.dataformat.yaml.YAMLFactory;

import java.io.IOException;
import java.io.InputStream;

public class YamlConfigUtil {

    public static YamlConfigUtil instance = null;
    public static Config config;

    public YamlConfigUtil() throws IOException {
        ObjectMapper mapper = new ObjectMapper(new YAMLFactory());
        InputStream fileStream = getClass().getClassLoader().getResourceAsStream("config.yaml");
        YamlConfigUtil.config = mapper.readValue(fileStream, Config.class);
    }

    public static YamlConfigUtil getInstance() throws IOException {
        if(YamlConfigUtil.instance == null) {
            YamlConfigUtil.instance = new YamlConfigUtil();
        }
        return YamlConfigUtil.instance;
    }

    public static class Config {
        @JsonProperty("mysql.config")
        MysqlConfig mysqlConfig;

        @JsonProperty("hdfs.config")
        HdfsConfig hdfsConfig;
    }

    public static class MysqlConfig {
        @JsonProperty("database")
        MysqlDatabase database;
    }

    public static class MysqlDatabase {
        @JsonProperty("username")
        String username;
        @JsonProperty("password")
        String password;
    }

    public static class HdfsConfig {
        @JsonProperty("common.path")
        String commonPath;
    }


    public static void main(String[] args) throws IOException {
        YamlConfigUtil.Config configObj = YamlConfigUtil.getInstance().config;
        String config = configObj.mysqlConfig.database.username;
        System.out.println(config);
    }

}
