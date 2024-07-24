import pdfplumber
import re
import os
import pandas as pd


# def read_pdf(file_path):
#     if not os.path.exists(file_path):
#         print(f"Error: File '{file_path}' not found.")
#         return ""
    
#     with pdfplumber.open(file_path) as pdf:
#         pages = [page.extract_text() for page in pdf.pages]
#         # Print extracted text from PDF pages
#         print("PDF Pages Text:", pages)
#     return "\n".join(pages)




def extract_invoice_details(file_path):
    with pdfplumber.open(file_path) as pdf:
        page = pdf.pages[0]
        text = page.extract_text()
        invoice_number = re.search(r'Invoice No\.\s*(\d+)', text, re.IGNORECASE)
        invoice_date = re.search(r'Invoice Date\s*(\d{1,2}/\d{1,2}/\d{4})', text, re.IGNORECASE)
        po_number = re.search(r'Cust PO No:\s*(\d+)', text, re.IGNORECASE)
        vendor_name = re.search(r'Please Remit Payment To:\s*(.*?)\s*PO BOX', text, re.IGNORECASE)
        vendor_address = re.search(r'PO BOX:\s*(\d+)', text, re.IGNORECASE)
        billing_name = "Black Box Network Services"
        total_amt_due_section = re.search(r'Total Amt\. Due\s*(.*?)\s*Interest charges', text, re.IGNORECASE)
        if total_amt_due_section:
            amounts = total_amt_due_section.group(1).strip().split()
            if len(amounts) >= 6:
                net_amount = amounts[0]
                total_amount = amounts[1]
                shipping_charges = amounts[2]
                tax_amount = amounts[3]
            else:
                net_amount = total_amount = shipping_charges = tax_amount = None
        else:
            net_amount = total_amount = shipping_charges = tax_amount = None
        extracted_data = {
        "Vendor Name": vendor_name.group(1).strip() if vendor_name else None,
        "Vendor Address": f"PO BOX {vendor_address.group(1).strip()}" if vendor_address else None,
        "Billing Name": billing_name,
        "Invoice Date": invoice_date.group(1) if invoice_date else None,
        "Invoice Number": invoice_number.group(1) if invoice_number else None,
        "PO Number": po_number.group(1) if po_number else None,
        "Tax Amount": tax_amount,
        "Shipping Charges": shipping_charges,
        "Net Amount": net_amount,
        "Total Amount": total_amount,
                }
        # return extracted_data

        details = {
            # "invoice_number": None,
            # "order_date": None,
            # "order_number": None,
            # "customer_details": None,
            "items": []
        }
        lines = text.split('\n')
        # for line in lines:
        #     if 'Invoice No.' in line:
        #         details["invoice_number"] = line.split('Invoice No:')[-1].strip()
        #     elif 'Invoice Date' in line:
        #         details["Invoice Date"] = line.split('Invoice Date')[-1].strip()
        #     elif 'Cust PO No' in line:
        #         details["Cust PO No"] = line.split('Cust PO No:')[-1].strip()
        #     elif 'Order Date:' in line:
        #         details["order_date"] = line.split('Order Date:')[-1].strip()
        #     elif 'Order No:' in line:
        #         details["order_number"] = line.split('Order No:')[-1].strip()
        #     elif 'Sold To:' in line:
        #         details["customer_details"] = line.split('Sold To:')[-1].strip()
        item_section_start = None
        for i, line in enumerate(lines):
            if 'Item No / Description' in line:
                item_section_start = i
                break
        item_section_end = None
        for i, line in enumerate(lines):
            if 'SubTotal' in line:
                item_section_end = i
                break
        if item_section_start is not None and item_section_end is not None:
            for i in range(item_section_start + 1, item_section_end):
                item_line = lines[i]
                if item_line.strip() and not item_line.startswith(('SN:', 'Order', 'Doorplate','Tracking', 'Carton:', '(')):
                    item_details = item_line.split()
                    print("item",item_details)
                    if len(item_details) > 3:  # Ensure there are enough elements
                        item_total = item_details[-1]
                        item_price = item_details[-2]
                        # item_order = item_details[-3]
                        item_order = item_details[3]
                        item_description = ' '.join(item_details[:-3])
                        # item_description = item_details[1]
                        details["items"].append({
                            "Description": item_description,
                            "Quantity": item_order,
                            "Price": item_price,
                            "Total": item_total
                        })
        dic = details
        print("dic ",dic)
        filtered_items = [item for item in dic['items'] if item['Description']]
        print(extracted_data)
        for item in filtered_items:
            print(f"Description: {item['Description']}, Price: {item['Price']}, Total: {item['Total']}")
        return extracted_data,filtered_items

# pdf_file_path = '/home/buzzadmin/Desktop/Click_On_This/Data Extraction/Sample Data/424284M4990153_1.pdf'
# # pdf_file_path = '/home/buzzadmin/Desktop/Click_On_This/Data Extraction/Spdfs/424284M4990156_4.pdf'
# # pdf_file_path = '/home/buzzadmin/Desktop/Click_On_This/Data Extraction/Sample Data/424284M4990154_2.pdf'
# # pdf_file_path = '/home/buzzadmin/Desktop/Click_On_This/Data Extraction/Sample Data/424284M4990156_4.pdf'
# extracted_details = extract_invoice_details(pdf_file_path)
# print(extracted_details)

def save_to_excel(details, items, file_path):
    # for item in items:
    #     x = item['Description'].split(" ")
    #     if len(x) > 3:
    #         description_parts = item['Description'].split(" ")
    #         print("desc",description_parts)
    #         item['Description'] = description_parts[0]
    #         item['Quantity'] = description_parts[3]

    df_details = pd.DataFrame([details])
    df_items = pd.DataFrame(items)
    with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
        df_details.to_excel(writer, index=False, sheet_name='Invoice Details')
        df_items.to_excel(writer, index=False, sheet_name='Items')
    # Confirm data saved
    print(f"Data saved to {file_path} with sheet names 'Invoice Details' and 'Items'")


def process_pdfs_in_directory(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):
            file_path = os.path.join(directory, filename)
            print(f"Processing {file_path}...")
            extract,items = extract_invoice_details(file_path)

            # processed_text = preprocess_text(sample_text)
            # details = extract_invoice_details(processed_text)
            # items = extract_item_details(processed_text)
            # Save to Excel with the same base name as the PDF
            excel_file_path = os.path.splitext(file_path)[0] + ".xlsx"
            save_to_excel(extract, items, excel_file_path)

pdf_directory = "/home/buzzadmin/Desktop/Click_On_This/Data Extraction/Sample Data"
process_pdfs_in_directory(pdf_directory)
