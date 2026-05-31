# %%
# %run /Workspace/Users/admin@jkalexanderhotmail.onmicrosoft.com/ADLSoauth

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
base = "/Volumes/oaon_project/files/tablas/Purchase"

# %%
df = read_cdm_entity(
    f"{base}/PurchItem.cdm.json",
    f"{base}/PurchItem/*.csv"
)

display(df)

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
tables = read_manifest(
    "/Volumes/oaon_project/files/tablas/Purchase/Purchase.manifest.cdm.json",
    "/Volumes/oaon_project/files/tablas/Purchase"
)

display(tables["PurchItem"])


