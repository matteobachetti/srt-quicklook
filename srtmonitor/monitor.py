from pandas import read_csv
import numpy as np
import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import warnings
import subprocess as sp
warnings.filterwarnings('ignore')
global CONFIG_FILE


class MyHandler(PatternMatchingEventHandler):
    patterns = ["*.fits"]
    def process(self, event):
        """
        event.event_type
            'modified' | 'created' | 'moved' | 'deleted'
        event.is_directory
            True | False
        event.src_path
            path/to/observed/file
        """
        global CONFIG_FILE
        print(event)
        infile = event.src_path
        sp.check_call(
            "SDTpreprocess --debug {}".format(infile).split())

    def on_created(self, event):
        self.process(event)

    def on_modified(self, event):
        self.process(event)


def main(args=None):
    import argparse
    global CONFIG_FILE

    description = ('Run the SRT quicklook in a given directory.')
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument("directory",
                        help="Directory to monitor",
                        default=None, type=str)
    parser.add_argument("--config",
                        help="Config file",
                        default=None, type=str)
    parser.add_argument("--test",
                        help="Only to be used in tests!",
                        action='store_true', default=False)
    args = parser.parse_args(args)

    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = args.directory
    CONFIG_FILE = args.config

    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        count = 0
        while count < 10:
            time.sleep(1)
            if args.test:
                count += 1
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
