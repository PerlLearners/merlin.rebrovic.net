import hashlib
import os

from hyde.plugin import Plugin

class HashPlugin(Plugin):
    """
    Hasher plugin for hyde. Adds the ability to calculate hash
    values of source files and add them to metadata. Values
    are calculated at the beginning of the process so they can
    be used by a template, but there is the risk the template
    could change the file during generation.

    Configuration example
    ---------------------
    #yaml

    hasher:
        # A list of relative paths to files
        - path/to/file.css
        - media/js/init.js
    """

    def __init__(self, site):
        super(HashPlugin, self).__init__(site)

    def begin_site(self):
        config = self.site.config
        if not hasattr(config, 'hasher'):
            return

        for resource_path in config.hasher:
            res = self.site.content.resource_from_relative_path(resource_path)
            if res is not None:
                path = os.path.join(self.site.content.path, resource_path)
                res.meta.content_hash = \
                    hashlib.md5(open(path, 'rb').read()).hexdigest()[0:6]
