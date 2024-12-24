from __future__ import annotations

import os
import typing as t
from glob import glob

import importlib_resources
from tutor import hooks as tutor_hooks
from tutor.__about__ import __version_suffix__

from .__about__ import __version__

# Handle version suffix in main mode, just like tutor core
if __version_suffix__:
    __version__ += "-" + __version_suffix__

# Event Bus configuration.
#
# Responsibilities:
#
# - keeps configurations for different event bus backends:
#     - Redis (default)
#     - Kafka (TBD)
# - enables event bus on the supported Open edX services:
#     - LMS
#     - CMS
#     - Credentials
#     - Discovery
# - installs appropriate broker to each supported service
# - adds consuming configuration to each supported service
# - adds producing configuration to each supported service
#
# - (optional) adds Redis Insight service for development observability
# - (optional) installs event-bus-conductor to each supported service

EVENT_BUS_BACKEND_REDIS = "redis"
EVENT_BUS_BACKEND_KAFKA = "kafka"

########################################
# CONFIGURATION
########################################

backends: t.Dict[str, t.Dict[str, t.Any]] = {
    EVENT_BUS_BACKEND_REDIS: {
        "REDIS_CONNECTION_URL": "redis://@redis:6379/",
        "PRODUCER": "edx_event_bus_redis.create_producer",
        "CONSUMER": "edx_event_bus_redis.RedisEventConsumer",
        "RUN_REDIS_INSIGHT": True,
    },
    EVENT_BUS_BACKEND_KAFKA: {},
}

# TODO: define consumers config for services
consumers: t.Dict[str, t.Dict[str, t.Any]] = {
    "lms": {
        "topic-a": 2,  # group_id=lms.topic-a; consumers: [lms.topic-a.1, lms.topic-a.2]
        "topic-b": 1,
    },
    "credentials": {},
    "discovery": {},
}

# TODO: define producer config for services
producers: t.Dict[str, t.Dict[str, t.Any]] = {
    "lms": {},
    "credentials": {},
    "discovery": {},
}

config: t.Dict[str, t.Dict[str, t.Any]] = {
    "defaults": {
        "VERSION": __version__,
        "BACKEND": EVENT_BUS_BACKEND_REDIS,
        "BACKEND_REDIS": EVENT_BUS_BACKEND_REDIS,
        "BACKEND_KAFKA": EVENT_BUS_BACKEND_KAFKA,
        "LMS_CONSUMER_TOPIC": "learning-badges-lifecycle",  # FIXME de-hardcode
        "LMS_CONSUMER_GROUP": "lms.learning-badges-lifecycle",  # FIXME
        "LMS_CONSUMER_NAME": "lms.learning-badges-lifecycle.1",  # FIXME
        "CMS_CONSUMER_TOPIC": "learning-badges-lifecycle",  # FIXME
        "CMS_CONSUMER_GROUP": "cms.learning-badges-lifecycle",  # FIXME
        "CMS_CONSUMER_NAME": "cms.learning-badges-lifecycle.1",  # FIXME
        "CREDENTIALS_CONSUMER_TOPIC": "learning-badges-lifecycle",  # FIXME
        "CREDENTIALS_CONSUMER_GROUP": "credentials.learning-badges-lifecycle",  # FIXME
        "CREDENTIALS_CONSUMER_NAME": "credentials.learning-badges-lifecycle.1",  # FIXME
        "CREDENTIALS_CERTIFICATES_CONSUMER_TOPIC": "learning-certificate-lifecycle",
        "CREDENTIALS_CERTIFICATES_CONSUMER_GROUP": "credentials.learning-certificate-lifecycle",
        "CREDENTIALS_CERTIFICATES_CONSUMER_NAME": "credentials.learning-certificate-lifecycle.1",
        "DEBUG": False,
    },
    "unique": {
        "TOPIC_PREFIX": "{{ 3|random_string }}",
    },
    "overrides": {},
}

# pick active backend configuration:
current_backend = config["defaults"]["BACKEND"]
config["defaults"].update({k: v for k, v in backends.get(current_backend, {}).items()})

tutor_hooks.Filters.CONFIG_DEFAULTS.add_items(
    [(f"EVENT_BUS_{key}", value) for key, value in config.get("defaults", {}).items()]
)
tutor_hooks.Filters.CONFIG_UNIQUE.add_items(
    [(f"EVENT_BUS_{key}", value) for key, value in config.get("unique", {}).items()]
)
tutor_hooks.Filters.CONFIG_OVERRIDES.add_items(
    list(config.get("overrides", {}).items())
)

tutor_hooks.Filters.ENV_PATCHES.add_items(
    [
        (
            "openedx-common-settings",
            """EVENT_BUS_PRODUCER_CONFIG.update({\
'org.openedx.learning.course.passing.status.updated.v1': {'learning-badges-lifecycle': {'event_key_field': 'course_passing_status.course.course_key', 'enabled': True}},
'org.openedx.learning.ccx.course.passing.status.updated.v1': {'learning-badges-lifecycle': {'event_key_field': 'course_passing_status.course.ccx_course_key', 'enabled': True}}})""",
        ),
    ]
)
# TODO: validate RUN_REDIS is True if BACKEND == EVENT_BUS_BACKEND_REDIS

########################################
# Badges
# - Turn on badges feature on LMS side
########################################
tutor_hooks.Filters.ENV_PATCHES.add_items(
    [
        ("openedx-common-settings", "FEATURES['BADGES_ENABLED'] = True"),
    ]
)


########################################
# Verifiable credentials
# - Turn on Verifiable credentials on credentials side
# - Turn on Verifiable credentials on learner-record MFE side
########################################
tutor_hooks.Filters.ENV_PATCHES.add_items(
    [
        (
            "mfe-lms-common-settings",
            """
MFE_CONFIG_OVERRIDES = {
    'learner-record': {
        'ENABLE_VERIFIABLE_CREDENTIALS': 'true'
    }
}
# """,
        )
    ]
)

########################################
# TEMPLATE RENDERING
########################################

tutor_hooks.Filters.ENV_TEMPLATE_ROOTS.add_item(
    # Root path for template files, relative to the project root.
    str(importlib_resources.files("tutorcredentials_sharing") / "templates")
)


########################################
# PATCH LOADING
########################################

for path in glob(
    str(importlib_resources.files("tutorcredentials_sharing") / "patches" / "*")
):
    with open(path, encoding="utf-8") as patch_file:
        tutor_hooks.Filters.ENV_PATCHES.add_item(
            (os.path.basename(path), patch_file.read())
        )
