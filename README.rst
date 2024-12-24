Credentials Sharing plugin for `Tutor <https://docs.tutor.edly.io>`__
##################################################################

Tutor plugin that adds and configuring features for sharing to different “providers”:
  - `Verifiable Credentials <https://edx-credentials.readthedocs.io/en/latest/verifiable_credentials/overview.html#>`__ with different credential stores that support standards like VC1.1, OBv3 such as `LCWallet <https://lcw.app/>`__ for example.
     - program certificate
     - course certificate
  - Badges:
     - `Credly <https://info.credly.com/>`__
     - `Accredible <https://www.accredible.com/>`__

The plugin also configures event buse between Credentials and LMS/CMS services.

Installation
************

This tutor plugin interacts with the Credentials service, respectively,
one of its dependencies is the `tutor-credentials <https://github.com/overhangio/tutor-credentials/tree/release>`__ plugin, which must also be installed

.. code-block:: bash

    pip install tutor-credentials
    pip install git+https://github.com/raccoongang/tutor-contrib-credentials-sharing

Usage
*****

.. code-block:: bash

    tutor plugins enable tutor-credentials
    tutor plugins enable credentials-sharing
    tutor local start credentials-eventbus-consumer -d
    tutor local start credentials-certificates-eventbus-consumer -d
    tutor local start lms-eventbus-consumer -d
    tutor local start cms-eventbus-consumer -d

    tutor local start credentials -d

License
*******

This software is licensed under the terms of the AGPLv3.
