# Databricks notebook source
# MAGIC %run ../Misc/SharedLibraries

# COMMAND ----------

UpdateDateTime = dt.datetime.now()
entity = 'dimPurchItem'
schema = 'silver'

# COMMAND ----------

# DBTITLE 1,Read Bronze Tables
purchitemDF = spark.table('bronze.purchitem')

# COMMAND ----------

# DBTITLE 1,Build Dimension/Fact table
dimpurchitemDF = purchitemDF.filter(purchitemDF.RecordId.isNotNull()
    ).select(
        purchitemDF.ItemId,
        F.trim(purchitemDF.Txt).alias('Txt'),
        F.when(purchitemDF.LastProcessedChange_DateTime.isNull(),'1900-01-01').otherwise(purchitemDF.LastProcessedChange_DateTime).cast('timestamp').alias('LastProcessedChange_DateTime'),
        F.from_utc_timestamp(purchitemDF.DataLakeModified_DateTime,'CST').alias('DataLakeModified_DateTime'),
        F.from_utc_timestamp(purchitemDF.ValidFrom,'CST').alias('ValidFrom'),
        F.when(purchitemDF.ValidTo.isNull(),'1900-01-01').otherwise(purchitemDF.ValidTo).cast('timestamp').alias('ValidTo'),
        purchitemDF.Price,
        purchitemDF.RecordId.alias('PurchItemRecordId'),
        purchitemDF.CategoryID,
    ).withColumn('UpdateDateTime', F.lit(UpdateDateTime)
    ).withColumn("CurrencyHashKey", F.xxhash64("PurchItemRecordId"))
display(dimpurchitemDF)

# COMMAND ----------

# DBTITLE 1,Final Dataframe
df_final = dimpurchitemDF

# COMMAND ----------

# DBTITLE 1,Write to Silver Schema
saveDeltaTableToCatalog(df_final,schema,entity)
