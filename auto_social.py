import random
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Cấu hình thông tin tài khoản mạng xã hội tương ứng với từng website
WEBSITES_SOCIAL_ACCOUNTS = {
    "https://myglastar.com": {
        "consumer_key": "ck_945bc16950c79af2b73c3583935712c873378503",
        "consumer_secret": "cs_18e83c441317a4ac2b66d63379d575c3eea99865",
        "facebook": {
            "access_token": "EAANH9bkyaN4BO9fMi8DTIAsZCGOSDF92Se5uOdZBwBKgYrTvxlfyvRo1fS4kCAl9zJasbeiWnJ8TLnGGAHpaC14cwGhAhzRsm4sdvMrqoOIWMJ4k00bE3l9rSjDevHLA2uMHdQcael8y5UNzrZBZBF182VZCjhvLBS7gvKpKBdIEZAgVFsPFZBFK2rgUbxd0E01j3CirBJPEZACXnFuXf9VH",
        },
        "instagram": {
            "username": "tranthanhnhai08@gmail.com",
            "password": "Tranthanhnhai",
        },
        "x": {
            "api_key": "YOUR_X_API_KEY_WEBSITE1",
            "api_secret": "YOUR_X_API_SECRET_WEBSITE1",
            "access_token": "YOUR_X_ACCESS_TOKEN_WEBSITE1",
            "access_token_secret": "YOUR_X_ACCESS_TOKEN_SECRET_WEBSITE1",
        }
    },
    # "https://website2.com": {
    #     "consumer_key": "ck_945bc16950c79af2b73c3583935712c873378503",
    #     "consumer_secret": "cs_18e83c441317a4ac2b66d63379d575c3eea99865",
    #     "facebook": {
    #         "access_token": "YOUR_FACEBOOK_ACCESS_TOKEN_WEBSITE2",
    #     },
    #     "instagram": {
    #         "username": "YOUR_INSTAGRAM_USERNAME_WEBSITE2",
    #         "password": "YOUR_INSTAGRAM_PASSWORD_WEBSITE2",
    #     },
    #     "x": {
    #         "api_key": "YOUR_X_API_KEY_WEBSITE2",
    #         "api_secret": "YOUR_X_API_SECRET_WEBSITE2",
    #         "access_token": "YOUR_X_ACCESS_TOKEN_WEBSITE2",
    #         "access_token_secret": "YOUR_X_ACCESS_TOKEN_SECRET_WEBSITE2",
    #     }
    # },
    # Thêm các website khác nếu cần
}

# Danh sách các website
WEBSITES = [
    "https://myglastar.com",
    # "https://website2.com",
    # Thêm các website khác nếu cần
]

# Hàm đăng bài lên Facebook
def post_to_facebook(facebook_token, message, image_url):
    url = f"https://graph.facebook.com/v12.0/me/photos"
    payload = {
        "message": message,
        "url": image_url,
        "access_token": facebook_token
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        print("✅ Đăng bài lên Facebook thành công.")
    else:
        print(f"❌ Lỗi khi đăng bài lên Facebook: {response.text}")

# Hàm đăng bài lên Instagram
def post_to_instagram(instagram_username, instagram_password, image_url, caption):
    driver = create_driver()
    driver.get("https://www.instagram.com/accounts/login/")

    try:
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.NAME, "username")))
        driver.find_element(By.NAME, "username").send_keys(instagram_username)
        driver.find_element(By.NAME, "password").send_keys(instagram_password)
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        # Chờ và bỏ qua popup Save Login Info
        try:
            not_now_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]"))
            )
            not_now_button.click()
        except:
            pass

        # Chờ và bỏ qua popup Turn on Notifications
        try:
            not_now_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]"))
            )
            not_now_button.click()
        except:
            pass

        # Chờ nút New Post và click
        WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "svg[aria-label='New post']"))
        ).click()

        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR, "input[type='file']").send_keys(image_url)
        time.sleep(2)

        driver.find_element(By.CSS_SELECTOR, "textarea[aria-label='Write a caption…']").send_keys(caption)
        driver.find_element(By.CSS_SELECTOR, "button[type='button']").click()
        print("✅ Đăng bài lên Instagram thành công.")

    except Exception as e:
        print(f"❌ Lỗi khi đăng bài lên Instagram: {e}")

    driver.quit()
# Hàm đăng bài lên X (Twitter)
def post_to_x(api_key, api_secret, access_token, access_token_secret, message):
    url = "https://api.twitter.com/2/tweets"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    payload = {"status": message}
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 201:
        print("✅ Đăng bài lên X (Twitter) thành công.")
    else:
        print(f"❌ Lỗi khi đăng bài lên X (Twitter): {response.text}")

# Tạo WebDriver để duyệt web
def create_driver():
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

# Lấy một sản phẩm bất kỳ từ WordPress (REST API)
def get_random_product_from_wordpress(website_url, consumer_key, consumer_secret):
    rest_api_url = f"{website_url}/wp-json/wc/v3/products"
    try:
        response = requests.get(rest_api_url, auth=(consumer_key, consumer_secret), timeout=10)
        response.raise_for_status()
        product_data = response.json()
        if product_data:
            product = random.choice(product_data)
            product_name = product.get("name", "No Name")
            product_image = product.get("images", [{}])[0].get("src", "")
            return product_name, product_image
        else:
            print(f"❌ Không có sản phẩm nào ở {website_url}")
            return None, None
    except requests.exceptions.RequestException as e:
        print(f"❌ Lỗi khi lấy sản phẩm từ {website_url}: {e}")
        return None, None

# Đăng sản phẩm lên các mạng xã hội
def post_product_on_social_media(website_url):
    social_accounts = WEBSITES_SOCIAL_ACCOUNTS.get(website_url)
    if not social_accounts:
        print(f"❌ Không tìm thấy thông tin tài khoản mạng xã hội cho {website_url}")
        return

    consumer_key = social_accounts["consumer_key"]
    consumer_secret = social_accounts["consumer_secret"]

    facebook_token = social_accounts["facebook"]["access_token"]
    instagram_username = social_accounts["instagram"]["username"]
    instagram_password = social_accounts["instagram"]["password"]
    x_api_key = social_accounts["x"]["api_key"]
    x_api_secret = social_accounts["x"]["api_secret"]
    x_access_token = social_accounts["x"]["access_token"]
    x_access_token_secret = social_accounts["x"]["access_token_secret"]

    product_name, product_image_url = get_random_product_from_wordpress(
        website_url,
        consumer_key,
        consumer_secret
    )

    if product_name and product_image_url:
        post_message = f"New product: {product_name} - in website: {website_url}"
        post_to_facebook(facebook_token, post_message, product_image_url)
        post_to_instagram(instagram_username, instagram_password, product_image_url, post_message)
        # post_to_x(x_api_key, x_api_secret, x_access_token, x_access_token_secret, post_message)

# ======================== Chạy chương trình ========================

# Cập nhật thông tin sản phẩm và đăng lên các mạng xã hội
if __name__ == "__main__":
    for website_url in WEBSITES:  # Lặp qua tất cả các website
        post_product_on_social_media(website_url)