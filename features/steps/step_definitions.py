from behave import given, when, then
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


@given('I am on the Bank Manager Login page')
def step_go_to_login_page(context):
    context.driver.get("https://www.globalsqa.com/angularJs-protractor/BankingProject/#/login")


@when('I log in as a Bank Manager')
def step_login_as_bank_manager(context):
    print("Logging in as Bank Manager...")
    # Wait for the 'Bank Manager Login' button to be clickable
    WebDriverWait(context.driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Bank Manager Login')]"))
    ).click()


@when('I add a customer with "{first_name}" as first name, "{last_name}" as last name and "{postcode}" as postcode')
def step_add_customer_data(context, first_name, last_name, postcode):
    WebDriverWait(context.driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Add Customer')]"))
    ).click()
    # context.driver.find_element(By.XPATH, "//button[text()='Add Customer']").click()
    first_name_input = WebDriverWait(context.driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='First Name']"))
    )
    first_name_input.send_keys(first_name)
    context.driver.find_element(By.XPATH, "//input[@placeholder='Last Name']").send_keys(last_name)
    context.driver.find_element(By.XPATH, "//input[@placeholder='Post Code']").send_keys(postcode)
    context.driver.find_element(By.XPATH, "//button[text()='Add Customer']").click()
    # Handle alert popup
    alert = context.driver.switch_to.alert
    assert "Customer added successfully" in alert.text
    alert.accept()


@when('I search for the customer "{first_name}" in the Customers list')
def step_search_for_name_in_customer_list(context, first_name):
    context.driver.find_element(By.XPATH, "//button[contains(text(),'Customers')]").click()
    search_box = WebDriverWait(context.driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Search Customer']"))
    )
    search_box.send_keys(first_name)
    time.sleep(1)


@then('I should see "{full_name}" in the customers list')
def step_check_name_in_customer_list(context, full_name):
    first_name, last_name = full_name.split()
    
    # Wait for the first name to appear in the list
    try:
        # Locate the row containing both first and last name
        customer_row = WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//tr[td[1][contains(text(), '{first_name}')]][td[2][contains(text(), '{last_name}')]]"))
        )

        # Validate that both names are present
        assert customer_row is not None, f"{full_name} not found in the customers list."
        
    except Exception as e:
        print(context.driver.page_source)  
        raise e


@when('I delete the customer "{first_name}"')
def step_delete_customer(context, first_name):
    context.driver.find_element(By.XPATH,
    "//button[contains(text(),'Customers')]").click()
    search_box = context.driver.find_element(By.XPATH, "//input[@placeholder='Search Customer']")
    search_box.clear()
    search_box.send_keys(first_name)
    time.sleep(1)
    # Delete customer
    delete_button = context.driver.find_element(By.XPATH, "//button[text()='Delete']")
    delete_button.click()


@then('I should not see "{full_name}" in the customers list')
def step_check_no_name_in_customer_list(context, full_name):
    time.sleep(1) # Time for page to refresh
    no_results = len(context.driver.find_elements(By.XPATH, f"//td[contains(text(),'{full_name}')]")) == 0
    assert no_results, f"Customer {full_name} was not deleted."
