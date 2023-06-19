# Web Scraping and Data Analysis Tool

This is a Python-based web scraping and data analysis tool that allows you to automate the collection and analysis of product prices from any website. It provides valuable insights such as average, maximum, and minimum prices, as well as a price distribution plot. With this tool, you can make informed decisions and stay ahead of the competition.

## Features

- **Web Scraping**: Effortlessly scrape product prices from any website using robust web scraping techniques.
- **Data Analysis**: Analyze the scraped prices to gain insights into the average, maximum, and minimum prices.
- **Price Distribution Plot**: Visualize the distribution of prices using a histogram plot.
- **PDF Report Generation**: Generate a comprehensive PDF report containing the analyzed data and the price distribution plot.
- **Email Notifications**: Receive email notifications with the analysis results and the PDF report attached.

## Installation

1. Clone the repository:
   ```shell
   git clone https://github.com/lolito305/Automation/blob/main/automation/web_scraping.py
Install the required dependencies:
shell
Copy code
pip install -r requirements.txt
## Usage
Set the necessary configurations in the config.py file:

competitor_url: The URL of the website you want to scrape the prices from.
sender_email: The email address used to send the notification email.
sender_password: The password for the sender email address.
receiver_email: The email address where the notification email will be sent.
Run the main.py script:

shell
Copy code
python main.py
The tool will start scraping the website, analyzing the data, and generating a PDF report. The progress will be displayed in the console.

Once the job is completed, an email notification will be sent to the specified receiver email address, and a desktop notification will be displayed.

The PDF report (report.pdf) will be generated, containing the analyzed data and a price distribution plot.

## Customization
Modify the scraping logic by editing the scrape_website function in main.py.
Adjust the data analysis process by modifying the analyze_data function in main.py.
Customize the appearance and styling of the PDF report by adjusting the create_pdf_report function in main.py.
## License
This project is licensed under the MIT License. See the LICENSE file for more details.

## Contributing
Contributions are welcome! If you have any suggestions, improvements, or feature requests, please open an issue or submit a pull request.

## Authors
Johnny S. Perez
## Acknowledgments
This tool was inspired by the need for automating web scraping tasks and providing data analysis in a presentable format.

## Troubleshooting
If you encounter any errors or issues while running the tool, please check the log file (scraping.log) for detailed error messages and traceback.
