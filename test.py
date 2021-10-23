from azureml.core import compute_target, script_run_config
from interfaces import adapters_azure




import azureml.core
from azureml.core import Workspace
from azureml.core import Experiment
from azureml.core.compute import ComputeTarget, AmlCompute
from azureml.core.runconfig import RunConfiguration
from azureml.core import ScriptRunConfig
from azureml.core.conda_dependencies import CondaDependencies



print("SDK version:", azureml.core.VERSION)
ws = Workspace.from_config()
print(ws.name, ws.resource_group, ws.location, ws.subscription_id, sep='\n')

experiment_name = 'Container_Testing'
experiment = Experiment(workspace=ws, name=experiment_name)
# compute_target = ComputeTarget(workspace=ws, name='gpu-cluster')
compute_target = ComputeTarget(workspace=ws, name='gkurpasi1')


run_config = RunConfiguration(framework='python')
run_config.target = compute_target.name

script_run_config = ScriptRunConfig(
    source_directory="./container_files",
    script='entrypoint.py',
    run_config=run_config)


azureml_pip_packages = [
    'azureml-defaults', 'azureml-telemetry', 'azureml-interpret'
]
run_config.environment.python.conda_dependencies = CondaDependencies.create(pip_packages=azureml_pip_packages)



run = experiment.submit(config=script_run_config)
run









print("Done Sir Done")