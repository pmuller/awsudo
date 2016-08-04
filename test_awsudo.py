import sys
import os
import errno

import pytest
from mock import Mock
import boto3
from botocore.exceptions import ProfileNotFound, ClientError

import awsudo


CREDENTIALS_FILE_CONTENT = """\
[default]
aws_access_key_id = AKIAJ9FS2LJKFJSDFZ2Q
aws_secret_access_key = EozhjKLASFKLHJSDFjklSFDLKJDFSljkhLSDFOKa
"""

CONFIG_FILE_CONTENT = """\
[profile foo]
role_arn = arn:aws:iam:1234567890:role/foo
source_profile = default

[profile bar]
source_profile = default
role_arn = arn:aws:iam:1234567890:role/bar
mfa_serial = arn:aws:iam::1234567890:mfa/foobar
"""

STDOUT_TEMPLATE = """\
AWS_ACCESS_KEY_ID={access_key}
AWS_SECRET_ACCESS_KEY={secret_key}
AWS_SECURITY_TOKEN={token}
"""


def setup_test(monkeypatch, tmpdir):
    config = tmpdir.join('config')
    config.write(CONFIG_FILE_CONTENT)
    monkeypatch.setenv('AWS_CONFIG_FILE', str(config))
    credentials = {
        'access_key': 'aaa',
        'secret_key': 'bbb',
        'token': 'ccc',
    }
    get_credentials = Mock(return_value=Mock(**credentials))
    session_cls = Mock(return_value=Mock(get_credentials=get_credentials))
    monkeypatch.setattr(boto3, 'Session', session_cls)

    return session_cls, get_credentials, credentials


def test_stdout(monkeypatch, tmpdir, capsys):
    session_cls, get_credentials, credentials = setup_test(monkeypatch, tmpdir)

    awsudo.main(['foo'])

    session_cls.assert_called_once_with(profile_name='foo')
    get_credentials.assert_called_once_with()
    assert capsys.readouterr()[0] == STDOUT_TEMPLATE.format(**credentials)


def test_exec(monkeypatch, tmpdir):
    session_cls, get_credentials, credentials = setup_test(monkeypatch, tmpdir)
    environ_update = Mock()
    monkeypatch.setattr(os.environ, 'update', environ_update)
    execlp = Mock()
    monkeypatch.setattr(os, 'execlp', execlp)

    awsudo.main(['bar', 'executable', 'arg1', 'arg2'])

    session_cls.assert_called_once_with(profile_name='bar')
    get_credentials.assert_called_once_with()
    environ_update.assert_called_once_with({
        'AWS_ACCESS_KEY_ID': credentials['access_key'],
        'AWS_SECRET_ACCESS_KEY': credentials['secret_key'],
        'AWS_SECURITY_TOKEN': credentials['token'],
    })
    execlp.assert_called_once_with('executable', 'executable', 'arg1', 'arg2')


@pytest.mark.parametrize('exception, exc_args, exc_kwargs', (
    (ProfileNotFound, tuple(), dict(profile='foo')),
    (ClientError, ({'Error': {}}, 'foo'), {}),
))
def test_boto_errors(exception, exc_args, exc_kwargs, monkeypatch):
    def raise_exception(*args):
        raise exception(*exc_args, **exc_kwargs)
    monkeypatch.setattr(
        awsudo, 'get_credentials', Mock(side_effect=raise_exception))

    with pytest.raises(SystemExit):
        awsudo.main(['foo'])


def test_fatal_error(monkeypatch, capsys):
    exit = Mock()
    monkeypatch.setattr(sys, 'exit', exit)

    awsudo.fatal_error('foo', 42)

    assert capsys.readouterr()[1] == 'Fatal error: foo\n'
    exit.assert_called_once_with(42)


def test_run_enoent_error(monkeypatch):
    fatal_error = Mock()
    monkeypatch.setattr(awsudo, 'fatal_error', fatal_error)

    def raise_oserror_enoent(*args):
        raise OSError(errno.ENOENT, os.strerror(errno.ENOENT))
    execlp = Mock(side_effect=raise_oserror_enoent)
    monkeypatch.setattr(os, 'execlp', execlp)

    awsudo.run({}, 'foobarbaz', [])

    fatal_error.assert_called_once_with('No such file or directory: foobarbaz')
