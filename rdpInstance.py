# -*- coding:utf8 -*-

import io
import sys
import os
import string

class RDPInstance:

    def __init__(self):
        self.data = {}

    def set_displayconnectionbar(self, enable):
        self.data[u"displayconnectionbar:i"] = u'1' if enable else u'0'

    def get_displayconnectionbar(self):
        if u"displayconnectionbar:i" in self.data:
            return self.data[u"displayconnectionbar:i"] == u'1'
        else:
            return None

    def set_redirectprinters(self, enable):
        self.data[u"redirectprinters:i"] = u'1' if enable else u'0'

    def get_redirectprinters(self):
        if u"redirectprinters:i" in self.data:
            return self.data[u"redirectprinters:i"] == u'1'
        else:
            return None

    def set_redirectclipboard(self, enable):
        self.data[u"redirectclipboard:i"] = u'1' if enable else u'0'

    def get_redirectclipboard(self):
        if u"redirectclipboard:i" in self.data:
            return self.data[u"redirectclipboard:i"] == u'1'
        else:
            return None

    def set_autoreconnection(self, enable):
        self.data[u"autoreconnection enabled:i"] = u'1' if enable else u'0'

    def get_autoreconnection(self):
        if u"autoreconnection enabled:i" in self.data:
            return self.data[u"autoreconnection enabled:i"] == u'1'
        else:
            return None

    def set_authentication_level(self, level):
        self.data[u"authentication level:i"] = u'%s' % level

    def get_authentication_level(self):
        if u"authentication level:i" in self.data:
            return self.data[u"authentication level:i"]
        else:
            return None

    def set_full_address(self, addr):
        self.data[u"full address:s"] = u'%s' % addr

    def get_full_address(self):
        if u"full address:s" in self.data:
            return self.data[u"full address:s"]
        else:
            return None

    def set_audiocapturemode(self, mode):
        self.data[u"audiocapturemode:i"] = u'%s' % mode

    def get_audiocapturemode(self):
        if u"audiocapturemode:i" in self.data:
            return self.data[u"audiocapturemode:i"]
        else:
            return None

    def set_audiomode(self, mode):
        self.data[u"audiomode:i"] = u'%s' % mode

    def get_audiomode(self):
        if u"audiomode:i" in self.data:
            return self.data[u"audiomode:i"]
        else:
            return None

    def set_keyboardhook(self, hook):
        self.data[u"keyboardhook:i"] = u'%s' % hook

    def get_keyboardhook(self):
        if u"keyboardhook:i" in self.data:
            return self.data[u"keyboardhook:i"]
        else:
            return None

    def set_redirectsmartcards(self, enable):
        self.data[u"redirectsmartcards:i"] = u'1' if enable else u'0'

    def get_redirectsmartcards(self):
        if u"redirectsmartcards:i" in self.data:
            return self.data[u"redirectsmartcards:i"] == u'1'
        else:
            return None

    def set_redirectcomports(self, enable):
        self.data[u"redirectcomports:i"] = u'1' if enable else u'0'

    def get_redirectcomports(self):
        if u"redirectcomports:i" in self.data:
            return self.data[u"redirectcomports:i"] == u'1'
        else:
            return None

    def set_drivestoredirect(self, enable, name):
        if u"drivestoredirect:s" not in self.data:
            self.data[u"drivestoredirect:s"] = []
        if enable:
            if name not in self.data[u"drivestoredirect:s"]:
                self.data[u"drivestoredirect:s"].append(name)
        else:
            if name in self.data[u"drivestoredirect:s"]:
                self.data[u"drivestoredirect:s"].remove(name)

    def get_drivestoredirect(self, name):
        if u"drivestoredirect:s" in self.data:
            if name in self.data[u"drivestoredirect:s"]:
                return True
        return None

    def set_devicestoredirect(self, enable, name):
        if u"devicestoredirect:s" not in self.data:
            self.data[u"devicestoredirect:s"] = []
        if enable:
            if name not in self.data[u"devicestoredirect:s"]:
                self.data[u"devicestoredirect:s"].append(name)
        else:
            if name in self.data[u"devicestoredirect:s"]:
                self.data[u"devicestoredirect:s"].remove(name)

    def get_devicestoredirect(self, name):
        if u"devicestoredirect:s" in self.data:
            if name in self.data[u"devicestoredirect:s"]:
                return True
        return None

    def set_session_bpp(self, bpp):
        self.data[u"session bpp:i"] = u'%s' % bpp

    def get_session_bpp(self):
        if u"session bpp:i" in self.data:
            return self.data[u"session bpp:i"]
        else:
            return None

    def set_connection_type(self, t):
        self.data[u"connection type:i"] = u'%s' % t

    def get_connection_type(self):
        if u"connection type:i" in self.data:
            return self.data[u"connection type:i"]
        else:
            return None

    def set_wallpaper(self, enable):
        self.data[u"disable wallpaper:i"] = u'0' if enable else u'1'

    def get_wallpaper(self):
        if u"disable wallpaper:i" in self.data:
            return self.data[u"disable wallpaper:i"] == u'0'
        else:
            return None

    def set_font_smoothing(self, enable):
        self.data[u"allow font smoothing:i"] = u'1' if enable else u'0'

    def get_font_smoothing(self):
        if u"allow font smoothing:i" in self.data:
            return self.data[u"allow font smoothing:i"] == u'1'
        else:
            return None

    def set_desktop_composition(self, enable):
        self.data[u"allow desktop composition:i"] = u'1' if enable else u'0'

    def get_desktop_composition(self):
        if u"allow desktop composition:i" in self.data:
            return self.data[u"allow desktop composition:i"] == u'1'
        else:
            return None

    def set_full_window_drag(self, enable):
        self.data[u"disable full window drag:i"] = u'0' if enable else u'1'

    def get_full_window_drag(self):
        if u"disable full window drag:i" in self.data:
            return self.data[u"disable full window drag:i"] == u'0'
        else:
            return None

    def set_menu_anims(self, enable):
        self.data[u"disable menu anims:i"] = u'0' if enable else u'1'

    def get_menu_anims(self):
        if u"disable menu anims:i" in self.data:
            return self.data[u"disable menu anims:i"] == u'0'
        else:
            return None

    def set_themes(self, enable):
        self.data[u"disable themes:i"] = u'0' if enable else u'1'

    def get_themes(self):
        if u"disable themes:i" in self.data:
            return self.data[u"disable themes:i"] == u'0'
        else:
            return None

    def set_bitmapcachepersistenable(self, enable):
        self.data[u"bitmapcachepersistenable:i"] = u'1' if enable else u'0'

    def get_bitmapcachepersistenable(self):
        if u"bitmapcachepersistenable:i" in self.data:
            return self.data[u"bitmapcachepersistenable:i"] == u'1'
        else:
            return None

    def set_desktopwidth(self, len):
        self.data[u"desktopwidth:i"] = u'%s' % len

    def get_desktopwidth(self):
        if u"desktopwidth:i" in self.data:
            return self.data[u"desktopwidth:i"]
        else:
            return None

    def set_desktopheight(self, len):
        self.data[u"desktopheight:i"] = u'%s' % len

    def get_desktopheight(self):
        if u"desktopheight:i" in self.data:
            return self.data[u"desktopheight:i"]
        else:
            return None

    def write(self, outfile=sys.stdout):
        try:
            if isinstance(outfile, unicode):
                outfile = io.open(outfile, mode='wb')
        except:
            sys.stderr.write("write to %s failed!\n" % outfile)
            return
        outfile.write("".encode("UTF-16"))
        for key, value in sorted(self.data.items()):
            if isinstance(value, list):
                value = ";".join(value)
            elif isinstance(value, dict):
                value = ";".join(value.values())
            line = key+":"+value+os.linesep
            outfile.write(line.encode("UTF-16")[2:])
        outfile.close()

    def read(self, infile):
        try:
            if isinstance(infile, unicode):
                infile = io.open(infile, mode='r', encoding="UTF-16")
        except:
            sys.stderr.write("read from %s failed!\n" % infile)
            return
        for line in infile:
            items = line.strip(os.linesep).split(':', 2)
            if len(items) > 2:
                key = ':'.join(items[:2])
                value = items[2]
                self.data[key] = value
        return self.data



