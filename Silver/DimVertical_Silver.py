# Databricks notebook source
# MAGIC %run ../Misc/SharedLibraries

# COMMAND ----------

UpdateDateTime = dt.datetime.now()
entity = 'dimVertical'
schema = 'silver'

# COMMAND ----------

# DBTITLE 1,Read Bronze Tables
workerdf = spark.table('bronze.workertable')

# COMMAND ----------

# DBTITLE 1,Create New Table
# MAGIC %sql
# MAGIC -- Se crea una nueva tabla usando (BIGINT GENERATED ALWAYS AS IDENTITY)
# MAGIC
# MAGIC CREATE TABLE IF NOT EXISTS silver.dimvertical (
# MAGIC   VerticalId BIGINT GENERATED ALWAYS AS IDENTITY,
# MAGIC   Vertical STRING
# MAGIC )

# COMMAND ----------

# DBTITLE 1,Read distinct from column
# Tomar solo la columna de Vertical de WorkerTable con valores distintos

df = workerdf.select(F.expr("trim(Vertical) AS Vertical")).distinct()
display(df)

# COMMAND ----------

# DBTITLE 1,Read table
verticaldf = spark.table("silver.dimvertical")
display(verticaldf)

# COMMAND ----------

# Se extrae solo registros nuevos al comparar las dos tablas

newrowsdf=df.filter(F.col("Vertical").isNotNull()).exceptAll(verticaldf.select("Vertical"))
display(newrowsdf)

# COMMAND ----------

# Inserta los nuevos registros

newrowsdf.write.mode("append").saveAsTable("silver.dimvertical")

# COMMAND ----------

# DBTITLE 1,Show table
display(spark.table("silver.dimvertical"))

# COMMAND ----------

# DBTITLE 1,Para probar
# %sql
# INSERT INTO bronze.workertable(Vertical)VALUES("Data & AI")

# COMMAND ----------

# DBTITLE 1,Eliminar despues de probar
# %sql
# DELETE FROM bronze.workertable WHERE Vertical ="Data & AI"
