"""awsudo - get temporary AWS privileges using roles."""
import sys
import os
import argparse

import boto3
from botocore.exceptions import ProfileNotFound, ClientError


VERSION = '0.1.1'
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


def main(argv=None):
    """CLI main entry point."""
    arguments = parse_arguments(argv)

    try:
        credentials = get_credentials(arguments.profile_name)
    except (ProfileNotFound, ClientError) as exception:
        sys.stderr.write('Fatal error: {}\n'.format(exception))
        sys.exit(-1)

    if arguments.executable:
        os.environ.update(credentials)
        os.execlp(
            arguments.executable, arguments.executable, *arguments.arguments)
    else:
        result = '\n'.join(
            '{}={}'.format(k, v) for k, v in sorted(credentials.items()))
        sys.stdout.write(result + '\n')


if __name__ == '__main__':
    main()
