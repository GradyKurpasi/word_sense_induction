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

class AzureMLPlatform(AbstractPlatform):
    """
        (Really) Thin wrapper for connection to AzureML platform
        encapsulates:
            connection testing
            deployment of training scripts
            deployment models
        employs docker file/image hosted in Azure Container Registry
        CURRENTLY USES CLI AUTHENTICATION
    """

    def __init__(self, experiment_name="", environment_name="", container_files_folder="./container_files"): 
        super().__init__()
        self.workspace = self.connect_workspace()
        self.experiment = self.connect_experiment(experiment_name)
        self.environment = self.connect_environment(environment_name)
        self.container_files_folder = container_files_folder
        self.test_workspace_connection()


    def connect_workspace(self):
        """
            Connect to workspace
            expects config.json in ./azureml
            config.json must contain workspace, resource group and subscription id
        """
        try:
            return  Workspace.from_config()
        except Exception as e:
            err = "AzureMLPlatform connect_workspace(): Cannot connect to Workspace via config file \n"
            result = err + e
            return result


    def connect_experiment(self, experiment_name=""):
        """
            Connect experiment
            if no experiment_name, creates 'Testing' experiment
        """
        try:
            if experiment_name == "" : experiment_name = "Testing"
            return Experiment(workspace=self.workspace, name=experiment_name)
        except Exception as e:
            err = "AzureMLPlatform connect_experiment(): Error Creating or Connecting to Experiment """ + experiment_name + " "" \n"
            result = err + e
            return result


    def connect_environment(self, environment_name=""):
        """
            Connect environment
            if no environment_name, attempts to connect to "test_env"
            ENVIRONMENT EXPECTED TO BE A DOCKER FILE OR IMAGE REGISTERED WITH AZURE CONTAINER REGISTRY
        """
        try:
            if environment_name == "" : environment_name = "test_env"
            return Environment.get(workspace=self.workspace, name="test_env")
        except Exception as e:
            err = "AzureMLPlatofrm connect_environment: Error Connecting to Environment """ + environment_name + " ""\n"
            result = err + e
            return result 


    def test_workspace_connection(self):
        try:
            print ("")
            print ("AzureML SDK version: " + azureml.core.VERSION)
            print ("Subscription ID: " + self.workspace.subscription_id)
            print ("Resource Group: " +  self.workspace.resource_group)
            print ("Workspace: " + self.workspace.name)
            print ("Location: " + self.workspace.location)        
            print ("")
        except Exception as e:
            err = "AzureMLPlatform test_workspace_connection(): Error Connecting to Workspace\n"
            result = err + e
            return result


    def copy_container_files(self, filelist):
        """
            copies files in filelist to container_files_folder
            in preparation for a container run
        """
        import os
        import shutil
        
        os.makedirs(self.container_files_folder, exist_ok=True)
        for file in filelist:
            shutil.copy(file, self.container_files_folder)
        

    def run_training(self, filelist=[], comp_target='local', entrypoint='train.py'):
        """
            executes training run
            value compute targets are 'local', 'gkurpasi1' (compute instance), 'cpu-cluster', 'gpu-cluster'
        """

        self.copy_container_files(filelist)        

        run_config = RunConfiguration(framework='python')
        run_config.target = comp_target
        run_config.environment = self.environment

        script_run_config = ScriptRunConfig(
            source_directory=self.container_files_folder,
            script=entrypoint,
            run_config=run_config)

        print ("Experiment: "+ self.experiment.name)
        print ("Compute Target: " + comp_target)
        print ("Entry Point: " + entrypoint)
        print ("Container Files: " + self.container_files_folder)
        print ("Files " + str(filelist))
        run = self.experiment.submit(config=script_run_config)




