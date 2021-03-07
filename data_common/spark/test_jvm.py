import traceback
from data_common.spark.hbase_util import HbaseConf
from data_common.spark.spark_util import SparkUtil

if __name__ == '__main__':

    session = SparkUtil.get_spark_session(appName='hbase', master='local')
    sc = SparkUtil.get_spark_context()
    jvm = SparkUtil.get_spark_jvm()
    logger = SparkUtil.get_spark_logger(__name__)

    def logger_exception():
        s = traceback.format_exc()
        for line in s.split('\n'):
            logger.error(line)
    try:
        line = "This order was placed for QT3000! OK?"
        pattern = ".*(order.*placed).*"
        value = jvm.com.jsw.kg.JavaRegUtil.findAll(pattern, line)
        logger.info(f'jvm_jsw1: {value}')
        keys = ["0001", "0002", "0003", "0004"]
        values = jvm.com.jsw.kg.HbaseUtil.getValue(keys)
        for value in values:
            logger.info(f'jvm_jsw2: {value}')
    except:
        logger_exception()
    sc.stop()