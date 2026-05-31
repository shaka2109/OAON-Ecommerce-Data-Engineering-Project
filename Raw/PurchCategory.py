# Databricks notebook source
# MAGIC %md #### Run shared libraries

# COMMAND ----------

# MAGIC %run ../Misc/SharedLibraries

# COMMAND ----------

# MAGIC %md #### Define Variables

# COMMAND ----------

EntityName = 'PurchCategory'
Manifest = 'Purchase'

# COMMAND ----------

deltaLakePath = f'delta/raw/{Manifest}/{EntityName}'

# COMMAND ----------

# MAGIC %md #### Read Entity

# COMMAND ----------

PurchCategorydf = read_entity(Manifest,EntityName)
# display(PurchCategorydf)

# COMMAND ----------

# MAGIC %md
# MAGIC #### Write to DeltaLake in ADLS

# COMMAND ----------

writeRawToDeltaLake(PurchCategorydf,deltaLakePath)
