"""
Spark Session Factory
Centralized Spark session creation with standard configurations
"""

from pyspark.sql import SparkSession
import yaml
import os
from pathlib import Path


class SparkSessionFactory:
    """Factory class for creating configured Spark sessions"""

    _instance = None

    def __init__(self, config_path=None):
        """
        Initialize Spark Session Factory

        Args:
            config_path: Path to spark configuration file
        """
        if config_path is None:
            base_path = Path(__file__).parent.parent.parent
            config_path = base_path / "config" / "spark_config.yaml"

        self.config = self._load_config(config_path)
        self.spark = None

    def _load_config(self, config_path):
        """Load Spark configuration from YAML file"""
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            print(f"Config file not found: {config_path}")
            print("Using default configuration")
            return self._default_config()

    def _default_config(self):
        """Default Spark configuration"""
        return {
            'spark': {
                'master': 'local[4]',
                'app_name': 'DeploymentManagerETL',
                'executor_memory': '4g',
                'executor_cores': 4,
                'dynamic_allocation': True,
                'sql': {
                    'warehouse_dir': '/user/hive/warehouse'
                }
            }
        }

    def create_session(self, app_name=None):
        """
        Create and configure Spark session

        Args:
            app_name: Optional application name override

        Returns:
            SparkSession: Configured Spark session
        """
        if self.spark is not None:
            return self.spark

        spark_config = self.config['spark']

        builder = SparkSession.builder \
            .appName(app_name or spark_config.get('app_name', 'DeploymentManagerETL')) \
            .master(spark_config.get('master', 'local[4]'))

        # Apply configuration
        builder = builder.config(
            "spark.executor.memory",
            spark_config.get('executor_memory', '4g')
        )

        builder = builder.config(
            "spark.executor.cores",
            spark_config.get('executor_cores', 4)
        )

        if spark_config.get('dynamic_allocation', False):
            builder = builder.config("spark.dynamicAllocation.enabled", "true")

        # Hive support
        warehouse_dir = spark_config.get('sql', {}).get('warehouse_dir', '/user/hive/warehouse')
        builder = builder.config("spark.sql.warehouse.dir", warehouse_dir)

        # Enable Hive support
        builder = builder.enableHiveSupport()

        # Additional optimizations
        builder = builder.config("spark.sql.adaptive.enabled", "true")
        builder = builder.config("spark.sql.adaptive.coalescePartitions.enabled", "true")

        self.spark = builder.getOrCreate()

        # Set log level
        self.spark.sparkContext.setLogLevel("WARN")

        return self.spark

    def stop_session(self):
        """Stop the Spark session"""
        if self.spark is not None:
            self.spark.stop()
            self.spark = None

    @classmethod
    def get_instance(cls, config_path=None):
        """
        Get singleton instance of SparkSessionFactory

        Args:
            config_path: Path to configuration file

        Returns:
            SparkSessionFactory: Singleton instance
        """
        if cls._instance is None:
            cls._instance = cls(config_path)
        return cls._instance


def get_spark_session(app_name=None, config_path=None):
    """
    Convenience function to get a Spark session

    Args:
        app_name: Application name
        config_path: Path to configuration file

    Returns:
        SparkSession: Configured Spark session
    """
    factory = SparkSessionFactory.get_instance(config_path)
    return factory.create_session(app_name)
