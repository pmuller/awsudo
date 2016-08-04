"""awsudo - get temporary AWS privileges using IAM roles."""
import sys
import os
import argparse

import boto3
from botocore.exceptions import ProfileNotFound, ClientError


VERSION = '0.1.2'
CLI_DESCRIPTION = """\
Get temporary credentials for a given IAM role.

If an executable is given, run it with proper credentials in its environment.
If not, show the credentials environment variables.

"""


def parse_arguments(argv):
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(description=CLI_DESCRIPTION)

    parser.add_argument('profile_name', help='Name of the AWS profile.')
    parser.add_argument('executable', nargs='?',
                        help='Executable to run with credentials.')
    parser.add_argument('arguments', metavar='argument', nargs='*',
                        help='Executable arguments.')
    parser.add_argument('-V', '--version', action='version', version=VERSION,
                        help='Show version.')

    return parser.parse_args(argv)


def get_credentials(profile_name):
    """Retrieve credentials from AWS."""
    session = boto3.Session(profile_name=profile_name)
    credentials = session.get_credentials()

    return {
        'AWS_ACCESS_KEY_ID': credentials.access_key,
        'AWS_SECRET_ACCESS_KEY': credentials.secret_key,
        'AWS_SECURITY_TOKEN': credentials.token,
    }


def fatal_error(error, code=-1):
    """Show an error message then exit with an error code."""
    sys.stderr.write('Fatal error: {}\n'.format(error))
    sys.exit(code)


def run(credentials, executable, arguments):
    """Run an executable, passing it temporary credentials."""
    os.environ.update(credentials)

    try:
        os.execlp(executable, executable, *arguments)
    except OSError as error:
        fatal_error('{}: {}'.format(os.strerror(error.errno), executable))


def show_credentials(credentials):
    """Show temporary credentials as environment variables."""
    result = '\n'.join(
        '{}={}'.format(k, v) for k, v in sorted(credentials.items()))
    sys.stdout.write(result + '\n')


def main(argv=None):
    """CLI main entry point."""
    arguments = parse_arguments(argv)

    try:
        credentials = get_credentials(arguments.profile_name)
    except (ProfileNotFound, ClientError) as exception:
        fatal_error(exception)

    if arguments.executable:
        run(credentials, arguments.executable, arguments.arguments)
    else:
        show_credentials(credentials)


if __name__ == '__main__':  # pragma: no cover
    main()
