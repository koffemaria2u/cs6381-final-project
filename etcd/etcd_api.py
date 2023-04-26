import time

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

    result = client.status()
    logger.info("cluster id STATUS: %r" % result['header']['cluster_id'])

    result = client.members()
    logger.info("first MEMBER info : %r" % result[0])

    logger.info("demo LEASE...")
    lease = client.lease()
    logger.info("LEASE id : %r" % lease.id)
    logger.info("LEASE ttl : %r" % lease.ttl())
    logger.info("LEASE refresh : %r" % lease.refresh())

    result = client.put('foo2', 'bar2', lease)
    logger.info("Key PUT foo2 : %r" % result)
    result = client.put('foo3', 'bar3', lease)
    logger.info("Key PUT foo3 : %r" % result)
    logger.info("LEASE Keys : %r" % lease.keys())
    result = lease.revoke()
    logger.info("LEASE Revoke : %r" % result)

    logger.info("demo basic PUT/GET/DELETE keys...")
    result = client.get('foox')
    logger.info("Key GET foox : %r" % result)

    result = client.put('foo', 'bar')
    logger.info("Key PUT foo : %r" % result)

    result = client.get('foo')
    logger.info("Key GET foo : %r" % result)

    result = client.delete('foo')
    logger.info("Key DELETE foo : %r" % result)

    result = client.delete('foo-unknown')
    logger.info("Key DELETE foo-unknown : %r" % result)

    logger.info('demo LOCK...')
    lock = Lock('xyz-%s' % clock(), ttl=10000, client=client)
    result = lock.acquire()
    logger.info("acquire : %r" % result)

    result = lock.refresh()
    logger.info("refresh : %r" % result)

    result = lock.is_acquired()
    logger.info("is_acquired : %r" % result)

    result = lock.release()
    logger.info("release : %r" % result)

    result = lock.is_acquired()
    logger.info("is_acquired : %r" % result)

    logger.info('demo WATCH...')
    result = client.put('watch_key', 'init_val')
    logger.info("Key PUT watch_key : %r" % result)
    result = client.get('watch_key')
    logger.info("Key GET watch_key : %r" % result)

    logger.info('Watch watch_key')
    watcher, watch_cancel = client.watch(key='watch')
    # watcher, watch_cancel = client.watch_once(key='watch', timeout=10)

    watch_count = 0
    for event in watcher:  # blocks until event comes, cancel via watch_cancel()
        logger.info(event)
        watch_count += 1
        logger.info("Watch count: %s" % watch_count)
        if watch_count > 2:
            watch_cancel()

    logger.info("And now his watch is ended...")


if __name__ == "__main__":
    main()
