awsudo
======

awsudo is a command-line tool that requests temporary credentials from `STS
<https://docs.aws.amazon.com/fr_fr/STS/latest/APIReference/Welcome.html>`_
to use an `IAM role
<https://docs.aws.amazon.com/fr_fr/IAM/latest/UserGuide/id_roles.html>`_.

If `MFA <https://aws.amazon.com/iam/details/mfa/>`_ is enabled,
you'll be prompted for the token code.


Usage
-----

First, you need to define your credentials in ``~/.aws/credentials``:

.. code-block:: ini

    [default]
    aws_access_key_id = AKIAIJFLKDSJFKLDSZ2Q
    aws_secret_access_key = Eoz3FDKJLSfdsJLKFDjflsFDjklJFDjfdFDjdOKa

Then define your profiles in ``~/.aws/config``:

.. code-block:: ini

    [profile administrator@development]
    role_arn = arn:aws:iam::00000000002:role/administrator
    source_profile = default
    mfa_serial = arn:aws:iam::00000000001:mfa/pmuller

    [profile administrator@staging]
    role_arn = arn:aws:iam::00000000003:role/administrator
    source_profile = default
    mfa_serial = arn:aws:iam::00000000001:mfa/pmuller

    [profile administrator@production]
    role_arn = arn:aws:iam::00000000004:role/administrator
    source_profile = default
    mfa_serial = arn:aws:iam::00000000001:mfa/pmuller


You can use awsudo either to get temporary credentials as ready-to-use
environment variables:

.. code-block:: console

    $ awsudo administrator@staging
    Enter MFA code:
    AWS_ACCESS_KEY_ID=ASIAJFSDLKJFS3VLA
    AWS_SECRET_ACCESS_KEY=UKvIegRLKJSFLKJFDSLKFJSDLKJ
    AWS_SESSION_TOKEN=FQoDYXdzEHIaDONIt4M0O10zRms0ac2.....


Or to directly run another executable with credentials defined in its
environment:

.. code-block:: console

    $ awsudo administrator@development aws iam list-groups
    Enter MFA code:
    {
        "Groups": [
            {
                "Path": "/",
                "CreateDate": "2016-08-01T02:13:52Z",
                "GroupId": "AGPAILKJFSDLFKJSDLFS2",
                "Arn": "arn:aws:iam::1234567890:group/administrators",
                "GroupName": "administrators"
            },
            {
                "Path": "/",
                "CreateDate": "2016-08-01T02:24:05Z",
                "GroupId": "AGPAFSJDKLJFDSLKJFST6",
                "Arn": "arn:aws:iam::1234567890:group/users",
                "GroupName": "users"
            }
        ]
    }


Development
-----------

Run tests:

.. code-block:: console

    $ make check
