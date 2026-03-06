# Databricks notebook source
# MAGIC %md #### Run shared libraries

# COMMAND ----------

# MAGIC %run ../Misc/SharedLibraries

# COMMAND ----------

# MAGIC %md #### Define Variables

# COMMAND ----------

EntityName = 'WorkerTable'
Manifest = 'Hr'
deltaLakePath = 'DeltaLake/Raw/Hr/' + EntityName

# COMMAND ----------

# MAGIC %md #### Read Entity

# COMMAND ----------

workertabledf = read_entity(Manifest,EntityName)

# COMMAND ----------

# MAGIC %md
# MAGIC #### Write to DeltaLake in ADLS

# COMMAND ----------

writeRawToDeltaLake(workertabledf,deltaLakePath)
