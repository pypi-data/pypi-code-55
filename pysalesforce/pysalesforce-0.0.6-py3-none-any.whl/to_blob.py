import csv
import os

from azure.storage.blob import BlobServiceClient

# with open('people.csv', 'w', encoding='utf8', newline='') as output_file:
#     fc = csv.DictWriter(output_file, fieldnames=columns)
#     fc.writeheader()
#     fc.writerows(data)




def to_blob():
    connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    container_name = "orders"
    print(container_name)
    container_client = blob_service_client.create_container(container_name)
    local_file_name = "order_testing5.csv"
    upload_file_path = "order_testing5.csv"
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=upload_file_path)
    print("\nUploading to Azure Storage as blob:\n\t" + local_file_name)
    # Upload the created file
    with open(upload_file_path, "rb") as data:
        blob_client.upload_blob(data)
