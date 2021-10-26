# from container_files import entry



# from infertaces import adapters_azureml

from  interfaces.adapters_azureml import AzureMLPlatform
import os

default_test_experiment = 'Testing'
default_test_environment = 'test-env'
default_training_file = 'hello_there.py'

def test_azureml_connect(test_environment=default_test_environment, test_experiment=default_test_experiment):
    """
        Default experiment = 'Testing'
        Default environment = 'test-env'
    """
    az_plat = AzureMLPlatform(experiment_name=test_experiment, environment_name=test_environment)
    assert az_plat != None
    print("test_azureml_connect(): Connected")
    # print("Experiment: " + az_plat.experiment.name)
    # print("Environment: " + az_plat.environment.name)


def test_azureml_run_training(test_environment=default_test_environment, test_experiment=default_test_experiment):
    """
        runs default_training_file in the specified experiment and environment
    """    
    # create_training_file()
    az_plat = AzureMLPlatform(experiment_name=test_experiment, environment_name=test_environment)
    print("test_azureml_run_training(): Connected")
    az_plat.run_training(filelist=[default_training_file],  comp_target='local', entrypoint=default_training_file)
    print("test_azureml_run_training(): Complete")
    # remove_training_file()    

def create_training_file():
    """"
    Creates default_training_file
    """
    with open(default_training_file, 'w') as f:
        f.write("from pip import _internal\n")
        f.write("_internal.main(['list'])\n")
        f.write("print(\"Hello There\")\n")

def remove_training_file():
    """
    deletes default_training_file
    """
    os.remove(default_training_file)
     
    