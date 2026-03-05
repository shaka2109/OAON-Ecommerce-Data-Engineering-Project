# Databricks notebook source
# MAGIC %md #### Run shared libraries

# COMMAND ----------

# MAGIC %run ../Misc/SharedLibraries

# COMMAND ----------

# MAGIC %md #### Define Variables

# COMMAND ----------

EntityName = 'PurchaseOrder'
Manifest = 'Purchase'
deltaLakePath = 'DeltaLake/Raw/Purchase/' + EntityName

# COMMAND ----------

# MAGIC %md #### Read Entity

# COMMAND ----------

PurchaseOrderdf = read_entity(Manifest,EntityName)
display(PurchaseOrderdf)

# COMMAND ----------

# MAGIC %md
# MAGIC #### Write to DeltaLake in ADLS

# COMMAND ----------

writeRawToDeltaLake(PurchaseOrderdf,deltaLakePath)
