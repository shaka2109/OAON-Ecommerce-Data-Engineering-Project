# Databricks notebook source
# MAGIC %md #### Run shared libraries

# COMMAND ----------

# MAGIC %run ../Misc/SharedLibraries

# COMMAND ----------

# MAGIC %md #### Define Variables

# COMMAND ----------

EntityName = 'PartyAddress'
Manifest = 'Purchase'
deltaLakePath = 'DeltaLake/Raw/Purchase/' + EntityName

# COMMAND ----------

# MAGIC %md #### Read Entity

# COMMAND ----------

partyAddressdf = read_entity(Manifest,EntityName)
display(partyAddressdf)

# COMMAND ----------

# MAGIC %md
# MAGIC #### Write to DeltaLake in ADLS

# COMMAND ----------

writeRawToDeltaLake(partyAddressdf,deltaLakePath)
