import os
from utils.aws.ssm.parameter_store.parameter_store_protocol import ParameterStoreProtocol


class LocalParameterStore(ParameterStoreProtocol):
    
    def get_parameter(self, name):
        value = os.getenv(name)
        if value is None:
            raise RuntimeError(f"Parameter {name} not found in environment variables.")
        return value