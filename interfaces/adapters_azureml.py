"""
AzureML SDK provided by Microsoft Corporation under MIT license
Copyright (c) Microsoft Corporation. All rights reserved.
"""

from os import environ

from numpy.lib.utils import source
import container_files
from interfaces.ports_platform import AbstractPlatform
import azureml.core
from azureml.core import compute_target, script_run_config
from azureml.core import compute
from azureml.core import conda_dependencies
from azureml.core import Workspace
from azureml.core import Experiment
from azureml.core import Environment
from azureml.core.compute import ComputeTarget, AmlCompute
from azureml.core.runconfig import RunConfiguration
from azureml.core import ScriptRunConfig
from azureml.core.conda_dependencies import CondaDependencies

class AzureMLException(Exception):
    pass
class AzureMLWorkspaceException(AzureMLException):
    pass
class AzureMLEnvironmentException(AzureMLException):
    pass
class AzureMLExperimentException(AzureMLException):
    pass

default_experiment = 'Testing'  
default_environment = 'word_sense_induction_env'  
default_comp_target = 'local' # 'local' / 'gkurpasi1' (compute instance) / 'cpu-cluster' / 'gpu-cluster'
default_entrypoint = 'train.py' # entry script to be run in docker container
default_container_files_folder = '.' #location of files to be uploaded to docker container
# default_config_folder = '../.azureml'

class AzureMLPlatform(AbstractPlatform):
    """
        (Really) Thin wrapper for connection to AzureML platform
        CURRENTLY USES CLI AUTHENTICATION
        encapsulates:
            connection
            deployment of training scripts
            deployment of models
        employs docker file/image hosted in Azure Container Registry
                Public
            connect() - from base
            display_connection - from base
            run_training
    """


    def __init__(self, experiment_name=default_experiment, environment_name=default_environment, container_files_folder=default_container_files_folder): 
        super().__init__()
        self.container_files_folder = container_files_folder
        self.connect(experiment_name, environment_name)


    def connect(self, experiment_name, environment_name):
        self.workspace = self.__connect_workspace()
        self.experiment = self.__connect_experiment(experiment_name)
        self.environment = self.__connect_environment(environment_name)
        self.display_connection()


    def __connect_workspace(self):
        """
            Connect to workspace
            expects config.json in ./azureml
            config.json must contain workspace, resource group and subscription id
        """
        try:
            ws = Workspace.from_config()
            assert ws != None
            return  ws
        except Exception as e:
            err = "\nAzureMLPlatform connect_workspace(): Cannot connect to Workspace via config file \n"
            result = err + str(e)
            print(result)
            raise AzureMLWorkspaceException


    def __connect_experiment(self, experiment_name):
        """
            Connect experiment
        """
        try:
            ex = Experiment(workspace=self.workspace, name=experiment_name)
            assert ex != None
            return ex
        except Exception as e:
            err = "\nAzureMLPlatform connect_experiment(): Error Creating or Connecting to Experiment \"" + experiment_name + "\"\n"
            result = err + str(e)
            print(result)
            raise AzureMLExperimentException


    def __connect_environment(self, environment_name):
        """
            Connect environment
            ENVIRONMENT EXPECTED TO BE A DOCKER FILE OR IMAGE REGISTERED WITH AZURE CONTAINER REGISTRY
        """
        try:
            en = Environment.get(workspace=self.workspace, name=environment_name)
            assert en != None
            return en
        except Exception as e:
            err = "\nAzureMLPlatform connect_environment: Error Connecting to Environment \"" + environment_name + "\"\n"
            result = err + str(e)
            print(result)
            raise AzureMLEnvironmentException


    def display_connection(self):
        try:
            print ("")
            print ("AzureML SDK version: " + azureml.core.VERSION)
            print ("Subscription ID: " + self.workspace.subscription_id)
            print ("Resource Group: " +  self.workspace.resource_group)
            print ("Workspace: " + self.workspace.name)
            print ("Location: " + self.workspace.location)     
            print ("Environment: " + self.environment.name)   
            print ("Experiment: " + self.experiment.name)
            print ("")
        except Exception as e:
            err = "\nAzureMLPlatform display_connection():\n"
            result = err + str(e)
            print(result)
            raise AzureMLException


    def __copy_container_files(self, filelist):
        """
            DEPRECATED
            copies files in filelist to container_files_folder
            in preparation for a container run
        """
        import os
        import shutil
        
        os.makedirs(self.container_files_folder, exist_ok=True)
        for file in filelist:
            shutil.copy(file, self.container_files_folder)
        

    def run_training(self, comp_target=default_comp_target, entrypoint=default_entrypoint):
        """
            executes training run
        """

        run_config = RunConfiguration(framework='python')
        run_config.target = comp_target
        run_config.environment = self.environment

        script_run_config = ScriptRunConfig(
            source_directory=self.container_files_folder,
            script=entrypoint,
            run_config=run_config)

        print ("Experiment: "+ self.experiment.name)
        print ("Environment " + self.environment.name)
        print ("Compute Target: " + comp_target)
        print ("Entry Point: " + entrypoint)
        print ("Container Files Location: " + self.container_files_folder)
        # print ("Files " + str(filelist))
        run = self.experiment.submit(config=script_run_config)





