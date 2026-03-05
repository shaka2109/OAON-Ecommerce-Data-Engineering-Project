# Databricks notebook source
# MAGIC %run ../Misc/SharedLibraries

# COMMAND ----------

UpdateDateTime = dt.datetime.now()
entity = 'dimCurrency'
schema = 'silver'

# COMMAND ----------

# DBTITLE 1,Read Bronze Tables
currencyDF = spark.table('bronze.currency')

# COMMAND ----------

# DBTITLE 1,Build Dimension/Fact table
dimcurrencyDF = currencyDF.filter(currencyDF.RecordId.isNotNull()
    ).select(
        currencyDF.CurrencyId,
        F.trim(currencyDF.Code).alias('Code'),
        F.when(currencyDF.LastProcessedChange_DateTime.isNull(),'1900-01-01').otherwise(currencyDF.LastProcessedChange_DateTime).cast('timestamp').alias('LastProcessedChange_DateTime'),
        F.from_utc_timestamp(currencyDF.DataLakeModified_DateTime,'CST').alias('DataLakeModified_DateTime'),
        F.trim(currencyDF.Country).alias('Country'),
        F.trim(currencyDF.CurrencyName).alias('CurrencyName'),
        currencyDF.RecordId.alias('CurrencyRecordId')
    ).withColumn('UpdateDateTime', F.lit(UpdateDateTime)
    ).withColumn("CurrencyHashKey", F.xxhash64("CurrencyRecordId"))
display(dimcurrencyDF)

# COMMAND ----------

# DBTITLE 1,Final Dataframe
df_final = dimcurrencyDF

# COMMAND ----------

# DBTITLE 1,Write to Silver Schema
saveDeltaTableToCatalog(df_final,schema,entity)
