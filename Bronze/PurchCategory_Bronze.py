# Databricks notebook source
# MAGIC %run ../Misc/SharedLibraries

# COMMAND ----------

model = 'Purchase'
entity = 'PurchCategory'
schema = 'bronze'

# COMMAND ----------

PurchCategorydf = readFromDeltaPath(model,entity)
display(PurchCategorydf)

# COMMAND ----------

saveDeltaTableToCatalog(PurchCategorydf,schema,entity)
