# %%
service_credential = dbutils.secrets.get(scope="proyecto01scope", key="ClientSecret")
application_id = dbutils.secrets.get(scope="proyecto01scope", key="appid")
tenant_id = dbutils.secrets.get(scope="proyecto01scope", key="tenantid")

spark.conf.set(
    "fs.azure.account.auth.type.adlsproyecto01.dfs.core.windows.net", "OAuth"
)
spark.conf.set(
    "fs.azure.account.oauth.provider.type.adlsproyecto01.dfs.core.windows.net",
    "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
)

spark.conf.set(
    "fs.azure.account.oauth2.client.id.adlsproyecto01.dfs.core.windows.net",
    application_id,
)
spark.conf.set(
    "fs.azure.account.oauth2.client.secret.adlsproyecto01.dfs.core.windows.net",
    service_credential,
)
spark.conf.set(
    "fs.azure.account.oauth2.client.endpoint.adlsproyecto01.dfs.core.windows.net",
    f"https://login.microsoftonline.com/{tenant_id}/oauth2/token",
)

# %%
# dbutils.fs.ls("abfss://proyecto01@adlsproyecto01.dfs.core.windows.net/ProyectoOAON/Tables")


