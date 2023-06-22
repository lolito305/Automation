# QuickBooks Invoice Automation

This script enables automated invoice creation and management using the QuickBooks API. It allows you to create invoices, fetch customer information, send invoices via email, retrieve invoice details, update invoice status, and retrieve customer invoices.

## Prerequisites

- Python 3.x
- QuickBooks API credentials (client ID, client secret, access token, refresh token)
- QuickBooks company ID

## Installation

1. Clone the repository:

   ```shell
   git clone https://github.com/your-username/quickbooks-invoice-automation.git

Install the dependencies:

shell
Copy code
pip install -r requirements.txt
Set up QuickBooks API credentials:

Obtain the client ID, client secret, access token, refresh token from the QuickBooks Developer portal.
Replace the placeholder values in the script with your own credentials.

## Usage
Run the script:

shell
Copy code
python invoice_automation.py
Enter the required information when prompted:

Client ID: Your QuickBooks API client ID.
Client Secret: Your QuickBooks API client secret.
Access Token: Your QuickBooks API access token.
Refresh Token: Your QuickBooks API refresh token.
Company ID: Your QuickBooks company ID.
Contractor Name: The name of the contractor.
Invoice Amount: The amount for the invoice.
Due Date: The due date for the invoice in the format YYYY-MM-DD.
Payment Terms: The payment terms for the invoice.
Recipient Email: The email address of the recipient.
Customer ID: The ID of the customer.
Follow the script's instructions to create and manage invoices.

## Script Functions
create_invoice: Creates an invoice with the specified details.
get_customer_info: Retrieves information about a customer based on the name.
send_invoice_email: Sends an invoice via email to the recipient.
get_invoice_details: Retrieves details of a specific invoice.
update_invoice_status: Updates the status of an invoice.
get_customer_invoices: Retrieves all invoices associated with a customer.
validate_input: Validates user input and prompts for input if necessary.
main: Main function that orchestrates the invoice creation and management process.
Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License
This project is licensed under the MIT License.
