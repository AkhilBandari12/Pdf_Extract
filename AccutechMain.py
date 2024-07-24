import pdfplumber
import re
import pandas as pd
import os
import config

pdf_directory = config.pdf_directory

def read_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        pages = [page.extract_text() for page in pdf.pages]
    return "\n".join(pages)

def preprocess_text(text):
    text = text.replace('\n', ' ')
    text = re.sub(r'\s+', ' ', text)
    return text

def extract_invoice_details(text):
    invoice_number = re.search(r'INVOICE NO\.\s*(\d+)', text, re.IGNORECASE)
    total_amount = re.search(r'TOTAL DUE\s*[\$]?(\d+[\.,]?\d*\.\d{2})', text, re.IGNORECASE)
    vendor_name = re.search(r'PLEASE REMIT PAYMENT TO:\s*(.*?)\s*PO BOX', text, re.IGNORECASE)
    vendor_address = re.search(r'PO BOX\s*(\d+).*?([A-Z\s]+)', text, re.IGNORECASE)
    billing_name = re.search(r'DUE DATE\s*\d{2}/\d{2}/\d{2}\s*(.{0,27})', text, re.IGNORECASE)
    invoice_date = re.search(r'INVOICE DATE\s*(\d{2}/\d{2}/\d{2})', text, re.IGNORECASE)
    tracking_number = re.search(r'TRACKING NUMBER\s*([A-Z0-9]+)', text, re.IGNORECASE)
    tax_amount = re.search(r'SALES TAX\s*[\$]?(\d+[\.,]?\d*\.\d{2})', text, re.IGNORECASE)
    shipping_charges = re.search(r'FREIGHT\s*[\$]?(\d+[\.,]?\d*\.\d{2})', text, re.IGNORECASE)
    net_amount = re.search(r'MATERIAL TOTAL\s*[\$]?(\d+[\.,]?\d*\.\d{2})', text, re.IGNORECASE)

    extracted_data = {
        "Vendor Name": vendor_name.group(1).strip() if vendor_name else None,
        "Vendor Address": f"PO BOX {vendor_address.group(1)} {vendor_address.group(2).strip()}" if vendor_address else None,
        "Billing Name": billing_name.group(1).strip() if billing_name else None,
        "Invoice Date": invoice_date.group(1) if invoice_date else None,
        "Invoice Number": invoice_number.group(1) if invoice_number else None,
        "PO Number": tracking_number.group(1) if tracking_number else None,
        "Tax Amount": tax_amount.group(1) if tax_amount else None,
        "Shipping Charges": shipping_charges.group(1) if shipping_charges else None,
        "Net Amount": net_amount.group(1) if net_amount else None,
        "Total Amount": total_amount.group(1) if total_amount else None,
    }
    return extracted_data

def extract_item_details(text):
    pattern = re.compile(r'(\d+)\s+(.*?)\s+(\d+)\s+(\d+)\s+(\d+)\s+([\d\.]+)\s+([A-Z]+)\s+([\d\.]+)')
    matches = pattern.findall(text)
    items = []

    for match in matches:
        item = {
            "Description": match[1][:40],  # Limit the description to 40 characters
            "Quantity": match[3],
            "Unit Price": match[5],
            "Line Amount": match[7]
        }
        items.append(item)
    return items

def save_to_excel(details, items, file_path):
    df_details = pd.DataFrame([details])
    df_items = pd.DataFrame(items)
    with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
        df_details.to_excel(writer, index=False, sheet_name='Invoice Details')
        df_items.to_excel(writer, index=False, sheet_name='Items')

def process_pdf(file_path):
    text = read_pdf(file_path)
    processed_text = preprocess_text(text)
    details = extract_invoice_details(processed_text)
    items = extract_item_details(processed_text)

    excel_file_path = os.path.splitext(file_path)[0] + ".xlsx"
    save_to_excel(details, items, excel_file_path)

def process_pdfs_in_directory(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):
            file_path = os.path.join(directory, filename)
            print(f"Processing {file_path}...")
            process_pdf(file_path)

# Example usage:
process_pdfs_in_directory(pdf_directory)
