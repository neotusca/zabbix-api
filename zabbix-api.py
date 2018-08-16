#!/usr/bin/python

from pyzabbix import ZabbixAPI
import json




def auth(api_str, id, pw):
    zapi = ZabbixAPI(url=api_str, user=id, password=pw)
    return zapi


def get_usagedata(_zapi):

    # get hostid
    _hosts = _zapi.do_request('host.get', {
                                              'output': [
                                                  'hostid',
                                                  'name'
                                              ]
                                          })

    #print _hosts, type(_hosts)  # dictionary
    #print _hosts.get('result'), type(_hosts.get('result'))  # list
    _hosts = _hosts.get('result')
    print _hosts
  
    for _hostid in _hosts:     
        print '[hostid]:'+_hostid.get('hostid'), _hostid.get('name')

        # get graph of hostid
        _graphs = _zapi.do_request('graph.get', {
                                                       'filter': {'hostid': _hostid.get('hostid')},
                                                       'output': [
                                                           'graphid',
                                                           'name'
                                                       ]
                                                   })
        _graphs = _graphs.get('result')
        #print _graphs, type(_graphs) # list

        for _graph in _graphs:
            #print _graph, type(_graph) # dict
            print '['+_hostid.get('hostid')+']'+'['+_graph.get('graphid')+']'+'['+_graph.get('name')+']------------------' 
            print type(_hostid.get('hostid'))
            print type(_graph.get('graphid'))

            _graphitems = _zapi.do_request('graphitem.get', {
                                                                'filter': {'graphids': _graph.get('graphid')},
                                                                'output': [
                                                                    'gitemid',
                                                                    'itemid'
                                                                ]   
                                                            })
            _graphitems = _graphitems.get('result')
            #print _graphitems, type(_graphitems)

            for _graphitem in _graphitems:
                print _graphitem, type(_graphitem)




def get_test(_zapi):
    _result = _zapi.do_request('graphitem.get', {
                                                    'filter': {'hostid': '10505'},
                                                    'output': [
                                                        'graphid',
                                                        'gitemid',
                                                        'itemid'
                                                    ]
                                                })
    print _result




def get_hostinfo(zabbix_api):
    #result1 = zabbix_api.host.get(monitored_hosts=1, output='extend')
    result1 = zabbix_api.host.get()

    for INFO in result1:
        print '--------------'
        print INFO, type(INFO)
        print INFO['hostid'], INFO['host'], INFO['name']

    print '-1------------------------------------'

    result2 = zabbix_api.do_request('host.get',
                          {
                              'output': [
                                  'hostid',
                                  'host',
                                  'name'
                              ],
                              'selectInterfaces': [
                                  'interfaceid',
                                  'ip'
                              ]
                          })

    print result2


def get_graphinfo(_zapi):
    _hostids = zabbix_api.get_id('host') 
    #print _hostids, type(_hostids)  # list

    print "### hostid-list ###"
    for _hostid in _hostids:
        print _hostid, type(_hostid) # integer 
        _result = _zapi.do_request('host.get', {'filter':{'hostid': _hostid},
                                                'output':['hostid',
                                                          'host',
                                                          'name'],
                                                'selectInterfaces':['interfaceid',
                                                                    'ip']})
        #print _result,type(_result) # dict
        #print _result.get('result'), type(_result.get('result'))  # list

        print "### host-graph-list ###"
        for _data in _result.get('result'):
            #print _data, type(_data) # dict
            print _data.get('hostid'), _data.get('name')
            
            _graphs = _zapi.do_request('graph.get', {'filter':{'hostid': _data.get('hostid')},
                                                     'output':['graphid',
                                                               'name']})
            #print _graphs, type(_graphs) # dict
            print _graphs.get('result'), type(_graphs.get('result')) # list

            for _data in _graphs.get('result'):
                print _data, type(_data)
                print _data.get('graphid'), _data.get('name')






if __name__ == "__main__":
    ID='Admin'
    PW='zabbix'
    API_STR='http://192.168.100.7/zabbix/'
    #ID='harvana'
    #PW='Media1!'
    #API_STR='http://zabbix.medialog.co.kr/'

    zabbix_api = auth(API_STR, ID, PW)
    #print zabbix_api

    #get_hostinfo(zabbix_api)
    #get_graphinfo(zabbix_api)
    #get_usagedata(zabbix_api)
    get_test(zabbix_api)


