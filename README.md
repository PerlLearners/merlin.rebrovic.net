Personal website
================

It is a simple static website generated with [Hyde](http://hyde.github.com)
so feel free to look around.

Setup
-----

Make sure you have `pip` installed.

    pip install -r requirements.txt
    ln -s content/media/external /path/to/local/images
    fab dev

Before publishing put this in your `.bashrc`:

    export REMOTE_HOST_AND_PATH='user@server:/path/to/public/'

