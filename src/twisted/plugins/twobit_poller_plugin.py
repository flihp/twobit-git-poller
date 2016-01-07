# This program is my git fetcher. It's a simple twisted
# application that periodically polls the specified git repos.
# Copyright (C) 2014  Philip Tricca <flihp@twobit.us>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
""" twobit git poller

This plugin file defines an application that periodically fetches a
collection of git repos.  Repos are descriped in the accompanying INI-
style configuration file.
"""

from twobit.twisted_gitpoller import PollerMultiServiceFactory

plugin = PollerMultiServiceFactory()
