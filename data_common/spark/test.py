import traceback
from data_common.spark.hbase_util import HbaseConf
from data_common.spark.spark_util import SparkUtil

if __name__ == '__main__':

    session = SparkUtil.get_spark_session(appName='hbase')
    sc = SparkUtil.get_spark_context()
    jvm = SparkUtil.get_spark_jvm()
    logger = SparkUtil.get_spark_logger(__name__)

    table = 'student'
    hosts = 'master:3000,slave1:3000,slave2:3000'
    conf = HbaseConf.get_hbase_conf()
    hbase_conf_read = SparkUtil.get_hbase_conf_read(table=table, conf={'conf': conf})
    print(hbase_conf_read)
    hbase_conf_write = SparkUtil.get_hbase_conf_write(table=table, conf={'conf': conf})
    print(hbase_conf_write)

    def logger_exception():
        s = traceback.format_exc()
        for line in s.split('\n'):
            logger.error(line)
    try:
        rdd = sc.newAPIHadoopRDD(**hbase_conf_read)
        cache = rdd.cache()

        for item in cache.collect():
            logger.info(f'rdd_collect: {item}')

        rdd2 = rdd.map(lambda row: HbaseConf.convert_read(row))\
            .map(lambda row: (f'{row[0]}01', row[1]))\
            .flatMap(lambda row: HbaseConf.convert_write(row))\
            .map(lambda row: (row[0], row))\
            .saveAsNewAPIHadoopDataset(**hbase_conf_write)
        cache.unpersist()
    except:
        logger_exception()
    sc.stop()