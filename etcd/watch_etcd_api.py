import time
import argparse
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

parser = argparse.ArgumentParser()
parser.add_argument('--watch_key', '-w', type=str, default="watch_key")
parser.add_argument('--old_val', '-ov', type=str, default="init_val")
parser.add_argument('--new_val', '-nv', type=str, default="new_val")
args = parser.parse_args()


def main():
    client = Etcd3Client()

    result = client.status()
    logger.info("cluster id STATUS: %r" % result['header']['cluster_id'])

    result = client.members()
    logger.info("first MEMBER info : %r" % result[0])

    logger.info('demo WATCH...')
    result = client.replace(key=args.watch_key, initial_value=args.old_val, new_value=args.new_val)
    logger.info("Key REPLACE watch_key : %r" % result)


if __name__ == "__main__":
    main()
