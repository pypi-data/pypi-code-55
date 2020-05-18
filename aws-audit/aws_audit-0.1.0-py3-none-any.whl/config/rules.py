import os

services = {
    "acm": [
        {
            "rule" : "expired_certificates",
            "id" : "ACM_001", 
            "severity" : "high",
            "issue": "AWS ACM Certificates are expired.",
            "resolution" : "Ensure expired SSL/TLS certificates are removed from AWS Certificate Manager (ACM)."
        },
        {
            "rule": "certificates_expires_in_30_days",
            "severity": "medium",
            "id" : "ACM_002",
            "issue": "ACM Certificates are about to expires in 30 days.",
            "resolution": "Ensure Amazon Certificate Manager (ACM) certificates are renewed before their expiration."
        },
        {
            "rule": "certificates_with_wildcard_domain",
            "severity": "low",
            "id" : "ACM_003",
            "issue": "ACM Certificate issued for wildcard domain.",
            "resolution" : "Ensure that wildcard certificates issued by Amazon Certificate Manager (ACM) or imported to ACM are not in use."
        }
    ],
    "kms": [
        {
            "rule" : "kms_key_exposed",
            "id" : "KMS_001",
            "severity" : "high",
            "issue": "KMS Key is exposed to everyone.",
            "resolution" : "Ensure Amazon KMS master keys are not exposed to everyone."
        },
        {
            "rule" : "kms_key_rotation_not_enabled",
            "id" : "KMS_002",
            "severity" : "medium",
            "issue": "KMS Key rotation is not enabled",
            "resolution" : "Ensure KMS key rotation feature is enabled for all your Customer Master Keys (CMK)."
        },
        {
            "rule" : "kms_key_scheduled_for_deletion",
            "id" : "KMS_003",
            "severity" : "medium",
            "issue": "KMS key is scheduled for deleteion. It may impact services if key is in use.",
            "resolution" : "Identify any KMS Customer Master Keys (CMK) scheduled for deletion."
        },
        {
            "rule" : "kms_key_cross_account_access",
            "id" : "KMS_004",
            "severity" : "high",
            "issue": "KMS Key allows cross account access.",
            "resolution" : "Ensure Amazon KMS master keys do not allow unknown cross account access."
        }
    ],
    "secretsmanager": [
        {
            "rule" : "secret_not_encrypted_with_kms_cmk",
            "id" : "SECRETSMANAGER_001",
            "severity" : "high",
            "issue": "Secret is not encrypted with KMS CMK.",
            "resolution" : "Ensure that AWS Secrets Manager service enforces data-at-rest encryption using KMS CMKs."
        },
        {
            "rule" : "secret_rotation_not_enabled",
            "id" : "SECRETSMANAGER_002",
            "severity" : "medium",
            "issue": "Secret rotation is not enabled.",
            "resolution" : "Ensure that automatic rotation is enabled for your Amazon Secrets Manager secrets."
        },
        {
            "rule" : "secret_rotation_interval_not_configured",
            "id" : "SECRETSMANAGER_003",
            "severity" : "medium",
            "issue": "Secret rotation interval is not configured.",
            "resolution" : "Ensure that Amazon Secrets Manager automatic rotation interval is properly configured."
        }
    ],
    "route53": [
        {
            "rule" : "route53domain_privacy_protection_not_enabled",
            "id" : "ROUTE53_001",
            "severity" : "low",
            "issue": "Privacy protection is not enabled for Route53 Domains.",
            "resolution" : "Ensure that Privacy Protection feature is enabled for your Amazon Route 53 domains."
        },
        {
            "rule" : "route53_spf_record_not_present",
            "id" : "ROUTE53_002",
            "severity" : "medium",
            "issue": "SPF record is not present for Hosted Zones.",
            "resolution" : "Ensure there is an SPF record set for each MX DNS record in order to stop spammers from spoofing your domains."
        },
        {
            "rule" : "route53domain_transfter_lock_not_enabled",
            "id" : "ROUTE53_003",
            "severity" : "medium",
            "issue": "Transfer lock is not enabled for Route53 Domains.",
            "resolution" : "Ensure your domain names have the Transfer Lock feature enabled in order to keep them secure."
        }
    ],
    "ec2" : [
        {
            "rule" : "ami_not_encrypted",
            "id" : "EC2_001",
            "severity" : "high",
            "issue": "AMI is not encrypted.",
            "resolution" : "Ensure that your AMI is encrypted."
        },
        {
            "rule" : "ami_publicly_shared",
            "id" : "EC2_002",
            "severity" : "medium",
            "issue": "AMI is publicly shared. Your data on AMI is accessible to everyone.",
            "resolution" : "Ensure AMI is not publicly shared."
        },
        {
            "rule" : "default_security_group_unrestricted",
            "id" : "EC2_003",
            "severity" : "medium",
            "issue": "EC2 Default security groups are unrestricted.",
            "resolution" : "Ensure that your AWS EC2 default security groups restrict all inbound public traffic in order to enforce AWS users (EC2 administrators, resource managers, etc) to create custom security groups that exercise the rule of least privilege instead of using the default security groups."
        },
        {
            "rule" : "default_security_group_inuse",
            "id" : "EC2_004",
            "severity" : "medium",
            "issue": "Default EC2 security group is in use.",
            "resolution" : "Ensure default EC2 security groups are not in use in order to follow AWS security best practices."
        },
        {
            "rule" : "security_groups_rule_description_not_present",
            "id" : "EC2_005",
            "severity" : "low",
            "issue": "Security groups rule description not present.",
            "resolution" : "Ensure that all the rules defined for your Amazon EC2 security groups have a description to help simplify your operations and remove any opportunities for operator errors."
        },
        {
            "rule" : "ami_too_old",
            "id" : "EC2_006",
            "severity" : "low",
            "issue": "Your account has too old AMI.",
            "resolution" : "Ensure that your existing AWS Amazon Machine Images (AMIs) are not older than 180 days in order to ensure their reliability and to meet security and compliance requirements."
        },
        {
            "rule" : "ec2_instance_not_in_vpc",
            "id" : "EC2_007",
            "severity" : "medium",
            "issue": "EC2 instance not in VPC",
            "resolution" : "Ensure EC2 instances are launched using the EC2-VPC platform instead of EC2-Classic outdated platform."
        },
        {
            "rule" : "ec2_instances_not_using_iam_role",
            "id" : "EC2_008",
            "severity" : "medium",
            "issue": "EC2 instances are not using IAM role.",
            "resolution" : "Use Instance Profiles/IAM Roles to appropriately grant permissions to applications running on amazon EC2 instances"
        },
        {
            "rule" : "security_group_prefixed_with_launch_wizard",
            "id" : "EC2_009",
            "severity" : "low",
            "issue": "EC2 security groups prefixed with 'launch-wizard'.",
            "resolution" : "Ensure EC2 security groups prefixed with 'launch-wizard' are not in use in order to follow AWS security best practices."
        },
        {
            "rule" : "security_group_open_port_range",
            "id" : "EC2_010",
            "severity" : "medium",
            "issue": "EC2 Security groups opening wide port range to allow inbound traffic.",
            "resolution" : "Ensure that your security groups don't have range of ports opened for inbound traffic in order to protect your EC2 instances against denial-of-service (DoS) attacks or brute-force attacks."
        },
        {
            "rule" : "unrestricted_cifs_access",
            "id" : "EC2_011",
            "severity" : "medium",
            "issue": "EC2 security group allows unrestricted inbound access for TCP port 445.",
            "resolution" : "Ensure no AWS EC2 security group allows unrestricted inbound access to TCP port 445 and (CIFS).",
            "function" : "find_unrestricted_open_ports",
            "parameters" : {
                "ports" : [445]
            }

        },
        {
            "rule" : "unrestricted_dns_access",
            "id" : "EC2_012",
            "severity" : "medium",
            "issue": "EC2 security group allows unrestricted inbound access for TCP port 53.",
            "resolution" : "Ensure no AWS EC2 security group allows unrestricted inbound access to TCP port 53 (DNS).",
            "function" : "find_unrestricted_open_ports",
            "parameters" : {
                "ports" : [53]
            }
        },
        {
            "rule" : "unrestricted_elasticsearch_access",
            "id" : "EC2_013",
            "severity" : "medium",
            "issue": "EC2 security group allows unrestricted inbound access for TCP port 9200.",
            "resolution" : "Ensure no AWS EC2 security group allows unrestricted inbound access to TCP port 9200 (Elasticsearch).",
            "function" : "find_unrestricted_open_ports",
            "parameters" : {
                "ports" : [9200]
            }
        },
        {
            "rule" : "unrestricted_ftp_access",
            "id" : "EC2_014",
            "severity" : "medium",
            "issue": "EC2 security group allows unrestricted inbound access for TCP port 20 and 21.",
            "resolution" : "Ensure no AWS EC2 security group allows unrestricted inbound access to TCP port 20 and 21 (FTP).",
            "function" : "find_unrestricted_open_ports",
            "parameters" : {
                "ports" : [20,21]
            }
        },
        {
            "rule" : "unrestricted_http_access",
            "id" : "EC2_015",
            "severity" : "medium",
            "issue": "EC2 security group allows unrestricted inbound access for TCP port 80.",
            "resolution" : "Ensure no AWS EC2 security group allows unrestricted inbound access to TCP port 80 (HTTP).",
            "function" : "find_unrestricted_open_ports",
            "parameters" : {
                "ports" : [80]
            }

        },
        {
            "rule" : "unrestricted_https_access",
            "id" : "EC2_016",
            "severity" : "medium",
            "issue": "EC2 security group allows unrestricted inbound access for TCP port 443.",
            "resolution" : "Ensure no AWS EC2 security group allows unrestricted inbound access to TCP port 443 (HTTPS).",
            "function" : "find_unrestricted_open_ports",
            "parameters" : {
                "ports" : [443]
            }
        },
        {
            "rule" : "unrestricted_icmp_access",
            "id" : "EC2_017",
            "severity" : "medium",
            "issue": "EC2 security group allows unrestricted inbound access for ICMP.",
            "resolution" : "Ensure no security group allows unrestricted inbound access using Internet Control Message Protocol (ICMP).",
            "function" : "find_unrestricted_open_ports",
            "parameters" : {
                "ports" : ['icmp']
            }
        },
        {
            "rule" : "unrestricted_mangodb_access",
            "id" : "EC2_018",
            "severity" : "medium",
            "issue": "EC2 security group allows unrestricted inbound access for TCP port 27017.",
            "resolution" : "Ensure no security group allows unrestricted ingress access to MongoDB port 27017",
            "function" : "find_unrestricted_open_ports",
            "parameters" : {
                "ports" : [27017]
            }
        },
        {
            "rule" : "unrestricted_mssql_access",
            "id" : "EC2_019",
            "severity" : "medium",
            "issue": "EC2 security group allows unrestricted inbound access for TCP port 1433.",
            "resolution" : "Ensure no security group allows unrestricted inbound access to TCP port 1433 (MSSQL).",
            "function" : "find_unrestricted_open_ports",
            "parameters" : {
                "ports" : [1433]
            }
        },
        {
            "rule" : "unrestricted_mysql_access",
            "id" : "EC2_020",
            "severity" : "medium",
            "issue": "EC2 security group allows unrestricted inbound access for TCP port 3306.",
            "resolution" : "Ensure no security group allows unrestricted inbound access to TCP port 3306 (MySQL).",
            "function" : "find_unrestricted_open_ports",
            "parameters" : {
                "ports" : [3306]
            }
        },
        {
            "rule" : "unrestricted_netbios_access",
            "id" : "EC2_021",
            "severity" : "medium",
            "issue": "EC2 security group allows unrestricted inbound access for TCP port 137, 138, and 139.",
            "resolution" : "Ensure no AWS EC2 security group allows unrestricted inbound access to TCP port 139 and UDP ports 137 and 138 (NetBIOS).",
            "function" : "find_unrestricted_open_ports",
            "parameters" : {
                "ports" : [137,138,139]
            }
        },
        {
            "rule" : "unrestricted_oracle_access",
            "id" : "EC2_022",
            "severity" : "medium",
            "issue": "EC2 security group allows unrestricted inbound access for TCP port 1521.",
            "resolution" : "Ensure no security group allows unrestricted inbound access to TCP port 1521 (Oracle Database).",
            "function" : "find_unrestricted_open_ports",
            "parameters" : {
                "ports" : [1521]
            }
        },
        {
            "rule" : "unrestricted_outbound_access_for_all_ports",
            "id" : "EC2_023",
            "severity" : "medium",
            "issue": "EC2 security group allows unrestricted outbound access for all ports.",
            "resolution" : "Ensure that your EC2 security groups do not allow unrestricted outbound/egress access."
        },
        {
            "rule" : "unrestricted_postgresql_access",
            "id" : "EC2_024",
            "severity" : "medium",
            "issue": "EC2 security group allows unrestricted inbound access for TCP port 5432.",
            "resolution" : "Ensure no security group allows unrestricted inbound access to TCP port 5432 (PostgreSQL Database).",
            "function" : "find_unrestricted_open_ports",
            "parameters" : {
                "ports" : [5432]
            }
        },
        {
            "rule" : "unrestricted_rdp_access",
            "id" : "EC2_025",
            "severity" : "medium",
            "issue": "EC2 security group allows unrestricted inbound access for TCP port 3389.",
            "resolution" : "Ensure no AWS EC2 security group allows unrestricted inbound access to TCP port 3389 (RDP).",
            "function" : "find_unrestricted_open_ports",
            "parameters" : {
                "ports" : [3389]
            }
        },
        {
            "rule" : "unrestricted_rpc_access",
            "id" : "EC2_026",
            "severity" : "medium",
            "issue": "EC2 security group allows unrestricted inbound access for TCP port 135.",
            "resolution" : "Ensure no security group allows unrestricted inbound access to TCP port 135 (RPC).",
            "function" : "find_unrestricted_open_ports",
            "parameters" : {
                "ports" : [135]
            }
        },
        {
            "rule" : "unrestricted_smtp_access",
            "id" : "EC2_027",
            "severity" : "medium",
            "issue": "EC2 security group allows unrestricted inbound access for TCP port 25.",
            "resolution" : "Ensure no AWS EC2 security group allows unrestricted inbound access to TCP port 25 (SMTP).",
            "function" : "find_unrestricted_open_ports",
            "parameters" : {
                "ports" : [25]
            }
        },
        {
            "rule" : "unrestricted_ssh_access",
            "id" : "EC2_028",
            "severity" : "medium",
            "issue": "EC2 security group allows unrestricted inbound access for TCP port 22.",
            "resolution" : "Ensure no AWS EC2 security group allows unrestricted inbound access to TCP port 22 (SSH).",
            "function" : "find_unrestricted_open_ports",
            "parameters" : {
                "ports" : [22]
            }
        },
        {
            "rule" : "unrestricted_telnet_access",
            "id" : "EC2_029",
            "severity" : "medium",
            "issue": "EC2 security group allows unrestricted inbound access for TCP port 23.",
            "resolution" : "Ensure no AWS EC2 security group allows unrestricted inbound access to TCP port 23 (Telnet).",
            "function" : "find_unrestricted_open_ports",
            "parameters" : {
                "ports" : [23]
            }
        },
        {
            "rule" : "unrestricted_kibana_access",
            "id" : "EC2_030",
            "severity" : "medium",
            "issue": "EC2 security group allows unrestricted inbound access for TCP port 5601.",
            "resolution" : "Ensure no AWS EC2 security group allows unrestricted inbound access to TCP port 5601 (Kibana).",
            "function" : "find_unrestricted_open_ports",
            "parameters" : {
                "ports" : [5601]
            }
        },
        {
            "rule" : "unrestricted_vnc_client_access",
            "id" : "EC2_031",
            "severity" : "medium",
            "issue": "EC2 security group allows unrestricted inbound access for TCP port 5500.",
            "resolution" : "Ensure no AWS EC2 security group allows unrestricted inbound access to TCP port 5500  (VNC Client).",
            "function" : "find_unrestricted_open_ports",
            "parameters" : {
                "ports" : [5500]
            }
        },
        {
            "rule" : "unrestricted_vnc_server_access",
            "id" : "EC2_032",
            "severity" : "medium",
            "issue": "EC2 security group allows unrestricted inbound access for TCP port 5900.",
            "resolution" : "Ensure no AWS EC2 security group allows unrestricted inbound access to TCP port 5900 (VNC Server).",
            "function" : "find_unrestricted_open_ports",
            "parameters" : {
                "ports" : [5900]
            }
        },
        {
            "rule" : "unrestricted_hadoop_namenode_access",
            "id" : "EC2_033",
            "severity" : "medium",
            "issue": "EC2 security group allows unrestricted inbound access for TCP port 8020.",
            "resolution" : "Ensure no AWS EC2 security group allows unrestricted inbound access to TCP port 8020 (Hadoop HDFS NameNode).",
            "function" : "find_unrestricted_open_ports",
            "parameters" : {
                "ports" : [8020]
            }
        },
        {
            "rule" : "unrestricted_hadoop_namenode_webui_access",
            "id" : "EC2_034",
            "severity" : "medium",
            "issue": "EC2 security group allows unrestricted inbound access for TCP port 50070 and 50470.",
            "resolution" : "Ensure no AWS EC2 security group allows unrestricted inbound access to TCP port 50070 and 50470 (Hadoop/HDFS NameNode WebUI).",
            "function" : "find_unrestricted_open_ports",
            "parameters" : {
                "ports" : [50070,50470]
            }
        },
        {
            "rule" : "unused_key_pairs",
            "id" : "EC2_035",
            "severity" : "medium",
            "issue": "Unused key pairs present",
            "resolution" : "Ensure unused AWS EC2 key pairs are decommissioned to follow AWS security best practices."
        },
        {
            "rule" : "ebs_public_snapshot",
            "id" : "EC2_036",
            "severity" : "high",
            "issue": "EBS Volume snapshots are public.",
            "resolution" : "Ensure that your Amazon EBS volume snapshots are not accessible to all AWS accounts."
        },
        {
            "rule" : "ebs_volume_not_encrypted",
            "id" : "EC2_037",
            "severity" : "high",
            "issue": "EBS volumes are not encrypted",
            "resolution" : "Ensure that existing Elastic Block Store (EBS) attached volumes are encrypted to meet security and compliance requirements."
        },
        {
            "rule" : "ebs_volume_not_encrypted_with_kms_cmk",
            "id" : "EC2_038",
            "severity" : "high",
            "issue": "EBS volumes are not encrypted with KMS CMK.",
            "resolution" : "Ensure EBS volumes are encrypted with KMS CMKs in order to have full control over data encryption and decryption."
        },
        {
            "rule" : "ebs_snapshot_not_encrypted",
            "id" : "EC2_039",
            "severity" : "medium",
            "issue": "EBS snapshots are not encrypted.",
            "resolution" : "Ensure Amazon EBS snapshots are encrypted to meet security and compliance requirements."
        },
        {
            "rule" : "vpc_endpoint_cross_account_access_enabled",
            "id" : "EC2_040",
            "severity" : "medium",
            "issue": "VPC enpoints allows cross account access.",
            "resolution" : "Ensure Amazon VPC endpoints do not allow unknown cross account access."
        },
        {
            "rule" : "vpc_endpoint_exposed",
            "id" : "EC2_041",
            "severity" : "medium",
            "issue": "VPC endpoints are exposed to everyone.",
            "resolution" : "Ensure Amazon VPC endpoints are not exposed to everyone."
        },
        {
            "rule" : "vpc_flowlog_not_enabled",
            "id" : "EC2_042",
            "severity" : "low",
            "issue": "VPC Flow Log is not enabled.",
            "resolution" : "Ensure Virtual Private Cloud (VPC) Flow Logs feature is enabled in all applicable AWS regions."
        },
        {
            "rule" : "default_vpc_exists",
            "id" : "EC2_043",
            "severity" : "medium",
            "issue": "Default VPC exists.",
            "resolution" : "Determines whether the default VPC exists."
        }
    ],
    "rds": [
        {
            "rule" : "rds_public_snapshot",
            "id" : "RDS_001",
            "severity" : "high",
            "issue": "RDS Database snapshots are publicly accessible.",
            "resolution" : "Ensure that your Amazon RDS database snapshots are not accessible to all AWS accounts."
        },
        {
            "rule" : "rds_aurora_deletion_protection_not_enabled",
            "id" : "RDS_002",
            "severity" : "medium",
            "issue": "RDS Aurora database deletetion protection feature is not enabled.",
            "resolution" : "Ensure that Deletion Protection feature is enabled for your Aurora database clusters (provisioned and serverless)."
        },
        {
            "rule" : "rds_log_export_not_enabled",
            "id" : "RDS_003",
            "severity" : "low",
            "issue": "RDS Log exports feature is not enabled.",
            "resolution" : "Ensure Log Exports feature is enabled for your AWS RDS MySQL, Aurora and MariaDB database instances."
        },
        {
            "rule" : "rds_aurora_serverless_log_exports_not_enabled",
            "id" : "RDS_004",
            "severity" : "low",
            "issue": "Log exports features is not enabled for Aurora Serverless databases.",
            "resolution" : "Ensure Log Exports feature is enabled for your Amazon Aurora Serverless databases."
        },
        {
            "rule" : "rds_iam_authentication_not_enabled",
            "id" : "RDS_005",
            "severity" : "medium",
            "issue": "IAM database authentication feature is not enabled.",
            "resolution" : "Ensure IAM Database Authentication feature is enabled for your AWS RDS MySQL and PostgreSQL database instances."
        },
        {
            "rule" : "rds_deletion_protection_not_enabled",
            "id" : "RDS_006",
            "severity" : "medium",
            "issue": "RDS deletetion protection is not enabled for database instances.",
            "resolution" : "Ensure Deletion Protection feature is enabled for your AWS RDS database instances."
        },
        {
            "rule" : "rds_auto_minor_version_upgrade_not_enabled",
            "id" : "RDS_007",
            "severity" : "medium",
            "issue": "RDS auto minor version upgrade is not enabled.",
            "resolution" : "Ensure AWS RDS instances have the Auto Minor Version Upgrade feature enabled."
        },
        {
            "rule" : "rds_default_port_using",
            "id" : "RDS_008",
            "severity" : "low",
            "issue": "RDS insatnces are using default ports.",
            "resolution" : "Ensure Amazon RDS database instances are not using the default ports."
        },
        {
            "rule" : "rds_not_encypted_with_kms_cmk",
            "id" : "RDS_009",
            "severity" : "high",
            "issue": "RDS instances are not encypted with KMS CMK.",
            "resolution" : "Ensure RDS instances are encrypted with KMS CMKs in order to have full control over data encryption and decryption."
        },
        {
            "rule" : "rds_encryption_not_enabled",
            "id" : "RDS_0010",
            "severity" : "high",
            "issue": "RDS instances are not encrypted.",
            "resolution" : "Ensure AWS RDS instances are encrypted to meet security and compliance requirements."
        },
        {
            "rule" : "rds_publicly_accessible",
            "id" : "RDS_0011",
            "severity" : "high",
            "issue": "RDS instance is publicly accessible.",
            "resolution" : "Ensure RDS database instances are not publicly accessible and prone to security risks."
        },
        {
            "rule" : "rds_unrestricted_security_group",
            "id" : "RDS_0012",
            "severity" : "medium",
            "issue": "Unrestricted security groups assign to RDS Instances.",
            "resolution" : "Ensure there aren’t any unrestricted DB security groups assigned to your RDS instances."
        },
        {
            "rule" : "rds_snapshot_not_encrypted",
            "id" : "RDS_0013",
            "severity" : "high",
            "issue": "RDS Database snapshots are not encrypted.",
            "resolution" : "Ensure that your Amazon RDS database snapshots are encrypted."
        },
    ],
    "es": [
        {
            "rule" : "es_domain_not_encypted_kms_cmk",
            "id" : "ES_001",
            "severity" : "high",
            "issue": "AWS ElasticSearch domains are not encrypted with KMS Customer Master Keys.",
            "resolution" : "Ensure AWS ElasticSearch domains are encrypted with KMS Customer Master Keys."
        },
        {
            "rule" : "es_node_to_node_encyption_not_enabled",
            "id" : "ES_002",
            "severity" : "high",
            "issue": "Node to Node encryption is not enabled for ES clusters.",
            "resolution" : "Ensure node-to-node encryption is enabled for your Amazon ElasticSearch (ES) clusters."
        },
        {
            "rule" : "es_allow_cross_account_access",
            "id" : "ES_003",
            "severity" : "high",
            "issue": "ES Clusters are allowed cross account access.",
            "resolution" : "Ensure Amazon Elasticsearch clusters do not allow unknown cross account access."
        },
        {
            "rule" : "es_domain_exposed_to_everyone",
            "id" : "ES_004",
            "severity" : "high",
            "issue": "ES Domains are exposed to everyone.",
            "resolution" : "Ensure Amazon Elasticsearch Service (ES) domains are not exposed to everyone."
        },
        {
            "rule" : "es_domain_not_in_vpc",
            "id" : "ES_005",
            "severity" : "medium",
            "issue": "ES Domains are not in VPC.",
            "resolution" : "Ensure AWS Elasticsearch domains are accessible from a Virtual Private Cloud (VPC)."
        },
        {
            "rule" : "es_domain_encyption_at_rest_not_enabled",
            "id" : "ES_006",
            "severity" : "high",
            "issue": "ES domains are not encrypted at-rest.",
            "resolution" : "Ensure at-rest encryption is enabled for your Amazon ElasticSearch domains."
        },
        {
            "rule" : "es_domain_not_enforcing_https_connections",
            "id" : "ES_007",
            "severity" : "high",
            "issue": "ES Domains are not enforcing HTTPS connections.",
            "resolution" : "Ensures ElasticSearch domains are configured to enforce HTTPS connections."
        }
    ],
    "elbv2": [
        {
            "rule" : "elb_not_using_https_listener",
            "id" : "ELBV2_001",
            "severity" : "medium",
            "issue": "Application load balancer not using HTTPS listener.",
            "resolution" : "Ensure that your Application Load Balancer (ALB) listeners are using a secure protocol such as HTTPS."
        },
        {
            "rule" : "elb_logging_not_enabled",
            "id" : "ELBV2_002",
            "severity" : "medium",
            "issue": "ALB Access logging in not enabled",
            "resolution" : "Ensure access logging is enabled for your AWS ALBs to follow security best practices."
        },
        {
            "rule" : "elb_waf_not_enabled",
            "id" : "ELBV2_003",
            "severity" : "medium",
            "issue": "WAF is not configured for ALBs",
            "resolution" : "Ensure that all Application Load Balancers have WAF enabled."
        },
        {
            "rule" : "elb_using_insecure_ciphers",
            "id" : "ELBV2_004",
            "severity" : "medium",
            "issue": "ALBs are using insecure ciphers.",
            "resolution" : "Ensure your ELBs do not use insecure or deprecated SSL ciphers."
        },
        {
            "rule" : "elb_invalid_http_header_dropped_not_enabled",
            "id" : "ELBV2_005",
            "severity" : "medium",
            "issue": "ALBs Invalid HTTP header dropped feature is not enabled.",
            "resolution" : "Ensure invalid HTTP header dropped for ELB's."
        },
        {
            "rule" : "elb_deletion_protection_not_enabled",
            "id" : "ELBV2_006",
            "severity" : "medium",
            "issue": "ALB deletion protection is not enabled.",
            "resolution" : "Ensure that elb deletion protection is enabled."
        }
    ],
    "firehose": [
        {
            "rule" : "firehose_delivery_stream_source_records_not_encrypted",
            "id" : "FIREHOSE_001",
            "severity" : "high",
            "issue": "Firehose delivery stream source records are not encrypted.",
            "resolution" : "Ensure Amazon Kinesis Firehose delivery streams enforce Server-Side Encryption (SSE) for source records."
        },
        {
            "rule" : "firehose_delivery_stream_s3_destination_not_encrypted",
            "id" : "FIREHOSE_002",
            "severity" : "high",
            "issue": "Firehose delivery stream S3 destination is not encrypted.",
            "resolution" : "Ensure Amazon Kinesis Firehose delivery streams enforce encryption for s3 destination."
        }
    ],
    "fsx": [
        {
            "rule" : "fsx_not_using_kms_cmk",
            "id" : "FSX_001",
            "severity" : "medium",
            "issue": "FSx for Windows File Server file systems are not encrypted using AWS KMS CMks",
            "resolution" : "Ensure AWS FSx for Windows File Server file systems data is encrypted using AWS KMS CMKs."
        }
    ],
    "kinesis": [
        {
            "rule" : "kinesis_server_side_encryption_not_enabled",
            "id" : "KINESIS_001",
            "severity" : "high",
            "issue": "Kinesis streams are not using server side encryption.",
            "resolution" : "Ensure Amazon Kinesis streams enforce Server-Side Encryption (SSE)."
        },
        {
            "rule" : "kinesis_stream_not_encrypted_with_cmk",
            "id" : "KINESIS_002",
            "severity" : "high",
            "issue": "Kinesis streams are not encrypted using KMS CMK.",
            "resolution" : "Ensure AWS Kinesis streams are encrypted with KMS Customer Master Keys for complete control over data encryption and decryption."
        }
    ],
    "mq": [
        {
            "rule" : "mq_log_export_not_enabled",
            "id" : "MQ_001",
            "severity" : "low",
            "issue": "MQ brokers log export feature is not enabled.",
            "resolution" : "Ensure Log Exports feature is enabled for your Amazon MQ brokers."
        },
        {
            "rule" : "mq_broker_publicaly_accessible",
            "id" : "MQ_002",
            "severity" : "medium",
            "issue": "MQ Brokers are publicly accessible.",
            "resolution" : "Ensure Amazon MQ brokers are not publicly accessible and prone to security risks."
        },
        {
            "rule" : "mq_broker_auto_minor_version_upgrade_not_enabled",
            "id" : "MQ_003",
            "severity" : "medium",
            "issue": "MQ brokers, auto minor version upgrade feature is not enabled.",
            "resolution" : "Ensure AWS MQ brokers have the Auto Minor Version Upgrade feature enabled."
        }
    ],
    "ses": [
        {
            "rule" : "ses_dkim_not_enabled",
            "id" : "SES_001",
            "severity" : "low",
            "issue": "SES DKIM is not enabled.",
            "resolution" : "Ensure DKIM signing is enabled in AWS SES to protect email senders and receivers against phishing."   
        },
        {
            "rule" : "ses_identities_exposed",
            "id" : "SES_002",
            "severity" : "high",
            "issue": "SES identities are exposed to everyone.",
            "resolution" : "Ensure that your AWS SES identities (domains and/or email addresses) are not exposed to everyone."   
        },
        {
            "rule" : "ses_identities_allow_cross_account_access",
            "id" : "SES_003",
            "severity" : "high",
            "issue": "SES identities allows cross account access.",
            "resolution" : "Ensure that AWS SES identities (domains and/or email addresses) do not allow cross-account access via authorization policies."   
        }
    ],
    "sns": [
        {
            "rule" : "sns_topics_not_encrypted",
            "id" : "SNS_001",
            "severity" : "high",
            "issue": "SNS topics are not encrypted.",
            "resolution" : "Ensure that Amazon SNS topics enforce Server-Side Encryption (SSE)."
        },
        {
            "rule" : "sns_topics_not_encrypted_with_kms_cmk",
            "id" : "SNS_002",
            "severity" : "high",
            "issue": "SNS topics are not encrypted with KMS CMK.",
            "resolution" : "Ensure that Amazon SNS topics are encrypted with KMS Customer Master Keys (CMKs)."
        },
        {
            "rule" : "sns_topic_is_exposed",
            "id" : "SNS_003",
            "severity" : "high",
            "issue": "SNS topics are exposed to everyone.",
            "resolution" : "Ensure that AWS Simple Notification Service (SNS) topics are not exposed to everyone."
        },
        {
            "rule" : "sns_topic_have_cross_account_access",
            "id" : "SNS_004",
            "severity" : "high",
            "issue": "SNS topics allows cross account access",
            "resolution" : "Ensure Amazon SNS topics do not allow unknown cross account access."
        },
        {
            "rule" : "sns_topic_using_insecure_subscription",
            "id" : "SNS_005",
            "severity" : "medium",
            "issue": "SNS topics are using insecure subscription.",
            "resolution" : "Ensure Amazon SNS topics shouldn’t have plain HTTP subscription"
        },
        {
            "rule" : "sns_topic_allows_eveyone_to_publish",
            "id" : "SNS_006",
            "severity" : "medium",
            "issue": "SNS topics allows everyone to publish.",
            "resolution" : "Ensure SNS topics do not allow 'Everyone' to publish."
        },
        {
            "rule" : "sns_topic_allows_eveyone_to_subscribe",
            "id" : "SNS_007",
            "severity" : "medium",
            "issue": "SNS topics allows everyone to subscribe.",
            "resolution" : "Ensure SNS topics do not allow 'Everyone' to subscribe."
        }
    ],
    "sqs": [
        {
            "rule" : "sqs_queue_server_side_encryption_not_enabled",
            "id" : "SQS_001",
            "severity" : "high",
            "issue": "SQS queues are enforcing server side encryption",
            "resolution" : "Ensure Amazon SQS queues enforce Server-Side Encryption (SSE)."
        },
        {
            "rule" : "sqs_queue_not_encypted_with_kms_cmk",
            "id" : "SQS_002",
            "severity" : "high",
            "issue": "SQS queues are not encrypted with KMS CMK.",
            "resolution" : "Ensure SQS queues are encrypted with KMS CMKs to gain full control over data encryption and decryption."
        },
        {
            "rule" : "sqs_queue_expose_to_eveyone",
            "id" : "SQS_003",
            "severity" : "high",
            "issue": "SQS Queues are exposed to everyone.",
            "resolution" : "Ensure that AWS Simple Queue Service (SQS) queues are not exposed to everyone."
        },
        {
            "rule" : "sqs_queue_cross_account_access_allow",
            "id" : "SQS_004",
            "severity" : "high",
            "issue": "SQS queues are allowing cross account access.",
            "resolution" : "Ensure AWS Simple Queue Service (SQS) queues do not allow unknown cross account access."
        }
    ],
    "transfer": [
        {
            "rule" : "transfer_logging_not_enabled",
            "id" : "TRANSFER_001",
            "severity" : "medium",
            "issue": "Cloudwatch logging is not enabled for Transfer for SFTP.",
            "resolution" : "Ensure that AWS CloudWatch logging is enabled for Amazon Transfer for SFTP user activity."
        },
        {
            "rule" : "transfer_not_using_privatelink_for_endpoints",
            "id" : "TRANSFER_002",
            "severity" : "medium",
            "issue": "Transfer for SFTP servers are not using PrivateLink for endpoints",
            "resolution" : "Ensure that Amazon Transfer for SFTP servers are using AWS PrivateLink for their endpoints."
        }
    ],
    "iam": [
        {
            "rule" : "iam_password_policy_not_defined",
            "id" : "IAM_001",
            "severity" : "medium",
            "issue": "IAM password policy is not defined.",
            "resolution" : "Ensure AWS account has an IAM strong password policy in use"
        },
        {
            "rule" : "iam_users_with_full_administrator_permission",
            "id" : "IAM_002",
            "severity" : "high",
            "issue": "IAM users are having full administrator permission.",
            "resolution" : "Ensure there are no IAM users with full administrator permissions within your AWS account."
        },
        {
            "rule" : "iam_policy_with_full_administrator_access",
            "id" : "IAM_003",
            "severity" : "high",
            "issue": "IAM policies have full administrator access.",
            "resolution" : "Ensure IAM policies that allow full '*:*' administrative privileges are not created."
        },
        {
            "rule" : "iam_group_with_inline_policy",
            "id" : "IAM_004",
            "severity" : "medium",
            "issue": "IAM ggroups are using inline policies.",
            "resolution" : "Ensure AWS IAM groups do not have inline policies attached."
        },
        {
            "rule" : "iam_users_not_present",
            "id" : "IAM_005",
            "severity" : "medium",
            "issue": "IAM users are not present.",
            "resolution" : "Ensure there is at least one IAM user currently used to access your AWS account."
        },
        {
            "rule" : "iam_mfa_not_enabled_for_users",
            "id" : "IAM_006",
            "severity" : "high",
            "issue": "MFA is not enabled for IAM users.",
            "resolution" : "Ensure Multi-Factor Authentication (MFA) is enabled for all AWS IAM users with AWS Console access."
        },
        {
            "rule" : "iam_root_account_access_key_present",
            "id" : "IAM_007",
            "severity" : "high",
            "issue": "IAM root account is using access keys.",
            "resolution" : "Ensure that your AWS account (root) is not using access keys as a security best practice."
        },
        {
            "rule" : "iam_root_account_mfa_not_enabled",
            "id" : "IAM_008",
            "severity" : "high",
            "issue": "MFA for root account is not enabled.",
            "resolution" : "Ensure Multi-Factor Authentication (MFA) is enabled for the AWS root account."
        },
        {
            "rule" : "iam_user_has_more_than_one_active_access_keys",
            "id" : "IAM_009",
            "severity" : "medium",
            "issue": "IAM users having more than one active access keys.",
            "resolution" : "Ensure there is a maximum of one active access keys available for any single IAM user."
        },
        {
            "rule" : "iam_user_has_more_than_one_active_ssh_keys",
            "id" : "IAM_010",
            "severity" : "medium",
            "issue": "IAM users having more than one active ssh keys.",
            "resolution" : "Ensure there is a maximum of one active SSH public keys assigned to any single IAM user."
        },
        {
            "rule" : "iam_unused_groups",
            "id" : "IAM_011",
            "severity" : "low",
            "issue": "IAM groups are not having users.",
            "resolution" : "Ensure AWS IAM groups have at least one user attached as a security best practice."
        },
        {
            "rule" : "iam_unused_users",
            "id" : "IAM_012",
            "severity" : "medium",
            "issue": "IAM having unused users.",
            "resolution" : "Ensure unused IAM users are removed from AWS account to follow security best practice."
        }
    ],
    "backup": [
        {
            "rule" : "backup_vault_access_policy_not_defined_to_prevent_deletion",
            "id" : "BACKUP_001",
            "severity" : "high",
            "issue": "Backup vault access policy is not configured to prevent the deletion.",
            "resolution" : "Ensure that an Amazon Backup vault access policy is configured to prevent the deletion (accidentally or intentionally) of AWS backups in the backup vault."
        },
        {
            "rule" : "backup_vault_not_encrypted_with_kms_cmk",
            "id" : "BACKUP_001",
            "severity" : "high",
            "issue": "Backup valult is not encrypted with KMS CMK.",
            "resolution" : "Ensure that your backups are encrypted at rest using KMS Customer Master Keys (CMKs)."
        },
        {
            "rule" : "backup_plan_lifecycle_configuration_not_enabled",
            "id" : "BACKUP_003",
            "severity" : "medium",
            "issue": "Backup plans lifecycle configuration is not enabled.",
            "resolution" : "Ensure Amazon Backup plans have a compliant lifecycle configuration enabled."
        }
    ],
    "cloudtrail": [
        {
            "rule" : "cloudtrail_not_enabled",
            "id" : "CLOUDTRAIL_001",
            "severity" : "high",
            "issue": "Cloudtrail trails are not enabled.",
            "resolution" : "Ensure AWS CloudTrail trails are enabled for all AWS regions."
        },
        {
            "rule" : "cloudtrail_global_services_not_enabled",
            "id" : "CLOUDTRAIL_002",
            "severity" : "high",
            "issue": "Cloudtrail is not enabled for global services.",
            "resolution" : "Ensure AWS CloudTrail trails track API calls for global services such as IAM, STS and CloudFront."
        },
        {
            "rule" : "cloudtrail_logs_not_encrypted",
            "id" : "CLOUDTRAIL_003",
            "severity" : "medium",
            "issue": "Cloudtrail logs are not encrypted.",
            "resolution" : "Ensure your AWS CloudTrail logs are encrypted using AWS KMS–Managed Keys (SSE-KMS)."
        },
        {
            "rule" : "cloudtrail_management_event_not_included",
            "id" : "CLOUDTRAIL_004",
            "severity" : "medium",
            "issue": "Management events are not included into Cloudtrail.",
            "resolution" : "Ensure management events are included into AWS CloudTrail trails configuration."
        },
        {
            "rule" : "cloudtrail_log_file_integrity_validation_enabled",
            "id" : "CLOUDTRAIL_005",
            "severity" : "medium",
            "issue": "File integrity validation not enabled for Cloudtrail.",
            "resolution" : "Ensure your AWS CloudTrail trails have log file integrity validation enabled."
        },
        {
            "rule" : "cloudtrail_log_delivery_failing",
            "id" : "CLOUDTRAIL_006",
            "severity" : "medium",
            "issue": "Log delivery failing for Cloudtrail.",
            "resolution" : "Ensure Amazon CloudTrail trail log files are delivered as expected."
        },
        {
            "rule" : "cloudtrail_bucket_logging_not_enabled",
            "id" : "CLOUDTRAIL_007",
            "severity" : "medium",
            "issue": "Bucket logging is not enabled for Cloudtrail.",
            "resolution" : "Ensure AWS CloudTrail buckets have server access logging enabled."
        },
        {
            "rule" : "cloudtrail_bucket_is_public",
            "id" : "CLOUDTRAIL_008",
            "severity" : "high",
            "issue": "Cloudtrail logging bucket is publicly accessible.",
            "resolution" : "Ensures CloudTrail logging bucket is not publicly accessible"
        }
    ],
    "config": [
        {
            "rule" : "aws_config_not_enabled",
            "id" : "CONFIG_001",
            "severity" : "high",
            "issue": "AWS Config is not enabled.",
            "resolution" : "Ensure AWS Config is enabled in all regions to get the optimal visibility of the activity on your account."
        },
        {
            "rule" : "aws_config_not_included_global_resources",
            "id" : "CONFIG_001",
            "severity" : "medium",
            "issue": "Global resources are not included in AWS Config.",
            "resolution" : "Ensure Global resources are included into Amazon Config service configuration."
        },
        {
            "rule" : "aws_config_delivery_failed",
            "id" : "CONFIG_001",
            "severity" : "medium",
            "issue": "AWS Config log delivery failed.",
            "resolution" : "Ensure Amazon Config log files are delivered as expected."
        }
    ],
    "dms": [
        {
            "rule" : "dms_replication_instance_not_encrypted_with_kms_cmk",
            "id" : "DMS_001",
            "severity" : "high",
            "issue": "DMS replication instances are not encrypted with KMS CMK.",
            "resolution" : "Ensure that Amazon DMS replication instances are encrypted with KMS Customer Master Keys (CMKs)."
        },
         {
            "rule" : "dms_replication_instance_publicly_accessible",
            "id" : "DMS_002",
            "severity" : "high",
            "issue": "DMS replication instances are publicly accessible.",
            "resolution" : "Ensure that AWS DMS replication instances are not publicly accessible and prone to security risks."
        },
         {
            "rule" : "dms_replication_instance_auto_minor_version_upgrade_not_enabled",
            "id" : "DMS_003",
            "severity" : "medium",
            "issue": "DMS replication instances auto minor version upgrade feature not enabled.",
            "resolution" : "Ensure Amazon DMS replication instances have Auto Minor Version Upgrade feature enabled."
        }
    ],
    "documentdb": [
        {
            "rule" : "documentdb_cluster_not_encypted_with_kms_cmk",
            "id" : "DOCUMENTDB_001",
            "severity" : "high",
            "issue": "DocumentDB clusters are not encrypted with KMS CMK.",
            "resolution" : "Ensure that Amazon DocumentDB clusters are encrypted with KMS Customer Master Keys (CMKs)."
        },
        {
            "rule" : "documentdb_cluster_encryption_not_enabled",
            "id" : "DOCUMENTDB_002",
            "severity" : "high",
            "issue": "DocumentDB Clusters are not encrypted at rest.",
            "resolution" : "Ensure that Amazon DocumentDB clusters data is encrypted at rest."
        },
        {
            "rule" : "documentdb_cluster_log_export_feature_not_enabled",
            "id" : "DOCUMENTDB_003",
            "severity" : "low",
            "issue": "Log export feature is not enabled for DocumentDB Clusters.",
            "resolution" : "Ensure Log Exports feature is enabled for your Amazon DocumentDB clusters."
        }
    ],
    "dynamodb": [
         {
            "rule" : "dynamodb_not_encrypted_with_kms_cmk",
            "id" : "DYNAMODB_001",
            "severity" : "high",
            "issue": "DynamoDB is not encrypted with KMS CMK.",
            "resolution" : "Ensure that Amazon DynamoDB data is encrypted using AWS-managed Customer Master Keys."
         }
    ],
    "ecr": [
        {
            "rule" : "ecr_repository_exposed_to_everyone",
            "id" : "ECR_001",
            "severity" : "high",
            "issue": "Repositories are exposed to everyone.",
            "resolution" : "Ensure that AWS Elastic Container Registry (ECR) repositories are not exposed to everyone."
        },
        {
            "rule" : "ecr_cross_account_access_allowed",
            "id" : "ECR_002",
            "severity" : "high",
            "issue": "Repositories are allows cross account access.",
            "resolution" : "Ensure that Amazon ECR repositories do not allow unknown cross account access."
        }
    ],
    "efs": [
        {
            "rule" : "efs_encryption_not_enabled",
            "id" : "EFS_001",
            "severity" : "high",
            "issue": "Encryption is not enabled for EFS File systems.",
            "resolution" : "Ensure encryption is enabled for AWS EFS file systems to protect your data at rest."
        },
        {
            "rule" : "efs_not_encrypted_with_kms_cmk",
            "id" : "EFS_002",
            "severity" : "high",
            "issue": "EFS file systems are not encrypted with KMS CMK.",
            "resolution" : "Ensure EFS file systems are encrypted with KMS Customer Master Keys (CMKs) in order to have full control over data encryption and decryption."
        }
    ],
    "elasticache": [
        {
            "rule" : "elasticache_cluster_using_default_port",
            "id" : "ELASTICACHE_001",
            "severity" : "low",
            "issue": "ElastiCache clusters are using default port.",
            "resolution" : "Ensure AWS ElastiCache clusters are not using the default ports set for Redis and Memcached cache engines."
        },
        {
            "rule" : "elasticache_cluster_not_in_vpc",
            "id" : "ELASTICACHE_002",
            "severity" : "medium",
            "issue": "ElastiCache clusters are not in VPC.",
            "resolution" : "Ensure Amazon ElastiCache clusters are deployed into a Virtual Private Cloud (VPC)"
        },
        {
            "rule" : "elasticache_redis_cluster_encryption_at_rest_and_in_transit_not_enabled",
            "id" : "ELASTICACHE_003",
            "severity" : "high",
            "issue": "ElastiCache clusters end-to-end encryption is not enabled.",
            "resolution" : "Ensure in-transit and at-rest encryption is enabled for Amazon ElastiCache Redis clusters."
        }
    ],
    "emr": [
        {
            "rule" : "emr_cluster_not_in_vpc",
            "id" : "EMR_001",
            "severity" : "medium",
            "issue": "EMR clusters are not in VPC.",
            "resolution" : "Ensure AWS EMR clusters are launched in a Virtual Private Cloud (i.e. are using EC2-VPC platform)."
        },
        {
            "rule" : "emr_cluster_in_transit_and_at_rest_encryption_not_enabled",
            "id" : "EMR_002",
            "severity" : "high",
            "issue": "EMR clusters end-to-end encryption is not enabled.",
            "resolution" : "Ensure in-transit and at-rest encryption is enabled for Amazon EMR clusters."
        }
    ],
    "lambda": [
        {
            "rule" : "lambda_function_exposed_to_everyone",
            "id" : "LAMBDA_001",
            "severity" : "high",
            "issue": "Lambda functions are exposed to everyone.",
            "resolution" : "Ensure that your Amazon Lambda functions are not exposed to everyone."
        },
        {
            "rule" : "lambda_function_with_cross_account_access",
            "id" : "LAMBDA_002",
            "severity" : "medium",
            "issue": "Lambda functions are allows cross account access.",
            "resolution" : "Ensure AWS Lambda functions do not allow unknown cross account access via permission policies."
        },
        {
            "rule" : "lambda_function_not_in_vpc",
            "id" : "LAMBDA_003",
            "severity" : "medium",
            "issue": "Lambda functions are not in VPC.",
            "resolution" : "Ensure AWS Lambda functions are configured to access resources in a Virtual Private Cloud (VPC)."
        }
    ],
    "kafka": [
        {
            "rule" : "kafka_cluster_using_kms_cmk",
            "id" : "KAFKA_001",
            "severity" : "medium",
            "issue": "Kafka clusters are not encrypted using KMS CMK.",
            "resolution" : "Ensure that your Amazon MSK data is encrypted using AWS KMS Customer Master Keys."
        }
    ], 
    "neptune": [
        {
            "rule" : "neptune_iam_authentication_not_enabled",
            "id" : "NEPTUNE_001",
            "severity" : "medium",
            "issue": "Neptune clusters are not using IAM Database authentication.",
            "resolution" : "Ensure IAM Database Authentication feature is enabled for Amazon Neptune clusters."
        },
        {
            "rule" : "neptune_database_not_encrypted_with_kms_cmk",
            "id" : "NEPTUNE_002",
            "severity" : "medium",
            "issue": "Neptune instances are not encrypted using KMS CMK.",
            "resolution" : "Ensure that AWS Neptune instances enforce data-at-rest encryption using KMS CMKs."
        },
        {
            "rule" : "neptune_database_encryption_not_enabled",
            "id" : "NEPTUNE_003",
            "severity" : "high",
            "issue": "Neptune instances are not encrypted.",
            "resolution" : "Ensure that Amazon Neptune graph database instances are encrypted."
        },
        {
            "rule" : "neptune_database_is_publicly_accessible",
            "id" : "NEPTUNE_004",
            "severity" : "high",
            "issue": "Neptune instances are publicly accessible.",
            "resolution" : "Ensure Amazon Neptune instances are not publicly accessible."
        },
        {
            "rule" : "neptune_database_auto_minor_version_upgrade_not_enabled",
            "id" : "NEPTUNE_005",
            "severity" : "medium",
            "issue": "Neptune instances auto minor version upgrade feature not enabled.",
            "resolution" : "Ensure Amazon Neptune instances have Auto Minor Version Upgrade feature enabled."
        },
        {
            "rule" : "neptune_database_using_default_port",
            "id" : "NEPTUNE_006",
            "severity" : "low",
            "issue": "Neptune instances are using default port.",
            "resolution" : "Ensure Amazon Neptune instances not using default port 8182."
        }
    ],
    "redshift": [
        {
            "rule" : "redshift_cluster_user_activity_logging_not_enabled",
            "id" : "REDSHIFT_001",
            "severity" : "low",
            "issue": "Activity logging is not enabled for Redshift clusters.",
            "resolution" : "Ensure that user activity logging is enabled for your Amazon Redshift clusters."
        },
        {
            "rule" : "redshift_cluster_audit_logging_not_enabled",
            "id" : "REDSHIFT_002",
            "severity" : "medium",
            "issue": "Audit logging is not eneabled for Redshift clusters.",
            "resolution" : "Ensure audit logging is enabled for Redshift clusters for security and troubleshooting purposes."
        },
        {
            "rule" : "redshift_cluster_using_default_port",
            "id" : "REDSHIFT_003",
            "severity" : "low",
            "issue": "Redshift clusters are using default port.",
            "resolution" : "Ensure Amazon Redshift clusters are not using port 5439 (default port) for database access."
        },
        {
            "rule" : "redshift_clutser_encryption_not_enabled",
            "id" : "REDSHIFT_004",
            "severity" : "high",
            "issue": "Redshift clusters are not encrypted.",
            "resolution" : "Ensure database encryption is enabled for AWS Redshift clusters to protect your data at rest."
        },
        {
            "rule" : "redshift_cluster_not_encrypted_with_kms_cmk",
            "id" : "REDSHIFT_005",
            "severity" : "high",
            "issue": "Redshift clusters are not encrypted using KMS CMK.",
            "resolution" : "Ensure Redshift clusters are encrypted with KMS customer master keys (CMKs) in order to have full control over data encryption and decryption."
        },
        {
            "rule" : "redshift_cluster_not_in_vpc",
            "id" : "REDSHIFT_006",
            "severity" : "medium",
            "issue": "Redshift clusters not in VPC.",
            "resolution" : "Ensure Amazon Redshift clusters are launched within a Virtual Private Cloud (VPC)."
        },
        {
            "rule" : "redshift_cluster_publicly_accessible",
            "id" : "REDSHIFT_007",
            "severity" : "high",
            "issue": "Redshift clusters are publicly accessible.",
            "resolution" : "Ensure Redshift clusters are not publicly accessible to minimise security risks."
        },
        {
            "rule" : "redshift_cluster_required_ssl_parameter_not_enabled",
            "id" : "REDSHIFT_008",
            "severity" : "medium",
            "issue": "Parameter groups associated with Redshift cluster do not have the require_ssl parameter enabled.",
            "resolution" : "Ensure that all the parameter groups associated with your Amazon Redshift clusters have the require_ssl parameter enabled in order to keep your data secure in transit by encrypting the connection between the clients (applications) and your warehouse clusters."
        }
    ],
    "s3": [
        {
            "rule" : "s3_server_side_encryption_not_enabled",
            "id" : "S3_001",
            "severity" : "medium",
            "issue": "Server side encryption is not enabled for S3 buckets.",
            "resolution" : "Ensure that your AWS S3 buckets are protecting their sensitive data at rest by enforcing Server-Side Encryption."
        },
        {
            "rule" : "s3_bucket_intransit_encyption_not_enabled",
            "id" : "S3_002",
            "severity" : "medium",
            "issue": "In-Transit encryption not enabled for S3 buckets.",
            "resolution" : "Ensures S3 buckets have bucket policy statements that deny insecure transport"
        },
        {
            "rule" : "s3_bucket_object_lock_not_enabled",
            "id" : "S3_003",
            "severity" : "low",
            "issue": "Object lock feature is not enabled for S3 Buckets.",
            "resolution" : "Ensure that AWS S3 buckets use Object Lock for data protection and/or regulatory compliance."
        },
        {
            "rule" : "s3_bucket_cross_account_access_allowed",
            "id" : "S3_004",
            "severity" : "high",
            "issue": "S3 Buckets are allowing cross account access.",
            "resolution" : "Ensure Amazon S3 buckets do not allow unknown cross account access via bucket policies."
        },
        {
            "rule" : "s3_bucket_lifecycle_rules_not_configured",
            "id" : "S3_005",
            "severity" : "low",
            "issue": "Lifecycle rules are not configured for S3 Buckets.",
            "resolution" : "Ensure that your AWS S3 buckets utilize lifecycle configurations to manage S3 objects during their lifetime."
        },
        {
            "rule" : "s3_bucket_not_encypted_with_kms_cmk",
            "id" : "S3_006",
            "severity" : "medium",
            "issue": "S3 Buckets are not encrypted using KMS CMK.",
            "resolution" : "Ensure that Amazon S3 buckets are encrypted with customer-provided AWS KMS CMKs."
        },
        {
            "rule" : "s3_bucket_default_encyption_not_enabled",
            "id" : "S3_007",
            "severity" : "high",
            "issue": "S3 Buckets are not encrypted using default encryption.",
            "resolution" : "Ensure Amazon S3 buckets have Default Encryption feature enabled."
        },
        {
            "rule" : "s3_bucket_allow_global_acl_permissions",
            "id" : "S3_008",
            "severity" : "high",
            "issue": "S3 Buckets are allowing global Read, Write, Delete permissions.",
            "resolution" : "Ensures S3 buckets do not allow global write, delete, or read ACL permissions."
        }
    ],
    "ssm": [
        {
            "rule" : "ssm_paramters_not_encrypted",
            "id" : "SSM_001",
            "severity" : "medium",
            "issue": "SSM Paramters are not encrypted.",
            "resolution" : "Ensure that Amazon SSM parameters that hold sensitive configuration data are encrypted."
        }
    ],
    "sagemaker": [
        {
            "rule" : "sagemaker_notebook_instance_not_in_vpc",
            "id" : "SAGEMAKER_001",
            "severity" : "medium",
            "issue": "Notebook instances are not in VPC.",
            "resolution" : "Ensure Amazon SageMaker notebook instances are running inside a Virtual Private Cloud (VPC)."
        },
        {
            "rule" : "sagemaker_notebook_data_is_not_encrypted",
            "id" : "SAGEMAKER_002",
            "severity" : "high",
            "issue": "Notebook instances are not encrypted.",
            "resolution" : "Ensure that data available on Amazon SageMaker notebook instances is encrypted."
        },
        {
            "rule" : "sagemaker_notebook_not_encrypted_with_kms_cmk",
            "id" : "SAGEMAKER_003",
            "severity" : "high",
            "issue": "Notebook instances are not encrypted using KMS CMK.",
            "resolution" : "Ensure Amazon SageMaker notebook instances enforce data-at-rest encryption using KMS CMKs."
        },
        {
            "rule" : "sagemaker_notebook_direct_internet_access_enabled",
            "id" : "SAGEMAKER_004",
            "severity" : "medium",
            "issue": "Notebook instances are publicly accessible.",
            "resolution" : "Ensure Notebook instance is not publicly available"
        },
    ],
    "xray": [
        {
            "rule" : "xray_not_encrypted_with_kms_cmk",
            "id" : "XRAY_001    ",
            "severity" : "high",
            "issue": "X-ray not encrypts traces and related data using KMS CMK.",
            "resolution" : "Ensure Amazon X-Ray encrypts traces and related data at rest using KMS CMKs."
        }
    ],
    "shield": [
        {
            "rule" : "shield_advance_not_enabled",
            "id" : "SHIELD_001    ",
            "severity" : "medium",
            "issue": "AWS Shield is not enabeld.",
            "resolution" : "Use AWS Shield Advanced to protect your web applications against DDoS attacks."
        }
    ],
    "eks": [
        {
            "rule" : "eks_cluster_logging_not_enabled",
            "id" : "EKS_001",
            "severity" : "low",
            "issue": "EKS Clusters logging is not enabled.",
            "resolution" : "Ensure that EKS control plane logging is enabled for your Amazon EKS clusters."
        },
        {
            "rule" : "eks_security_group_not_secure",
            "id" : "EKS_002",
            "severity" : "medium",
            "issue": "EKS Cluster security group is not secure.",
            "resolution" : "Ensure that AWS EKS security groups are configured to allow incoming traffic only on TCP port 443."
        },
        {
            "rule" : "eks_cluster_endpoint_publicly_accessible",
            "id" : "EKS_003",
            "severity" : "medium",
            "issue": "EKS Cluster endpoint is publicly accessible.",
            "resolution" : "Ensure that AWS EKS cluster endpoint access is not public and prone to security risks."
        }
    ],
    "cloudfront": [
        {
            "rule" : "cloudfront_geo_restriction_not_enabled",
            "id" : "CLOUDFRONT_001",
            "severity" : "low",
            "issue": "Cloudfront distributions are not using geo restriction.",
            "resolution" : "Ensure that geo restriction is enabled for your Amazon CloudFront CDN distribution to whitelist or blacklist a country in order to allow or restrict users in specific locations from accessing web application content."
        },
        {
            "rule" : "cloudfront_using_insecure_origin_ssl_protocols",
            "id" : "CLOUDFRONT_002",
            "severity" : "medium",
            "issue": "Cloudfront distributions are using insecure SSL protocols",
            "resolution" : "Ensure AWS CloudFront distributions origin(s) do not use insecure SSL protocols."
        },
        {
            "rule" : "cloudfront_not_integrated_with_waf",
            "id" : "CLOUDFRONT_003",
            "severity" : "medium",
            "issue": "Cloudfront distributions are not integrated with AWS WAF.",
            "resolution" : "Ensure your Cloudfront CDN distributions are integrated with AWS WAF."
        },
        {
            "rule" : "cloudfront_access_logging_not_enabled",
            "id" : "CLOUDFRONT_004",
            "severity" : "medium",
            "issue": "Access Logging is not enabled for Cloudfront distributions.",
            "resolution" : "Ensure AWS Cloudfront CDN distributions have access logging enabled."
        },
        {
            "rule" : "cloudfront_not_using_improved_security_policy_for_https",
            "id" : "CLOUDFRONT_005",
            "severity" : "medium",
            "issue": "CloudFront distributions are not using improved security policies for HTTPS connections.",
            "resolution" : "Ensure AWS CloudFront distributions are using improved security policies for HTTPS connections."
        },
        {
            "rule" : "cloudfront_traffic_to_origin_unencrypted",
            "id" : "CLOUDFRONT_006",
            "severity" : "medium",
            "issue": "Traffic between the AWS CloudFront distributions and their origins is not encrypted.",
            "resolution" : "Ensure the traffic between the AWS CloudFront distributions and their origins is encrypted."
        },
        {
            "rule" : "cloudfront_not_using_secure_protocol",
            "id" : "CLOUDFRONT_007",
            "severity" : "medium",
            "issue": "Cloudfront not using secure viewer protocol policy.",
            "resolution" : "Configure HTTP to HTTPS redirects for your CloudFront distribution viewer protocol policy."
        },
        {
            "rule" : "cloudfront_access_origin_identity_enabled",
            "id" : "CLOUDFRONT_008",
            "severity" : "medium",
            "issue": "Origin access identity is not enabled for Cloudfront distributions",
            "resolution" : "Ensure your AWS Cloudfront distributions are using an origin access identity for their origin S3 buckets."
        },
        {
            "rule" : "cloudfront_field_level_encryption_not_enabled",
            "id" : "CLOUDFRONT_009",
            "severity" : "medium",
            "issue": "Field level encryption is not enabled for Cloudfront distributions.",
            "resolution" : "Ensure that Amazon CloudFront web distributions enforce field-level encryption."
        },
    ],
    "apigateway": [
        {
            "rule" : "api_gateway_not_integrated_with_waf",
            "id" : "APIGATEWAY_001",
            "severity" : "medium",
            "issue": "Production stage APIs not integratated with AWS WAF.",
            "resolution" : "Use AWS WAF to protect Amazon API Gateway APIs from common web exploits."
        },
        {
            "rule" : "api_gateway_client_ssl_certificate_not_enabled",
            "id" : "APIGATEWAY_002",
            "severity" : "medium",
            "issue": "Production and Staging stage APIs not configured for SSL certificate.",
            "resolution" : "Use client-side SSL certificates for HTTP backend authentication within AWS API Gateway."
        },
        {
            "rule" : "api_gateway_api_publicly_accessible",
            "id" : "APIGATEWAY_003",
            "severity" : "medium",
            "issue": "APIs are publicly accessible.",
            "resolution" : "Ensure APIs created with Amazon API Gateway are only accessible via private endpoints."
        },
    ]

}
