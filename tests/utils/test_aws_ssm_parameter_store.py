from unittest.mock import MagicMock
import utils.aws.ssm.parameter_store.aws_parameter_store as aws_parameter_store


def test_get_parameter_success_using_env(monkeypatch):
    monkeypatch.setenv('TEST_KEY', 'secret-value')
    fake_client = MagicMock()
    fake_client.get_parameter.return_value = {
        'Parameter': {'Value': 'secret-value'}
    }
    monkeypatch.setattr(
        'utils.aws.ssm.parameter_store.boto3.client',
        lambda *_: fake_client
    )
    ps = aws_parameter_store.ParameterStore()
    value = ps.get_parameter('TEST_KEY')
    assert value == 'secret-value'


def test_get_parameter_success_using_aws_ssm(monkeypatch):
    monkeypatch.setattr(aws_parameter_store, "ENV", "prod")
    fake_client = MagicMock()
    fake_client.get_parameter.return_value = {
        "Parameter": {"Value": "aws-secret"}
    }
    monkeypatch.setattr(aws_parameter_store.boto3, "client", lambda *_: fake_client)
    store = aws_parameter_store.ParameterStore()
    # clears lru_cache
    store.get_parameter.cache_clear()
    value = store.get_parameter("MY_KEY")
    assert value == "aws-secret"
    fake_client.get_parameter.assert_called_once_with(
        Name="MY_KEY",
        WithDecryption=True
    )