# Databricks notebook source
# MAGIC %run ../Misc/SharedLibraries

# COMMAND ----------

model = 'Purchase'
entity = 'PurchContracts'
schema = 'bronze'

# COMMAND ----------

PurchContractsdf = readFromDeltaPath(model,entity)
display(PurchContractsdf)

# COMMAND ----------

saveDeltaTableToCatalog(PurchContractsdf,schema,entity)
