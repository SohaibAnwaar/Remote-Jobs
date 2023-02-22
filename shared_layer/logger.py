
import datetime
import enum
import logging
from logging.handlers import TimedRotatingFileHandler
from env import settings
import os


class Logger:
    """This class is used to create logger for the project
    """

    def __init__(self) -> None:
        """Initilise the logger
        """
        # Logger Paths
        self.db_logger_name = "db_logger"
        self.main_logger_name = "main_logger"
        self.logger_paths = {
            "db_logger": settings.db_log_path,
            "main_logger": settings.main_log_path,
            "scrapper_logger": settings.scrapper_log_path + datetime.datetime.now().strftime("%Y-%m-%d") + "/"
        }
        # Making Scrappers Log Folder
        if not os.path.exists(self.logger_paths["scrapper_logger"]):
            os.makedirs(self.logger_paths["scrapper_logger"])

        self.db_logger = self.setup_logger(
            name=self.db_logger_name, log_file=self.logger_paths["db_logger"])

        self.main_logger = self.setup_logger(
            name=self.main_logger_name, log_file=self.logger_paths["main_logger"])

    def setup_logger(self, name: str, log_file: str, level=logging.INFO) -> logging.getLogger:
        """To setup as many loggers as you want"""
        formatter = logging.Formatter(
            '%(asctime)s %(name)s - %(levelname)s - %(message)s')

        # Adding Rotating Handler
        handler = TimedRotatingFileHandler(filename=log_file,
                                           when='D',
                                           interval=1,
                                           backupCount=6,
                                           delay=False)
        # Setting formator
        handler.setFormatter(formatter)
        # Logger Name
        logger = logging.getLogger(name)
        # Set Level of log
        logger.setLevel(level)
        # Adding handler
        logger.addHandler(handler)
        return logger

    def get_logger(self, name: str) -> logging.getLogger:
        """Get log for 
        - Scrappers
        - Main Logs
        - Validated Lead Logs

        Args:
            name (str): Name of the log file

        Returns:
            _type_: _description_
        """
        # Making logging object with name
        logger = logging.getLogger(name)
        # Getting handler
        if not logger.hasHandlers():
            
            if name == "db_logger":
                logger = self.setup_logger(
                    name, f'{self.logger_paths["db_logger"]}{name}.log')

            elif name == "main_logger":
                logger = self.setup_logger(
                    name, f'{self.logger_paths["main_logger"]}{name}.log')

            else:
                logger = self.setup_logger(
                    name, f'{self.logger_paths["scrapper_logger"]}{name}.log')
        
        return logger


logger = Logger()
