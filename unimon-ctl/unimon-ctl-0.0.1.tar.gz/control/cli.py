# -*- coding: utf-8 -*-
from version import __version__
from controller import UnimonControl

import argparse
import logging

def main():
  logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s || %(message)s')
  controller = UnimonControl(logging.getLogger())

  def check_state(args):
    logging.debug("checking state")
    state = controller.get_router_state(args.get("mechanism"), domain_id, args.get("router_id"))
    if state:
      print("✅  ||| router state ||| \033[1m{}\033[0m".format(state))
      exit(0)
    print("⛔️  ||| router state could not be found")
    exit(1)

  def check_config(args):
    logging.debug("checking config")

  def install_config(args):
    logging.debug("installing config")
    controller.start

  def remove_router(args):
    logging.debug("removing router")

  def start_router(args):
    logging.debug("starting router")

  def stop_router(args):
    logging.debug("stopping router")

  def print_version():
    logging.debug("printing version")
    print("✅  ||| Unimon Control Version ||| \033[1m%s\033[0m" % __version__)

  # Args
  parser = argparse.ArgumentParser(description="Control ClickOS Xen Domains")

  # - Top Level
  parser.add_argument('domain_id', type=int, nargs=1, help="the xen domain id running a clickos image")
  parser.add_argument('--mechanism', type=str, default=controller.DEFAULT_COM_MECH, help="what mechanism to use for inter-domain communication (default: %(default)s)")
  parser.add_argument('--debug', action='store_true', help="enable debug level logging")
  parser.add_argument('--version', action='store_true', help="print the version")
  subparsers = parser.add_subparsers(help='sub-command help')
  state_parser = subparsers.add_parser('state', help="get the state of clickos router")
  check_parser = subparsers.add_parser('config', help="get the current config name on a clickos router")
  install_parser = subparsers.add_parser('install', help="install a click config to a clickos xen domain")
  remove_parser = subparsers.add_parser('remove', help="remove click router from clickos domain")
  start_parser = subparsers.add_parser('start', help="start a clickos router")
  stop_parser = subparsers.add_parser('stop', help="stop a clickos router")

  # -- State
  state_parser.add_argument('router_id', type=int, help="the id of the target clickos router")
  state_parser.set_defaults(func=check_state)

  # -- Config Check
  check_parser.add_argument('router_id', type=int, help="the id of the target clickos router")
  check_parser.set_defaults(func=check_config)

  # -- Install
  install_parser.add_argument('config-path', type=str, help="the path of the .click file to use as the config")
  install_parser.add_argument('-s', action='store_true', help="once config installed, start the clickos router")
  install_parser.add_argument('-f', action='store_true', help="starts the router when installing, removing the previous if required")
  install_parser.set_defaults(func=install_config)

  # -- Remove
  remove_parser.add_argument('router_id', type=int, help="the id of the target router")
  remove_parser.add_argument('-f', action='store_true', help="if router is still running, it will be stopped")
  remove_parser.set_defaults(func=remove_router)

  # -- Start
  start_parser.add_argument('router_id', type=int, help="the id of the target clickos router")
  start_parser.set_defaults(func=start_router)

  # -- Stop
  stop_parser.add_argument('router_id', type=int, help="the id of the target clickos router")
  stop_parser.set_defaults(func=stop_router)

  # Parse
  args = parser.parse_args()
  args_dict = vars(parser.parse_args())
  domain_id = args_dict.get("domain_id", -1)[0]
  if domain_id <= 0:
    logging.fatal("domain id must be greater than 0")
    exit(1)
  do_version = args_dict.get("version", False)
  if do_version:
    print_version()
  is_debug = args_dict.get("debug", False)
  if is_debug:
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s || %(message)s')
    controller.update_logger(logging.getLogger())

  args.func(vars(parser.parse_args()))

main()

