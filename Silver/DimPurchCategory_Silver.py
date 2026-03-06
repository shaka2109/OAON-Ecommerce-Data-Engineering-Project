# Databricks notebook source
# MAGIC %run ../Misc/SharedLibraries

# COMMAND ----------

UpdateDateTime = dt.datetime.now()
entity = 'dimPurchCategory'
schema = 'silver'

# COMMAND ----------

# DBTITLE 1,Read Bronze Tables
purchcategoryDF = spark.table('bronze.purchcategory')

# COMMAND ----------

# DBTITLE 1,Build Dimension/Fact table
dimpurchcategoryDF = purchcategoryDF.filter(purchcategoryDF.RecordId.isNotNull()
    ).select(
        purchcategoryDF.CategoryId,
        F.trim(purchcategoryDF.CategoryName).alias('CategoryName'),
        F.when(purchcategoryDF.LastProcessedChange_DateTime.isNull(),'1900-01-01').otherwise(purchcategoryDF.LastProcessedChange_DateTime).cast('timestamp').alias('LastProcessedChange_DateTime'),
        F.from_utc_timestamp(purchcategoryDF.DataLakeModified_DateTime,'CST').alias('DataLakeModified_DateTime'),
        purchcategoryDF.CategoryGroupId,
        purchcategoryDF.RecordId.alias('PurchCategoryRecordId')
    ).withColumn('UpdateDateTime', F.lit(UpdateDateTime)
    ).withColumn("CurrencyHashKey", F.xxhash64("PurchCategoryRecordId"))
display(dimpurchcategoryDF)

# COMMAND ----------

# DBTITLE 1,Final Dataframe
df_final = dimpurchcategoryDF

# COMMAND ----------

# DBTITLE 1,Write to Silver Schema
saveDeltaTableToCatalog(df_final,schema,entity)
