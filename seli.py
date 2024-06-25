from selenium import webdriver

# Assuming takecommand() is defined somewhere else
def takecommand():
    # Mocking the function for this example
    return "python selenium tutorial"

driver = webdriver.Chrome("chromedriver.exe")  # Ensure the path to chromedriver is correct

search_query = takecommand().lower()
if search_query != 'none':
    driver.get(f'https://www.google.com/search?q={search_query}')
