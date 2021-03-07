# encoding=utf-8
import json
from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession


class SparkUtil:
    _session = None
    _sc = None   # python
    _jsc = None  # java
    _rdd = None

    @staticmethod
    def get_spark_session(master=None, appName=None, conf=None):
        """
        :param master:
        :param appName:
        :param conf:
        :return:
        """
        if not SparkUtil._session:
            if not conf:
                conf = SparkConf()
            if master:
                conf.set('spark.master', master)
            if appName:
                conf.set('spark.app.name', appName)
            SparkUtil._session = \
                SparkSession.builder.config(conf=conf).getOrCreate()
        return SparkUtil._session

    @staticmethod
    def get_spark_context(master=None, appName=None, conf=None):
        if SparkUtil._session:
            SparkUtil._sc = SparkUtil._session.sparkContext
        elif not SparkUtil._sc:
            if not conf:
                conf = SparkConf()
            if master:
                conf.set('spark.master', master)
            if appName:
                conf.set('spark.app.name', appName)
            SparkUtil._sc = SparkContext(conf=conf)
        return SparkUtil._sc

    @staticmethod
    def get_java_spark_context():
        if SparkUtil._sc:
            SparkUtil._jsc = SparkUtil._sc._jsc
        return SparkUtil._jsc

    @staticmethod
    def get_sql_context():
        return SparkUtil._session._wrapped

    @staticmethod
    def get_java_sql_context():
        # return SparkUtil._session._jsparkSession.sqlContext()
        return SparkUtil._session._jwrapped

    @staticmethod
    def get_spark_jvm():
        return SparkUtil._sc._jvm

    @staticmethod
    def get_spark_logger(log_name=None, log_level='INFO'):
        SparkUtil._sc.setLogLevel(log_level)
        jvm = SparkUtil.get_spark_jvm()
        return jvm.org.apache.log4j.LogManager.getLogger(log_name)

    @staticmethod
    def stop():
        try:
            if SparkUtil._session:
                SparkUtil._session.stop()
            else:
                SparkUtil._sc.stop()
        except:
            pass

    @staticmethod
    def get_hbase_conf_read(hosts=None, table=None, columns='', conf={}):
        """
        rdd = sc.newAPIHadoopRDD(**conf)
        "hbase.mapreduce.scan.row.start": '2019-04-29_',
        "hbase.mapreduce.scan.row.stop": '2019-04-30_',
        "hbase.mapreduce.scan.columns": "family1:column1 family1:column2 family2:column1"
        hbase.mapreduce.scan.row.start
        hbase.mapreduce.scan.row.stop
        hbase.mapreduce.scan.column.family
        hbase.mapreduce.scan.columns
        hbase.mapreduce.scan.timestamp
        hbase.mapreduce.scan.timerange.start
        hbase.mapreduce.scan.timerange.end
        hbase.mapreduce.scan.maxversions
        hbase.mapreduce.scan.cacheblocks
        hbase.mapreduce.scan.cachedrows
        hbase.mapreduce.scan.batchsize
        hbase.mapreduce.scan
        :param hosts:
        :param table:
        :param columns:
        :param conf:
        :return:
        """
        config = {
            "inputFormatClass": "org.apache.hadoop.hbase.mapreduce.TableInputFormat",
            "keyClass": "org.apache.hadoop.hbase.io.ImmutableBytesWritable",
            "valueClass": "org.apache.hadoop.hbase.client.Result",
            "keyConverter": "org.apache.spark.examples.pythonconverters.ImmutableBytesWritableToStringConverter",
            "valueConverter": "org.apache.spark.examples.pythonconverters.HBaseResultToStringConverter",
            "conf": {
                "hbase.zookeeper.quorum": hosts,
                "hbase.mapreduce.inputtable": table
            }
        }
        if columns:
            config['conf']["hbase.mapreduce.scan.columns"] = columns
        if conf:
            if 'conf' in conf:
                config['conf'].update(conf['conf'])
                conf.pop('conf')
            config.update(conf)
        return config

    @staticmethod
    def get_hbase_conf_write(hosts=None, table=None, conf=None):
        """
        rdd.saveAsNewAPIHadoopDataset(**conf)
        :param hosts:
        :param table:
        :param conf:
        :return:
        """
        config = {
            # "path": "-",
            "keyConverter": "org.apache.spark.examples.pythonconverters.StringToImmutableBytesWritableConverter",
            "valueConverter": "org.apache.spark.examples.pythonconverters.StringListToPutConverter",
            "conf": {
                "hbase.zookeeper.quorum": hosts,
                "hbase.mapred.outputtable": table,
                "mapreduce.job.outputformat.class": "org.apache.hadoop.hbase.mapreduce.TableOutputFormat",
                "mapreduce.job.output.key.class": "org.apache.hadoop.hbase.io.ImmutableBytesWritable",
                "mapreduce.job.output.value.class": "org.apache.hadoop.io.Writable"
            }
        }
        if conf:
            if 'conf' in conf:
                config['conf'].update(conf['conf'])
                conf.pop('conf')
            config.update(conf)
        return config

    @staticmethod
    def get_es_conf_read(hosts, _index=None, _type=None, query=None, conf=None):
        """
        # spark-commit --jars elasticsearch-hadoop-6.4.1.jar
        rdd = sc.newAPIHadoopRDD(**conf)
        :return:
        """
        query = '' if not query else (json.dumps(query) if isinstance(query, dict) else query)
        config = {
            "inputFormatClass": "org.elasticsearch.hadoop.mr.EsInputFormat",
            "keyClass": "org.apache.hadoop.io.NullWritable",
            "valueClass": "org.elasticsearch.hadoop.mr.LinkedMapWritable",
            "conf": {
                "es.nodes": hosts,
                "es.resource": f"{_index}/{_type}",
                "es.query": query
            }
        }
        if conf:
            if 'conf' in conf:
                config['conf'].update(conf['conf'])
                conf.pop('conf')
            config.update(conf)
        return config

    @staticmethod
    def get_es_conf_write(hosts, _index=None, _type=None,
                          mapping_id=None, index_auto_create=False, conf=None):
        """
        rdd.saveAsNewAPIHadoopFile(**conf)
        另外一种形式
        df.write.format('org.elasticsearch.spark.sql') \
            .option('es.nodes', '10.0.0.0') \
            .option('es.port', '9200') \
            .option('es.resource', 'test/nested_type') \
            .option('es.mapping.id', 'id') \
            .option('es.write.operation', 'update') \
            .option('es.update.script.inline', "if(ctx._source.containsKey('hphm')){if(!ctx._source.hphm.contains('2222')){ctx._source.hphm.add('2222')}}") \
            .save(mode='append')
        :return:
        """
        config = {
            "path": "-",
            "outputFormatClass": "org.elasticsearch.hadoop.mr.EsOutputFormat",
            "keyClass": "org.apache.hadoop.io.NullWritable",
            "valueClass": "org.elasticsearch.hadoop.mr.LinkedMapWritable",
            "conf": {
                "es.nodes": hosts,
                "es.resource": f"{_index}/{_type}",
                "es.input.json": "yes",
                "es.index.auto.create": index_auto_create,  # 是否自动创建
                "es.mapping.id": None if not mapping_id or index_auto_create else mapping_id
            }
        }
        if conf:
            if 'conf' in conf:
                config['conf'].update(conf['conf'])
                conf.pop('conf')
            config.update(conf)
        return config

    # @staticmethod
    # def get_mongo_conf_read(uri, query, conf=None):
    #     """
    #     # spark-commit --packages org.mongodb.spark:mongo-spark-connector_2.11:2.3.1
    #     from pyspark.sql.types import StructType, StructField, StringType, IntegerType
    #     schema = StructType([
    #         StructField("name", StringType()),
    #         StructField("age", IntegerType()),
    #         StructField("sex", StringType())
    #     ])
    #     spark = SparkUtil.spark_session(master, app_name, conf=conf)
    #     df = spark.read.format('com.mongodb.spark.sql.DefaultSource').schema(schema).load()
    #     df.createOrReplaceTempView('user')
    #     resDf = spark.sql('select name,age,sex from user')
    #     resDf.show()
    #     :return:
    #     """
    #     conf = {
    #         'inputFormatClass': 'com.mongodb.hadoop.MongoInputFormat',
    #         'keyClass': 'org.apache.hadoop.io.Text',
    #         'valueClass': 'org.apache.hadoop.io.MapWritable',
    #         'conf': {
    #             'mongo.input.uri': 'mongodb://localhost:27017/db.collection',
    #             'mongo.input.query': query,
    #             'mongo.input.split.create_input_splits': 'false'
    #         }
    #     }
        # if not conf:
        #     conf = SparkConf()
        # conf.set('spark.mongodb.input.uri', uri)
        # return conf

    # @staticmethod
    # def get_mongo_conf_write(uri, conf=None):
    #     """
    #     # spark-commit --packages org.mongodb.spark:mongo-spark-connector_2.11:2.3.1
    #     from pyspark.sql.types import StructType, StructField, StringType, IntegerType
    #     schema = StructType([
    #         StructField("name", StringType()),
    #         StructField("age", IntegerType()),
    #         StructField("sex", StringType())
    #     ])
    #     spark = SparkUtil.spark_session(master, app_name, conf=conf)
    #     df = spark.createDataFrame([('caocao', 36, 'male'), ('sunquan', 26, 'male'), ('zhugeliang', 26, 'male')], schema)
    #     df.show()
    #     df.write.format('com.mongodb.spark.sql.DefaultSource').mode("append").save()
    #     :return:
    #     """
    #     conf = {
    #         'path': '-',
    #         'outputFormatClass': 'com.mongodb.hadoop.MongoOutputFormat',
    #         'keyClass': 'org.apache.hadoop.io.Text',
    #         'valueClass': 'org.apache.hadoop.io.MapWritable',
    #         'conf': {
    #             'mongo.output.uri': 'mongodb://localhost:27017/output.collection'
    #         }
    #     }
        # if not conf:
        #     conf = SparkConf()
        # conf.set('spark.mongodb.output.uri', uri)
        # return conf


if __name__ == '__main__':
    import os
    os.environ['JAVA_HOME'] = r'E:\Program Files\Java\jdk1.8.0_191'
    os.environ['HADOOP_HOME'] = r'E:\HadoopFiles\hadoop-2.7.7'
    os.environ['SPARK_HOME'] = r'E:\HadoopFiles\spark-2.3.4-bin-hadoop2.7'

    from pyspark.sql import SQLContext
    from pyspark.sql.types import StructType, StructField, StringType, IntegerType

    schema = StructType([
        StructField("name", StringType()),
        StructField("age", StringType()),
        StructField("type", StringType())
    ])

    master = 'local'
    app_name = "my_app_name"
    conf = SparkConf()
    # conf.set('--jars', os.path.dirname(__file__) + '/kg-0.0.1-SNAPSHOT.jar')
    sc = SparkUtil.get_spark_context(master, app_name)
    logger = SparkUtil.get_spark_logger('spark_util', 'INFO')
    jvm = SparkUtil.get_spark_jvm()

    sqlc = SQLContext(sc)
    data = ["1 b 28", "3 c 30", "2 d 29"]
    rdd = sc.parallelize(data)
    rdd = rdd.map(lambda line: line.split(" "))

    for item in rdd.collect():
        logger.info(f'rdd_collect: {item}')

    df = sqlc.createDataFrame(rdd, schema=schema)
    df.show()

    sqlc.clearCache()
    sc.stop()
