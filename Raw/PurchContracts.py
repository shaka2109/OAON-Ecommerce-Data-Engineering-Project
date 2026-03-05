# Databricks notebook source
# MAGIC %md #### Run shared libraries

# COMMAND ----------

# MAGIC %run ../Misc/SharedLibraries

# COMMAND ----------

# MAGIC %md #### Define Variables

# COMMAND ----------

EntityName = 'PurchContracts'
Manifest = 'Purchase'
deltaLakePath = 'DeltaLake/Raw/Purchase/' + EntityName

# COMMAND ----------

# MAGIC %md #### Read Entity

# COMMAND ----------

PurchContractsdf = read_entity(Manifest,EntityName)
display(PurchContractsdf)

# COMMAND ----------

# MAGIC %md
# MAGIC #### Write to DeltaLake in ADLS

# COMMAND ----------

writeRawToDeltaLake(PurchContractsdf,deltaLakePath)
