from config import ENV
from utils.aws.ssm.parameter_store.aws_parameter_store import AwsParameterStore
from utils.aws.ssm.parameter_store.local_parameter_store import LocalParameterStore


if ENV == 'local':
    parameter_store = LocalParameterStore() 
else:
    parameter_store = AwsParameterStore()  