import json, os
import importlib
from tqdm import tqdm
from boto3.session import Session
from aws_audit.config.regions import regions, all_regions
from aws_audit.config.rules import services
from aws_audit.utils.errors import AWSPermissionError, AWSRequestError
from aws_audit.helper.common import CommonHelper

class Initialize:
    
    def __init__(self, config, services, regions, logger):
        self.services = services
        self.regions = regions
        self.logger = logger
        self.config = config

        self.default_session = Session(
            aws_access_key_id= self.config['aws_access_key_id'],
            aws_secret_access_key= self.config['aws_secret_access_key']
        )

        self.enabled_regions = CommonHelper(self.default_session, 'us-east-1', logger).enabled_regions()
        
    def service(self):
        
        if not self.services:
            self.services = services
            
        findings = []
        
        for service in sorted(self.services.keys()):
            
            self.logger.info(f'Evaluting {service} service')            
            
            allowed_regions = []
            service_regions = []
            for region in self.regions:
                if region in regions[service]:
                    allowed_regions.append(region)

            if not len(allowed_regions):
                self.logger.info(f"Setting default regions for the service {service}.")
                service_regions = regions[service]                    
            else:
                service_regions = allowed_regions

            total_regions = len(service_regions)
            total_rules = len(self.services[service])
            
            total_region_rules = total_regions*total_rules

            progress_bar = tqdm(total=total_region_rules)
                
            for region in service_regions:

                progress_bar.set_description(f"Processing {service} for { region }" )
                
                if region not in self.enabled_regions:
                    progress_bar.update(total_rules)
                    continue
                
                self.logger.info(f"Evaluting service for region {region}")
                try:

                    session = Session(
                        aws_access_key_id= self.config['aws_access_key_id'],
                        aws_secret_access_key= self.config['aws_secret_access_key']
                    )

                    module_name = "aws_audit.plugins." + service + "." + service + "handler"
                    class_name = service + "handler"
                    module_object  = importlib.import_module(module_name)
                    class_obj = getattr(module_object, class_name)(session, region, self.logger)
                    
                except Exception as e:
                    self.logger.error(f'Error while plugin initialization for service {service} in region {region} : {e}')
                    continue

                for service_rule in self.services[service]:
                    
                    progress_bar.update(1)

                    finding = {
                        "service": service,
    					"rule": service_rule['rule'],
    					"id": service_rule['id'],
                        "severity": service_rule['severity'],
                        "issue": service_rule['issue'],
                        "resolution": service_rule['resolution'],
    					"status": 'success'
    				}
                    rule_error = None
                    results = {}
    				
                    self.logger.info(f"Evaluting rule {service_rule['rule']}")
                    try:
                        
                        if 'function' not in service_rule:
                            results = getattr(class_obj, service_rule['rule'])()
                        else:
                            results = getattr(class_obj, service_rule['function'])(service_rule['parameters'])
                        
                    except AWSPermissionError as e:
                        self.logger.error(f"Permission Error. Exception in rule {service_rule['rule']}: {e}")
                        finding['status'] = 'failure'
                        rule_error = e

                    except AWSRequestError as e:
                        self.logger.error(f"Exception in rule {service_rule['rule']}: {e}")
                        finding['status'] = 'failure'
                        rule_error = e
                    
                    except Exception as e:
                        self.logger.error(f'Error while execute rule {service_rule["rule"] } for service {service} in region {region} : {e}')
                        finding['status'] = 'failure'
                        rule_error = e
                        
                    if results:
                        finding['result'] = 'failure'
                        finding['data'] = results
                        
                    elif rule_error:
                        finding['result'] = 'failure'
                        finding['data'] = [{'region' : region, "message": f"Failed to run rule: {rule_error}"}]
                    
                    else:
                        finding['result'] = 'success'
                    
                    findings = self.append_result_to_findings(findings, finding)

            progress_bar.set_description(f"Completed for {service}" )
            progress_bar.close()
            print("")
                
        return findings
        
    def append_result_to_findings(self, findings, data):

        for finding in findings:
            if data['rule'] == finding['rule']:
                if data['result'] == 'failure':
                    finding['result'] = 'failure'
                    if 'data' in finding:
                        finding['data'] += data['data']
                    else:
                        finding['data'] = data['data'] 
                return findings

        findings.append(data)

        return findings
