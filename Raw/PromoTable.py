# Databricks notebook source
# MAGIC %md #### Run shared libraries

# COMMAND ----------

# MAGIC %run ../Misc/SharedLibraries

# COMMAND ----------

# MAGIC %md #### Define Variables

# COMMAND ----------

EntityName = 'PromoTable'
Manifest = 'Sales'
deltaLakePath = 'DeltaLake/Raw/Sales/' + EntityName

# COMMAND ----------

# MAGIC %md #### Read Entity

# COMMAND ----------

promotabledf = read_entity(Manifest,EntityName)

# COMMAND ----------

# MAGIC %md
# MAGIC #### Write to DeltaLake in ADLS

# COMMAND ----------

writeRawToDeltaLake(promotabledf,deltaLakePath)
