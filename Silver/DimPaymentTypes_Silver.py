# Databricks notebook source
# MAGIC %run ../Misc/SharedLibraries

# COMMAND ----------

entity = 'dimPaymentTypes'
schema = 'silver'

# COMMAND ----------

# DBTITLE 1,Read Bronze Tables
# Se observa la necesidad de normalizar la tabla creando una tabla de dimension con PaymentTypes

salesorderlineDF = spark.table('bronze.salesorderline')
display(salesorderlineDF)

# COMMAND ----------

# DBTITLE 1,Create new dim table
# MAGIC %sql
# MAGIC CREATE TABLE IF NOT EXISTS silver.dimpaymenttypes(
# MAGIC   PaymentTypeId INT,
# MAGIC   PaymentTypeDesc STRING
# MAGIC )
# MAGIC
# MAGIC -- Se crea la estructura de la nueva tabla de PaymentTypes

# COMMAND ----------

# DBTITLE 1,Build dim table
# Se extraen los datos distintos de la columna

df = salesorderlineDF.select("PaymentTypeDesc").distinct()
display(df)

# COMMAND ----------

# DBTITLE 1,Read new dim table
# Se lee la tabla creada con su estructura

paymenttypeDF = spark.table("silver.dimpaymenttypes")
display(paymenttypeDF)

# COMMAND ----------

# DBTITLE 1,Seleccionar nuevas filas a insertar
# Se compara la tabla creada con la tabla de la base de datos, y se extraen los nuevos registros

newrowsdf=df.exceptAll(paymenttypeDF.select("PaymentTypeDesc"))
display(newrowsdf)

# COMMAND ----------

# Se obtiene el maximo id de la tabla

maxdf = spark.sql("SELECT IFNULL(MAX(PaymentTypeId),0) AS maxid FROM silver.dimpaymenttypes")
maxid = maxdf.first()[0]
print(maxid)

# COMMAND ----------

# DBTITLE 1,Rellenar columna con Row_number
# Se agrega el id a la tabla

import pyspark.sql.window as W

idsdf = newrowsdf.withColumn("PaymentTypeId", F.row_number().over(window=W.Window.orderBy(F.col("PaymentTypeDesc"))))
display(idsdf)

# COMMAND ----------

# DBTITLE 1,Actualizar a incremental
# Se agrega el id a la tabla, sumandole el maximo id al nuevo registro que siempre es 1

idsFinal = idsdf.withColumn("PaymentTypeId", F.col("PaymentTypeId")+maxid)
display(idsFinal)

# COMMAND ----------

# DBTITLE 1,Chequear relleno
# MAGIC %sql
# MAGIC select  * from silver.dimpaymenttypes
# MAGIC
# MAGIC -- Se lee la tabla antes del incremental

# COMMAND ----------

# DBTITLE 1,DF Final
# Se guarda en otra variable

df_final = idsFinal

# COMMAND ----------

# DBTITLE 1,Write to silver
# Se agregan los datos a la tabla silver

appendToDeltaTable(df_final,"silver",entity)

# COMMAND ----------

# DBTITLE 1,Read new table
# MAGIC %sql
# MAGIC select  * from silver.dimpaymenttypes

# COMMAND ----------

# MAGIC %md
# MAGIC Una vez se agreguen nuevos registros a la tabla bronze.salesorderline, se corre nuevamente el notebook para actualizar la nueva tabla creada de dimpaymenttypes
