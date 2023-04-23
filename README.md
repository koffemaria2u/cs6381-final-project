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
#>>>> Status
#cluster id : '14841639068965178418'
#first member info : {'ID': '10276657743932975437', 'name': 'default', 'peerURLs': ['http://localhost:2380'], 'clientURLs': ['http://localhost:2379']}
#>>>> Lease
#Lease id : 7587870135924071463
#Lease ttl : 29
#Lease refresh : 30
#Key put foo2 : True
#Key put foo3 : True
#Lease Keys : [b'foo2', b'foo3']
#Lease Revoke : True
#Key get foox : []
#Key put foo : True
#Key get foo : [b'bar']
#Key delete foo : True
#Key delete foo-unknown : False
#>>>> Lock
#acquire : True
#refresh : 10000
#is_acquired : True
#release : True
#is_acquired : False
```
