# Databricks notebook source
# MAGIC %run ../Misc/SharedLibraries

# COMMAND ----------

model = 'Sales'
entity = 'PromoTable'
schema = 'bronze'

# COMMAND ----------

PromoTabledf = readFromDeltaPath(model,entity)
display(PromoTabledf)

# COMMAND ----------

saveDeltaTableToCatalog(PromoTabledf,schema,entity)
