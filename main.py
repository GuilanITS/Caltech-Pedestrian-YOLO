import logging
from logger import logger
from PyInquirer import prompt
from utils.imageGenerator import imageGenerator
from utils.plotAnnotations import annotationPlotter
from utils.annotationGenerator import annotationGenerator


modules = ['Image Generator', 'Annotation Generator', 'Annotation Plotter']


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
    # Getting inputs from usersd
    userInputs = getUserInput()['Action']
    if userInputs == 'Image Generator':
        imageGenerator()
    elif userInputs == 'Annotation Generator':
        annotationGenerator()
    elif userInputs == 'Annotation Plotter':
        annotationPlotter()


__init__()
