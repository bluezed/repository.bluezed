# -*- coding: utf-8 -*-
#
# FTV Guide
# Copyright (C) 2015 Thomas Geppert [bluezed]
# bluezed.apps@gmail.com
#
#      Modified for EPG-Direct (08/2016 onwards)
#      by Thomas Geppert [bluezed] - bluezed.apps@gmail.com
#
# This Program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2, or (at your option)
#  any later version.
#
#  This Program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this Program; see the file LICENSE.txt.  If not, write to
#  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
#  http://www.gnu.org/copyleft/gpl.html
#
import xbmc
import xbmcvfs
import os
import urllib2
import datetime
import zlib
from strings import ADDON


class FileFetcher(object):
    INTERVAL_ALWAYS = 0
    INTERVAL_12 = 1
    INTERVAL_24 = 2
    INTERVAL_48 = 3

    FETCH_ERROR = -1
    FETCH_NOT_NEEDED = 0
    FETCH_OK = 1

    TYPE_DEFAULT = 1
    TYPE_REMOTE = 2

    basePath = xbmc.translatePath(ADDON.getAddonInfo('profile'))
    filePath = ''
    fileUrl = ''
    addon = None
    fileType = TYPE_DEFAULT

    def __init__(self, fileName, addon):
        self.addon = addon

        if fileName.startswith("http://") or fileName.startswith("sftp://") or fileName.startswith("ftp://") or \
                fileName.startswith("https://") or fileName.startswith("ftps://") or fileName.startswith("smb://") or \
                fileName.startswith("nfs://"):
            self.fileType = self.TYPE_REMOTE
            self.fileUrl = fileName
            self.filePath = os.path.join(self.basePath, fileName.split('/')[-1])
        else:
            self.fileType = self.TYPE_DEFAULT
            self.fileUrl = fileName
            self.filePath = os.path.join(self.basePath, fileName)

        # make sure the folder is actually there already!
        if not os.path.exists(self.basePath):
            os.makedirs(self.basePath)

    def fetchFile(self):
        ret_val = self.FETCH_NOT_NEEDED
        fetch = False
        if not os.path.exists(self.filePath):  # always fetch if file doesn't exist!
            fetch = True
        else:
            interval = int(self.addon.getSetting('sd.interval'))
            if interval != self.INTERVAL_ALWAYS:
                mod_time = datetime.datetime.fromtimestamp(os.path.getmtime(self.filePath))
                td = datetime.datetime.now() - mod_time
                # need to do it this way cause Android doesn't support .total_seconds() :(
                diff = (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10 ** 6) / 10 ** 6
                if ((interval == self.INTERVAL_12 and diff >= 43200) or
                        (interval == self.INTERVAL_24 and diff >= 86400) or
                        (interval == self.INTERVAL_48 and diff >= 172800)):
                    fetch = True
            else:
                fetch = True

        if fetch:
            tmp_file = os.path.join(self.basePath, 'tmp')
            if self.fileType == self.TYPE_REMOTE:
                xbmc.log('[%s] file is in remote location: %s' %
                         (ADDON.getAddonInfo('id'), self.fileUrl), xbmc.LOGDEBUG)
                if not xbmcvfs.copy(self.fileUrl, tmp_file):
                    xbmc.log('[%s] Remote file couldn\'t be copied: %s' %
                             (ADDON.getAddonInfo('id'), self.fileUrl), xbmc.LOGERROR)
            else:
                f = open(tmp_file, 'wb')
                xbmc.log('[%s] file is on the internet: %s' %
                         (ADDON.getAddonInfo('id'), self.fileUrl), xbmc.LOGDEBUG)
                tmp_data = urllib2.urlopen(self.fileUrl)
                data = tmp_data.read()
                if tmp_data.info().get('content-encoding') == 'gzip':
                    data = zlib.decompress(data, zlib.MAX_WBITS + 16)
                f.write(data)
                f.close()
            if os.path.getsize(tmp_file) > 256:
                if os.path.exists(self.filePath):
                    os.remove(self.filePath)
                os.rename(tmp_file, self.filePath)
                ret_val = self.FETCH_OK
                xbmc.log('[%s] file %s was downloaded' % (ADDON.getAddonInfo('id'), self.filePath),
                         xbmc.LOGDEBUG)
            else:
                ret_val = self.FETCH_ERROR
        return ret_val
