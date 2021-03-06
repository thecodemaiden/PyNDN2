# -*- Mode:python; c-file-style:"gnu"; indent-tabs-mode:nil -*- */
#
# Copyright (C) 2014 Regents of the University of California.
# Author: Jeff Thompson <jefft0@remap.ucla.edu>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# A copy of the GNU General Public License is in the file COPYING.

"""
This module defines the KeyLocator class which represents an NDN KeyLocator which
is used in a Sha256WithRsaSignature and Interest selectors.
"""

from pyndn.util.change_counter import ChangeCounter
from pyndn.util import Blob
from pyndn.name import Name

class KeyLocator(object):
    """
    Create a new KeyLocator object, possibly copying values from 
    another object.
    
    :param KeyLocator value: (optional) If value is a KeyLocator, copy its 
      values.  If value is omitted, set the fields to unspecified.
    """
    def __init__(self, value = None):
        if value == None:
            self._type = None
            self._keyName = ChangeCounter(Name())
            self._keyData = Blob()
        elif type(value) is KeyLocator:
            # Copy its values.
            self._type = value._type
            self._keyName = ChangeCounter(Name(value.getKeyName()))
            self._keyData = value._keyData
        else:
            raise RuntimeError(
              "Unrecognized type for KeyLocator constructor: " +
              repr(type(value)))
            
        self._changeCount = 0

    def getType(self):
        """
        Get the key locator type. If KeyLocatorType.KEYNAME, you may also
        getKeyName().  If KeyLocatorType.KEY_LOCATOR_DIGEST, you may also
        getKeyData() to get the digest.
        
        :return: The key locator type, or None if not specified.
        :rtype: an int from KeyLocatorType
        """
        return self._type
        
    def getKeyName(self):
        """
        Get the key name.  This is meaningful if getType() is
        KeyLocatorType.KEYNAME.
        
        :return: The key name. If not specified, the Name is empty.
        :rtype: Name
        """
        return self._keyName.get()

    def getKeyData(self):
        """
        Get the key data.  This is the digest bytes if getType() is
        KeyLocatorType.KEY_LOCATOR_DIGEST.
        
        :return: The key data as a Blob, which isNull() if unspecified.
        :rtype: Blob
        """
        return self._keyData

    def setType(self, type):
        """
        Set the key locator type.  If KeyLocatorType.KEYNAME, you must also
        setKeyName().  If KeyLocatorType.KEY_LOCATOR_DIGEST, you must also
        setKeyData() to set the digest.
        
        :param type: The key locator type.  If None, the type is unspecified.
        :type type: an int from KeyLocatorType
        """
        self._type = None if type == None or type < 0 else type
        self._changeCount += 1
        
    def setKeyName(self, keyName):
        """
        Set key name to a copy of the given Name.  This is the name if 
        getType() is KeyLocatorType.KEYNAME.
        
        :param Name keyName: The key name which is copied.
        """
        self._keyName.set(keyName if type(keyName) is Name else Name(keyName))
        self._changeCount += 1
        
    def setKeyData(self, keyData):
        """
        Set the key data to the given value.  This is the digest bytes if 
        getType() is KeyLocatorType.KEY_LOCATOR_DIGEST.
        
        :param keyData: The array with the key data bytes. If keyData is not a 
          Blob, then create a new Blob to copy the bytes (otherwise 
          take another pointer to the same Blob).
        :type keyData: A Blob or an array type with int elements 
        """
        self._keyData = keyData if type(keyData) is Blob else Blob(keyData)
        self._changeCount += 1

    def clear(self):
        """
        Clear the fields and set the type to None.
        """
        self._type = None
        self._keyName.get().clear()
        self._keyData = Blob()
        self._changeCount += 1

    def getChangeCount(self):
        """
        Get the change count, which is incremented each time this object 
        (or a child object) is changed.
        
        :return: The change count.
        :rtype: int
        """
        # Make sure each of the checkChanged is called.
        changed = self._keyName.checkChanged()
        if changed:
            # A child object has changed, so update the change count.
            self._changeCount += 1

        return self._changeCount

class KeyLocatorType(object):
    """
    A KeyLocatorType specifies the type of a KeyLocator object.
    """
    KEYNAME = 1
    KEY_LOCATOR_DIGEST = 2
