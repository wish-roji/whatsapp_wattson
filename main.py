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



# ACTUAL CODE BELOW ---------------------------------------------------------

def open_window():
    global driver
    driver = webdriver.Chrome(service=service)
    driver.get('https://web.whatsapp.com')

    if os.name == 'nt':
        _ = os.system('cls')

    print('1. Scan QR Code\n')
    print('2. Open A Chat\n')
    input("3. Press Enter\n")



    # WHATSAPP----------------------------------------
    
def load():
    global message_text, generated_text, model, tokenizer, input_text
    WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.XPATH, '//div[@role="listitem"]')))
    messages = driver.find_elements(By.XPATH, '//span[@dir="ltr"]//span')
    if not messages:
        print("No messages found!\n")
        print()
    else:
        most_recent_message = messages[-1]
        message_text = most_recent_message.text.strip()
        clear_terminal()
        print("Found Message:\n")
        print("-----------------")
        print(message_text)
        print("-----------------")
        print()    
    model_name = "gpt2-large"  # You can use other models like "gpt2-medium", "gpt2-large", etc.
    model = TFGPT2LMHeadModel.from_pretrained(model_name)
    tokenizer = GPT2Tokenizer.from_pretrained(model_name)
    input_text = message_text


def clear_terminal():
    if os.name == 'nt':
        _ = os.system('cls')
    print("Loading...\n")

def gpt_output():
    global generated_text
    input_ids = tokenizer.encode(input_text, return_tensors="tf")
    output = model.generate(
        input_ids,
        max_length=15,           # Adjusted length
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

def main():
    global service, x, y
    service = Service('chromedriver.exe')
    open_window()
    message_bar_location = pyautogui.locateOnScreen('message_bar.png', confidence=0.8)
    x,y = pyautogui.center(message_bar_location)
    load()
    output = gpt_output()
    # ----------------
    clear_terminal()
    print("Loading Completed!\n")
    print("Executing Message...\n")
    # ----------------
    pyautogui.click(x,y)
    pyautogui.typewrite(output, interval=0.05)
    pyautogui.press('enter')
    
main()    
