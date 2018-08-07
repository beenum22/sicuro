#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Beenum'
__version__ = '3.0'

import argparse
import os
import sys
from src.maestro import Maestro
from src.utilities import Utilities
import logging.config


def main():
    try:
        usage = ('python %prog <add variables here>')
        #workDir = os.path.dirname(os.path.realpath(__file__))
        #bL = 32
        parser = argparse.ArgumentParser(
            description='Maestro is here!', version=__version__)
        parser.add_argument(
            "task",
            help="Select Encryption/Decryption.",
            choices=['E','D']
            )
        parser.add_argument(
            "--save",
            help="Save the decrypted output.",
            action='store_true'
            )
        parser.add_argument(
            "--debug",
            help="Debug mode.",
            action='store_true'
            )
        parser.add_argument(
            "-t", "--target", default=None,
            help="Target file source path."
            )
        parser.add_argument(
            "-k", "--key", default=None,
            help="Key file source path."
            )
        args = parser.parse_args()
        Utilities._create_dir("./logs")
        logging.config.fileConfig(
            'logging.ini', disable_existing_loggers=False)
        maestro_logger = logging.getLogger()
        if args.debug:
            maestro_logger.setLevel('DEBUG')
        maestro = Maestro(32)
        if args.task == 'E':
            maestro.encrypt_maestro(data_path=args.target)
        elif args.task == 'D':
            maestro.decrypt_maestro(data_path=args.target, key_path=args.key, store=args.save)
    except KeyboardInterrupt:
        maestro_logger.error("Interrupted. Exiting...")
        sys.exit()

if __name__ == "__main__":
    main()
