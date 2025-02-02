#!/usr/bin/env python3

import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd
from dotenv import load_dotenv
import os
from datetime import datetime  # Ensure this is correct
import sys

# Load environment variables
load_dotenv()

sender_email = os.getenv("SENDER_EMAIL")
sender_password = os.getenv("SENDER_PASSWORD")

if not sender_email or not sender_password:
    raise ValueError("Missing email credentials in .env file")

# File paths
csv_file_path = "/Users/jacobford/Documents/GitHub/LinkOfTheDay/data.csv"
log_path = "/Users/jacobford/Documents/GitHub/LinkOfTheDay/logfile.log"

def log_message(message):
    with open(log_path, "a") as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")

def send_email(receiver_email, subject, body, sender_email, sender_password):
    """Sends an email with the given subject and body."""
    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            log_message(f"Email sent to {receiver_email}")
    except Exception as e:
        log_message(f"Error sending email to {receiver_email}: {e}")

def main():
    log_message("Script started.")

    # Read data from the CSV file
    try:
        data = pd.read_csv(csv_file_path)
    except FileNotFoundError:
        log_message(f"File not found: {csv_file_path}")
        return

    now = datetime.now()

    # Ensure the Date column is properly formatted
    data["Date"] = data["Date"].astype(str).str.strip()

    for index, row in data.iterrows():
        if not row["Date"] or row["Date"] == "nan":
            log_message(f"Skipping row {index}: Date is missing.")
            continue

        try:
            scheduled_date = datetime.strptime(row["Date"], "%m/%d/%y")
        except ValueError:
            log_message(f"Skipping row {index}: Invalid date format '{row['Date']}'")
            continue

        if now.date() == scheduled_date.date():  # Compare only the dates
            receiver_email = row['Email']
            link = row['Link']
            subject = f"Here's the daily link for {scheduled_date.strftime('%m/%d/%Y')}!"
            blurb = row['Blurb']
            body = f"Greetings Rambo, \n\n It may be the finest day of my life :) \n\nHere is your weekly link of interest: {link} \n\n{blurb} \n\nLove ya,\nJake"
            send_email(receiver_email, subject, body, sender_email, sender_password)

    log_message("Script completed successfully.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log_message(f"Script failed: {e}")
