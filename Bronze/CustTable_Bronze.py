# Databricks notebook source
# MAGIC %run ../Misc/SharedLibraries

# COMMAND ----------

model = 'Sales'
entity = 'CustTable'
schema = 'bronze'

# COMMAND ----------

custtabledf = readFromDeltaPath(model,entity)
display(custtabledf)

# COMMAND ----------

saveDeltaTableToCatalog(custtabledf,schema,entity)
