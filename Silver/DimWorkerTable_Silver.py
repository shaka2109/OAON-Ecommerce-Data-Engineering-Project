# Databricks notebook source
# MAGIC %run ../Misc/SharedLibraries

# COMMAND ----------

UpdatedDateTime = dt.datetime.now()
entity = 'dimWorkerTable'
schema = 'silver'

# COMMAND ----------

# DBTITLE 1,Read Bronze Tables
workertableDF = spark.table('bronze.workertable')
verticalDF = spark.table('silver.dimvertical')

# COMMAND ----------

# DBTITLE 1,Build Dimension/Fact table
dimworkertabledf = workertableDF.filter(workertableDF.RecordId.isNotNull()
    ).join(
        verticalDF,workertableDF.Vertical == verticalDF.Vertical,"left"
    ).select(
       workertableDF.WorkerID,
       F.when(workertableDF.LastProcessedChange_DateTime.isNull(), "1900-01-01").otherwise(workertableDF.LastProcessedChange_DateTime).cast("timestamp").alias("LastProcessedChange_DateTime"),
       F.from_utc_timestamp(workertableDF.DataLakeModified_DateTime,'CST').alias("DataLakeModified_DateTime"),
       workertableDF.SupervisorId,
       F.trim(workertableDF.WorkerName).alias("WorkerName"),
       F.trim(workertableDF.WorkerEmail).alias("WorkerEmail"),
       F.trim(workertableDF.Phone).alias("Phone"),
       F.from_utc_timestamp(workertableDF.DOJ,'CST').alias("DOJ"),
       F.from_utc_timestamp(workertableDF.DOL,'CST').alias("DOL"), 
       verticalDF.VerticalId,
       workertableDF.Type,
       workertableDF.PayPerAnnum,
       workertableDF.Rate,
       workertableDF.RecordId.alias("WorkerTableRecordId")  
    ).withColumn("UpdatedDateTime", F.lit(UpdatedDateTime)
    ).withColumn("WorkerHashKey", F.xxhash64("WorkerTableRecordId")
    )
display(dimworkertabledf)

# COMMAND ----------

# DBTITLE 1,Final Dataframe
df_final = dimworkertabledf

# COMMAND ----------

# DBTITLE 1,Write to Silver Schema
saveDeltaTableToCatalog(df_final,schema,entity)
