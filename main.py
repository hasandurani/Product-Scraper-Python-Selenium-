from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)
def scrape_daraz(max_pages=3):
    url = "https://www.daraz.pk/"
    driver.get(url)

    # Search box
    search = wait.until(EC.presence_of_element_located((By.ID, 'q')))
    search.send_keys("Mobile")  # keyword fixed
    search.submit()

    all_products = []

    for page in range(1, max_pages + 1):
        print(f"Scraping page {page}...")

        # Wait for products to load
        wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'RfADt')))
        time.sleep(2)  # small delay for stability

        # Collect product elements
        names = driver.find_elements(By.CLASS_NAME, "RfADt")  # Product names
        prices = driver.find_elements(By.CLASS_NAME, "ooOxS")  # Prices
        links = driver.find_elements(By.XPATH, "//div[@class='RfADt']/a")  # Product links

        for i in range(len(names)):
            try:
                product = {
                    "Name": names[i].text,
                    "Price": prices[i].text if i < len(prices) else "N/A",
                    "Link": links[i].get_attribute("href") if i < len(links) else "N/A"
                }
                all_products.append(product)
            except Exception as e:
                print("Error extracting product:", e)

        # Next page
        try:
            next_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[@title='Next Page']")))
            driver.execute_script("arguments[0].click();", next_btn)
        except:
            print("No more pages.")
            break

    return all_products


if __name__ == "__main__":
    products = scrape_daraz(max_pages=3)

    # Save to CSV
    df = pd.DataFrame(products)
    file_name = "daraz_mobiles.csv"
    df.to_csv(file_name, index=False, encoding="utf-8-sig")

    print(f"\nScraping complete. {len(products)} products saved to {file_name}")

    driver.quit()
