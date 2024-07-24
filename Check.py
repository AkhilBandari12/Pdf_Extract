import pdfplumber
import re
import pandas as pd
import os
import config


# Set the pdf_directory path
pdf_directory = "/home/buzzadmin/Desktop/Click_On_This/Data Extraction/Sample Data"


def read_pdf(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return ""
    
    with pdfplumber.open(file_path) as pdf:
        pages = [page.extract_text() for page in pdf.pages]
        # Print extracted text from PDF pages
        print("PDF Pages Text:", pages)
    return "\n".join(pages)


def preprocess_text(text):
    text = text.replace('\n', ' ')
    text = re.sub(r'\s+', ' ', text)
    # Print preprocessed text
    print("Preprocessed Text:", text)
    return text


def extract_invoice_details(text):
    invoice_number = re.search(r'Invoice No\.\s*(\d+)', text, re.IGNORECASE)
    invoice_date = re.search(r'Invoice Date\s*(\d{1,2}/\d{1,2}/\d{4})', text, re.IGNORECASE)
    po_number = re.search(r'Cust PO No:\s*(\d+)', text, re.IGNORECASE)
    vendor_name = re.search(r'Please Remit Payment To:\s*(.*?)\s*PO BOX', text, re.IGNORECASE)
    vendor_address = re.search(r'PO BOX:\s*(\d+)', text, re.IGNORECASE)
    billing_name = re.search(r'Sold To:\s*(.*?)\s*Ship To:', text, re.IGNORECASE)  # Updated pattern to correctly capture the billing name


    # Extract text between 'Total Amt. Due' and 'Interest charges'
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
        "Billing Name": billing_name.group(1).strip() if billing_name else None,
        "Invoice Date": invoice_date.group(1) if invoice_date else None,
        "Invoice Number": invoice_number.group(1) if invoice_number else None,
        "PO Number": po_number.group(1) if po_number else None,
        "Tax Amount": tax_amount,
        "Shipping Charges": shipping_charges,
        "Net Amount": net_amount,
        "Total Amount": total_amount,
    }
    # Print extracted details
    print("Extracted Details:", extracted_data)
    return extracted_data


def extract_item_details(text):
    # Pattern to extract item details
    item_pattern = re.compile(r'(\w+-\w+\s+.*?)\s+(\d+)\s+(\w{2})\s+(\d+\.\d{2})\s+(\d+\.\d{2})')
    items = item_pattern.findall(text)
    
    item_list = []
    for item in items:
        item_dict = {
            "Description": item[0].strip()[:40],  # Extract up to 40 characters
            "Quantity": item[1].strip(),
            "Unit Price": item[3].strip(),
            "Line Amount": item[4].strip(),
        }
        item_list.append(item_dict)
    
    # Print extracted items
    print("Extracted Items:", item_list)
    return item_list


def save_to_excel(details, items, file_path):
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


            sample_text = read_pdf(file_path)
            if not sample_text:
                continue
            processed_text = preprocess_text(sample_text)
            details = extract_invoice_details(processed_text)
            items = extract_item_details(processed_text)


            # Save to Excel with the same base name as the PDF
            excel_file_path = os.path.splitext(file_path)[0] + ".xlsx"
            save_to_excel(details, items, excel_file_path)


# Example usage:
process_pdfs_in_directory(pdf_directory)