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

You can use awsudo either to get temporary credentials as ready-to-use
environment variables:

.. code-block:: console

    $ awsudo foo
    Enter MFA code:
    AWS_ACCESS_KEY_ID=ASIAJFSDLKJFS3VLA
    AWS_SECRET_ACCESS_KEY=UKvIegRLKJSFLKJFDSLKFJSDLKJ
    AWS_SECURITY_TOKEN=FQoDYXdzEHIaDONIt4M0O10zRms0ac2.....


Or to directly run another executable with credentials defined in its
environment:

.. code-block:: console

    $ awsudo foo aws iam list-groups
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
