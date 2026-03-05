# Databricks notebook source
# MAGIC %run ../Misc/SharedLibraries

# COMMAND ----------

model = 'Purchase'
entity = 'VendTable'
schema = 'bronze'

# COMMAND ----------

VendTabledf = readFromDeltaPath(model,entity)
display(VendTabledf)

# COMMAND ----------

saveDeltaTableToCatalog(VendTabledf,schema,entity)
