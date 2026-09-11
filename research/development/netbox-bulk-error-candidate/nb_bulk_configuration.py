"""Upstream test settings with a dedicated disposable database."""
from copy import deepcopy
import os
from netbox.configuration_testing import *  # noqa: F403

DATABASES = deepcopy(DATABASES)  # noqa: F405
DATABASES["default"]["NAME"] = "netbox_nb_bulk_reproduction"
DATABASES["default"]["HOST"] = os.environ.get("NB_BULK_DB_HOST", "localhost")
REDIS = deepcopy(REDIS)  # noqa: F405
for _service in REDIS.values():
    _service["HOST"] = os.environ.get("NB_BULK_REDIS_HOST", "localhost")
