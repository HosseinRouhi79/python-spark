from pyspark.sql import SparkSession
from flask import Flask
# import os
# os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages o.apache.spark:spark-streaming-kafka-0-10_2.12:3.5.0,org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1 pyspark-shell'



app = Flask(__name__)


@app.route("/spark", methods=["POST"])
def do_spark():
    # return jsonify("test")
    spark = SparkSession.builder \
    .appName("KafkaSparkConsumer") \
    .getOrCreate()
    spark.conf.set("spark.sql.shuffle.partitions", 1)

    bootstrap_servers = "kafka1:39092"  # Replace with your Kafka broker addresses
    topic = "logtopic"  # Replace with your topic name

    df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", bootstrap_servers) \
        .option("subscribe", topic) \
        .option("startingOffsets", "earliest") \
        .load()

    # Cast key and value to strings and print to console
    deserialized_df = df.selectExpr("CAST(value AS STRING)")

    # Start the streaming query and await its termination
    query = deserialized_df\
    .writeStream \
    .outputMode("append") \
    .format("text") \
    .option("checkpointLocation", "/tmp/checkpoint") \
    .option("path", "/tmp/kafka_messages") \
    .start()

    query.awaitTermination()

    # Stop the SparkSession
    spark.stop()


if __name__ == "__main__":
    # Please do not set debug=True in production
    app.run(host="0.0.0.0", port=5000, debug=True)