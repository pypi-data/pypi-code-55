#
with open('orders_test_4.csv', 'w', encoding='utf8', newline='\n') as output_file:
    fc = csv.DictWriter(output_file, fieldnames=columns)
    fc.writeheader()
    fc.writerows(data)
with open('orders_test_4.csv', 'r') as f:
    fc = f.read()

find_str = 'False'
replace_str = '0'
new_csv_str = re.sub(find_str, replace_str, fc)

find_str = 'True'
replace_str = '1'

new_csv_str_1 = re.sub(find_str, replace_str, new_csv_str)

with open('orders_test_5.csv', 'w', encoding='utf8', newline='\n') as f:
    f.write(new_csv_str_1)

#
#
#

#
# df = pd.read_fwf('orders_test_4.csv',delimiter=',')
# df.to_csv('orders_test_5.csv')
# substitute

time2 = time.time()
# print(time2-time1)
connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
blob_service_client = BlobServiceClient.from_connection_string(connect_str)
# container_client = blob_service_client.create_container('orders')
blob_client = blob_service_client.get_blob_client(container='orders', blob='orders_test_6.csv')
print("\nUploading to Azure Storage as blob:\n\t" + 'orders_f.csv')
# Upload the created file
with open('orders_test_5.csv', "rb") as data_cc:
    blob_client.upload_blob(data_cc)
#
# time3=time.time()
# print(time3-time2)
# insert_query = '''BULK INSERT %s.%s FROM "%s" WITH (DATA_SOURCE = '%s', FIELDTERMINATOR = ',', ROWTERMINATOR = '\n',FIRSTROW =2);''' % ('chandon_salesforce', 'order_1','chandon_orders.csv','MHUSBlob')
# print(insert_query)
# self.dbstream.execute_query(insert_query)
# time4=time.time()