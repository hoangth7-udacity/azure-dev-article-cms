import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
from azure.keyvault.secrets import SecretClient

load_dotenv(dotenv_path="./app.env")
key_vault_uri = "https://{}.vault.azure.net/".format(os.getenv("SECRET_VAULT"))
credential = DefaultAzureCredential()
if os.getenv("APP_LOCATION") == "Azure":
    print("Using Managed Identity")
    credential = ManagedIdentityCredential()
secret_client = SecretClient(vault_url=key_vault_uri, credential=credential)

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    ### secret key for CSRF
    SECRET_KEY = secret_client.get_secret("secret-key").value
    if not SECRET_KEY:
        raise ValueError("Need to define SECRET_KEY environment variable")

    # storage account
    BLOB_ACCOUNT = os.environ.get("BLOB_ACCOUNT")
    BLOB_STORAGE_KEY = secret_client.get_secret("blob-storage-key").value
    BLOB_CONTAINER = os.getenv("BLOB_CONTAINER")
    if not BLOB_ACCOUNT or not BLOB_STORAGE_KEY or not BLOB_CONTAINER:
        raise ValueError("Need to define blob storage config")

    # database server
    SQL_SERVER = os.environ.get("SQL_SERVER")
    SQL_SERVER_PORT = os.environ.get("SQL_SERVER_PORT", "1433")
    SQL_DATABASE = os.environ.get("SQL_DATABASE")
    SQL_USER_NAME = os.environ.get("SQL_USER_NAME")
    SQL_PASSWORD = secret_client.get_secret("sql-password").value
    if (
        not SQL_SERVER
        or not SQL_SERVER_PORT
        or not SQL_DATABASE
        or not SQL_USER_NAME
        or not SQL_PASSWORD
    ):
        raise ValueError("Need to define database config")
    # Below URI may need some adjustments for driver version, based on your OS, if running locally
    SQLALCHEMY_DATABASE_URI = (
        "mssql+pyodbc://"
        + SQL_USER_NAME
        + ":"
        + SQL_PASSWORD
        + "@"
        + SQL_SERVER
        + ":"
        + SQL_SERVER_PORT
        + "/"
        + SQL_DATABASE
        + "?driver=ODBC+Driver+17+for+SQL+Server"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ### Info for MS Authentication ###
    ### As adapted from: https://github.com/Azure-Samples/ms-identity-python-webapp ###
    # In your production app, Microsoft recommends you to use other ways to store your secret,
    # such as KeyVault, or environment variable as described in Flask's documentation here:
    # https://flask.palletsprojects.com/en/1.1.x/config/#configuring-from-environment-variables
    CLIENT_ID = os.getenv("AUTH_CLIENT_ID")
    CLIENT_SECRET = secret_client.get_secret("auth-client-secret").value
    if not CLIENT_SECRET or not CLIENT_ID:
        raise ValueError("Need to define CLIENT_ID/CLIENT_SECRET environment variable")

    REDIRECT_PATH = "/getAToken"  # Used to form an absolute URL; must match to app's redirect_uri set in AAD

    AUTHORITY = "https://login.microsoftonline.com/common"
    # For multi-tenant app, else put tenant name
    # AUTHORITY = "https://login.microsoftonline.com/Enter_the_Tenant_Name_Here"

    # You can find the proper permission names from this document
    # https://docs.microsoft.com/en-us/graph/permissions-reference
    SCOPE = ["User.Read"]  # Only need to read user profile for this app
    SESSION_TYPE = "filesystem"  # Token cache will be stored in server-side session
