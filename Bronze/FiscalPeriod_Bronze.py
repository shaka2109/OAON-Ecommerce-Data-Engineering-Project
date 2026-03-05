# Databricks notebook source
# MAGIC %run ../Misc/SharedLibraries

# COMMAND ----------

model = 'Others'
entity = 'FiscalPeriod'
schema = 'bronze'

# COMMAND ----------

fiscaldf = readFromDeltaPath(model,entity)
display(fiscaldf)

# COMMAND ----------

saveDeltaTableToCatalog(fiscaldf,schema,entity)
