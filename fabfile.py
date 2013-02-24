# -- coding: utf-8 --
import os
import sys
from fabric.api import local

CONFIGURATION = { "development": "site.yaml",
                  "production" : "prod.yaml" }
EXTERNAL_MEDIA_PATH = "content/media/external"

def init():
    """Create a symlink from an external media storage to Hyde's media
    folder for easier development and deployment.
    """
    if not os.path.exists(EXTERNAL_MEDIA_PATH):
        external_media_path = os.environ.get("EXTERNAL_MEDIA_PATH")
        if external_media_path is None:
            _print_and_exit("EXTERNAL_MEDIA_PATH environment variable not set.")
        local("ln -s {0} {1}".format(external_media_path,
            EXTERNAL_MEDIA_PATH))
    else:
        print("A link to external media already exists.")

def clean():
    if os.path.exists("deploy"):
        local("rm -r deploy")

def gen():
    _generate_website("development")

def _generate_website(config_type):
    try:
        local("hyde gen -c " + CONFIGURATION[config_type])
    except KeyError:
        _print_and_exit(
            "Configuration type '" + config_type + "' is not supported.")

def regen():
    clean()
    gen()

def serve():
    local("hyde serve")

def publish(dry_run=False):
    clean()
    _generate_website("production")
    _tweak_website()
    _remove_local_fonts()
    _upload(dry_run)

def _remove_local_fonts():
    """ Remove local fonts so they're not uploaded to the production. """
    local("rm -r deploy/media/fonts")

def _tweak_website():
    """ There are a few tweaks needed for the site and all sub-sites
    to work properly. """

    # The custom .htaccess is on the server taking care of subfolders. At
    # the moment the local .htaccess is only the subset of the full one.
    local("rm deploy/.htaccess")

    # The hosting throws internal server error for the PHP app (only wiki
    # at the moment) if the group has a write permission. This "corrects"
    # the permission locally so that rsync can transfer it properly.
    local("chmod g-w deploy")

def _upload(dry_run):
    remote_host_and_path = os.environ.get("REMOTE_HOST_AND_PATH")
    if remote_host_and_path is None:
        _print_and_exit("REMOTE_HOST_AND_PATH environment variable not set.")

    dry_run_flag = ""
    if dry_run:
        dry_run_flag = "n"
    local("rsync -avz{0} deploy/ {1}".format(dry_run_flag, remote_host_and_path))

def _print_and_exit(message):
    print(message)
    sys.exit(1)
