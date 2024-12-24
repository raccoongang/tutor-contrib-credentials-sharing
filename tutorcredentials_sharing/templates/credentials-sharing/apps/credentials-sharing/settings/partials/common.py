########################################
# Badges
########################################
BADGES_ENABLED = True

########################################
# Verifiable credentials
########################################
ENABLE_VERIFIABLE_CREDENTIALS = True

########################################
# Event Bus
########################################
EVENT_BUS_BACKEND = "{{ EVENT_BUS_BACKEND }}"
EVENT_BUS_TOPIC_PREFIX = "{{ EVENT_BUS_TOPIC_PREFIX }}"
{% if EVENT_BUS_BACKEND == EVENT_BUS_BACKEND_REDIS %}
EVENT_BUS_REDIS_CONNECTION_URL = "{{ EVENT_BUS_REDIS_CONNECTION_URL }}"
EVENT_BUS_PRODUCER = "{{ EVENT_BUS_PRODUCER }}"
EVENT_BUS_CONSUMER = "{{ EVENT_BUS_CONSUMER }}"
{% endif %}
{% if EVENT_BUS_BACKEND == EVENT_BUS_BACKEND_KAFKA %}
EVENT_BUS_KAFKA_CONNECTION_URL = "EVENT_BUS_TBD"
EVENT_BUS_PRODUCER = "EVENT_BUS_TBD"
EVENT_BUS_CONSUMER = "EVENT_BUS_TBD"

{{ patch("credentials-settings-common") }}
{% endif %}########################################