#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Muneeb Ahmad'
__version__ = '0.1.0'

import argparse
import sys
from .maestro import Maestro
import logging.config
from colorama import Fore, Style
import coloredlogs


def banner():
    print(f"""{Fore.LIGHTMAGENTA_EX}
 _____  _                           
/  ___|(_)                          
\ `--.  _   ___  _   _  _ __   ___  
 `--. \| | / __|| | | || '__| / _ \ 
/\__/ /| || (__ | |_| || |   | (_) |
\____/ |_| \___| \__,_||_|    \___/ 
{Style.RESET_ALL}
{Fore.LIGHTWHITE_EX}
Sicuro is a simple tool to secure your sensitive data using the Advanced Encryption Standard (AES) ciphering
technique.

Copyright 2021 Muneeb Ahmad
{Style.RESET_ALL}""")

def main():
    # formatter = "%(asctime)s %(name)s - %(levelname)s - %(message)s"
    maestro_logger = logging.getLogger()
    coloredlogs.install(fmt="%(asctime)s %(name)s - %(levelname)s - %(message)s", level='DEBUG')
    banner()
    try:
        usage = ('python %prog <add variables here>')
        parser = argparse.ArgumentParser(
            prog="sicuro",
            description="Lock/unlock your sensitive data using Sicuro.")
        parser.add_argument(
            "--version",
            action="version",
            help="Print Sicuro version",
            version="%(prog)s " + __version__
            )
        parser.add_argument(
            "--save",
            help="Save the decrypted output.",
            action="store_true"
            )
        parser.add_argument(
            "--debug",
            help="Debug mode.",
            action="store_true"
            )
        parser.add_argument(
            "-t",
            "--target",
            default=None,
            help="Target file source path or target string"
            )
        parser.add_argument(
            "-k",
            "--key",
            default=None,
            help="Key file source path."
            )
        parser.add_argument(
            "-o", "--output_dir", default="~/sicuro_data/",
            help="Output directory for encrypted/decrypted files"
            )
        crypto_group = parser.add_mutually_exclusive_group()
        crypto_group.add_argument(
            "-e",
            "--encrypt",
            help="Encrypt target",
            action="store_true"
            )
        crypto_group.add_argument(
            "-d",
            "--decrypt",
            help="Decrypt target",
            action="store_true"
            )
        args = parser.parse_args()
        if args.debug:
            maestro_logger.setLevel(logging.DEBUG)
            maestro_logger.info("Sicuro log level set to debug")
        else:
            maestro_logger.setLevel(logging.INFO)
        maestro = Maestro(key=args.key, key_byte_size=32, output_dir=args.output_dir)
        if args.encrypt:
            e_data = maestro.lock_data(data_path=args.target, store=args.save)
            maestro.display_key()
            maestro.display_data(e_data)
        elif args.decrypt:
            d_data = maestro.unlock_data(data_path=args.target, store=args.save)
            maestro.display_data(d_data)
    except Exception as err:
        maestro_logger.error("Something went wrong!. Exception(%s). Exiting..." % err)
    except KeyboardInterrupt:
        maestro_logger.error("Interrupted. Exiting...")
        sys.exit()

if __name__ == "__main__":
    main()