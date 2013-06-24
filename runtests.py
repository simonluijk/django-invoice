#!/usr/bin/env python
import sys
from django.conf import settings

if not settings.configured:
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        INSTALLED_APPS=(
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'addressbook',
            'invoice',
        ),
        SITE_ID=1,
        SITE_NAME='Test site name',
        SECRET_KEY='this-is-just-for-tests-so-not-that-secret',
    )

from django.test.utils import get_runner


def runtests():
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=1, interactive=True, failfast=False)
    failures = test_runner.run_tests(['invoice', ])
    sys.exit(failures)


if __name__ == '__main__':
    runtests()
