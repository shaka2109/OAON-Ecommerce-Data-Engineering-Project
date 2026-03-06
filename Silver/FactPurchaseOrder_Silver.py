# Databricks notebook source
# MAGIC %run ../Misc/SharedLibraries

# COMMAND ----------

UpdateDateTime = dt.datetime.now()
entity = 'factpurchaseorder'
schema = 'Silver'

# COMMAND ----------

# DBTITLE 1,Read Bronze Tables
purchaseorderDf= spark.table("bronze.purchaseorder")
dimcostcenterDf= spark.table("silver.dimcostcenter")
dimcurrencyDf= spark.table("silver.dimcurrency")

# COMMAND ----------

# DBTITLE 1,Fact table
factpurchaseorderDf = purchaseorderDf.filter(purchaseorderDf.RecordId.isNotNull()
    ).join(dimcostcenterDf, purchaseorderDf.CostCenter == dimcostcenterDf.CostCenterNumber, "left"
    ).join(dimcurrencyDf, purchaseorderDf.currencycode == dimcurrencyDf.Code, "left"
    ).select(
        purchaseorderDf.PoNumber,
        purchaseorderDf.LineItem,
        purchaseorderDf.VendId.alias("VendorKey"),
        F.when(purchaseorderDf.LastProcessedChange_DateTime.isNull(), "1900-01-01").otherwise(purchaseorderDf.LastProcessedChange_DateTime).cast("timestamp").alias("LastProcessedChange_DateTime"),
        F.from_utc_timestamp(purchaseorderDf.DataLakeModified_DateTime,'CST').alias("DataLakeModified_DateTime"),
        purchaseorderDf.Qty,
        purchaseorderDf.PurchasePrice,
        purchaseorderDf.TotalOrder,
        purchaseorderDf.CostCenter.alias("CostCenterKey"),
        dimcostcenterDf.Vat.alias("VatAmount"),
        F.round((purchaseorderDf.TotalOrder + (purchaseorderDf.TotalOrder * dimcostcenterDf.Vat)),4).alias("TotalAmount"),
        purchaseorderDf.ExchangeRate,
        purchaseorderDf.Itemkey,
        dimcurrencyDf.CurrencyId.alias("CurrencyKey"),
        F.from_utc_timestamp(purchaseorderDf.OrderDate,'CST').alias("OrderDate"),
        F.from_utc_timestamp(purchaseorderDf.ShipDate,'CST').alias("ShipDate"),
        F.from_utc_timestamp(purchaseorderDf.DeliveredDate,'CST').alias("DeliveredDate"),
        F.date_format(purchaseorderDf.OrderDate,'yyyyMMdd').cast("int").alias("OrderDateKey"),
        F.date_format(purchaseorderDf.ShipDate,'yyyyMMdd').cast("int").alias("ShipDateKey"),
        F.date_format(purchaseorderDf.DeliveredDate,'yyyyMMdd').cast("int").alias("DeliveredDateKey"),
        purchaseorderDf.TrackingNumber,
        purchaseorderDf.Batchid.alias("BatchId"),
        purchaseorderDf.CreatedBy,
        purchaseorderDf.RecordId.alias("PurchaseOrderRecordId"),
        purchaseorderDf.CategoryId.alias("CategoryKey")
    ).withColumn("UpdateDateTime", F.lit(UpdateDateTime)
    ).withColumn("PurchaseOrderHashKey", F.xxhash64("PurchaseOrderRecordId")
    )
display(factpurchaseorderDf)

# COMMAND ----------

# DBTITLE 1,Final Dataframe
df_final = factpurchaseorderDf

# COMMAND ----------

# DBTITLE 1,Write to Silver Schema
saveDeltaTableToCatalog(df_final,schema,entity)
