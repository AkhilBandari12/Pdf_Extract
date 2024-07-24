# dic = {'invoice_number': 'Invoice No. 4745558',
#        'order_date': '7/10/2024',
#        'order_number': '4877682-0',
#        'customer_details': 'CUS01752 Ship To:SHIP', 
#        'items': [{'description': '1 SMS84100 5 0', 'price': '32.30', 'total': '0.00'},
#                   {'description': '2 2200-37147-001 5 5', 'price': '341.40', 'total': '1,707.00'}, 
#                   {'description': '', 'price': 'SN:', 'total': '631727729'}, 
#                   {'description': '', 'price': 'SN:', 'total': '631727746'},
#                     {'description': '', 'price': 'SN:', 'total': '631727787'},
#                       {'description': '', 'price': 'SN:', 'total': '631728000'}, 
#                       {'description': '', 'price': 'SN:', 'total': '641730882'}, 
                      
#                       {'description': '', 'price': 'Tracking', 'total': 'Information'},
#                         {'description': 'Carton:', 'price': 'Tracking:', 'total': '404085394410'}]}




"""I N V O I C E
Invoice No. 4745558
Invoice Date 7/10/2024
Due Date: 09/23/2024
Order No: 4877682-0
Order Date: 7/10/2024
Cust PO No: 4500128826
Salesperson: David Bokisa
Sold To: CUS01752 Ship To:SHIP
Black Box Network Services DIGNITY HEALTH/MARIAN MEDICAL RECEI
Attn: Centralized Accounts Payable 1400 E CHURCH ST
1000 Park Drive PO 3641391285 RECEIVING IT364
Lawrence, PA 15055 Santa Maria, CA 93454
Date Shipped Carrier Freight FOB Tax Terms Contact
7/10/2024 FedEx Ground Pre-Paid Origin No Tax Net 75 Days DAVID RIVAS
Item No / Description Serial Number(s) Order Ship UOM Unit Price Ext Amount
1 SMS84100 5 0 EA 32.30 0.00
(INTITAL) First Year SpectraCare, Spectralink 84 - Series **MUST BE PURCHASED AT TIME OF SALE**
2 2200-37147-001 5 5 EA 341.40 1,707.00
(PHONE) Spectralink 8440 without Lync Support, North American Handset, BLUE (Order Battery & Charger Separately) **Spectracare Purchase Required with Sale**
SN: 631727729
SN: 631727746
SN: 631727787
SN: 631728000
SN: 641730882
Order Tracking Information
Carton: 11427076 Tracking: 404085394410
SubTotal Ext. Total Freight Tax Invoice Total Total Payments Total Amt. Due
1,707.00 1,707.00 0.00 0.00 1,707.00 0.00 1,707.00
Interest charges will be accrued on past due balances.
Please Remit Payment To: Jenne, Inc.
PO BOX: 639629
Cincinnati, OH 45263-9629
Electronically delivered to: centralized.ap@blackbox.com
For information on Electronic Invoicing or Online Bill Pay, contact accounting at accounting@jenne.com.
This invoice supersedes any other agreements and buyer’s purchase order. Jenne, Inc. objects to any additional terms in buyer’s purchase order or other
writing of any party. This invoice is a contract which is not affected by differences in any purchase order that do not mirror the terms of this offer. This
document becomes a binding contract once a common carrier has received delivery, in whole or part, or when the buyer has otherwise consented to the terms
and conditions hereof. Jenne Terms and Conditions apply at all times and are readily available at www.jenne.com."""




import pandas as pd

dic = {'items': 
       [{'description': '1 SMS84100 5 0', 'price': '32.30', 'total': '0.00'},
         {'description': '2 2200-37147-001 5 5', 'price': '341.40', 'total': '1,707.00'}, 
         {'description': '', 'price': 'SN:', 'total': '631727729'}, 
         {'description': '', 'price': 'SN:', 'total': '631727746'}, 
         {'description': '', 'price': 'SN:', 'total': '631727787'}, 
         {'description': '', 'price': 'SN:', 'total': '631728000'},
           {'description': '', 'price': 'SN:', 'total': '641730882'}, 
           {'description': '', 'price': 'Tracking', 'total': 'Information'}, 
           {'description': 'Carton:', 'price': 'Tracking:', 'total': '404085394410'}]}

filtered_items = [item for item in dic['items'] if item['description']]
"""
[{'description': '1 SMS84100 5 0', 'price': '32.30', 'total': '0.00'},
 {'description': '2 2200-37147-001 5 5', 'price': '341.40', 'total': '1,707.00'}, 
 {'description': 'Carton:', 'price': 'Tracking:', 'total': '404085394410'}]
"""
df_items = pd.DataFrame(filtered_items)
print(df_items)
# print(filtered_items)
