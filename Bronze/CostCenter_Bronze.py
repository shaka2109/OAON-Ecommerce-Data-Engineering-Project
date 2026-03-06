# Databricks notebook source
# MAGIC %run ../Misc/SharedLibraries

# COMMAND ----------

model = 'Others'
entity = 'CostCenter'
schema = 'bronze'

# COMMAND ----------

costcenterdf = readFromDeltaPath(model,entity)
display(costcenterdf)

# COMMAND ----------

saveDeltaTableToCatalog(costcenterdf,schema,entity)
