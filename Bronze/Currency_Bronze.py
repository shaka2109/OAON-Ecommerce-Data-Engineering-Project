# Databricks notebook source
# MAGIC %run ../Misc/SharedLibraries

# COMMAND ----------

model = 'Others'
entity = 'Currency'
schema = 'bronze'

# COMMAND ----------

currencydf = readFromDeltaPath(model,entity)
display(currencydf)

# COMMAND ----------

saveDeltaTableToCatalog(currencydf,schema,entity)
