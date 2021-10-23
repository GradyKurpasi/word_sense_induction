from interfaces.adapters_azureml import AzureMLPlatform


az_plat = AzureMLPlatform('Container_Testing', 'word_sense_induction_env')

az_plat.run_training(filelist=["entry.py"], entrypoint="entry.py")
