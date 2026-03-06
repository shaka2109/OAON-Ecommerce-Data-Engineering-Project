# Databricks notebook source
# MAGIC %run ../Misc/SharedLibraries

# COMMAND ----------

UpdateDateTime = dt.datetime.now()
entity = 'dimDate'
schema = 'silver'

# COMMAND ----------

# DBTITLE 1,Read Bronze Tables
fiscalperiodDF = spark.table('bronze.fiscalperiod')

# COMMAND ----------

# DBTITLE 1,Date dimension from pandas
start_date = dt.date(2018,1,1)
end_date = start_date + dateutil.relativedelta.relativedelta(years=8,month=12,day=31)

start_date = dt.datetime.strptime(
    f"{start_date}", "%Y-%m-%d"
)
end_date = dt.datetime.strptime(
    f"{end_date}", "%Y-%m-%d"
)
print(start_date)
print(end_date)

# COMMAND ----------

# DBTITLE 1,Series with dates
datepddf = pd.date_range(start_date,end_date, freq='D').to_frame(name='Date')
datedf=spark.createDataFrame(datepddf)
display(datedf)

# COMMAND ----------

# DBTITLE 1,join with condition
joindf = (
    datedf.join(
        fiscalperiodDF.filter(fiscalperiodDF.RecordId.isNotNull()),
         (datedf.Date >= fiscalperiodDF.FiscalStartDate)
        & (datedf.Date <= fiscalperiodDF.FiscalEndDate),
        "left",
    ))
display(joindf)

# COMMAND ----------

# DBTITLE 1,Date dimension
datedimdf = joindf.select(
    "Date",
    F.date_format(F.col("Date"), "yyyyMMdd").cast("int").alias("DateId"),
    F.year(F.col("Date")).alias("Year"),
    F.month(F.col("Date")).alias("Month"),
    F.date_format(F.col("Date"), "MMM").cast("string").alias("MonthName"),
    F.dayofmonth(F.col("Date")).alias("Day"),
    F.date_format(F.col("Date"), "E").cast("string").alias("DayName"),
    F.quarter(F.col("Date")).alias("Quarter"),
    F.col("FiscalPeriodName").alias("FiscalPeriodName"),    
    "FiscalStartDate",
    "FiscalEndDate",
    "FiscalMonth",
    "FiscalYearStart",
    "FiscalYearEnd",
    "FiscalQuarter",
    "FiscalQuarterStart",
    "FiscalQuarterEnd",
    F.concat(F.lit("FY"),"FiscalYear").alias("FiscalYear"),
    F.lit(UpdateDateTime).alias("UpdatedDateTime"),
    F.xxhash64("DateId").alias("DateKey")
)
display(datedimdf)

# COMMAND ----------

df_final = datedimdf

# COMMAND ----------

# DBTITLE 1,Write to Silver Schema
saveDeltaTableToCatalog(df_final,schema,entity)
