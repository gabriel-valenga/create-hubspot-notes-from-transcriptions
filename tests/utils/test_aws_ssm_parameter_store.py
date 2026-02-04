from unittest.mock import MagicMock
import utils.aws.ssm.parameter_store.aws_parameter_store as aws_parameter_store
import utils.aws.ssm.parameter_store.local_parameter_store as local_parameter_store


def test_local_parameter_store_get_parameter_success(monkeypatch):
    monkeypatch.setenv('TEST_KEY', 'secret-value')
    ps = local_parameter_store.LocalParameterStore()
    value = ps.get_parameter('TEST_KEY')
    assert value == 'secret-value'


def test_aws_ssm_parameter_store_get_parameter_success(monkeypatch):
    fake_client = MagicMock()
    fake_client.get_parameter.return_value = {
        "Parameter": {"Value": "aws-secret"}
    }
    monkeypatch.setattr(aws_parameter_store.boto3, "client", lambda *_: fake_client)
    store = aws_parameter_store.AwsParameterStore()
    # clears lru_cache
    store.get_parameter.cache_clear()
    value = store.get_parameter("MY_KEY")
    assert value == "aws-secret"
    fake_client.get_parameter.assert_called_once_with(
        Name="MY_KEY",
        WithDecryption=True
    )