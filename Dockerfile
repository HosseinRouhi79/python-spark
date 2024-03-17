FROM apache/spark:3.5.1

USER root

RUN mkdir -p /var/lib/apt/lists/partial && chmod 644 /var/lib/apt/lists/partial

# Install Python and required dependencies
RUN apt-get update && apt-get install -y python3 python3-pip

# Install PySpark
ENV PYSPARK_PYTHON=python3
RUN pip install pyspark

# Set up your application code
COPY . /app/


RUN pip install Werkzeug==2.2.2
RUN pip install flask==2.2.2

# Set the Spark master URL
# ENV SPARK_MASTER spark://spark-master:7077
# ENV PYSPARK_SUBMIT_ARGS "--master spark://spark-master:7077 pyspark-shell"

# Set up Hadoop configurations if needed
# ENV HADOOP_CONF_DIR /path/to/your/hadoop/conf

# Expose Spark UI ports
EXPOSE 4040 4041

# Run the PySpark application
CMD ["spark-submit", "--conf" , "spark.driver.extraJavaOptions=-Divy.cache.dir=/tmp -Divy.home=/tmp" , "--packages" , "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1" , "/app/spark.py"]
