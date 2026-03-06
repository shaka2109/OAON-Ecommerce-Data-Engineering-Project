# Databricks notebook source
# MAGIC %run ../Misc/SharedLibraries

# COMMAND ----------

model = 'Sales'
entity = 'SalesOrderLine'
schema = 'bronze'

# COMMAND ----------

SalesOrderLinedf = readFromDeltaPath(model,entity)
display(SalesOrderLinedf)

# COMMAND ----------

saveDeltaTableToCatalog(SalesOrderLinedf,schema,entity)
