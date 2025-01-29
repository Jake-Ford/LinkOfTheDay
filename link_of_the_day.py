#!/usr/bin/env python3


import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd
from dotenv import load_dotenv
import os
from datetime import datetime  # Ensure this is correct

# Load environment variables
load_dotenv()

sender_email = os.getenv("SENDER_EMAIL")
sender_password = os.getenv("SENDER_PASSWORD")

def send_email(receiver_email, subject, body, sender_email, sender_password):
    """Sends an email with the given subject and body."""
    try:
        # Set up the email
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Connect to the Gmail SMTP server
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            print(f"Email sent to {receiver_email}")
    except Exception as e:
        print(f"Error sending email: {e}")

def main():
    # File path to your CSV
    #csv_file_path = "data.csv"  # Replace with your CSV file path
    csv_file_path = '/Users/jacobford/Documents/GitHub/LinkOfTheDay/data.csv'
    
    # Read data from the CSV file
    data = pd.read_csv(csv_file_path)
    now = datetime.now()

    for index, row in data.iterrows():
        # Update the format to match your CSV
        scheduled_date = datetime.strptime(row['Date'], "%m/%d/%y")  # Parse the 'Date' column
        if now.date() == scheduled_date.date():  # Compare only the dates
            receiver_email = row['Email']  # Assumes 'Email' column in CSV
            link = row['Link']  # Assumes 'Link' column in CSV
            subject = f"Here's the daily link for {scheduled_date.strftime('%m/%d/%Y')}!"
            blurb = row['Blurb']  # Assumes 'Blurb' column in CSV
            body = f"Greetings Rambo, \n\n It may be the finest day of my life :) \n\nHere is your weekly link of interest: {link} \n\n{blurb} \n\nLove ya,\nJake"
            send_email(receiver_email, subject, body, sender_email, sender_password)

if __name__ == "__main__":
    main()
