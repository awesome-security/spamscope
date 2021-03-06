"""
Copyright 2016 Fedele Mantuano (https://twitter.com/fedelemantuano)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from __future__ import absolute_import, print_function, unicode_literals
from bolts.abstracts import AbstractUrlsHandlerBolt


class UrlsHandlerAttachments(AbstractUrlsHandlerBolt):
    outputs = ['sha256_random', 'with_urls', 'urls']

    def initialize(self, stormconf, context):
        super(UrlsHandlerAttachments, self).initialize(stormconf, context)

    def process(self, tup):
        sha256_mail_random = tup.values[0]
        attachments = tup.values[2]
        with_urls = False
        urls = None
        all_contents = u""

        # Get all contents for all attachments and files archived
        for i in attachments:
            try:
                if i.get("is_archive"):
                    for j in i.get("files"):
                        all_contents += \
                            j["payload"].decode('base64') + u"\n"
                else:
                    all_contents += \
                        i["payload"].decode('base64') + u"\n"

            except UnicodeDecodeError:
                continue

            except KeyError:
                continue

        with_urls, urls = self._extract_urls(all_contents, False)

        self.emit([sha256_mail_random, with_urls, urls])
