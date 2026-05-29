# Databricks notebook source
# MAGIC %run ../Misc/SharedLibraries

# COMMAND ----------

UpdateDateTime = dt.datetime.now()
entity = 'dimCustTable'
schema = 'silver'

# COMMAND ----------

# DBTITLE 1,Read Bronze Tables
custtableDF = spark.table('bronze.custtable')

# COMMAND ----------

# DBTITLE 1,Build Dimension/Fact table
dimcusttabledf = custtableDF.filter(custtableDF.RecordId.isNotNull()
    ).select(
        custtableDF.CustomerId,
        F.when(custtableDF.LastProcessedChange_DateTime.isNull(), "1900-01-01").otherwise(custtableDF.LastProcessedChange_DateTime).cast("timestamp").alias("LastProcessedChange_DateTime"),
        F.from_utc_timestamp(custtableDF.DataLakeModified_DateTime,'CST').alias("DataLakeModified_DateTime"),
        F.trim(custtableDF.CustomerName).alias("CustomerName"),
        F.trim(custtableDF.Email).alias("Email"),
        F.trim(custtableDF.Phone).alias("Phone"),
        F.trim(custtableDF.Address).alias("Address"),
        F.trim(custtableDF.City).alias("City"),
        F.trim(custtableDF.State).alias("State"),
        F.trim(custtableDF.Country).alias("Country"),
        F.trim(custtableDF.Country).alias("ZipCode"),
        F.trim(custtableDF.Region).alias("Region"),
        F.from_utc_timestamp(custtableDF.SignupDate,'CST').alias("SignupDate"),
        custtableDF.RecordId.alias("CustTableRecordId")
    ).withColumn("UpdateDateTime", F.lit(UpdateDateTime)
    ).withColumn("PartyHashKey", F.xxhash64("CustTableRecordId")
    )
display(dimcusttabledf)

# COMMAND ----------

# DBTITLE 1,Final Dataframe
df_final = dimcusttabledf

# COMMAND ----------

# DBTITLE 1,Write to Silver Schema
saveDeltaTableToCatalog(df_final,schema,entity)
