"""
5G Core Registration Analytics
Analyzes UE registration events from AMF logs
Calculates registration success rates and KPIs
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, count, avg, sum, when, date_format,
    current_timestamp, percentile_approx, stddev, desc
)
from pathlib import Path
import yaml
import sys

sys.path.append(str(Path(__file__).parent.parent))
from common.spark_session import get_spark_session


class RegistrationAnalytics:
    """
    Analyze 5G Core registration data
    Processes UE registration attempts from AMF
    """

    def __init__(self, config_path=None):
        """Initialize 5G Registration Analytics"""
        self.spark = get_spark_session("5GRegistrationAnalytics")
        self.config = self._load_db_config(config_path)

    def _load_db_config(self, config_path):
        """Load database configuration"""
        if config_path is None:
            base_path = Path(__file__).parent.parent.parent
            config_path = base_path / "config" / "database_config.yaml"

        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            return {
                'source_db': {
                    'host': 'localhost',
                    'port': 5432,
                    'database': 'core5g_db',
                    'user': 'postgres',
                    'password': 'postgres'
                },
                'hive': {'database': 'deployment_analytics'}
            }

    def extract_registration_events(self):
        """
        Extract UE registration events from AMF logs
        Data source: 5G-Core-Automation AMF telemetry
        """
        print("=" * 60)
        print("EXTRACTING: UE Registration Events")
        print("=" * 60)

        db_config = self.config['source_db']
        jdbc_url = f"jdbc:postgresql://{db_config['host']}:{db_config['port']}/{db_config['database']}"

        registration_df = self.spark.read \
            .format("jdbc") \
            .option("url", jdbc_url) \
            .option("dbtable", "amf_registration_events") \
            .option("user", db_config['user']) \
            .option("password", db_config['password']) \
            .option("driver", "org.postgresql.Driver") \
            .load()

        print(f"✓ Extracted {registration_df.count()} registration events")
        registration_df.printSchema()

        return registration_df

    def calculate_registration_kpis(self, registration_df):
        """
        Calculate registration KPIs
        - Success rate
        - Average latency
        - Failure reasons
        """
        print("\n" + "=" * 60)
        print("CALCULATING: Registration KPIs")
        print("=" * 60)

        # Add date column
        registration_with_date = registration_df \
            .withColumn("date", date_format(col("event_time"), "yyyy-MM-dd"))

        # Calculate KPIs by site and AMF instance
        registration_kpis = registration_with_date \
            .groupBy("site_id", "amf_instance", "date") \
            .agg(
                count("*").alias("total_attempts"),
                count(when(col("result") == "SUCCESS", 1)).alias("successful"),
                count(when(col("result") == "FAILED", 1)).alias("failed"),
                avg("latency_ms").alias("avg_latency"),
                percentile_approx("latency_ms", 0.95).alias("p95_latency"),
                stddev("latency_ms").alias("stddev_latency")
            ) \
            .withColumn(
                "success_rate",
                (col("successful") / col("total_attempts")) * 100
            ) \
            .withColumn(
                "deployment_status",
                when(col("success_rate") >= 99, "EXCELLENT")
                .when(col("success_rate") >= 95, "HEALTHY")
                .when(col("success_rate") >= 90, "WARNING")
                .otherwise("CRITICAL")
            ) \
            .withColumn("processed_at", current_timestamp())

        print(f"✓ Calculated KPIs: {registration_kpis.count()} records")

        print("\nSample Registration KPIs:")
        registration_kpis.select(
            "site_id", "date", "total_attempts",
            "success_rate", "avg_latency", "deployment_status"
        ).show(10, truncate=False)

        return registration_kpis

    def analyze_failure_causes(self, registration_df):
        """Analyze registration failure causes"""
        print("\n" + "=" * 60)
        print("ANALYZING: Failure Causes")
        print("=" * 60)

        failures_df = registration_df \
            .filter(col("result") == "FAILED") \
            .withColumn("date", date_format(col("event_time"), "yyyy-MM-dd"))

        failure_analysis = failures_df \
            .groupBy("failure_reason", "site_id") \
            .agg(
                count("*").alias("failure_count")
            ) \
            .orderBy(desc("failure_count"))

        print(f"✓ Analyzed {failures_df.count()} failures")
        print("\nTop Failure Reasons:")
        failure_analysis.show(10, truncate=False)

        return failure_analysis

    def load_to_hive(self, df, table_name, partition_cols=None):
        """Load data to Hive"""
        hive_db = self.config['hive']['database']
        full_table_name = f"{hive_db}.{table_name}"

        print(f"\nLoading to Hive: {full_table_name}")

        self.spark.sql(f"CREATE DATABASE IF NOT EXISTS {hive_db}")

        writer = df.write.mode("overwrite").format("hive")
        if partition_cols:
            writer = writer.partitionBy(*partition_cols)

        writer.saveAsTable(full_table_name)

        row_count = self.spark.sql(f"SELECT COUNT(*) FROM {full_table_name}").collect()[0][0]
        print(f"✓ Loaded {row_count} rows")

    def run_pipeline(self):
        """Execute the registration analytics pipeline"""
        try:
            print("\n" + "=" * 60)
            print("5G REGISTRATION ANALYTICS PIPELINE")
            print("=" * 60)

            # Extract
            registration_df = self.extract_registration_events()

            # Calculate KPIs
            registration_kpis = self.calculate_registration_kpis(registration_df)
            self.load_to_hive(
                registration_kpis,
                "registration_kpis",
                partition_cols=["date"]
            )

            # Analyze failures
            failure_analysis = self.analyze_failure_causes(registration_df)
            self.load_to_hive(failure_analysis, "registration_failure_analysis")

            print("\n" + "=" * 60)
            print("✓ PIPELINE COMPLETED SUCCESSFULLY")
            print("=" * 60)

        except Exception as e:
            print(f"\n✗ ERROR: {str(e)}")
            raise

    def cleanup(self):
        """Cleanup resources"""
        if self.spark:
            self.spark.stop()


def main():
    analytics = RegistrationAnalytics()
    try:
        analytics.run_pipeline()
    finally:
        analytics.cleanup()


if __name__ == "__main__":
    main()
