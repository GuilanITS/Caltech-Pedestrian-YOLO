import logging
from logger import logger
from PyInquirer import prompt
from utils.imageGenerator import imageGenerator


modules = ['Image Generator']


# Receives input from user by command line
def getUserInput():
    questions = [
        {
            'type': 'list',
            'name': 'Action',
            'message': 'Choose the module you want to use:',
            'choices': modules
        },
    ]
    userInputs = prompt(questions)
    return userInputs


def __init__():
    # Creating log file
    logging.basicConfig(filename='logger.log', level=logging.INFO)
    logger('Caltech pedestrian framework started!')
    # Getting inputs from users
    userInputs = getUserInput()['Action']
    if userInputs == 'Image Generator':
        imageGenerator()


__init__()
