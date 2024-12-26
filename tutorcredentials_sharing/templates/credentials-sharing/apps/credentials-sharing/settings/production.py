from credentials.settings.production import *

{% include "credentials-sharing/apps/credentials-sharing/settings/partials/common.py" %}

BADGES_CONFIG['credly']['USE_SANDBOX'] = CONFIG_FILE.get('USE_CREDLY_SANDBOX', False)
BADGES_CONFIG['accredible']['USE_SANDBOX'] = CONFIG_FILE.get('USE_ACCREDIBLE_SANDBOX', False)

{{ patch("credentials-settings-production") }}
