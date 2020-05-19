#!/usr/bin/env python3
'''Commandline tool to retrieve and dupmp info stored in regapp based on unix user name stored in bwIDM regApp (aka LDAP Facade)'''
# pylint
# vim: tw=100
# pylint: disable=bad-continuation, invalid-name, superfluous-parens
# pylint: disable=bad-whitespace, mixed-indentation
# pylint: disable=redefined-outer-name, logging-not-lazy, logging-format-interpolation

import os
import json
import logging
import urllib.parse as ul
import requests

from regapp_tools.parse_args import args
from regapp_tools.bwidmtools import external_id_from_subiss, get_external_id_from_username
from regapp_tools.bwidmtools import get_username_from_external_id, get_sshkey_from_external_id
from regapp_tools.bwidmtools import get_userinfo_from_external_id, get_user_registrations_from_external_id
from regapp_tools.bwidmtools import deregister_external_id_from_service, register_external_id_from_service
from regapp_tools.bwidmtools import get_list_of_all_users, deactivate_user, activate_user
from regapp_tools.bwidmconnection import BwIdmConnection
from regapp_tools.bwidm_user import User, Registry


# Logging
# logformat='[%(levelname)s] %(message)s'
logformat='[%(levelname)s] [%(filename)s:%(funcName)s:%(lineno)d] %(message)s'
if args.verbose:
    logformat='[%(levelname)s] [%(filename)s:%(funcName)s:%(lineno)d] %(message)s'
if args.debug:
    try:
        logging.basicConfig(filename="/var/log/ssh-key-retriever.log", level=os.environ.get("LOG", "DEBUG"), format = logformat)
    except PermissionError:
        logging.basicConfig(level=os.environ.get("LOG", "DEBUG"), format = logformat)
else:
    try:
        logging.basicConfig(filename="/var/log/ssh-key-retriever.log", level=os.environ.get("LOG", "INFO"), format = logformat)
    except PermissionError:
        logging.basicConfig(level=os.environ.get("LOG", "INFO"), format = logformat)
logger = logging.getLogger(__name__)


# def get_sshkeys(externalId='hdf_61230996-664f-4422-9caa-76cf086f0d6c@unity-hdf'):
def display_info():
    '''get info from externalId'''
    ##### in case we need user access:
    if args.deregister_from_service or\
        args.register_for_service or\
        args.activate or\
        args.deactivate or\
        args.grp or\
        args.reg or\
        args.ssh or\
        args.info:
        username = ""
        parameter = args.username[0]
        if len(parameter.split('@')) == 2: # we got sub@iss
            external_id = external_id_from_subiss(sub_iss=parameter)
            username = get_username_from_external_id(external_id)

        elif len(parameter.split('@')) == 1: # we got a username
            external_id = get_external_id_from_username(parameter)
            username = parameter
        else:
            logger.error(F"The provided parameter '{args.username}' is neither a username nor a sub@iss")
            raise ValueError()

        try:
            (sub,iss) = external_id.split('@')
            sub = ul.unquote_plus(sub)
            iss = ul.unquote_plus(iss)
        except AttributeError:
            sub = ""
            iss = ""
    
    ##### actions on users
    if args.deactivate:
        print ("Deactivating")
        resp=deactivate_user(external_id)
        if args.verbose:
            print(resp)
        if resp.status_code == 204:
            print ("Success")

    if args.activate:
        print ("Activating")
        resp=activate_user(external_id)
        if args.verbose:
            print(resp)
        if resp.status_code == 204:
            print ("Success")

    if args.deregister_from_service:
        print (F"Deregistering from {args.deregister_from_service}")
        resp=deregister_external_id_from_service(external_id, args.deregister_from_service)
        print (F"Result: {resp['result']}")
        if args.verbose:
            print(json.dumps(resp, sort_keys=True, indent=4, separators=(',', ': ')))

    if args.register_for_service:
        print (F"Registering for {args.deregister_from_service}")
        resp=register_external_id_from_service(external_id, args.register_for_service)
        print (F"{resp['registryStatus']}")
        if args.verbose:
            print(json.dumps(resp, sort_keys=True, indent=4, separators=(',', ': ')))

    ##### Information about users
    if args.info:
        external_user = get_userinfo_from_external_id(external_id)
        user = User(external_user)
        print (user.info(info=True, groups=False, extensive=args.extensive))
        if args.verbose:
            print(json.dumps(external_user, sort_keys=True, indent=4, separators=(',', ': ')))

    if args.grp:
        external_user = get_userinfo_from_external_id(external_id)
        user = User(external_user)
        print (user.info(info=False, groups=True))
        if args.verbose:
            print(json.dumps(external_user, sort_keys=True, indent=4, separators=(',', ': ')))

    if args.reg:
        reg_info      = get_user_registrations_from_external_id(external_id)
        
        if args.verbose:
            print(json.dumps(reg_info, sort_keys=True, indent=4, separators=(',', ': ')))

        for registry in reg_info:
            registry_object = Registry(registry)
            print (registry_object.info(extensive=args.extensive))
            # print (F"{registry['id']} - "\
            #        F"{registry['registryStatus']:13} - "\
            #        F"{registry['lastStatusChange']:30}- "\
            #        F"{registry['createdAt']:30}- "\
            #        F"{registry['serviceShortName']:10}- "\
            #        F"{registry['registryValues']['localUid']:20}"\
            #        )

    if args.ssh:
        sshkeys = get_sshkey_from_external_id(external_id)
        print (sshkeys)

    if args.findall:
        print ("List of all users")
        userlist = get_list_of_all_users()
        # if args.verbose:
        #     print(json.dumps(userlist, sort_keys=True, indent=4, separators=(',', ': ')))
        users = []
        for u in userlist:
            user = User(u)
            print (user.info(extensive=args.extensive))
def main():
    '''Main Program'''
    display_info()
    return 0


if __name__ == "__main__":
    keys = main()
