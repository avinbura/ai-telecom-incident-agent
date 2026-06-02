from pyspark.sql import SparkSession
from pyspark.sql.functions import count, avg

spark = SparkSession.builder \
    .appName("TelecomDataEngineeringAnalytics") \
    .getOrCreate()

print("\n=== Reading Synthetic Telecom Dataset ===")

synthetic_df = spark.read.csv(
    "data/synthetic/synthetic_telecom_incidents.csv",
    header=True,
    inferSchema=True
)

synthetic_df.show(5)

print("\n=== Synthetic: Incident Count by Severity ===")

synthetic_severity_df = synthetic_df.groupBy("severity").agg(
    count("*").alias("incident_count")
)

synthetic_severity_df.show()

print("\n=== Synthetic: Average Latency by Region ===")

synthetic_latency_df = synthetic_df.groupBy("region").agg(
    avg("latency_ms").alias("avg_latency")
)

synthetic_latency_df.show()

print("\n=== Reading PostgreSQL Export Dataset ===")

postgres_df = spark.read.csv(
    "data/postgres_export/postgres_incidents_export.csv",
    header=True,
    inferSchema=True
)

postgres_df.show(5)

print("\n=== PostgreSQL Export: Incident Count by Severity ===")

postgres_severity_df = postgres_df.groupBy("severity").agg(
    count("*").alias("incident_count")
)

postgres_severity_df.show()

print("\n=== Reading Hugging Face Telecom Dataset ===")

hf_df = spark.read.csv(
    "data/huggingface/telco_customer_churn.csv",
    header=True,
    inferSchema=True
)

hf_df.show(5)

print("\n=== Hugging Face Dataset Schema ===")

hf_df.printSchema()

spark.stop()
