# -*- coding: utf-8 -*-
#
#      Copyright (C) 2016 Thomas Geppert [bluezed] - bluezed.apps@gmail.com
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
from itertools import izip_longest

import xbmc
from strings import ADDON
from xml.etree import ElementTree as eT

LOGO_TYPE_DEFAULT = 0
LOGO_TYPE_CUSTOM = 1
DEFAULT_LOGO_URL = 'https://s3.amazonaws.com/schedulesdirect/assets/stationLogos/'


class SourceException(Exception):
    pass


class SourceUpdateCanceledException(SourceException):
    pass


class SourceNotConfiguredException(SourceException):
    pass


class Channel(object):
    def __init__(self, id, title, lineup, logo=None, streamUrl=None, visible=True, weight=-1):
        self.id = id
        self.title = title
        self.lineup = lineup
        self.logo = logo
        self.streamUrl = streamUrl
        self.visible = visible
        self.weight = weight

    def isPlayable(self):
        return hasattr(self, 'streamUrl') and self.streamUrl

    def __eq__(self, other):
        return self.id == other.id

    def __repr__(self):
        return 'Channel(id=%s, title=%s, lineup=%s, logo=%s, streamUrl=%s)' \
               % (self.id, self.title, self.lineup, self.logo, self.streamUrl)


class Program(object):
    def __init__(self, channel, title, startDate, endDate, description, imageLarge=None,
                 imageSmall=None,
                 notificationScheduled=None, season=None, episode=None, is_movie=False,
                 language="en"):
        """

        @param channel:
        @type channel: source.Channel
        @param title:
        @param startDate:
        @param endDate:
        @param description:
        @param imageLarge:
        @param imageSmall:
        """
        self.channel = channel
        self.title = title
        self.startDate = startDate
        self.endDate = endDate
        self.description = description
        self.imageLarge = imageLarge
        self.imageSmall = imageSmall
        self.notificationScheduled = notificationScheduled
        self.season = season
        self.episode = episode
        self.is_movie = is_movie
        self.language = language

    def __repr__(self):
        return 'Program(channel=%s, title=%s, startDate=%s, endDate=%s, description=%s, imageLarge=%s, ' \
               'imageSmall=%s, episode=%s, season=%s, is_movie=%s)' % (
                   self.channel, self.title, self.startDate,
                   self.endDate, self.description, self.imageLarge,
                   self.imageSmall, self.season, self.episode,
                   self.is_movie)


def save_setting(key, value, is_list=False):

    xbmc.log('[%s] Tyring to save setting: key "%s" / value "%s"' %
             (ADDON.getAddonInfo('id'), key, str(value)), xbmc.LOGDEBUG)

    file_path = xbmc.translatePath(
        os.path.join('special://profile', 'addon_data', ADDON.getAddonInfo('id'), 'settings.xml'))
    tree = eT.parse(file_path)
    root = tree.getroot()
    updated = False
    for item in root.findall('setting'):
        if item.attrib['id'] == key:
            if is_list:
                cur_values = item.attrib['value']
                if not cur_values:
                    cur_values = []
                else:
                    cur_values = json.loads(cur_values)
                if isinstance(value, list):
                    for val in value:
                        if val not in cur_values:
                            cur_values.append(val)
                else:
                    if value not in cur_values:
                        cur_values.append(value)
                item.attrib['value'] = json.dumps(cur_values)
                ADDON.setSetting(key, cur_values)
            else:
                item.attrib['value'] = value
                ADDON.setSetting(key, value)
            updated = True
    if updated:
        tree.write(file_path)


def get_setting(key, is_list=False):
    value = ADDON.getSetting(key)
    if value and is_list:
        value = json.loads(value)
    elif is_list:
        value = []
    return value


def grouper(n, iterable, fillvalue=None):
    """ grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx """
    args = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *args)


def get_logo(channel):
    logo = channel.logo
    logo_type = int(ADDON.getSetting('logos.source'))
    if logo and logo_type == LOGO_TYPE_DEFAULT:
        return logo

    logo_location = ADDON.getSetting('logos.folder')
    if not logo and logo_type == LOGO_TYPE_DEFAULT:
        logo = DEFAULT_LOGO_URL + 's' + channel.id + '_h3_aa.png'
    elif logo_type == LOGO_TYPE_CUSTOM:
        logo = logo_location + channel.title + '.png'
        if logo_location.startswith("http://") or logo_location.startswith("sftp://") or \
                logo_location.startswith("ftp://") or logo_location.startswith("https://") or \
                logo_location.startswith("ftps://") or logo_location.startswith("smb://") or \
                logo_location.startswith("nfs://"):  # looks like remote location
            logo = logo.replace(' ', '%20')
    return logo
