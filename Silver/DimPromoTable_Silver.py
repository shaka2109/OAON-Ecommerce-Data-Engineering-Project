# Databricks notebook source
# MAGIC %run ../Misc/SharedLibraries

# COMMAND ----------

UpdateDateTime = dt.datetime.now()
entity = 'dimPromoTable'
schema = 'silver'

# COMMAND ----------

# DBTITLE 1,Read Bronze Tables
promotableDF = spark.table('bronze.promotable')

# COMMAND ----------

# DBTITLE 1,Build Dimension/Fact table
dimpromotabledf = promotableDF.filter(promotableDF.RecordId.isNotNull()
    ).select(
        promotableDF.PromotionId,
        F.when(promotableDF.LastProcessedChange_DateTime.isNull(), "1900-01-01").otherwise(promotableDF.LastProcessedChange_DateTime).cast("timestamp").alias("LastProcessedChange_DateTime"),
        F.from_utc_timestamp(promotableDF.DataLakeModified_DateTime,'CST').alias("DataLakeModified_DateTime"),
        F.trim(promotableDF.PromotionName).alias("PromotionName"),
        F.trim(promotableDF.PromoCode).alias("PromoCode"),
        F.trim(promotableDF.PromoType).alias("PromoType"),
        promotableDF.PromoPercentage,
        F.from_utc_timestamp(promotableDF.ValidFrom,'CST').alias("ValidFrom"),
        F.from_utc_timestamp(promotableDF.ValidTo,'CST').alias("ValidTo"),
        promotableDF.IsActive,
        promotableDF.RecordId.alias("PromoRecordId")
    ).withColumn("UpdatedDateTime", F.lit(UpdateDateTime)
    ).withColumn("PartyHashKey", F.xxhash64("PromoRecordId")
    )
display(dimpromotabledf)

# COMMAND ----------

# DBTITLE 1,Final Dataframe
df_final = dimpromotabledf

# COMMAND ----------

# DBTITLE 1,Write to Silver Schema
saveDeltaTableToCatalog(df_final,schema,entity)
