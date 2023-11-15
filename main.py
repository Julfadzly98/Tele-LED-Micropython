from machine import Pin
import time
import urequests

# Replace 'YOUR_BOT_TOKEN' with your Telegram bot token
BOT_TOKEN = 'your-token'
# Replace 'YOUR_CHAT_ID' with your chat ID (you can get it by messaging the BotFather with the command /get_id)
CHAT_ID = 'your-ID'
# Replace 'YOUR_LED_PIN' with the GPIO pin connected to the LED
LED_PIN = 0

# Set up the LED pin
led_pin = Pin(LED_PIN, Pin.OUT)

def connect():
    import network
 
    ssid = "Staff KML" 
    password = "stafkml@15" 
 
    station = network.WLAN(network.STA_IF)
 
    if station.isconnected() == True:
        print("Already connected")
        return
 
    station.active(True)
    station.connect(ssid, password)
 
    while station.isconnected() == False:
        pass
 
    print("Connection successful")
    print(station.ifconfig())
    
connect()

# Function to turn on the LED
def turn_on_led():
    led_pin.on()
    send_telegram_message("LED is ON")

# Function to turn off the LED
def turn_off_led():
    led_pin.off()
    send_telegram_message("LED is OFF")

# Function to send a message to the Telegram chat
def send_telegram_message(message):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    params = {'chat_id': CHAT_ID, 'text': message}
    urequests.post(url, json=params)

# Main loop
while True:
    try:
        # Make an HTTP request to get updates from Telegram
        response = urequests.get(f'https://api.telegram.org/bot{BOT_TOKEN}/getUpdates')
        updates = response.json().get('result')
        response.close()

        if updates:
            # Process the latest update
            latest_update = updates[-1]
            message_text = latest_update.get('message', {}).get('text', '').lower()

            # Check for commands to control the LED
            if 'on' in message_text:
                turn_on_led()
            elif 'off' in message_text:
                turn_off_led()

        # Wait for a short duration before checking for updates again
        time.sleep(5)
    except Exception as e:
        print(f"An error occurred: {e}")


