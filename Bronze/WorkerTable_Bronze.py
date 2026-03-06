# Databricks notebook source
# MAGIC %run ../Misc/SharedLibraries

# COMMAND ----------

model = 'Hr'
entity = 'WorkerTable'
schema = 'bronze'

# COMMAND ----------

workertabledf = readFromDeltaPath(model,entity)
display(workertabledf)

# COMMAND ----------

saveDeltaTableToCatalog(workertabledf,schema,entity)
