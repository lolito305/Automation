from quickbooks import QuickBooks

def create_invoice(client_id, client_secret, access_token, refresh_token, company_id, contractor_name, amount, due_date, payment_terms):
    try:
        # Set up QuickBooks client
        quickbooks = QuickBooks(
            client_id=client_id,
            client_secret=client_secret,
            access_token=access_token,
            refresh_token=refresh_token,
            company_id=company_id
        )

        # Create an invoice
        invoice_data = {
            'CustomerRef': {'name': contractor_name},
            'Line': [
                {
                    'DetailType': 'SalesItemLineDetail',
                    'SalesItemLineDetail': {
                        'ItemRef': {'name': 'Contracting Services'},
                        'Qty': 1,
                        'UnitPrice': amount
                    }
                }
            ],
            'DueDate': due_date,
            'PaymentTermRef': {'name': payment_terms}
        }

        response = quickbooks.invoice.create(invoice_data)

        if response.status_code == 200:
            invoice = response.json()
            return invoice['Invoice']['Id']
        else:
            print('Failed to create invoice:', response.content)
            return None

    except Exception as e:
        print('Error creating invoice:', str(e))
        return None

def get_customer_info(client_id, client_secret, access_token, refresh_token, company_id, contractor_name):
    try:
        # Set up QuickBooks client
        quickbooks = QuickBooks(
            client_id=client_id,
            client_secret=client_secret,
            access_token=access_token,
            refresh_token=refresh_token,
            company_id=company_id
        )

        # Get customer info
        response = quickbooks.customer.filter(Name=contractor_name)

        if response.status_code == 200:
            customers = response.json()['QueryResponse']['Customer']
            if customers:
                customer = customers[0]
                return customer
        else:
            print('Failed to fetch customer information:', response.content)

        return None

    except Exception as e:
        print('Error fetching customer information:', str(e))
        return None

def send_invoice_email(client_id, client_secret, access_token, refresh_token, company_id, invoice_id, recipient_email):
    try:
        # Set up QuickBooks client
        quickbooks = QuickBooks(
            client_id=client_id,
            client_secret=client_secret,
            access_token=access_token,
            refresh_token=refresh_token,
            company_id=company_id
        )

        # Send invoice via email
        email_data = {
            'InvoiceEmail': {
                'Address': recipient_email
            }
        }

        response = quickbooks.invoice.send_email(invoice_id, email_data)

        if response.status_code == 200:
            print('Invoice email sent successfully.')
        else:
            print('Failed to send invoice email:', response.content)

    except Exception as e:
        print('Error sending invoice email:', str(e))

def get_invoice_details(client_id, client_secret, access_token, refresh_token, company_id, invoice_id):
    try:
        # Set up QuickBooks client
        quickbooks = QuickBooks(
            client_id=client_id,
            client_secret=client_secret,
            access_token=access_token,
            refresh_token=refresh_token,
            company_id=company_id
        )

        # Retrieve invoice details
        response = quickbooks.invoice.get(invoice_id)

        if response.status_code == 200:
            invoice_details = response.json()
            return invoice_details['Invoice']
        else:
            print('Failed to retrieve invoice details:', response.content)

        return None

    except Exception as e:
        print('Error retrieving invoice details:', str(e))
        return None

def update_invoice_status(client_id, client_secret, access_token, refresh_token, company_id, invoice_id, status):
    try:
        # Set up QuickBooks client
        quickbooks = QuickBooks(
            client_id=client_id,
            client_secret=client_secret,
            access_token=access_token,
            refresh_token=refresh_token,
            company_id=company_id
        )

        # Update invoice status
        invoice_data = {
            'Id': invoice_id,
            'InvoiceStatus': status
        }

        response = quickbooks.invoice.update(invoice_data)

        if response.status_code == 200:
            print('Invoice status updated successfully.')
        else:
            print('Failed to update invoice status:', response.content)

    except Exception as e:
        print('Error updating invoice status:', str(e))

def get_customer_invoices(client_id, client_secret, access_token, refresh_token, company_id, customer_id):
    try:
        # Set up QuickBooks client
        quickbooks = QuickBooks(
            client_id=client_id,
            client_secret=client_secret,
            access_token=access_token,
            refresh_token=refresh_token,
            company_id=company_id
        )

        # Get customer invoices
        response = quickbooks.customer.get_invoices(customer_id)

        if response.status_code == 200:
            invoices = response.json()['QueryResponse']['Invoice']
            return invoices
        else:
            print('Failed to fetch customer invoices:', response.content)

        return None

    except Exception as e:
        print('Error fetching customer invoices:', str(e))
        return None

def validate_input(value, message):
    while not value:
        value = input(message)
    return value

def main():
    # Example usage
    client_id = validate_input(input('Enter your client ID: '), 'Client ID: ')
    client_secret = validate_input(input('Enter your client secret: '), 'Client Secret: ')
    access_token = validate_input(input('Enter your access token: '), 'Access Token: ')
    refresh_token = validate_input(input('Enter your refresh token: '), 'Refresh Token: ')
    company_id = validate_input(input('Enter your company ID: '), 'Company ID: ')
    contractor_name = validate_input(input('Enter contractor name: '), 'Contractor Name: ')
    amount = None
    while amount is None:
        try:
            amount = float(input('Enter the invoice amount: '))
        except ValueError:
            print('Invalid input. Please enter a valid number.')

    due_date = validate_input(input('Enter due date (YYYY-MM-DD): '), 'Due Date: ')
    payment_terms = validate_input(input('Enter payment terms: '), 'Payment Terms: ')

    recipient_email = validate_input(input('Enter recipient email: '), 'Recipient Email: ')
    customer_id = validate_input(input('Enter customer ID: '), 'Customer ID: ')

    # Create invoice
    invoice_id = create_invoice(client_id, client_secret, access_token, refresh_token, company_id, contractor_name, amount, due_date, payment_terms)

    if invoice_id:
        print('Invoice created successfully. Invoice ID:', invoice_id)

        # Fetch customer information
        customer_info = get_customer_info(client_id, client_secret, access_token, refresh_token, company_id, contractor_name)

        if customer_info:
            print('Customer Name:', customer_info['DisplayName'])
            print('Customer Email:', customer_info['PrimaryEmailAddr']['Address'])

            # Send invoice via email
            send_invoice_email(client_id, client_secret, access_token, refresh_token, company_id, invoice_id, recipient_email)

            # Retrieve invoice details
            invoice_details = get_invoice_details(client_id, client_secret, access_token, refresh_token, company_id, invoice_id)

            if invoice_details:
                print('Invoice Details:')
                print('-------------------------')
                print('Invoice ID:', invoice_details['Id'])
                print('Invoice Number:', invoice_details['DocNumber'])
                print('Invoice Status:', invoice_details['InvoiceStatus'])
                print('Invoice Total:', format_currency(invoice_details['TotalAmt']))

                # Update invoice status
                new_status = input('Enter new invoice status: ')
                update_invoice_status(client_id, client_secret, access_token, refresh_token, company_id, invoice_id, new_status)

                # Get customer invoices
                customer_invoices = get_customer_invoices(client_id, client_secret, access_token, refresh_token, company_id, customer_id)

                if customer_invoices:
                    print('Customer Invoices:')
                    print('-------------------------')
                    for invoice in customer_invoices:
                        print('Invoice ID:', invoice['Id'])
                        print('Invoice Number:', invoice['DocNumber'])
                        print('Invoice Status:', invoice['InvoiceStatus'])
                        print('Invoice Total:', format_currency(invoice['TotalAmt']))
                else:
                    print('No invoices found for the customer.')
        else:
            print('Failed to fetch customer information.')

if __name__ == '__main__':
    main()