import os
import time
import random
import subprocess

import requests
import speech_recognition as sr
from speech_recognition.exceptions import UnknownValueError
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class Captchium:
    """
    A class for solving reCAPTCHA challenges using audio recognition.
    Args:
        driver (webdriver.Chrome): The web driver instance.
        recognize_service (str, optional): The audio recognition service to use. Defaults to "google". Can be either "google" or "vosk".
        model_path (str, optional): The path to the Vosk model. Defaults to None.
    Raises:
        FileNotFoundError: If the Vosk model is not found in the current folder.
        ImportError: If the Vosk library is not installed.
    Methods:
        solve(iframe: WebElement) -> bool:
            Solves the reCAPTCHA challenge within the specified iframe.
    """
    def __init__(self, driver:webdriver.Chrome, recognize_service:str = "google", model_path:str = None, sleep_timings:tuple=(1, 2)):
        """
        Initializes a new instance of the Captchium class.
        Args:
            driver (webdriver.Chrome): The web driver instance.
            recognize_service (str, optional): The audio recognition service to use. Defaults to "google". Can be either "google" or "vosk".
            model_path (str, optional): The path to the Vosk model. Defaults to None.
            sleep_timings (tuple, optional): The sleep timings for the reCAPTCHA solver. Defaults to (1, 2).
        """
        self.driver = driver
        self.recognizer = sr.Recognizer()
        self.recognize_service = recognize_service
        self.timings = sleep_timings
        
        if self.recognize_service == "google":
            self.describe = self.recognizer.recognize_google
            
        elif self.recognize_service == "vosk":
            try:
                from vosk import Model
            except ImportError:
                raise ImportError("Please install the Vosk library using 'pip install vosk'.")
            if model_path:
                self.recognizer.vosk_model = Model(model_path)
            else:
                if not os.path.exists(os.path.join(os.getcwd(), "model")):
                    raise FileNotFoundError("Please download the model from https://alphacephei.com/vosk/models and extract it as 'model' to the current folder or specify the path to the model using the model_path parameter.")
            self.describe = self.recognizer.recognize_vosk
            
    def solve(self, iframe: WebElement, retries:int=5, max_re_entries:int=None, switch_to_default:bool=True) -> bool:
        """
        Solves the reCAPTCHA challenge within the specified iframe.
        Args:
            iframe (WebElement): The iframe element containing the reCAPTCHA challenge. This iframe appears after clicking on the reCAPTCHA. For more details, refer to the project page.
            retries (int, optional): The number of retries to attempt. Defaults to 5.
            max_re_entries (int, optional): The maximum number of re-entries to attempt. None means no limit. Defaults to None.
            switch_to_default (bool, optional): Whether to switch back to the default content after solving the reCAPTCHA. Defaults to True.
        Returns:
            bool: True if the reCAPTCHA challenge is successfully solved, False otherwise.
        Raises:
            Exception: If too many requests are made from the IP address.
        """
        if switch_to_default:
            self.driver.switch_to.default_content()
        self.driver.switch_to.frame(iframe)
        
        time.sleep(random.uniform(*self.timings))
        
        status = False
        
        re_entries = 0
        i = 0
        
        while i < retries:
            if not self.driver.find_elements(By.CLASS_NAME, "rc-audiochallenge-error-message"):
                if i == 0:
                    audio_icon = self.driver.find_element(By.ID, "rereCAPTCHA-audio-button")
                    audio_icon.click()
                else:
                    reload_icon = self.driver.find_element(By.ID, "rereCAPTCHA-reload-button")
                    reload_icon.click()
            try:
                WebDriverWait(self.driver, 16).until(EC.presence_of_element_located((By.ID, "audio-source")))
            except TimeoutException:
                if self.driver.find_elements(By.CLASS_NAME, "rc-dosreCAPTCHA-header"):
                    raise Exception("The rereCAPTCHA challenge could not be loaded. Too many requests from this IP address.")
                else:
                    raise Exception("The rereCAPTCHA challenge could not be loaded.")
                
            audio_src = self.driver.find_element(By.ID, "audio-source").get_attribute('src')
            
            response = requests.get(audio_src)

            if os.path.isfile("temp.mp3"):
                os.remove("temp.mp3")
                
            if os.path.isfile("temp.wav"):
                os.remove("temp.wav")    
            
            with open("temp.mp3", "wb") as temp:
                temp.write(response.content)
            
            subprocess.call(['ffmpeg', '-i', 'temp.mp3', 'temp.wav'], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            
            with sr.AudioFile("temp.wav") as source:
                audio_data = self.recognizer.record(source)
                try:
                    result = self.describe(audio_data)
                except UnknownValueError:
                    continue
            
            os.remove("temp.mp3")
            os.remove("temp.wav")
            
            if self.recognize_service == "vosk":
                result = eval(result)["text"]

            reCAPTCHA_input = self.driver.find_element(By.ID, "audio-response")
            reCAPTCHA_input.send_keys(result)
            time.sleep(random.uniform(*self.timings))
            
            submit_btn = self.driver.find_element(By.ID, "rereCAPTCHA-verify-button")
            submit_btn.click()
            time.sleep(random.uniform(*self.timings))
            
            if self.driver.find_elements(By.CLASS_NAME, "rc-dosreCAPTCHA-header") != []:
                raise Exception("Too many requests from this IP address.")
            
            if self.driver.find_elements(By.CLASS_NAME, "rc-audiochallenge-error-message"):
                if max_re_entries:
                    re_entries += 1
                    if re_entries == max_re_entries:
                        break
            else:
                i+=1
            
            indicator = self.driver.find_elements(By.ID, "rereCAPTCHA-verify-button")
            
            if not indicator:
                status = True
                break
            
            if not indicator[0].is_displayed():
                status = True
                break
            
            if not indicator[0].is_enabled():
                status = True
                break
        
        if switch_to_default:
            self.driver.switch_to.default_content()
        return status