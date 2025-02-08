from dotenv import dotenv_values,load_dotenv
import os

load_dotenv()

config = {**dotenv_values(".env"), **os.environ}

if(config["MS_INVENTORY_IS_DOCKER"] == "False"):
    config["DATABASE_HOST_NAME"] = "localhost"
    config["KAFKA_HOST_NAME"] = "localhost"
    
