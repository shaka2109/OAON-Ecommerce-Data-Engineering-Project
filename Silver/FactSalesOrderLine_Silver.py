# Databricks notebook source
# MAGIC %run ../Misc/SharedLibraries

# COMMAND ----------

UpdateDateTime = dt.datetime.now()
entity = 'factsalesorderline'
schema = 'Silver'

# COMMAND ----------

# DBTITLE 1,Read Bronze Tables
# Se lee la tabla de la base de datos a usar como fact

salesorderlinedf= spark.table("bronze.salesorderline")

# COMMAND ----------

# DBTITLE 1,Read table SQL
# MAGIC %sql
# MAGIC select * from bronze.promotable
# MAGIC
# MAGIC -- Entendemos que se deben crear nuevas columnas con condiones de las promociones para unir con la tabla que servira como FACT

# COMMAND ----------

# DBTITLE 1,TempView
# MAGIC %sql
# MAGIC -- Se crea una TempView para hacer un CASE para crear minimos y maximos para el rango de volumen de promociones.
# MAGIC
# MAGIC CREATE OR REPLACE TEMP VIEW vwPromotable
# MAGIC AS
# MAGIC
# MAGIC SELECT 
# MAGIC   PromotionId,
# MAGIC   CASE PromotionName
# MAGIC     WHEN 'Volume Discount 11 to 20' THEN 11
# MAGIC     WHEN 'Volume Discount 21 to 40' THEN 21
# MAGIC     WHEN 'Volume Discount 41 to 60' THEN 41
# MAGIC     WHEN 'Volume Discount > 60' THEN 61
# MAGIC     ELSE NULL
# MAGIC   END VolumeStart,
# MAGIC   CASE PromotionName
# MAGIC     WHEN 'Volume Discount 11 to 20' THEN 20
# MAGIC     WHEN 'Volume Discount 21 to 40' THEN 40
# MAGIC     WHEN 'Volume Discount 41 to 60' THEN 60
# MAGIC     WHEN 'Volume Discount > 60' THEN 9999999
# MAGIC     ELSE NULL
# MAGIC   END VolumeEnd,
# MAGIC   ValidFrom,
# MAGIC   ValidTo,
# MAGIC   PromoPercentage
# MAGIC FROM bronze.promotable
# MAGIC

# COMMAND ----------

# DBTITLE 1,Read TempView
# MAGIC %sql
# MAGIC -- Se lee la TempView para obetener los datos
# MAGIC select * from vwPromotable

# COMMAND ----------

# DBTITLE 1,FactTable
# MAGIC %sql
# MAGIC /* Se crea otra TempView para hacer joins con las tablas de silver y crear la Fact Table.
# MAGIC    Se hacen joins y se llaman las columnas requeridas. Se modifican y aplican funciones a algunas.
# MAGIC    Las dos primeras columnas sirven como llave compuesta. Se usa CASE para crear nuevas columnas con condiciones. El Join con la TempView creada anteriormente es para aplicar descuentos si es que hay, se usa un join con una condicion dinamica.
# MAGIC */
# MAGIC
# MAGIC CREATE OR REPLACE TEMP VIEW vwFactSalesOrderLine
# MAGIC AS
# MAGIC
# MAGIC SELECT 
# MAGIC   S.SalesOrderNumber,
# MAGIC   S.SalesOrderLine,
# MAGIC   CASE  
# MAGIC     WHEN isnull(S.LastProcessedChange_DateTime) 
# MAGIC       THEN'1900-01-01'
# MAGIC     ELSE
# MAGIC       S.LastProcessedChange_DateTime 
# MAGIC   END AS LastProcessedChange_DateTime,
# MAGIC   from_utc_timestamp(S.DataLakeModified_DateTime,'CST') AS DataLakeModified_DateTime,
# MAGIC   S.ItemId,
# MAGIC   S.Qty,
# MAGIC   S.Price,
# MAGIC   S.Qty * S.Price AS TotalAmount,
# MAGIC   CASE 
# MAGIC     WHEN PR.PromotionId IS NULL THEN TotalAmount
# MAGIC   ELSE
# MAGIC     TotalAmount * (1- PR.promoPercentage)
# MAGIC   END  AS TotalAmountWithDiscount,  
# MAGIC   S.VatPercentage,
# MAGIC   TotalAmountWithDiscount * s.VatPercentage as VatAmount,
# MAGIC   TotalAmountWithDiscount + VatAmount AS TotalOrderAmount,
# MAGIC   C.CurrencyId,
# MAGIC   from_utc_timestamp(S.BookDate,'CST') AS BookDate,
# MAGIC   cast(date_format(S.BOOKDate,'yyyyMMdd') AS INT ) AS BookDateKey,
# MAGIC   from_utc_timestamp(S.ShippedDate,'CST') AS ShippedDate,
# MAGIC   cast(date_format(S.ShippedDate,'yyyyMMdd') AS INT ) AS ShippedDateKey,
# MAGIC   from_utc_timestamp(S.DeliveredDate,'CST') AS DeliveredDate,
# MAGIC   cast(date_format(S.DeliveredDate,'yyyyMMdd') AS INT ) AS DeliveredKey,
# MAGIC   S.TrackingNumber,
# MAGIC   S.CustId,
# MAGIC   P.PaymentTypeId,
# MAGIC   PR.PromotionId,
# MAGIC   current_timestamp() AS UpdatedDateTime,
# MAGIC   xxhash64(s.RecordId) AS SalesOrderLineRecordId
# MAGIC  FROM bronze.salesorderline AS S
# MAGIC  LEFT JOIN bronze.currency AS C ON S.CurrencyCode = C.Code
# MAGIC  LEFT JOIN silver.dimpaymenttypes AS P  ON S.PaymentTypeDesc = P.PaymentTypeDesc
# MAGIC  LEFT JOIN vwPromotable AS PR
# MAGIC    ON (
# MAGIC       MONTH(S.BookDate) = 1
# MAGIC       AND S.BookDate BETWEEN PR.ValidFrom AND PR.ValidTo
# MAGIC       )
# MAGIC    OR (
# MAGIC       MONTH(S.BookDate) <> 1
# MAGIC       AND S.Qty BETWEEN PR.VolumeStart AND PR.VolumeEnd
# MAGIC       )

# COMMAND ----------

# DBTITLE 1,Read Fact Table
factsalesorderlinedf =  spark.table("vwFactSalesOrderLine")
display(factsalesorderlinedf)

# COMMAND ----------

# DBTITLE 1,Final Dataframe
df_final = factsalesorderlinedf

# COMMAND ----------

# DBTITLE 1,Write to Silver Schema
saveDeltaTableToCatalog(df_final,schema,entity)
