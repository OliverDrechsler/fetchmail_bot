import yaml
import os
import logging
from collections import ChainMap

logger: logging.Logger = logging.getLogger(name="config")


class YamlReadError(Exception):
    """Exception raised for config yaml file read error.

    Attributes:
        message -- explanation of the error
    """

    def __init__(
        self, message="A YAML config file readerror" + " is ocurred during parsing file"
    ) -> None:
        self.message: str = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return f"{self.message}"


class Configuration:
    """Reads general yaml Config file into class."""

    def __init__(self) -> None:
        """Initial class definition.
        Read from config.yaml file it configuration into class attribute
        config dict and from there into multiple attributes.
        :return: Nothing adds class instance attribues
        :rtype: None
        """
        self.logger: logging.Logger = logging.getLogger(name="config")
        self.base_path: str = self.get_base_path()
        logger.debug(msg=self.base_path)
        self.config_file: str = self.define_config_file()
        logger.debug(msg=self.define_config_file())
        self.config: dict = self.read_config(config_file=self.config_file)
        self.telegram_token: str = self.config["telegram"]["token"]
        self.telegram_chat_nr: list[str] = self.config["telegram"]["chat_number"]
        self.additional_list: list[str] = self.config["telegram"]["additional_list"]
        self.user_dict: dict[str, str] = self.get_user_dict()
        self.list_id: list[str] = self.get_id_list()
        self.list_user: list[str] = self.get_user_list()

    def get_user_dict(self) -> dict:
        """Get user dict from list of yaml telegram.list

        :return: dict of user key and values of telegram id
        :rtype: dict
        """
        return dict(ChainMap(*self.config["telegram"]["allow_list"]))

    def get_user_list(self) -> list:
        """
        Get a list of users from user_dict and additional_list.
        """
        return (
            [i for i in self.user_dict.keys()]
            + [i.upper() for i in self.additional_list]
            + [i.lower() for i in self.additional_list]
            + [i.capitalize() for i in self.additional_list]
        )

    def get_id_list(self) -> list:
        """Gets a list if telegram id of user dict from yaml telegram.list

        :return: list of telegram id
        :rtype: list
        """
        return [i for i in self.user_dict.values()]

    def get_base_path(self) -> None:
        """
        Get from project base path. This normally one folder
        up from the config_util.py
        """
        return os.path.dirname(p=os.path.abspath(path=__file__)) + "/"

    def read_config(self, config_file: str) -> None:
        """
        Reads config.yaml file into variables.

        :params config_file: the config file to be read
        :type config_file: string
        :return: Noting - adds class attribute self.config dictionary
          from config yaml file
        :rtype: None
        """
        self.logger.debug("reading config {0} file info dict".format(config_file))
        try:
            with open(file=config_file, mode="r") as file:
                return yaml.load(stream=file, Loader=yaml.SafeLoader)
        except FileNotFoundError:
            self.logger.error("Could not find %s", self.config_file)
            raise FileNotFoundError("Could not find config file")
        except:
            self.logger.error(
                "a YAML error is ocurred during parsing file %s ", self.config_file
            )
            raise YamlReadError(
                message="a YAML error is " + "ocurred during parsing file"
            )

    def define_config_file(self) -> None:
        """
        Checks and defines Config yaml file path.

        :return: adds a new class path attribute for the config file.
        :rtype: None
        """
        self.logger.debug("checking if config.yaml file exists")

        if os.path.isfile(path=self.base_path + "config.yaml"):
            return self.base_path + "config.yaml"

        self.logger.info("No config.yaml file detected. Using" + " template one.")
        if not os.path.exists(path=self.base_path + "config_template.yaml"):
            raise (NameError("No config file found!"))
        return self.base_path + "config_template.yaml"
