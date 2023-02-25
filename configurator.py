import configparser
import os
from logger import Logger as log


class Config:
    @staticmethod
    def verify():
        if not os.path.exists("config.ini"):
            log.info("Config.ini file is being created for the first time...")
            config = configparser.ConfigParser()
            config["CONSTANTS"] = {
                "version": os.environ.get("USERNAME"),
                "username": "TEST",
                "tesseract_path": ""
            }
            with open("config.ini", "w") as file:
                config.write(file)
            log.info("Config.ini file has been created.")

    @staticmethod
    def read(section,key):
        config = configparser.ConfigParser()
        config.read("config.ini")
        return config[section][key]

    @staticmethod
    def edit(section, key, value):
        config = configparser.ConfigParser()
        config.read("config.ini")
        config.set(section, key, value)
        with open("config.ini", "w") as file:
            config.write(file)

