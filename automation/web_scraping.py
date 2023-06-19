import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import csv
import schedule
import time
import smtplib
import logging
import threading
import tkinter as tk
from tkinter import messagebox
from tqdm import tqdm
from plyer import notification
import seaborn as sns
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image
from reportlab.lib.styles import getSampleStyleSheet

# Logging configuration
logging.basicConfig(filename='scraping.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def scrape_website(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract product prices
        prices = []
        price_elements = soup.find_all('span', class_='price')
        for element in price_elements:
            price = element.text.strip()
            prices.append(price)

        return prices

    except Exception as e:
        logging.exception(f"Error occurred while scraping {url}: {str(e)}")

def analyze_data(prices):
    try:
        df = pd.DataFrame({'Prices': prices})

        average_price = df['Prices'].mean()
        max_price = df['Prices'].max()
        min_price = df['Prices'].min()

        # Plot price distribution
        sns.histplot(data=df, x='Prices', kde=True)
        plt.title('Price Distribution')
        plt.xlabel('Price')
        plt.ylabel('Count')
        plt.savefig('price_distribution.png')
        plt.close()

        return average_price, max_price, min_price

    except Exception as e:
        logging.exception(f"Error occurred while analyzing data: {str(e)}")

def save_data_to_csv(prices, filename):
    try:
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Price'])
            for price in prices:
                writer.writerow([price])

    except Exception as e:
        logging.exception(f"Error occurred while saving data to CSV: {str(e)}")

def create_pdf_report(prices, average_price, max_price, min_price):
    try:
        doc = SimpleDocTemplate("report.pdf", pagesize=letter)
        styles = getSampleStyleSheet()

        elements = []

        # Add title
        title = Paragraph("Scraping Job Report", styles['Title'])
        elements.append(title)

        # Add analyzed data
        analyzed_data = f"Average Price: {average_price}<br/>Max Price: {max_price}<br/>Min Price: {min_price}"
        data = Paragraph(analyzed_data, styles['BodyText'])
        elements.append(data)

        # Add price distribution plot
        image = Image("price_distribution.png", width=400, height=300)
        elements.append(image)

        doc.build(elements)

    except Exception as e:
        logging.exception(f"Error occurred while creating the PDF report: {str(e)}")

def send_email(subject, body, receiver_email, attachment):
    try:
        sender_email = 'your_email@example.com'
        password = 'your_email_password'

        message = f'Subject: {subject}\n\n{body}'

        with smtplib.SMTP_SSL('smtp.example.com', 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)

    except Exception as e:
        logging.exception(f"Error occurred while sending email: {str(e)}")

def job():
    try:
        competitor_url = 'https://www.example.com'
        prices = scrape_website(competitor_url)
        average_price, max_price, min_price = analyze_data(prices)
        save_data_to_csv(prices, 'scraped_data.csv')
        create_pdf_report(prices, average_price, max_price, min_price)

        # Prepare email notification
        subject = 'Scraping Job Result'
        body = f'Average Price: {average_price}\nMax Price: {max_price}\nMin Price: {min_price}'
        receiver_email = 'receiver_email@example.com'

        # Send email notification with PDF report attached
        send_email(subject, body, receiver_email, 'report.pdf')

        print('Scraping job completed successfully.')
        logging.info('Scraping job completed successfully.')

        # Display notification
        notification.notify(
            title='Scraping Job',
            message='Scraping job completed successfully.',
            timeout=5
        )

    except Exception as e:
        logging.exception(f"Error occurred while executing the job: {str(e)}")

def start_job():
    schedule.every().day.at('09:00').do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)

def start_thread():
    thread = threading.Thread(target=start_job)
    thread.start()
    messagebox.showinfo('Information', 'Scraping job has started.')

if __name__ == '__main__':
    # Create a Tkinter window
    window = tk.Tk()
    window.title('Scraping Job')
    window.geometry('300x100')

    # Create a Start button
    start_button = tk.Button(window, text='Start Job', command=start_thread)
    start_button.pack(pady=20)

    # Run the Tkinter event loop
    window.mainloop()