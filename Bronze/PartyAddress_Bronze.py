# Databricks notebook source
# MAGIC %run ../Misc/SharedLibraries

# COMMAND ----------

model = 'Purchase'
entity = 'PartyAddress'
schema = 'bronze'

# COMMAND ----------

PartyAddressdf = readFromDeltaPath(model,entity)
display(PartyAddressdf)

# COMMAND ----------

saveDeltaTableToCatalog(PartyAddressdf,schema,entity)
