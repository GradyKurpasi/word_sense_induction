# from container_files import entry



# from infertaces import adapters_azureml

from  interfaces.adapters_azureml import AzureMLPlatform

test_experiment = 'Container_Testing'
test_environment = 'test-env'

def test_azureml_connect():
    az_plat = AzureMLPlatform(test_experiment, test_environment)
    az_plat.connect()

def test_azureml_run_training():
    """
        writes and runs "Hello There" script
    """    
    import os
    with open("hello_there.py", 'w') as f:
        f.write("print(\"Hello There\")")

    az_plat = AzureMLPlatform(test_experiment, test_environment)
    az_plat.run_training(filelist=["hello_there.py"],  comp_target='local', entrypoint="hello_there.py")
    
    os.remove("hello_there.py")


