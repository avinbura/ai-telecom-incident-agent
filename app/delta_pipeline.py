from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, count
import os

spark = SparkSession.builder \
    .appName("TelecomDeltaLakePipeline") \
    .getOrCreate()

# =========================
# BRONZE LAYER
# =========================

print("\n=== BRONZE LAYER ===")

bronze_df = spark.read.csv(
    "data/synthetic/synthetic_telecom_incidents.csv",
    header=True,
    inferSchema=True
)

bronze_df.show(5)

bronze_output = "data/bronze/telecom_bronze"

bronze_df.write.mode("overwrite").csv(bronze_output, header=True)

print(f"Bronze layer saved to: {bronze_output}")

# =========================
# SILVER LAYER
# =========================

print("\n=== SILVER LAYER ===")

silver_df = bronze_df.filter(
    col("packet_loss").isNotNull()
).filter(
    col("latency_ms").isNotNull()
)

silver_df = silver_df.dropDuplicates()

silver_df.show(5)

silver_output = "data/silver/telecom_silver"

silver_df.write.mode("overwrite").csv(silver_output, header=True)

print(f"Silver layer saved to: {silver_output}")

# =========================
# GOLD LAYER
# =========================

print("\n=== GOLD LAYER ===")

gold_df = silver_df.groupBy("region", "severity").agg(
    count("*").alias("incident_count"),
    avg("latency_ms").alias("avg_latency")
)

gold_df.show()

gold_output = "data/gold/telecom_gold"

gold_df.write.mode("overwrite").csv(gold_output, header=True)

print(f"Gold layer saved to: {gold_output}")

spark.stop()
