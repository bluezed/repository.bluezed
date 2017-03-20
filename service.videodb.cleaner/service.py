# -*- coding: utf-8 -*-
#
#  Copyright (C) 2017 by Thomas Geppert [bluezed] - bluezed.apps@gmail.com
#
#  This Program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
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

import json
import os
import sqlite3
import xbmc
import xbmcaddon


class Cleaner:
    addon = ''
    force_clean = False
    db_path = ''

    # Mapping Kodi-version to its corresponding Video-DB version
    # @link http://kodi.wiki/view/database_versions
    ver_map = {10: '37', 11: '60', 12: '75', 13: '78', 14: '90', 15: '93', 16: '99', 17: '107', 18: '108'}

    def __init__(self):
        self.addon = xbmcaddon.Addon('service.videodb.cleaner')
        ver = self.get_kodi_version()
        self.db_path = os.path.join(xbmc.translatePath('special://database'), 'MyVideos' + self.ver_map[ver] + '.db')
        xbmc.log('[service.videodb.cleaner] Kodi-Version: %s, DB-Path: %s' % (str(ver), self.db_path), xbmc.LOGDEBUG)

    def run_manual(self):
        xbmc.log("[service.videodb.cleaner] Started manually", xbmc.LOGINFO)
        self._run()

    def run(self):
        if self.addon.getSetting('service_enabled') == "true":
            wait_time = 86400  # 24 hours
            monitor = xbmc.Monitor()
            xbmc.log("[service.videodb.cleaner] Background service started...", xbmc.LOGINFO)
            self._run()
            while not monitor.abortRequested():
                # Sleep/wait for specified time
                xbmc.log("[service.videodb.cleaner] Service waiting for interval %s" % wait_time, xbmc.LOGDEBUG)
                if monitor.waitForAbort(wait_time):
                    # Abort was requested while waiting. We should exit
                    break
                xbmc.log("[service.videodb.cleaner] Service now triggered...", xbmc.LOGDEBUG)
                self._run()
        else:
            xbmc.log("[service.videodb.cleaner] Background service is disabled", xbmc.LOGINFO)

    def _run(self):
        json_query = xbmc.executeJSONRPC(
            '{ "jsonrpc": "2.0", "method": "Files.GetSources", "params": {"media": "video"}, "id": 1 }')
        json_query = unicode(json_query, 'utf-8', errors='ignore')
        json_query = json.loads(json_query)
        sql = ''
        if 'result' in json_query and 'sources' in json_query['result']:
            xbmc.log('[service.videodb.cleaner] Found these sources: %s' % str(json_query['result']['sources'])
                     , xbmc.LOGDEBUG)
            for source in json_query['result']['sources']:
                if len(sql) > 0:
                    sql += ' AND'
                sql += " strpath NOT LIKE '" + source['file'] + "%'"

        xbmc.log('[service.videodb.cleaner] Cleaning all external sources from Video-DB...', xbmc.LOGDEBUG)
        conn = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("DELETE FROM path WHERE" + sql + ";")
        xbmc.log("[service.videodb.cleaner] Executing: \"DELETE FROM path WHERE%s;\"" % sql, xbmc.LOGDEBUG)
        c.execute('DELETE FROM files WHERE idPath NOT IN (SELECT p.idPath FROM path p);')
        c.execute('DELETE FROM episode WHERE idFile NOT IN (SELECT f.idFile FROM files f);')
        c.execute('DELETE FROM streamdetails WHERE idFile NOT IN (SELECT f.idFile FROM files f);')
        c.close()
        conn.commit()
        conn.close()

    @staticmethod
    def get_kodi_version():
        # retrieve current installed version
        json_query = xbmc.executeJSONRPC(
            '{ "jsonrpc": "2.0", "method": "Application.GetProperties", '
            '"params": {"properties": ["version", "name"]}, "id": 1 }')
        json_query = unicode(json_query, 'utf-8', errors='ignore')
        json_query = json.loads(json_query)
        if 'result' in json_query and 'version' in json_query['result']:
            version = json_query['result']['version']
            return int(version['major'])
        return 0
