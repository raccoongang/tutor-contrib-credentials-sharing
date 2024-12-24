from credentials.settings.production import *

{% include "credentials-sharing/apps/credentials-sharing/settings/partials/common.py" %}
BADGES_CONFIG['credly']['USE_SANDBOX'] = True
{{ patch("credentials-settings-production") }}
