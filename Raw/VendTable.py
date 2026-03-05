# Databricks notebook source
# MAGIC %md #### Run shared libraries

# COMMAND ----------

# MAGIC %run ../Misc/SharedLibraries

# COMMAND ----------

# MAGIC %md #### Define Variables

# COMMAND ----------

EntityName = 'VendTable'
Manifest = 'Purchase'
deltaLakePath = 'DeltaLake/Raw/Purchase/' + EntityName

# COMMAND ----------

# MAGIC %md #### Read Entity

# COMMAND ----------

VendTabledf = read_entity(Manifest,EntityName)
display(VendTabledf)

# COMMAND ----------

# MAGIC %md
# MAGIC #### Write to DeltaLake in ADLS

# COMMAND ----------

writeRawToDeltaLake(VendTabledf,deltaLakePath)
