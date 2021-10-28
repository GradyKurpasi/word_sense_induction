
from interfaces.adapters_azureml import AzureMLPlatform
from tests.test_azureml import *
import requests


training_file = 'train.py'
experiment = 'Transformer-Testing'
environment = 'word_sense_induction_env'
compute = 'local'


azml = AzureMLPlatform(experiment_name=experiment, environment_name=environment)
print("Connected to AzureML")
azml.run_training(filelist=[training_file],  comp_target=compute, entrypoint=training_file)
print("AzureML Training Complete")


