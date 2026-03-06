# Databricks notebook source
# MAGIC %md #### Run shared libraries

# COMMAND ----------

# MAGIC %run ../Misc/SharedLibraries

# COMMAND ----------

# MAGIC %md #### Define Variables

# COMMAND ----------

EntityName = 'CostCenter'
Manifest = 'Others'
deltaLakePath = 'DeltaLake/Raw/Others/' + EntityName

# COMMAND ----------

# MAGIC %md #### Read Entity

# COMMAND ----------

costcenterdf = read_entity(Manifest,EntityName)

# COMMAND ----------

# MAGIC %md
# MAGIC #### Write to DeltaLake in ADLS

# COMMAND ----------

writeRawToDeltaLake(costcenterdf,deltaLakePath)
