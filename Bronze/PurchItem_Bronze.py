# Databricks notebook source
# MAGIC %run ../Misc/SharedLibraries

# COMMAND ----------

model = 'Purchase'
entity = 'PurchItem'
schema = 'bronze'

# COMMAND ----------

PurchItemdf = readFromDeltaPath(model,entity)
display(PurchItemdf)

# COMMAND ----------

saveDeltaTableToCatalog(PurchItemdf,schema,entity)
