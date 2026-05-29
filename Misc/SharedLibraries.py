# %%
import pyspark.sql.functions as F 
import datetime as dt
import pandas as pd
import dateutil

# %%
ADLS_DEV_BASE_PATH = "abfss://proyecto01@adlsproyecto01.dfs.core.windows.net/"
DELTALAKE_RAW_PATH = "DeltaLake/Raw/"

# %%
service_credential = dbutils.secrets.get(scope="proyecto02scope",key="ClientSecret")
application_id = dbutils.secrets.get(scope="proyecto02scope",key="appid")
tenant_id = dbutils.secrets.get(scope="proyecto02scope",key="tenantid")

spark.conf.set("fs.azure.account.auth.type.adlsproyecto01.dfs.core.windows.net", "OAuth")
spark.conf.set("fs.azure.account.oauth.provider.type.adlsproyecto01.dfs.core.windows.net",
               "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider")

spark.conf.set("fs.azure.account.oauth2.client.id.adlsproyecto01.dfs.core.windows.net", application_id)
spark.conf.set("fs.azure.account.oauth2.client.secret.adlsproyecto01.dfs.core.windows.net", service_credential)
spark.conf.set("fs.azure.account.oauth2.client.endpoint.adlsproyecto01.dfs.core.windows.net",
               f"https://login.microsoftonline.com/{tenant_id}/oauth2/token")

# %%
from pyspark.sql.types import *

type_map = {
    "Int64": LongType(),
    "String": StringType(),
    "DateTime": TimestampType(),
    "Decimal": DecimalType(18,2),
    "Double": DoubleType(),
    "Boolean": BooleanType()
}

def build_schema_from_cdm(cdm_path):
    cdm_json = spark.read.option("multiline","true").json(cdm_path).collect()[0].asDict()

    attrs = cdm_json["definitions"][0]["hasAttributes"]

    fields = [
        StructField(a["name"], type_map.get(a["dataFormat"], StringType()), True)
        for a in attrs
    ]

    return StructType(fields)


def read_cdm_entity(cdm_path, csv_path, header=False, delimiter=","):
    schema = build_schema_from_cdm(cdm_path)

    return (spark.read
            .schema(schema)
            .option("header", str(header).lower())
            .option("delimiter", delimiter)
            .csv(csv_path))

# %%
def read_manifest(manifest_path, base_folder):
    manifest = (spark.read
                .option("multiline","true")
                .json(manifest_path)
                .collect()[0]
                .asDict())

    dfs = {}

    for e in manifest["entities"]:
        name = e["entityName"]

        dfs[name] = read_cdm_entity(
            f"{base_folder}/{name}.cdm.json",
            f"{base_folder}/{name}/*.csv"
        )

    return dfs

# %%
def read_entity(model, entity):

    base = "abfss://proyecto01@adlsproyecto01.dfs.core.windows.net/ProyectoOAON/Tables"
    
    manifest_path = f"{base}/{model}/{model}.manifest.cdm.json"
    folder_path = f"{base}/{model}"
    
    tables = read_manifest(manifest_path, folder_path)
    
    df = tables[entity]
    
    return df

# %%
def writeRawToDeltaLake(entityDF,deltaLakePath):
    entityDF.write.mode('overwrite').option('overwriteSchema',True).option('path', ADLS_DEV_BASE_PATH+deltaLakePath).save()

# %%
def readFromDeltaPath(model,entity):
   df = (spark.read.format('delta')
    .option('path', f'{ADLS_DEV_BASE_PATH}{DELTALAKE_RAW_PATH}{model}/{entity}/')
    .load())
   return df

# %%
def saveDeltaTableToCatalog(df,schema,tableName):
    schema = schema.lower()
    tableName = tableName.lower()
    spark.sql(f"CREATE SCHEMA IF NOT EXISTS {schema}")
    df.write.format("delta").mode("overwrite").saveAsTable(f"{schema}.{tableName}")


