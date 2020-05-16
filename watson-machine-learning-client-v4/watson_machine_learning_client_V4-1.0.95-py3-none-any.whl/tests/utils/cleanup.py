from watson_machine_learning_client.wml_client_error import WMLClientError


def delete_model_deployment(wml_client, deployment_name: 'str'):
    '''
    Delete deployment (and model) with name `deployment_name`

    '''
    deployments_details = wml_client.deployments.get_details()
    for deployment in deployments_details['resources']:
        if deployment['entity']['name'] == deployment_name:
            deployment_id = deployment['metadata']['id']
            print('Deleting deployment id', deployment_id)
            wml_client.deployments.delete(deployment_id)
            model_href_split = deployment['entity']['asset']['href'].split('/')
            model_id = model_href_split[model_href_split.index('models') + 1].split('?')[0]
            try:
                print('Deleting model id', model_id)
                wml_client.repository.delete(model_id)
            except WMLClientError as client_error:
                print("Could not delete model. Error message:")
                print(client_error)
        else:
            pass



