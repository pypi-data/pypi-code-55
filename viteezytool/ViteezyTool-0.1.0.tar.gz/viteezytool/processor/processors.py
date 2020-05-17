import pandas as pd
import csv
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Cm
from viteezytool.data.data_loader import load_excel, lookup_by_id, load_lookup, save_folder
from viteezytool.data.shared import IMG, RESOURCES, is_number, C_KEY, F_NAME, L_NAME, PILL_COLUMNS, MAX_TABLE_HEIGHT, \
    MAX_IMG_HEIGHT


def extract_customers(df: pd.DataFrame()):
    """
    This function will extract the customers from a pandas dataframe.
    :param df: A pandas dataframe constructed from the Paklijst excel
    :return: A dictionary of customers, including their blend
    """
    customers = dict()  # Initialise empty dictionary
    lookup = load_lookup()  # Load the lookup dataframe containing ingredient/supplement information
    num_entries = len(df.index)  # The number of entries in the dataframe
    blend_columns = [x for x in df.columns if is_number(x)]  # get the columns that contain blend information
    blend_df = df[blend_columns]  # Create a dataframe containing only the blend data for each customer
    non_blend_columns = [x for x in df.columns if not is_number(x)]  # Get columns without blend info
    non_blend_df = df[non_blend_columns]  # Create a datafrane cotaining only the non blend data

    # The below loop will loop over each customer in the dataframe
    for x in range(num_entries):
        row = non_blend_df.iloc[x]  # Select the row for that customer
        blend_row = blend_df.iloc[x]  # Select the blend row for that customer
        selection = blend_row[blend_row >= 1]  # If column contains number >1 it means it is in the mix
        blend = []  # Initialise an empty blend array

        # The below loop will loop over every item in the blend/mix
        for key in selection.keys():
            ingredient = lookup_by_id(key, lookup)  # Grab the ingredient information
            if not (ingredient[4]):  # Ingredient 4 stores if it is a flavour or not
                dose = "{0} {1}".format(int(selection[key]), ingredient[
                    2])  # selection[key] returns the quantity and ingredient[2] returns the suffix e.g. 2 schepjes
                label = ingredient[1]  # The name e.g. Zink
                pakcode = ingredient[3]  # The code used by packing company
                is_pil = ingredient[5]  # Flag if it is a pill or not
                blend.append(  # Append the ingredient the blend list
                    {'label': label, 'dose': dose, 'img': "{0}.png".format(key), 'id': pakcode, 'is_pil': is_pil})
        # Add the current customer to the customer dictionary
        customers[row[C_KEY]] = row.to_dict()
        customers[row[C_KEY]]['mix'] = blend
        customers[row[C_KEY]][C_KEY] = str(row[C_KEY]).zfill(5)
    return customers


def process_document(customer: dict, save_dir):
    """
    Loads an existing template document and fills in customer information and saves it to file
    :param customer: Dictionary containing customer information
    :return: None
    """
    table_height = MAX_TABLE_HEIGHT
    max_img_height = MAX_IMG_HEIGHT
    doc = DocxTemplate(RESOURCES / 'word_templates/template.docx')
    # Set the image height based on the number of elements in the blend and max allowed image height
    try:
        img_height = table_height / len(customer['mix'])
        img_height = max_img_height if img_height > max_img_height else img_height
    except ZeroDivisionError:
        img_height = max_img_height

    # Loop over ever supplement/ingredient in the mix
    for item in customer['mix']:
        img_name = item['img']  # Set image name
        img_path = (IMG / img_name).absolute().as_posix()  # Create path to image
        image = InlineImage(doc, img_path, width=Cm(img_height),
                            height=Cm(img_height))  # Create word inline image object
        item['img'] = image  # Replace the image name with the inline image object

    context = customer  # Set the context for document rendering
    doc.render(context)  # Render the document

    docx_file = save_dir / "{0}_{1}.docx".format(customer[L_NAME], customer[F_NAME])  # Set the save directory
    try:  # Try to save the document
        doc.save(docx_file)
    except PermissionError:  # Permission error likely caused due to file being open
        print(
            "PermissionError saving {0}\n Please try a different folder or change rights \n "
            "Misschien is het bestand open in een ander programma, sluit dat programma".format(
                docx_file))
    return doc


def process_orders(orders: dict, save_dir=None):
    """
    This function processes the orders and outputs them in the format required by the packing company
    :param orders: Dictionary met customers
    :param save_dir: Save directory
    :return: None
    """

    client_columns = (RESOURCES / 'columns.csv').read_text().split(
        ';')  # Load the columns that contain the client information
    pill_columns = PILL_COLUMNS  # Load the pill columns
    data = []  # Empty data array
    order_number = input("Please provide order number")  # Request user to input the order number
    for id, client in orders.items():  # Loop over the client
        for supplement in client['mix']:  # Loop over the supplements
            client_data = [client[x] for x in client_columns]
            if supplement['is_pil']:
                pill_data = [order_number, supplement['id'], supplement['dose'][0]]
                [client_data.append(x) for x in pill_data]
                data.append(client_data)
    client_columns.extend(pill_columns)
    df = pd.DataFrame(data, columns=client_columns)
    df.to_csv(save_dir / '{0}.csv'.format(order_number), index=False, sep=';')


def process_clients(clients: dict):
    save_dir = save_folder()
    for item in clients.values():
        document = process_document(item, save_dir)
    process_orders(clients, save_dir)


if __name__ == '__main__':
    df = load_excel('Paklijst')
    customers = extract_customers(df)
    process_clients(customers)
    # process_document(customers[8], OUTPUT)
    # list = process_orders(customers)
