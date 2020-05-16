#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import sys
import os
import re
from datetime import datetime

sys.path.append('/Users/roberto/projects/dbmodel')

import dbmodel

from model.deploy import Deploy
from model.acompanhanteestatistica import AcompanhanteEstatistica

def main(arg):
    #AWS
    #db = dbmodel.Connection(db_user="idp_master", db_password="aWkqH2MJFhCspZFV4m3JugUnnu", db_host="idp-instance.celwa7bjtmnw.us-east-2.rds.amazonaws.com", db_port=3306, db_database="ilhadoprazer")

    #LOCAL
    db = dbmodel.Connection(db_user="root", db_password="", db_host="localhost", db_port=3306, db_database="ilhadoprazer")


    acompanhante = db.acompanhantes.join("sexos").where("id=299").first



    new_deploy = Deploy()
    new_deploy.deploy_url = "acompanhantes-es"
    new_deploy.deploy_data = datetime.now()
    new_deploy.deploy_realizado = 0

    db.deploys.add(new_deploy)


    acompanhante.aco_nome = "Roberto Teste"

    estatistica = AcompanhanteEstatistica()
    estatistica.stat_ano = 2019
    estatistica.stat_mes = 11
    estatistica.stat_acessos_unicos = 10
    estatistica.stat_acessos_totais = 20

    acompanhante.acompanhantes_estatisticas.add(estatistica)

    #print(db.__commit__)
    #for value in db.__commit__:
    #    print(value.__status__)
    #    for subvalue in value.__commit__:
    #        print(subvalue.__status__)
    #        print(subvalue.toJSON())

    db.save()
    db.close()

if __name__ == "__main__":
    main(sys.argv)
