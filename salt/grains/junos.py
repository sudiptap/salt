# -*- coding: utf-8 -*-
'''
Grains for junos.
NOTE this is a little complicated--junos can only be accessed via salt-proxy-minion.
Thus, some grains make sense to get them from the minion (PYTHONPATH), but others
don't (ip_interfaces)
'''
from __future__ import absolute_import
from jnpr.junos.device import Device
import logging

__proxyenabled__ = ['junos']

__virtualname__ = 'junos'

log = logging.getLogger(__name__)


def __virtual__():
    if 'proxy' not in __opts__:
        return False
    else:
        return __virtualname__


def _remove_complex_types(dictionary):
    '''
    Linode-python is now returning some complex types that
    are not serializable by msgpack.  Kill those.
    '''

    for k, v in dictionary.iteritems():
        if isinstance(v, dict):
            dictionary[k] = _remove_complex_types(v)
        elif hasattr(v, 'to_eng_string'):
            dictionary[k] = v.to_eng_string()

    return dictionary


def defaults():
    return {'os': 'proxy', 'kernel': 'unknown', 'osrelease': 'proxy'}


def facts():
    #This is a temporary work around until __proxy__ can be called from the grains.
    
    dev = Device(user=__opts__['proxy']['username'],
                    host=__opts__['proxy']['host'],
                    password=__opts__['proxy']['passwd'])
    dev.open()
    facts = dev.facts
    facts['version_info'] = 'override'
    dev.close()
    return facts


def os_family():
    return {'os_family': 'junos'}
