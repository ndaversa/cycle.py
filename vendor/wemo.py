# Copyright (c) 2010, Issac Kelly
# https://github.com/issackelly/wemo
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the tastypie nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL tastypie BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from miranda import upnp, msearch

conn = upnp()
msearch(0, 0, conn, 2)

SWITCHES = []

# populate all the host info, for every upnp device on the network
for index in conn.ENUM_HOSTS:
    hostInfo = conn.ENUM_HOSTS[index]
    if hostInfo['dataComplete'] == False:
        xmlHeaders, xmlData = conn.getXML(hostInfo['xmlFile'])
        conn.getHostInfo(xmlData,xmlHeaders,index)


for index in conn.ENUM_HOSTS:
    try:
        if conn.ENUM_HOSTS[index]['deviceList']['controllee']['modelName'] == 'Socket':
            SWITCHES = [index]
    except KeyError:
        pass


def _send(action, args=None):
    if not args:
        args = {}
    host_info = conn.ENUM_HOSTS[SWITCHES[0]]
    device_name = 'controllee'
    service_name = 'basicevent'
    controlURL = host_info['proto'] + host_info['name']
    controlURL2 = hostInfo['deviceList'][device_name]['services'][service_name]['controlURL']
    if not controlURL.endswith('/') and not controlURL2.startswith('/'):
        controlURL += '/'
    controlURL += controlURL2

    resp = conn.sendSOAP(
        host_info['name'],
        'urn:Belkin:service:basicevent:1',
        controlURL,
        action,
        args
    )
    return resp

def get():
    """
    Gets the value of the first switch that it finds
    """
    resp = _send('GetBinaryState')
    tagValue = conn.extractSingleTag(resp, 'BinaryState')
    return True if tagValue == '1' else False

def on():
    """
    Turns on the first switch that it finds.

    BinaryState is set to 'Error' in the case that it was already on.
    """
    resp = _send('SetBinaryState', {'BinaryState': (1, 'Boolean')})
    tagValue = conn.extractSingleTag(resp, 'BinaryState')
    return True if tagValue in ['1', 'Error'] else False

def off():
    """
    Turns off the first switch that it finds.

    BinaryState is set to 'Error' in the case that it was already off.
    """
    resp = _send('SetBinaryState', {'BinaryState': (0, 'Boolean')})
    tagValue = conn.extractSingleTag(resp, 'BinaryState')
    return True if tagValue in ['0', 'Error'] else False
