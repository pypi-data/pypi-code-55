import sys,os,logging
from google.cloud import firestore
import traceback

import argparse
import time

from models.conversion import DS_Customer, DS_EmailNotifications, DS_Plants, DS_Product, \
                          DS_Supplier, DS_GrowWeek, DS_PlantGrow, DS_PlantGrowNotes, \
                          DS_PlantGrowSupply, DS_ProductPlant, DS_ProductReserve, Reserve_Summary

def start_conversion(fsProject, dsProject, steps=None):
    if steps is None:
        steps = ['plants','customer','product','supplier','email','growweek','plantgrow','notes','supply','prodplant','prodreserve','summary']

    plts = None
    custs = None
    prods = None
    supps = None
    supps = None
    gws = None
    pgs = None
    prdPlts = None
    prdReserve = None

    if 'plants' in steps:
        logging.info('Processing Plants... ')
        plts = DS_Plants(fsProject,dsProject)

    if 'customer' in steps:
        logging.info('Processing customers... ')
        custs = DS_Customer(fsProject,dsProject)
    
    if 'product' in steps:
        logging.info('Processing products... ')
        prods = DS_Product(fsProject,dsProject)

    if 'supplier' in steps:
        logging.info('Processing suppliers... ')
        supps = DS_Supplier(fsProject,dsProject)

    if 'email' in steps:
        logging.info('Processing emails... ')
        DS_EmailNotifications(fsProject,dsProject)
    
    if 'growweek' in steps:
        logging.info('Processing Grow Week... ')
        gws = DS_GrowWeek(fsProject,dsProject)

    if 'plantgrow' in steps:
        logging.info('Processing Plant Grow... ')
        pgs = DS_PlantGrow(fsProject,dsProject,gws,plts)

    if 'notes' in steps:
        logging.info('Processing Notes... ')
        DS_PlantGrowNotes(fsProject,dsProject,pgs)
    
    if 'supply' in steps:
        logging.info('Processing Supply... ')
        DS_PlantGrowSupply(fsProject,dsProject,pgs,supps)

    if 'prodplant' in steps:
        logging.info('Processing Prod Plants... ')
        prdPlts = DS_ProductPlant(fsProject,dsProject,prods,plts)
    
    if 'prodreserve' in steps:
        logging.info('Processing Reserves... ')
        prdReserve = DS_ProductReserve(fsProject,dsProject,prods,custs,prdPlts, gws)

    if 'summary' in steps:
        logging.info("Processing reserve summary")
        Reserve_Summary(fsProject,dsProject,prdReserve)


def parse_arg(args, arg_num):
    if len(args) > arg_num:
        arg = args[arg_num]
        if arg.startswith("-"):
            arg_dash = arg[1:]
            if arg_dash.lower() == 's' or arg_dash.lower() == 'step':
                return args[arg_num+1],arg_num+2,'step'
            elif arg_dash.lower() == 'ds':
                return args[arg_num+1],arg_num+2,'ds_project'
            elif arg_dash.lower() == 'fs':
                return args[arg_num+1],arg_num+2,'fs_project'
            else:
                logging.info('unknown flag: '+arg)
                return None, arg_num+1,'unknown'
        else:
            return arg,arg_num+1,'project'
    else:
        return None, 0, None

if __name__ == '__main__':
    '''
    You can set the datastore project by using the environment variable DS_PROJECT
    You can set the firestore project by susing the environment variable FS_PROJECT
    .. whatever you set can be overridden by command line args
    Arg 1 = DataStore Project
    Arg 2 = Firestore Project
    
    If you do neither, it will default to the folling:
    DS_PROJECT = 'item-tracking-colororchids'
    FS_PROJECT = 'backend-firestore-test'
    '''
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',level=logging.INFO)
    dsProject = os.environ.get('DS_PROJECT','sales-inv-colororchids')
    fsProject = os.environ.get('FS_PROJECT','backend-firestore-test')
    os.environ['APP_FIRESTORE_NAME'] = 'Customer_Tracking'
    steps = []
    
    arg,num,arg_type = parse_arg(sys.argv,1)
    while arg is not None:
        logging.info("Arg passed: {}, next number: {}, argument type: {}".format(arg,num,arg_type))
        if arg_type == 'fs_project':
            fsProject = arg
        if arg_type == 'ds_project':
            dsProject = arg
        if arg_type == 'step':
            parse_steps = arg.split(",")
            for stp in parse_steps:
                steps.append(stp)
        arg, num,arg_type = parse_arg(sys.argv,num)

    process_steps = steps if len(steps) > 0 else None

    logging.info('converstion to run...')
    start_conversion(fsProject,dsProject,process_steps)