from interfaces.adapters_azureml import *

from azureml.core import Workspace

import azureml.core
print(azureml.core.VERSION)

# ws = Workspace.from_config()


azureml_client = AzureMLPlatform()
azureml_client.display_connection()


# from bert_examples import *


# simple_model()


