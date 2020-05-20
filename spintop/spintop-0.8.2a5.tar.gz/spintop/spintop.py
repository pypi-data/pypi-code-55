import os
import argparse
from incremental_module_loader import IncrementalModuleLoader

from .auth import AuthModule, FilePathCredentialsStore
from .logs import _logger, setup_logging
from .storage import SITE_DATA_DIR
from .api_client import SpintopAPIClientModule, SpintopAPISpecAuthBootstrap

logger = _logger('root')

def SpintopFactory(
        api_url,
        verbose=False,
        credentials_filepath=None,
        org_id=None,
        messages_publisher=None,
        logs_factory=setup_logging,
        auth_bootstrap_factory=SpintopAPISpecAuthBootstrap,
        credentials_store_factory=FilePathCredentialsStore,
        auth_factory=AuthModule,
        spintop_api_factory=SpintopAPIClientModule,
        final_factory=None
    ):

    loader = IncrementalModuleLoader()
    loader.update(
        api_url=api_url,
        verbose=verbose,
        credentials_filepath=credentials_filepath,
        org_id=org_id,
        messages_publisher=messages_publisher
    )
    
    loader.load(logs=logs_factory)
    loader.load(credentials_store=credentials_store_factory)
    loader.load(auth_bootstrap=auth_bootstrap_factory)
    loader.load(auth=auth_factory)
    spintop_or_final = loader.load(spintop_api=spintop_api_factory)
    

    if final_factory:
        spintop_or_final = loader.load(final_factory)
    
    return spintop_or_final

def SpintopWorkerFactory(worker_cls, **factory_kwargs):
    worker = SpintopFactory(final_factory=worker_cls, **factory_kwargs)
    return worker
        
        
    
    
        