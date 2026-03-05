# Databricks notebook source
# MAGIC %run ../Misc/SharedLibraries

# COMMAND ----------

model = 'Purchase'
entity = 'Parties'
schema = 'bronze'

# COMMAND ----------

partiesdf = readFromDeltaPath(model,entity)
display(partiesdf)

# COMMAND ----------

saveDeltaTableToCatalog(partiesdf,schema,entity)
