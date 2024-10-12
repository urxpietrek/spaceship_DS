import os
import zipfile
import shutil
import subprocess

import logging
from config import settings

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
DATA_DIR = os.path.join(os.getcwd(),'data')

def download_from_kaggle():
    install_args = 'kaggle competitions download -c spaceship-titanic'.split(' ')
    try:
        process = subprocess.Popen(args = install_args,
                                    stdout=subprocess.PIPE)
        
    except subprocess.CalledProcessError:
        raise ValueError('Failure while retrieving data.')
    else:
        logger.info(process.communicate())
        logger.info('Successfuly retrieved data.')

def is_authanticated():
    kaggle_json_path = os.path.join(settings.KAGGLE_DIR, 'kaggle.json')
    if os.path.exists(kaggle_json_path):
        return True
    return False
    
def organize():
    with zipfile.ZipFile('spaceship-titanic.zip', mode = 'r') as zip:
        zip.extractall()
        os.mkdir(DATA_DIR)
    csv_files = ['sample_submission.csv', 'test.csv', 'train.csv']
    for csvf in csv_files:
        shutil.move(csvf, DATA_DIR)

def preprocess_data():
    if not os.path.isdir(DATA_DIR):
        try:
            if is_authanticated():
                download_from_kaggle()
                organize()
        except Exception:
            logger.exception('Exception occured')
            raise
