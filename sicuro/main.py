#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Beenum'
__version__ = '3.0'

import argparse
import os
import sys
from src.maestro import Maestro
from zizou import Zizou
import logging.config


def main():
    formatter = "%(asctime)s %(name)s - %(levelname)s - %(message)s"
    maestro_logger = logging.getLogger()
    logging.basicConfig(format=formatter)
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
        parser.add_argument(
            "-o", "--output_dir", default="~/sicuro_data/",
            help="Output directory for encrypted/decrypted files"
            )
        args = parser.parse_args()
        if args.debug:
            maestro_logger.setLevel(logging.DEBUG)
            maestro_logger.info("Sicuro log level set to debug")
        else:
            maestro_logger.setLevel(logging.INFO)
        maestro = Maestro(32, output_dir=args.output_dir)
        if args.task == 'E':
            key, e_data = maestro.encrypt_maestro(data_path=args.target)
            maestro.display_output(key=key, data=e_data)
        elif args.task == 'D':
            d_data = maestro.decrypt_maestro(data_path=args.target, key_path=args.key, store=args.save)
            maestro.display_output(data=d_data)
    except KeyboardInterrupt:
        maestro_logger.error("Interrupted. Exiting...")
        sys.exit()

if __name__ == "__main__":
    main()
