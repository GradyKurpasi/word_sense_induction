# from container_files import entry



# from infertaces import adapters_azureml

from  interfaces.adapters_azureml import AzureMLPlatform

def test_azureml_connect():
    az_plat = AzureMLPlatform('Container_Testing', 'word_sense_induction_env')
    az_plat.connect()

def test_azureml_run_training():
    az_plat = AzureMLPlatform('Container_Testing', 'word_sense_induction_env')
    az_plat.run_training(filelist=["entry.py"], entrypoint="entry.py")
