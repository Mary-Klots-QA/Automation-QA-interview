from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Setup browser before each scenario
def before_scenario(context, scenario):
    # Initialize Chrome WebDriver with Service
    service = Service(ChromeDriverManager().install())
    context.driver = webdriver.Chrome(service=service)
    context.driver.maximize_window()

# Teardown browser after each scenario
def after_scenario(context, scenario):
    if hasattr(context, 'driver'):
        context.driver.quit()
