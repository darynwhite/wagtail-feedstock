#!/usr/bin/env python

import argparse
import os
import shutil
import sys
import warnings

from django.core.management import execute_from_command_line

os.environ["DJANGO_SETTINGS_MODULE"] = "wagtail.test.settings"


def make_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--deprecation",
        choices=["all", "pending", "imminent", "none"],
        default="imminent",
    )
    parser.add_argument("--postgres", action="store_true")
    parser.add_argument("--elasticsearch5", action="store_true")
    parser.add_argument("--elasticsearch6", action="store_true")
    parser.add_argument("--elasticsearch7", action="store_true")
    parser.add_argument("--emailuser", action="store_true")
    parser.add_argument("--disabletimezone", action="store_true")
    parser.add_argument("--bench", action="store_true")
    return parser


def parse_args(args=None):
    return make_parser().parse_known_args(args)


def runtests():
    args, rest = parse_args()

    only_wagtail = r"^wagtail(\.|$)"
    if args.deprecation == "all":
        # Show all deprecation warnings from all packages
        warnings.simplefilter("default", DeprecationWarning)
        warnings.simplefilter("default", PendingDeprecationWarning)
    elif args.deprecation == "pending":
        # Show all deprecation warnings from wagtail
        warnings.filterwarnings(
            "default", category=DeprecationWarning, module=only_wagtail
        )
        warnings.filterwarnings(
            "default", category=PendingDeprecationWarning, module=only_wagtail
        )
    elif args.deprecation == "imminent":
        # Show only imminent deprecation warnings from wagtail
        warnings.filterwarnings(
            "default", category=DeprecationWarning, module=only_wagtail
        )
    elif args.deprecation == "none":
        # Deprecation warnings are ignored by default
        pass

    if args.postgres:
        os.environ["DATABASE_ENGINE"] = "django.db.backends.postgresql"

    if args.elasticsearch5:
        os.environ.setdefault("ELASTICSEARCH_URL", "http://localhost:9200")
        os.environ.setdefault("ELASTICSEARCH_VERSION", "5")
    elif args.elasticsearch6:
        os.environ.setdefault("ELASTICSEARCH_URL", "http://localhost:9200")
        os.environ.setdefault("ELASTICSEARCH_VERSION", "6")
    elif args.elasticsearch7:
        os.environ.setdefault("ELASTICSEARCH_URL", "http://localhost:9200")
        os.environ.setdefault("ELASTICSEARCH_VERSION", "7")

    elif "ELASTICSEARCH_URL" in os.environ:
        # forcibly delete the ELASTICSEARCH_URL setting to skip those tests
        del os.environ["ELASTICSEARCH_URL"]

    if args.emailuser:
        os.environ["USE_EMAIL_USER_MODEL"] = "1"

    if args.disabletimezone:
        os.environ["DISABLE_TIMEZONE"] = "1"

    if args.bench:
        benchmarks = ["wagtail.admin.tests.benches"]

        argv = [sys.argv[0], "test", "-v2"] + benchmarks + rest
    else:
        argv = [sys.argv[0], "test"] + rest

    try:
        execute_from_command_line(argv)
    finally:
        from wagtail.test.settings import MEDIA_ROOT, STATIC_ROOT

        shutil.rmtree(STATIC_ROOT, ignore_errors=True)
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)


if __name__ == "__main__":
    runtests()

# import django
# from django.conf import settings

# settings.configure(
#     INSTALLED_APPS=["wagtail", "django.contrib.contenttypes", "django.contrib.auth"]
# )
# django.setup()

# import wagtail
# import wagtail.snippets
# import wagtail.snippets.views
# import wagtail.core
# import wagtail.core.blocks
# import wagtail.core.models
# import wagtail.core.permission_policies
# import wagtail.core.rich_text
# import wagtail.core.templatetags
# import wagtail.bin
# import wagtail.images
# import wagtail.images.templatetags
# import wagtail.images.migrations
# import wagtail.images.tests
# import wagtail.images.api
# import wagtail.images.api.admin
# import wagtail.images.api.v2
# import wagtail.images.views
# import wagtail.test
# import wagtail.test.snippets
# import wagtail.test.snippets.migrations
# import wagtail.test.customuser
# import wagtail.test.customuser.migrations
# import wagtail.test.testapp
# import wagtail.test.testapp.migrations
# import wagtail.test.modeladmintest
# import wagtail.test.modeladmintest.migrations
# import wagtail.test.routablepage
# import wagtail.test.routablepage.migrations
# import wagtail.test.utils
# import wagtail.test.demosite
# import wagtail.test.demosite.migrations
# import wagtail.test.search
# import wagtail.test.search.migrations
# import wagtail.admin
# import wagtail.admin.templatetags
# import wagtail.admin.migrations
# import wagtail.admin.viewsets
# import wagtail.admin.tests
# import wagtail.admin.tests.api
# import wagtail.admin.urls
# import wagtail.admin.api
# import wagtail.admin.rich_text
# import wagtail.admin.rich_text.editors
# import wagtail.admin.rich_text.editors.draftail
# import wagtail.admin.rich_text.converters
# import wagtail.admin.views
# import wagtail.utils
# import wagtail.contrib
# import wagtail.contrib.settings
# import wagtail.contrib.settings.templatetags
# import wagtail.contrib.settings.tests
# import wagtail.contrib.frontend_cache
# import wagtail.contrib.routable_page
# import wagtail.contrib.routable_page.templatetags
# import wagtail.contrib.forms
# import wagtail.contrib.forms.migrations
# import wagtail.contrib.forms.tests
# import wagtail.contrib.search_promotions
# import wagtail.contrib.search_promotions.templatetags
# import wagtail.contrib.search_promotions.migrations
# import wagtail.contrib.table_block
# import wagtail.contrib.styleguide
# import wagtail.contrib.redirects
# import wagtail.contrib.redirects.migrations
# import wagtail.contrib.modeladmin
# import wagtail.contrib.modeladmin.templatetags
# import wagtail.contrib.modeladmin.tests
# import wagtail.contrib.modeladmin.helpers
# import wagtail.contrib.sitemaps
# import wagtail.search
# import wagtail.search.migrations
# import wagtail.search.backends
# import wagtail.search.tests
# import wagtail.search.management
# import wagtail.search.management.commands
# import wagtail.search.urls
# import wagtail.search.views
# import wagtail.sites
# import wagtail.project_template.home
# import wagtail.project_template.home.migrations
# import wagtail.project_template.project_name
# import wagtail.project_template.project_name.settings
# import wagtail.project_template.search
# import wagtail.users
# import wagtail.users.templatetags
# import wagtail.users.migrations
# import wagtail.users.urls
# import wagtail.users.views
# import wagtail.api
# import wagtail.api.v2
# import wagtail.api.v2.tests
# import wagtail.documents
# import wagtail.documents.migrations
# import wagtail.documents.tests
# import wagtail.documents.api
# import wagtail.documents.api.admin
# import wagtail.documents.api.v2
# import wagtail.documents.views
# import wagtail.embeds
# import wagtail.embeds.templatetags
# import wagtail.embeds.migrations
# import wagtail.embeds.finders
# import wagtail.embeds.views
