# coding: latin-1

# (c) Massachusetts Institute of Technology 2015-2018
# (c) Brian Teague 2018-2021
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''
package.hooks.rthook_qtconf
---------------------------

Runtime hook -- updates two copies of qt.conf to point to the one-click's
Qt resources
'''

import os
import sys

qt_path = os.path.join(sys._MEIPASS, 'PyQt5', 'Qt')

# QT's init file format requires front-slashes even on windows
if sys.platform.startswith('win'):
    qt_path = qt_path.replace("\\", '/')
    
# need one qt.conf in the _MEIPASS
qt_conf_path = os.path.join(sys._MEIPASS, 'qt.conf')
with open(qt_conf_path, 'w' ) as f:
    f.write('[Paths]\nPrefix = {}\n'.format(qt_path))
      
# need another qt.conf in _MEIPASS / PyQt5 / Qt / libexec, for
# QtWebEngineProcess to find
qt_libexec_conf_path = os.path.join(qt_path, 'libexec', 'qt.conf')
with open(qt_libexec_conf_path, 'w') as f:
    f.write('[Paths]\nPrefix = {}\n'.format(qt_path))
