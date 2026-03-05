# Databricks notebook source
# MAGIC %run ../Misc/SharedLibraries

# COMMAND ----------

model = 'Purchase'
entity = 'PurchaseOrder'
schema = 'bronze'

# COMMAND ----------

PurchaseOrderdf = readFromDeltaPath(model,entity)
display(PurchaseOrderdf)

# COMMAND ----------

saveDeltaTableToCatalog(PurchaseOrderdf,schema,entity)
