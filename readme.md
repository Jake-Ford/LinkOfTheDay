# Introduction

This code creates a simple automated tool to send a daily link to your friends, family or frenemies. I copied this idea from a friend in Toronto who sends her Dad a weekly email with an interesting link; I loved this idea and wanted to make it pythonic. 

## Requirements

1. Google gmail account with Two-Factor Authentication (2FA) enabled
2. Genearte a App Password, 16 character password for your app
3. Save the password and your email address you wish to send to in your .env file 

## Deployment

For this project, I set up a simple cron job to automatically run the script, reading through the data.csv file i have here as an example, to check the date. See the `link_of_the_day.py` script for the mechanics, relatively straighforward date check logic. 