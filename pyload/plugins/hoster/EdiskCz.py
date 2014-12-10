# -*- coding: utf-8 -*-

import re

from pyload.plugins.internal.SimpleHoster import SimpleHoster, create_getInfo


class EdiskCz(SimpleHoster):
    __name    = "EdiskCz"
    __type    = "hoster"
    __version = "0.22"

    __pattern = r'http://(?:www\.)?edisk\.(cz|sk|eu)/(stahni|sk/stahni|en/download)/.*'

    __description = """Edisk.cz hoster plugin"""
    __license     = "GPLv3"
    __authors     = [("zoidberg", "zoidberg@mujmail.cz")]


    INFO_PATTERN = r'<span class="fl" title="(?P<N>[^"]+)">\s*.*?\((?P<S>[\d.,]+) (?P<U>[\w^_]+)\)</h1></span>'
    OFFLINE_PATTERN = r'<h3>This file does not exist due to one of the following:</h3><ul><li>'

    ACTION_PATTERN = r'/en/download/(\d+/.*\.html)'
    LINK_PATTERN = r'http://.*edisk\.cz.*\.html'


    def setup(self):
        self.multiDL = False


    def process(self, pyfile):
        url = re.sub("/(stahni|sk/stahni)/", "/en/download/", pyfile.url)

        self.logDebug("URL:" + url)

        m = re.search(self.ACTION_PATTERN, url)
        if m is None:
            self.error(_("ACTION_PATTERN not found"))
        action = m.group(1)

        self.html = self.load(url, decode=True)
        self.getFileInfo()

        self.html = self.load(re.sub("/en/download/", "/en/download-slow/", url))

        url = self.load(re.sub("/en/download/", "/x-download/", url), post={
            "action": action
        })

        if not re.match(self.LINK_PATTERN, url):
            self.fail(_("Unexpected server response"))

        self.download(url)


getInfo = create_getInfo(EdiskCz)