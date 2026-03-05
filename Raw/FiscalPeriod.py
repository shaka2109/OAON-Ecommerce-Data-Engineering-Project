# Databricks notebook source
# MAGIC %md #### Run shared libraries

# COMMAND ----------

# MAGIC %run ../Misc/SharedLibraries

# COMMAND ----------

# MAGIC %md #### Define Variables

# COMMAND ----------

EntityName = 'FiscalPeriod'
Manifest = 'Others'
deltaLakePath = 'DeltaLake/Raw/Others/' + EntityName

# COMMAND ----------

# MAGIC %md #### Read Entity

# COMMAND ----------

fiscaldf = read_entity(Manifest,EntityName)
# display(currencydf)

# COMMAND ----------

# MAGIC %md
# MAGIC #### Write to DeltaLake in ADLS

# COMMAND ----------

writeRawToDeltaLake(fiscaldf,deltaLakePath)
