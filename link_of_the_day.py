import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd
from dotenv import load_dotenv
import os
import datetime

load_dotenv()

sender_email = os.getenv("SENDER_EMAIL")
sender_password = os.getenv("SENDER_PASSWORD")



def read_csv(file_path):
    """Reads data from a CSV file."""
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        return list(reader)

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
    csv_file_path = "data.csv"  # Replace with your CSV file path
    sender_email = "jake.ford927@gmail.com"  # Replace with your Gmail address
    # get today's date
    today = datetime.date.today()
    
    subject = f"Here's the daily link for {today}!"
    
    # Read data from the CSV file
    data = pd.read_csv(csv_file_path)    
   
    for index, row in data.iterrows():
        receiver_email = row['Email']  # Assumes 'Email' column in CSV
        link = row['Link']  # Assumes 'Link' column in CSV
        body = f"Hello,\n\nHere is your link: {link}\n\nBest regards,\nYour Name"
        send_email(receiver_email, subject, body, sender_email, sender_password)

if __name__ == "__main__":
    main()