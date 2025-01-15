print()
print("Note: Messages will appear in console \n")
print("Ignore and proceed with steps (Just Loading Messages) \n")
print()

from transformers import TFGPT2LMHeadModel, GPT2Tokenizer
import os
import pyautogui
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

service = Service('chromedriver.exe')
driver = webdriver.Chrome(service=service)
driver.get('https://web.whatsapp.com')

if os.name == 'nt':
    _ = os.system('cls')

print('1. Scan QR Code\n')
print('2. Open A Chat\n')
print("3. Press Enter\n")


# ACTUAL CODE BELOW _--------------------------------------------------------

def clear_terminal():
    # For Windows
    if os.name == 'nt':
        _ = os.system('cls')

def whatsapp_output():
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '//div[@role="listitem"]')))
    messages = driver.find_elements(By.XPATH, '//span[@dir="ltr"]//span')
    if not messages:
        print("No messages found!")
    else:
        for message in messages:
            message_text = message.text.strip()
            if message_text:
                clear_terminal()
                print("Found Message!\n")
                print("-----------------")
                print(message_text)
                print("-----------------")
                print()
                return message_text


def gpt_output(message):
    global generated_text
    model_name = "gpt2-large"  # You can use other models like "gpt2-medium", "gpt2-large", etc.
    model = TFGPT2LMHeadModel.from_pretrained(model_name)
    tokenizer = GPT2Tokenizer.from_pretrained(model_name)
    
    input_text = message
    
    input_ids = tokenizer.encode(input_text, return_tensors="tf")
    output = model.generate(
        input_ids,
        max_length=25,           # Adjusted length
        num_return_sequences=2,  # Only return one sequence
        no_repeat_ngram_size=2,  # Avoid repeating n-grams
        temperature=0.01,        # Control randomness (lower is less random)
        top_p=0.9,               # Use nucleus sampling
        top_k=50,                # Limit to top 50 most likely next words
        do_sample=True,          # Enable sampling for more creative output
        pad_token_id=tokenizer.eos_token_id  # Avoid padding issues
    )
    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
    generated_text = generated_text.strip()
    return generated_text

def enter_message():
    message_bar_location = pyautogui.locateOnScreen('message_bar.png', confidence=0.8)
    x,y = pyautogui.center(message_bar_location)
    pyautogui.click(x,y)
    pyautogui.typewrite(generated_text, interval=0.05)
    pyautogui.press('enter')
    
    

message_data = whatsapp_output()
gpt_data = gpt_output(message_data)
clear_terminal()
print("Remove Hands 🤚🤚  Off Computer\n")
time.sleep(0.75)
print("Printing Message...")
enter_message()     
