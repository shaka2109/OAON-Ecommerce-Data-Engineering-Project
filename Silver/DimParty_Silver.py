# Databricks notebook source
# MAGIC %run ../Misc/SharedLibraries

# COMMAND ----------

UpdateDateTime = dt.datetime.now()
entity = 'dimParty'
schema = 'Silver'

# COMMAND ----------

# DBTITLE 1,Read Bronze Tables
partiesDF = spark.table('bronze.parties')
partyaddressDF = spark.table('bronze.partyaddress')

# COMMAND ----------

# DBTITLE 1,Build Dimension/Fact table
dimPartyDf = partiesDF.join(
    partyaddressDF, partiesDF.PartyId == partyaddressDF.PartyNumber, "left"
    ).filter(partiesDF.RecordId.isNotNull()
    ).select(partiesDF.PartyId,
             F.trim(partiesDF.PartyName).alias('PartyName'),
             F.when(partiesDF.LastProcessedChange_DateTime.isNull(),'1900-01-01').otherwise(partiesDF.LastProcessedChange_DateTime).cast('timestamp').alias('LastProcessedChange_DateTime'),
             F.from_utc_timestamp(partiesDF.DataLakeModified_DateTime,'CST').alias('DataLakeModified_DateTime'),
             partiesDF.PartyAddressCode,
             F.from_utc_timestamp(partiesDF.EstablishedDate,'CST').alias('EstablishedDate'),
             F.trim(partiesDF.PartyEmailId).alias('PartyEmailId'),
             F.trim(partiesDF.PartyContactNumber).alias('PartyContactNumber'),
             partiesDF.RecordId.alias('PartyRecordID'),
             F.trim(partiesDF.TaxId).alias('TaxId'),
             F.trim(partyaddressDF.Address).alias('Address'),
             F.trim(partyaddressDF.City).alias('City'),
             F.trim(partyaddressDF.State).alias('State'),
             F.trim(partyaddressDF.Country).alias('Country'),
             F.trim(partyaddressDF.ZipCode).alias('ZipCode'),
             F.trim(partyaddressDF.Region).alias('Region'),
             F.from_utc_timestamp(partyaddressDF.ValidFrom,'CST').alias('ValidFrom'),
             F.when(partyaddressDF.ValidTo.isNull(),'1900-01-01').otherwise(partyaddressDF.ValidTo).cast('timestamp').alias('ValidTo'),
             partyaddressDF.RecordId.alias('PartyAddressRecordID'),   
    ).withColumn('UpdateDateTime', F.lit(UpdateDateTime)
    ).withColumn("PartyHashKey", F.xxhash64("PartyRecordId"))
display(dimPartyDf)

# COMMAND ----------

# DBTITLE 1,Final Dataframe
df_final = dimPartyDf

# COMMAND ----------

# DBTITLE 1,Write to Silver Schema
saveDeltaTableToCatalog(df_final,schema,entity)
