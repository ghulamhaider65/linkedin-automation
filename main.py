import time
import random
import pandas as pd
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


EMAIL = "dummy@gmail.com"
PASSWORD = "xyz"
KEYWORD = "Data Scientist"
WAIT_TIME = 10


def random_sleep(a=2, b=5):
    time.sleep(random.uniform(a, b))


def login_linkedin(driver):
    driver.get("https://www.linkedin.com/login")
    WebDriverWait(driver, WAIT_TIME).until(EC.presence_of_element_located((By.ID, "username")))
    email_input = driver.find_element(By.ID, "username")
    password_input = driver.find_element(By.ID, "password")

    email_input.send_keys(EMAIL)
    password_input.send_keys(PASSWORD)
    password_input.send_keys(Keys.RETURN)
    print("Logged in Successfully!")
    random_sleep(5, 8)


def scrape_jobs(driver):
    search_url = f"https://www.linkedin.com/jobs/search/?keywords={KEYWORD}"
    driver.get(search_url)
    random_sleep(5, 8)

    jobs_data = []

    job_cards = driver.find_elements(By.CSS_SELECTOR, "div.base-card")
    print(f"Found {len(job_cards)} job cards.")

    for card in job_cards:
        try:
            title_elem = card.find_element(By.CSS_SELECTOR, "h3")
            company_elem = card.find_element(By.CSS_SELECTOR, "h4")
            location_elem = card.find_element(By.CSS_SELECTOR, "span.job-search-card__location")
            posted_elem = card.find_element(By.CSS_SELECTOR, "time")
            link_elem = card.find_element(By.CSS_SELECTOR, "a.base-card__full-link")

            title = title_elem.text.strip()
            company = company_elem.text.strip()
            location = location_elem.text.strip()
            posted_date = posted_elem.get_attribute("datetime")
            job_link = link_elem.get_attribute("href")

            driver.execute_script("arguments[0].scrollIntoView();", card)
            card.click()
            random_sleep(3, 5)

            description_elem = WebDriverWait(driver, WAIT_TIME).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.show-more-less-html__markup"))
            )
            description = description_elem.text.strip()

            jobs_data.append({
                'Title': title,
                'Company': company,
                'Location': location,
                'Posted Date': posted_date,
                'Job Link': job_link,
                'Description': description
            })

            random_sleep(2, 4)

        except Exception as e:
            print(f"Error scraping a card: {e}")
            continue

    return jobs_data


def save_to_csv(jobs_data):
    df = pd.DataFrame(jobs_data)
    df.to_csv('linkedin_jobs.csv', index=False)
    print("Data saved to linkedin_jobs.csv")


def main():
    options = uc.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = uc.Chrome(options=options)

    try:
        login_linkedin(driver)
        jobs_data = scrape_jobs(driver)
        save_to_csv(jobs_data)

    finally:
        driver.quit()


if __name__ == "__main__":
    main()


