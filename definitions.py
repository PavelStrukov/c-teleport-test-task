import os

RESOURCES_DIR_NAME = 'resources'
PASSENGER_PERSONAL_INFO_FILE_NAME = 'passenger_personal_info.json'

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCES_DIR = os.path.join(ROOT_DIR, RESOURCES_DIR_NAME)
PASSENGER_PERSONAL_INFO_FILE = os.path.join(RESOURCES_DIR, PASSENGER_PERSONAL_INFO_FILE_NAME)
