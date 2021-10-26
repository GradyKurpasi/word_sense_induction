
# from azureml.core import environment
from tests.test_azureml import *
import requests



# response = requests.get("https://babelnet.io/v6/getVersion?key=aa9e9919-5481-483b-8be2-25f6786657b4")
# print(response.json())
# test_azureml_connect(test_environment = "word_sense_induction_env")
test_azureml_run_training(test_environment="word_sense_induction_env")