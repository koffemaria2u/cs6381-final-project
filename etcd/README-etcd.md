# cs6381-final-project
Service management exploration


## etcd
### Usage
To run on Ubuntu 22.04:
1. [Install etcd on Ubuntu 22.04](https://snapcraft.io/install/etcd-arm64/ubuntu)
2. Python 3.8.16
3. [etcd3gw](https://pypi.org/project/etcd3gw/) 
4. Create python venv
5. Run `etcd`


```bash
python -m venv env_38
source env_38/bin/activate
pip install etcd3gw

python -V
# Python 3.8.16

# Terminal 1
etcd

# Terminal 2
python pyetcd_api.py
#EtcdClient - INFO - cluster id STATUS: '14841639068965178418'
#EtcdClient - INFO - first MEMBER info : {'ID': '10276657743932975437', 'name': 'default', 'peerURLs': ['http://localhost:2380'], 'clientURLs': ['http://localhost:2379']}
#EtcdClient - INFO - demo LEASE...
#EtcdClient - INFO - LEASE id : 7587870180556262441
#EtcdClient - INFO - LEASE ttl : 29
#EtcdClient - INFO - LEASE refresh : 30
#EtcdClient - INFO - Key PUT foo2 : True
#EtcdClient - INFO - Key PUT foo3 : True
#EtcdClient - INFO - LEASE Keys : [b'foo2', b'foo3']
#EtcdClient - INFO - LEASE Revoke : True
#EtcdClient - INFO - demo basic PUT/GET/DELETE keys...
#EtcdClient - INFO - Key GET foox : []
#EtcdClient - INFO - Key PUT foo : True
#EtcdClient - INFO - Key GET foo : [b'bar']
#EtcdClient - INFO - Key DELETE foo : True
#EtcdClient - INFO - Key DELETE foo-unknown : False
#EtcdClient - INFO - demo LOCK...
#EtcdClient - INFO - acquire : True
#EtcdClient - INFO - refresh : 10000
#EtcdClient - INFO - is_acquired : True
#EtcdClient - INFO - release : True
#EtcdClient - INFO - is_acquired : False
#EtcdClient - INFO - demo WATCH...
#EtcdClient - INFO - Key PUT watch_key : True
#EtcdClient - INFO - Key GET watch_key : [b'watch_value']
#EtcdClient - INFO - {'kv': {'key': b'watch_key', 'create_revision': '51', 'mod_revision': '139', 'version': '12', 'value': b'new_val'}}
#EtcdClient - INFO - Watch count: 1
#EtcdClient - INFO - {'kv': {'key': b'watch_key', 'create_revision': '51', 'mod_revision': '140', 'version': '13', 'value': b'watch_value'}}
#EtcdClient - INFO - Watch count: 2
#EtcdClient - INFO - {'kv': {'key': b'watch_key', 'create_revision': '51', 'mod_revision': '141', 'version': '14', 'value': b'new_val'}}
#EtcdClient - INFO - Watch count: 3
#EtcdClient - INFO - And now his watch is ended...

# Terminal 3
python watcher_etcd_api.py -w watch_key -ov init_val -nv new_val
python watcher_etcd_api.py -w watch_key -ov new_val -nv newer_val
python watcher_etcd_api.py -w watch_key -ov newer_val -nv even_newer_val
```

## Demo Images
Watcher demo:
![alt text](etcd/resources/etcd_watcher_demo.png "Title")


CLI `etcdctl` demo:
![alt text](etcd/resources/etcdctl_cli_demo.png "Title")


## Resources
1. `etcdctl` - [etcd cli commands](https://etcd.io/docs/v3.4/dev-guide/interacting_v3/) 