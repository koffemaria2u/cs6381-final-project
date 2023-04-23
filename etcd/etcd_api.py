from etcd3gw.client import Etcd3Client
from etcd3gw.lock import Lock
import logging

try:
    # Python 3.8 : time.clock was deprecated and removed.
    from time import perf_counter as clock
except ImportError:
    from time import clock


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("EtcdClient")


def main():
    client = Etcd3Client()

    print('>>>> Status')
    result = client.status()
    print("cluster id : %r" % result['header']['cluster_id'])

    result = client.members()
    print("first member info : %r" % result[0])

    print('>>>> Lease')
    lease = client.lease()
    print("Lease id : %r" % lease.id)
    print("Lease ttl : %r" % lease.ttl())
    print("Lease refresh : %r" % lease.refresh())

    result = client.put('foo2', 'bar2', lease)
    print("Key put foo2 : %r" % result)
    result = client.put('foo3', 'bar3', lease)
    print("Key put foo3 : %r" % result)
    print("Lease Keys : %r" % lease.keys())

    result = lease.revoke()
    print("Lease Revoke : %r" % result)

    result = client.get('foox')
    print("Key get foox : %r" % result)

    result = client.put('foo', 'bar')
    print("Key put foo : %r" % result)
    result = client.get('foo')
    print("Key get foo : %r" % result)
    result = client.delete('foo')
    print("Key delete foo : %r" % result)
    result = client.delete('foo-unknown')
    print("Key delete foo-unknown : %r" % result)

    print('>>>> Lock')
    lock = Lock('xyz-%s' % clock(), ttl=10000, client=client)
    result = lock.acquire()
    print("acquire : %r" % result)
    result = lock.refresh()
    print("refresh : %r" % result)
    result = lock.is_acquired()
    print("is_acquired : %r" % result)
    result = lock.release()
    print("release : %r" % result)
    result = lock.is_acquired()
    print("is_acquired : %r" % result)


if __name__ == "__main__":
    main()
