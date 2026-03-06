# Databricks notebook source
# MAGIC %run ../Misc/SharedLibraries

# COMMAND ----------

UpdateDateTime = dt.datetime.now()
entity = 'dimCostCenter'
schema = 'silver'

# COMMAND ----------

# DBTITLE 1,Read Bronze Tables
costcenterDF = spark.table('bronze.costcenter')

# COMMAND ----------

# DBTITLE 1,Build Dimension/Fact table
dimcostcenterDF = costcenterDF.filter(costcenterDF.RecordId.isNotNull()
    ).select(
        costcenterDF.CostCenterNumber,
        F.when(costcenterDF.LastProcessedChange_DateTime.isNull(),'1900-01-01').otherwise(costcenterDF.LastProcessedChange_DateTime).cast('timestamp').alias('LastProcessedChange_DateTime'),
        F.from_utc_timestamp(costcenterDF.DataLakeModified_DateTime,'CST').alias('DataLakeModified_DateTime'),
        costcenterDF.Vat,
        costcenterDF.RecordId.alias('CostCenterRecordId')
    ).withColumn('UpdateDateTime', F.lit(UpdateDateTime)
    ).withColumn("CostCenterHashKey", F.xxhash64("CostCenterRecordId"))
display(dimcostcenterDF)

# COMMAND ----------

# DBTITLE 1,Final Dataframe
df_final = dimcostcenterDF

# COMMAND ----------

# DBTITLE 1,Write to Silver Schema
saveDeltaTableToCatalog(df_final,schema,entity)
