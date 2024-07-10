import pyspark
from pyspark.sql import SparkSession
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--date', required=True)
args = parser.parse_args()
date = args.date


# Create SparkSession from builder

spark = SparkSession.builder.master("local") \
                    .appName('project-pipeline') \
                    .getOrCreate()

df = spark.read.json(f'gs://gc-sales-datalake/{date}/*.json', header=True, inferSchema=True, multiLine=True)
