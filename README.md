Personal website
================

It is a simple static website generated with [Hyde][hyde] so feel free
to look around.

Setup
-----

Make sure you have `pip` installed.

    pip install -r requirements.txt
    ln -s /path/to/local/images content/media/external
    fab dev

Before publishing put this in your `.bashrc`:

    export REMOTE_HOST_AND_PATH='user@server:/path/to/public/'

License
-------

Unless stated differently, the content (all HTML, Markdown, and image
files) is licensed as [CC BY-NC-ND 4.0][CC] while the remaining (CSS,
JS, layout) is licensed as [MIT][MIT]. Other software not written by me
and used on this site has its own respective license.

[hyde]: http://hyde.github.com
[CC]: https://creativecommons.org/licenses/by-nc-nd/4.0/
[MIT]: http://opensource.org/licenses/MIT
