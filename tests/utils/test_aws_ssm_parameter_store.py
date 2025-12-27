from unittest.mock import MagicMock
from utils.aws.ssm.parameter_store import ParameterStore


def test_get_parameter_success(monkeypatch):
    monkeypatch.setenv('TEST_KEY', 'secret-value')
    fake_client = MagicMock()
    fake_client.get_parameter.return_value = {
        'Parameter': {'Value': 'secret-value'}
    }
    monkeypatch.setattr(
        'utils.aws.ssm.parameter_store.boto3.client',
        lambda *_: fake_client
    )
    ps = ParameterStore()
    value = ps.get_parameter('TEST_KEY')
    assert value == 'secret-value'