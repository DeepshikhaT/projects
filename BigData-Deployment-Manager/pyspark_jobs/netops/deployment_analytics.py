"""
NetOps Deployment Analytics
Analyzes Ansible deployment logs from NetOps-Automation project
Calculates deployment success rates, failure patterns, and trends
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, count, avg, sum, when, date_format,
    current_timestamp, datediff, lit, max, min,
    row_number, desc, window
)
from pyspark.sql.window import Window
from pathlib import Path
import yaml
import sys

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))
from common.spark_session import get_spark_session


class NetOpsDeploymentAnalytics:
    """
    Analyze NetOps deployment data from Ansible automation
    Processes logs from ansible_api_with_db.py and playbook executions
    """

    def __init__(self, config_path=None):
        """
        Initialize NetOps Deployment Analytics

        Args:
            config_path: Path to database configuration file
        """
        self.spark = get_spark_session("NetOpsDeploymentAnalytics")
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
            print(f"Config file not found: {config_path}, using defaults")
            return self._default_db_config()

    def _default_db_config(self):
        """Default database configuration"""
        return {
            'source_db': {
                'host': 'localhost',
                'port': 5432,
                'database': 'netops_db',
                'user': 'postgres',
                'password': 'postgres'
            },
            'hive': {
                'database': 'deployment_analytics'
            }
        }

    def extract_ansible_logs(self):
        """
        Extract Ansible execution logs from PostgreSQL
        Data source: NetOps-Automation/api/ansible_api_with_db.py
        """
        print("=" * 60)
        print("EXTRACTING: Ansible Execution Logs")
        print("=" * 60)

        db_config = self.config['source_db']
        jdbc_url = f"jdbc:postgresql://{db_config['host']}:{db_config['port']}/{db_config['database']}"

        # Read ansible execution logs
        ansible_logs_df = self.spark.read \
            .format("jdbc") \
            .option("url", jdbc_url) \
            .option("dbtable", "ansible_execution_logs") \
            .option("user", db_config['user']) \
            .option("password", db_config['password']) \
            .option("driver", "org.postgresql.Driver") \
            .load()

        print(f"✓ Extracted {ansible_logs_df.count()} execution log records")
        ansible_logs_df.printSchema()

        return ansible_logs_df

    def process_deployment_metrics(self, ansible_logs_df):
        """
        Calculate deployment success metrics
        Analyzes: configure_vlans.yml, configure_ospf.yml, backup_configs.yml, health_check.yml
        """
        print("\n" + "=" * 60)
        print("PROCESSING: Deployment Success Metrics")
        print("=" * 60)

        # Filter for deployment playbooks
        deployment_playbooks = [
            'configure_vlans.yml',
            'configure_ospf.yml',
            'backup_configs.yml',
            'health_check.yml'
        ]

        deployment_df = ansible_logs_df \
            .filter(col("playbook").isin(deployment_playbooks)) \
            .withColumn("date", date_format(col("execution_time"), "yyyy-MM-dd"))

        # Calculate metrics by playbook and site
        deployment_metrics = deployment_df \
            .groupBy("playbook", "site_id", "date") \
            .agg(
                count("*").alias("total_executions"),
                count(when(col("status") == "success", 1)).alias("successful"),
                count(when(col("status") == "failed", 1)).alias("failed"),
                avg("duration_seconds").alias("avg_duration"),
                min("duration_seconds").alias("min_duration"),
                max("duration_seconds").alias("max_duration")
            ) \
            .withColumn(
                "success_rate",
                (col("successful") / col("total_executions")) * 100
            ) \
            .withColumn(
                "failure_rate",
                (col("failed") / col("total_executions")) * 100
            ) \
            .withColumn("processed_at", current_timestamp())

        # Add deployment status classification
        deployment_metrics = deployment_metrics.withColumn(
            "deployment_status",
            when(col("success_rate") >= 95, "HEALTHY")
            .when(col("success_rate") >= 80, "WARNING")
            .otherwise("CRITICAL")
        )

        print(f"✓ Processed deployment metrics: {deployment_metrics.count()} records")

        # Show sample results
        print("\nSample Deployment Metrics:")
        deployment_metrics.select(
            "playbook", "site_id", "date",
            "total_executions", "success_rate", "deployment_status"
        ).show(10, truncate=False)

        return deployment_metrics

    def analyze_failure_patterns(self, ansible_logs_df):
        """
        Analyze failure patterns and trends
        Identify common error types and problematic sites
        """
        print("\n" + "=" * 60)
        print("ANALYZING: Failure Patterns")
        print("=" * 60)

        # Get failed deployments
        failures_df = ansible_logs_df \
            .filter(col("status") == "failed") \
            .withColumn("date", date_format(col("execution_time"), "yyyy-MM-dd"))

        # Analyze failures by playbook and error type
        failure_analysis = failures_df \
            .groupBy("playbook", "error_message", "site_id") \
            .agg(
                count("*").alias("failure_count"),
                max("execution_time").alias("last_failure_date")
            ) \
            .orderBy(desc("failure_count"))

        # Identify top failing sites
        top_failing_sites = failures_df \
            .groupBy("site_id") \
            .agg(
                count("*").alias("total_failures"),
                count("playbook").alias("distinct_playbooks")
            ) \
            .orderBy(desc("total_failures")) \
            .limit(20)

        print(f"✓ Analyzed {failures_df.count()} failure records")
        print("\nTop Failing Sites:")
        top_failing_sites.show(10, truncate=False)

        return failure_analysis, top_failing_sites

    def calculate_time_series_trends(self, ansible_logs_df):
        """
        Calculate deployment trends over time
        Track improvement or degradation in deployment success
        """
        print("\n" + "=" * 60)
        print("CALCULATING: Time Series Trends")
        print("=" * 60)

        # Daily deployment trends
        daily_trends = ansible_logs_df \
            .withColumn("date", date_format(col("execution_time"), "yyyy-MM-dd")) \
            .groupBy("date", "playbook") \
            .agg(
                count("*").alias("total_deployments"),
                count(when(col("status") == "success", 1)).alias("successful"),
                avg("duration_seconds").alias("avg_duration")
            ) \
            .withColumn(
                "success_rate",
                (col("successful") / col("total_deployments")) * 100
            ) \
            .orderBy("date", "playbook")

        # Weekly aggregations
        weekly_trends = ansible_logs_df \
            .withColumn("week", date_format(col("execution_time"), "yyyy-ww")) \
            .groupBy("week") \
            .agg(
                count("*").alias("total_deployments"),
                count(when(col("status") == "success", 1)).alias("successful"),
                count("site_id").alias("sites_deployed")
            ) \
            .withColumn(
                "success_rate",
                (col("successful") / col("total_deployments")) * 100
            ) \
            .orderBy("week")

        print(f"✓ Calculated daily trends: {daily_trends.count()} records")
        print(f"✓ Calculated weekly trends: {weekly_trends.count()} records")

        return daily_trends, weekly_trends

    def load_to_hive(self, df, table_name, partition_cols=None):
        """
        Load processed data to Hive tables

        Args:
            df: DataFrame to save
            table_name: Target table name
            partition_cols: List of partition columns
        """
        hive_db = self.config['hive']['database']
        full_table_name = f"{hive_db}.{table_name}"

        print(f"\nLoading data to Hive: {full_table_name}")

        # Create database if not exists
        self.spark.sql(f"CREATE DATABASE IF NOT EXISTS {hive_db}")

        # Write to Hive
        writer = df.write.mode("overwrite").format("hive")

        if partition_cols:
            writer = writer.partitionBy(*partition_cols)

        writer.saveAsTable(full_table_name)

        # Verify
        row_count = self.spark.sql(f"SELECT COUNT(*) FROM {full_table_name}").collect()[0][0]
        print(f"✓ Successfully loaded {row_count} rows to {full_table_name}")

    def run_pipeline(self):
        """Execute the complete NetOps deployment analytics pipeline"""
        try:
            print("\n" + "=" * 60)
            print("NETOPS DEPLOYMENT ANALYTICS PIPELINE")
            print("=" * 60)
            print(f"Started at: {current_timestamp()}\n")

            # Step 1: Extract
            ansible_logs_df = self.extract_ansible_logs()

            # Step 2: Process deployment metrics
            deployment_metrics = self.process_deployment_metrics(ansible_logs_df)
            self.load_to_hive(
                deployment_metrics,
                "ansible_deployment_metrics",
                partition_cols=["date"]
            )

            # Step 3: Analyze failures
            failure_analysis, top_failing_sites = self.analyze_failure_patterns(ansible_logs_df)
            self.load_to_hive(failure_analysis, "deployment_failure_analysis")
            self.load_to_hive(top_failing_sites, "top_failing_sites")

            # Step 4: Calculate trends
            daily_trends, weekly_trends = self.calculate_time_series_trends(ansible_logs_df)
            self.load_to_hive(
                daily_trends,
                "daily_deployment_trends",
                partition_cols=["date"]
            )
            self.load_to_hive(weekly_trends, "weekly_deployment_trends")

            print("\n" + "=" * 60)
            print("✓ PIPELINE COMPLETED SUCCESSFULLY")
            print("=" * 60)

            # Print summary statistics
            self._print_summary(deployment_metrics)

        except Exception as e:
            print(f"\n✗ ERROR in pipeline: {str(e)}")
            import traceback
            traceback.print_exc()
            raise

    def _print_summary(self, deployment_metrics):
        """Print pipeline execution summary"""
        print("\n" + "=" * 60)
        print("SUMMARY STATISTICS")
        print("=" * 60)

        summary = deployment_metrics.agg(
            count("*").alias("total_records"),
            avg("success_rate").alias("avg_success_rate"),
            count(when(col("deployment_status") == "CRITICAL", 1)).alias("critical_deployments")
        ).collect()[0]

        print(f"Total Records Processed: {summary['total_records']}")
        print(f"Average Success Rate: {summary['avg_success_rate']:.2f}%")
        print(f"Critical Deployments: {summary['critical_deployments']}")
        print("=" * 60)

    def cleanup(self):
        """Cleanup resources"""
        if self.spark:
            self.spark.stop()


def main():
    """Main entry point"""
    analytics = NetOpsDeploymentAnalytics()

    try:
        analytics.run_pipeline()
    finally:
        analytics.cleanup()


if __name__ == "__main__":
    main()
