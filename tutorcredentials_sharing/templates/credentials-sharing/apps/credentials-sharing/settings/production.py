from credentials.settings.production import *

{% include "credentials-sharing/apps/credentials-sharing/settings/partials/common.py" %}

{{ patch("credentials-settings-production") }}
