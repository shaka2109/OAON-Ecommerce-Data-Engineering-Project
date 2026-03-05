# Databricks notebook source
# MAGIC %run ../Misc/SharedLibraries

# COMMAND ----------

UpdateDateTime = dt.datetime.now()
entity = 'dimVendor'
schema = 'silver'

# COMMAND ----------

# DBTITLE 1,Read Bronze Tables
vendorDF = spark.table('bronze.vendtable')

# COMMAND ----------

# DBTITLE 1,Build Dimension/Fact table
dimVendorDf = vendorDF.filter(vendorDF.RecordId.isNotNull()
    ).select(
        vendorDF.VendId.alias('VendorId'),
        F.trim(vendorDF.VendorName).alias('VendorName'),
        F.when(vendorDF.LastProcessedChange_DateTime.isNull(),'1900-01-01').otherwise(vendorDF.LastProcessedChange_DateTime).cast('timestamp').alias('LastProcessedChange_DateTime'),
        F.from_utc_timestamp(vendorDF.DataLakeModified_DateTime,'CST').alias('DataLakeModified_DateTime'),
        F.trim(vendorDF.Address).alias('Address'),
        F.trim(vendorDF.City).alias('City'),
        F.trim(vendorDF.State).alias('State'),
        F.trim(vendorDF.Country).alias('Country'),
        F.trim(vendorDF.ZipCode).alias('ZipCode'),
        F.trim(vendorDF.Region).alias('Region'),
        F.from_utc_timestamp(vendorDF.ValidFrom,'CST').alias('ValidFrom'),
        F.from_utc_timestamp(vendorDF.ValidTo,'CST').alias('ValidTo'),
        vendorDF.Active,
        vendorDF.RecordId.alias('VendorRecordId'),
        F.trim(vendorDF.TaxId).alias('TaxId'),
        F.trim(vendorDF.CurrencyCode).alias('CurrencyCode')
    ).withColumn('UpdateDateTime', F.lit(UpdateDateTime)
    ).withColumn("VendorHashKey", F.xxhash64("VendorRecordId"))
display(dimVendorDf)

# COMMAND ----------

# DBTITLE 1,Final Dataframe
df_final = dimVendorDf

# COMMAND ----------

# DBTITLE 1,Write to Silver Schema
saveDeltaTableToCatalog(df_final,schema,entity)
