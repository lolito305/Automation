Web Scraping and Data Analysis Tool
This is a Python automation tool that performs web scraping, data analysis, and generates a PDF report for a given website's product prices. It provides insights into the price distribution and key statistics, such as average, maximum, and minimum prices. The tool also sends an email notification with the analysis results and the PDF report attached.

Features
Web scraping of product prices from a specified website.
Data analysis of the scraped prices, including average, maximum, and minimum prices.
Generation of a PDF report containing the analyzed data and a price distribution plot.
Email notification with the analysis results and the PDF report attached.
Prerequisites
Python 3.x
Libraries:
requests
beautifulsoup4
pandas
matplotlib
seaborn
reportlab
tqdm
plyer
smtplib
tkinter
Installation
Clone the repository or download the source code.
Install the required libraries by running the following command:
shell
Copy code
pip install -r requirements.txt
Usage
Open the config.py file and set the following variables:

competitor_url: The URL of the website you want to scrape the prices from.
sender_email: The email address used to send the notification email.
sender_password: The password for the sender email address.
receiver_email: The email address where the notification email will be sent.
Run the main.py script:

shell
Copy code
python main.py
The tool will start scraping the website, analyzing the data, and generating a PDF report. Progress will be displayed in the console.

Once the job is completed, an email notification will be sent to the specified receiver email address, and a desktop notification will be displayed.

The PDF report (report.pdf) will be generated, containing the analyzed data and a price distribution plot.

Customization
If you want to change the scheduled time for the scraping job, modify the start_job function in main.py.
You can customize the email subject and body in the job function in main.py.
Modify the appearance and styling of the PDF report by adjusting the create_pdf_report function in main.py.
License
This project is licensed under the MIT License. See the LICENSE file for details.

Contributing
Contributions are welcome! If you have any suggestions, improvements, or feature requests, please open an issue or submit a pull request.

Authors
Johnny S. Perez
Acknowledgments
This tool is inspired by the need for automating web scraping tasks and providing data analysis in a presentable format.

Troubleshooting
If you encounter any errors or issues while running the tool, please check the log file (scraping.log) for detailed error messages and traceback.
