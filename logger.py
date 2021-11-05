import logging
import datetime
from typing_extensions import Literal

logLevelType = Literal["info", "warn", "error"]


def logger(message: str, logLevel: logLevelType = "info", noConsolePrint: bool = False):
    """
    Generates logs for the system in both command line and logger file
    Parameters
    ----------
    message: str
        A message to be shown in both logger file and command line
        example: "My Sample Message"
    logLevel: Literal, optional (default to "info)
        The level of logs. Possible values are "info", "warn", and "error"
        example: "warn"
    noConsolePrint: bool, optional (default to False)
        If True, the log will only be printed in the logger file
        example: True
    """
    # Create a console log by default
    if (not noConsolePrint):
        print(message)
    # Create a log in the log file
    currentMoment = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    printMessage = f'[{currentMoment}] {message}'
    if (logLevel is 'warn'):
        logging.warn(printMessage)
    elif (logLevel is 'error'):
        logging.error(printMessage)
    else:
        logging.info(printMessage)
