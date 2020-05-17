from viteezytool.processor.processors import process_document, process_clients, extract_customers
from viteezytool.data.data_loader import load_excel


def run():
    df = load_excel(sheet_name='Paklijst')
    clients = extract_customers(df)
    process_clients(clients)


if __name__ == "__main__":
    run()
