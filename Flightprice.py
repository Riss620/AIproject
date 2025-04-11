import requests
import time
import smtplib
from email.mime.text import MIMEText

API_KEY = 'e9b389287aea36a58fe62ae01951153f'
API_URL = 'http://api.aviationstack.com/v1/flights'

# Your email config
EMAIL_SENDER = 'rishavku620@gmail.com'
EMAIL_RECEIVER = 'anmolrosera@gmail.com'
EMAIL_PASSWORD = 'xafs pnkn uwqs gvlq'  # Replace with your Gmail app password

# Get user input for flight details
AIRLINE = input("Enter the airline code (e.g., AA for American Airlines): ").strip().upper()
FLIGHT_NUMBER = input("Enter the flight number: ").strip()
ORIGIN_CITY = input("Enter the origin city: ").strip()
DESTINATION_CITY = input("Enter the destination city: ").strip()
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587  # Ensure this is correct for Gmail

# Flight you want to track
AIRLINE = 'AA'  # American Airlines
FLIGHT_NUMBER = '100'  # Example flight number

def get_flight_status():
    params = {
        'access_key': API_KEY,
        'flight_iata': f'{AIRLINE}{FLIGHT_NUMBER}'
    }

    response = requests.get(API_URL, params=params)
    data = response.json()
    
    if 'data' in data and len(data['data']) > 0:
        flight = data['data'][0]
        status = flight.get('flight_status', 'unknown')
        departure = flight['departure'].get('scheduled')
        arrival = flight['arrival'].get('scheduled')
        return f"Flight {AIRLINE}{FLIGHT_NUMBER} status: {status}\nDeparture: {departure}\nArrival: {arrival}"
    else:
        return "No flight data found."

def send_email_alert(status_message):
    message = f"Flight Status Update:\n\n{status_message}"
    msg = MIMEText(message)
    msg['Subject'] = 'Flight Status Update'
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER

    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(EMAIL_SENDER, EMAIL_PASSWORD)
    server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
    server.quit()

def monitor_flight(interval=3600):
    print("Monitoring flight... Press Ctrl+C to stop.")
    last_status = None

    while True:
        try:
            current_status = get_flight_status()
            print(current_status)

            if current_status != last_status:
                send_email_alert(current_status)
                last_status = current_status

            time.sleep(interval)
        except KeyboardInterrupt:
            print("Flight tracking stopped.")
            break
        except Exception as e:
            print(f"Error occurred: {e}")
            time.sleep(60)

if __name__ == "__main__":
    monitor_flight(interval=60)  # Check every 1 mins