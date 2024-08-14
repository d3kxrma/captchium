# Captchium

Captchium is a Python library for solving Google reCAPTCHA challenges using audio recognition. It provides a convenient way to automate CAPTCHA solving in web scraping or automation tasks.

## Installation

To install Captchium, you can use pip:

```shell
pip install captchium
```

## Usage

Here's an example of how to use Captchium:

```python
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
from captchium import Captchium
from driverium import Driverium

# Create a web driver instance
driver_options = webdriver.ChromeOptions()
service = Service(Driverium().get_driver())
driver = webdriver.Chrome(service=service, options=driver_options)

# Initialize Captchium with the web driver instance
captchium = Captchium(driver, recognize_service="google")

# Solve the CAPTCHA challenge within an iframe
iframe = driver.find_element(By.TAG_NAME, "iframe")
captchium.solve(iframe)

# Continue with your automation task
# ...
```

To use the `solve` function, you need to pass the iframe element that opens after clicking on the CAPTCHA. This can be done by locating the iframe element using Selenium's `find_element` method and passing it as an argument to the `solve` function.

**Do not pass this iframe to the function**
![Not this iframe ](https://i.imgur.com/oSyw2qx.png)

**Pass this iframe**
![This iframe](https://i.imgur.com/uF0AtlI.png)

## Supported Audio Recognition Services

Captchium currently supports two audio recognition services: Google and Vosk. By default, it uses the Google service. You can specify the service when initializing Captchium:

```python
captchium = Captchium(driver, recognize_service="vosk")
```

Please note that if you choose the Vosk service, you need to download the Vosk model from [https://alphacephei.com/vosk/models](https://alphacephei.com/vosk/models) and unpack it as 'model' in the current folder.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request on the [Captchium GitHub repository](https://github.com/d3kxrma/captchium).

## License

Captchium is licensed under the MIT License. See the [LICENSE](https://github.com/d3kxrma/captchium/LICENSE) file for more information.
