# Databricks notebook source
# INCLUDE_HEADER_TRUE
# INCLUDE_FOOTER_TRUE

# COMMAND ----------

# MAGIC %md
# MAGIC # Aggregating Streams
# MAGIC 
# MAGIC ##### Objectives
# MAGIC 1. Add watermarking
# MAGIC 1. Aggregate with windows
# MAGIC 1. Display streaming query results
# MAGIC 1. Monitor streaming queries
# MAGIC 
# MAGIC ##### Classes
# MAGIC - <a href="https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.sql.streaming.DataStreamReader.html#pyspark.sql.streaming.DataStreamReader" target="_blank">DataStreamReader</a>
# MAGIC - <a href="https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.sql.streaming.DataStreamWriter.html#pyspark.sql.streaming.DataStreamWriter" target="_blank">DataStreamWriter</a>
# MAGIC - <a href="https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.sql.streaming.StreamingQuery.html#pyspark.sql.streaming.StreamingQuery" target="_blank">StreamingQuery</a>
# MAGIC - <a href="https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.sql.streaming.StreamingQueryManager.html#pyspark.sql.streaming.StreamingQueryManager" target="_blank">StreamingQueryManager</a>

# COMMAND ----------

# MAGIC %md
# MAGIC ## Hourly Activity by Traffic Lab
# MAGIC Process streaming data to display the total active users by traffic source with a 1 hour window.
# MAGIC 1. Cast to timestamp and add watermark for 2 hours
# MAGIC 2. Aggregate active users by traffic source for 1 hour windows
# MAGIC 3. Execute query with `display` and plot results
# MAGIC 5. Use query name to stop streaming query

# COMMAND ----------

# MAGIC %md
# MAGIC ### Setup
# MAGIC Run the cells below to generate hourly JSON files of event data for July 3, 2020.

# COMMAND ----------

# MAGIC %run ./Includes/Classroom-Setup

# COMMAND ----------

schema = "device STRING, ecommerce STRUCT<purchase_revenue_in_usd: DOUBLE, total_item_quantity: BIGINT, unique_items: BIGINT>, event_name STRING, event_previous_timestamp BIGINT, event_timestamp BIGINT, geo STRUCT<city: STRING, state: STRING>, items ARRAY<STRUCT<coupon: STRING, item_id: STRING, item_name: STRING, item_revenue_in_usd: DOUBLE, price_in_usd: DOUBLE, quantity: BIGINT>>, traffic_source STRING, user_first_touch_timestamp BIGINT, user_id STRING"

# Directory of hourly events logged from the BedBricks website on July 3, 2020
hourlyEventsPath = "/mnt/training/ecommerce/events/events-2020-07-03.json"

df = (spark
      .readStream
      .schema(schema)
      .option("maxFilesPerTrigger", 1)
      .json(hourlyEventsPath)
     )

# COMMAND ----------

# MAGIC %md
# MAGIC ### 1. Cast to timestamp and add watermark for 2 hours
# MAGIC - Add a **`createdAt`** column by dividing **`event_timestamp`** by 1M and casting to timestamp
# MAGIC - Set a watermark of 2 hours on the **`createdAt`** column
# MAGIC 
# MAGIC Assign the resulting DataFrame to **`eventsDF`**.

# COMMAND ----------

# TODO
eventsDF = (df.FILL_IN
)

# COMMAND ----------

# MAGIC %md
# MAGIC **CHECK YOUR WORK**

# COMMAND ----------

assert "StructField(createdAt,TimestampType,true" in str(eventsDF.schema)

# COMMAND ----------

# MAGIC %md
# MAGIC ### 2. Aggregate active users by traffic source for 1 hour windows
# MAGIC - Set the default shuffle partitions to the number of cores on your cluster (not required, but runs faster)
# MAGIC - Group by **`traffic_source`** with 1-hour tumbling windows based on the **`createdAt`** column
# MAGIC - Aggregate the approximate count of distinct users per **`traffic_source`** and hour, and alias the column to "active_users"
# MAGIC - Select **`traffic_source`**, **`active_users`**, and the **`hour`** extracted from **`window.start`** with an alias of "hour"
# MAGIC - Sort by **`hour`** in ascending order
# MAGIC 
# MAGIC Assign the resulting DataFrame to **`trafficDF`**.

# COMMAND ----------

# TODO
spark.FILL_IN

trafficDF = (eventsDF.FILL_IN
)

# COMMAND ----------

# MAGIC %md
# MAGIC **CHECK YOUR WORK**

# COMMAND ----------

assert str(trafficDF.schema) == "StructType(List(StructField(traffic_source,StringType,true),StructField(active_users,LongType,false),StructField(hour,IntegerType,true)))"

# COMMAND ----------

# MAGIC %md
# MAGIC ### 3. Execute query with display() and plot results
# MAGIC - Use `display` to start **`trafficDF`** as a streaming query and display the resulting memory sink
# MAGIC   - Assign "hourly_traffic" as the name of the query by seting the **`streamName`** parameter of `display`
# MAGIC - Plot the streaming query results as a bar graph
# MAGIC - Configure the following plot options:
# MAGIC   - Keys: **`hour`**
# MAGIC   - Series groupings: **`traffic_source`**
# MAGIC   - Values: **`active_users`**

# COMMAND ----------

# TODO

# COMMAND ----------

# MAGIC %md
# MAGIC **CHECK YOUR WORK**
# MAGIC 
# MAGIC - The bar chart should plot `hour` on the x-axis and `active_users` on the y-axis
# MAGIC - Six bars should appear at every hour for all traffic sources
# MAGIC - The chart should stop at hour 23

# COMMAND ----------

# MAGIC %md
# MAGIC ### 4. Manage streaming query
# MAGIC - Iterate over SparkSession's list of active streams to find one with name "hourly_traffic"
# MAGIC - Stop the streaming query

# COMMAND ----------

# TODO
untilStreamIsReady("hourly_traffic")

for s in FILL_IN:

# COMMAND ----------

# MAGIC %md
# MAGIC %md **CHECK YOUR WORK**
# MAGIC Print all active streams to check that "hourly_traffic" is no longer there

# COMMAND ----------

for s in spark.streams.active:
    print(s.name)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Classroom Cleanup
# MAGIC Run the cell below to clean up resources.

# COMMAND ----------

# MAGIC %run ./Includes/Classroom-Cleanup