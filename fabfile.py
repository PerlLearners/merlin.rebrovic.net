# -- coding: utf-8 --
import os
import sys
from fabric.api import local, task

CONFIGURATION = { "development": "site.yaml",
                  "production" : "prod.yaml" }

@task
def clean():
    """Remove locally generated website."""
    if os.path.exists("deploy"):
        local("rm -r deploy")

@task
def gen():
    """Generate a development version."""
    _generate_website("development")

def _generate_website(config_type):
    try:
        local("hyde gen -c " + CONFIGURATION[config_type])
    except KeyError:
        _print_and_exit(
            "Configuration type '" + config_type + "' is not supported.")

@task
def regen():
    """Remove an old and generate a new website."""
    clean()
    gen()

@task
def serve():
    """Serve the website locally."""
    local("hyde serve")

@task
def dev():
    """Clean, generate and serve."""
    regen()
    serve()

@task
def publish(dry_run=False):
    """Generate with production settings and upload."""
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
