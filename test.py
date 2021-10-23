from os import name
from azureml.core import compute_target, script_run_config
from azureml.core import compute
from azureml.core import conda_dependencies
from interfaces import adapters_azure




import azureml.core
from azureml.core import Workspace
from azureml.core import Experiment
from azureml.core import Environment
from azureml.core.compute import ComputeTarget, AmlCompute
from azureml.core.runconfig import RunConfiguration
from azureml.core import ScriptRunConfig
from azureml.core.conda_dependencies import CondaDependencies



print("SDK version:", azureml.core.VERSION)
ws = Workspace.from_config()
print(ws.name, ws.resource_group, ws.location, ws.subscription_id, sep='\n')

experiment_name = 'Container_Testing'
experiment = Experiment(workspace=ws, name=experiment_name)



comp_target = ComputeTarget(workspace=ws, name='gpu-cluster')
# compute_target = ComputeTarget(workspace=ws, name='gkurpasi1')
# compute_target = 'local'



# myenv = Environment.from_conda_specification("envy.yml", "")
# myenv = Environment.from_existing_conda_environment(name="myenv",conda_environment_name="word_sense_induction")
# azureml_pip_packages = [
#     'azureml-defaults', 'azureml-telemetry', 'azureml-interpret'
# ]
# run_config.environment.python.conda_dependencies = CondaDependencies.create(pip_packages=azureml_pip_packages)


myenv = Environment.get(workspace=ws, name="test_env")
# clone = myenv.clone("word_sense_induction_env")


# conda_dep = CondaDependencies()
# conda_dep.add_conda_package("nltk")
# clone.python.conda_dependencies = conda_dep

myenv.save_to_directory(path="env", overwrite=True)



run_config = RunConfiguration(framework='python')
run_config.target = comp_target
run_config.environment = myenv




script_run_config = ScriptRunConfig(
    source_directory="./container_files",
    script='entrypoint.py',
    run_config=run_config)




run = experiment.submit(config=script_run_config)
# run









print("Done Sir Done")