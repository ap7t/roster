from pathlib import Path
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class OCR:
    def __init__(self):
        self.cwd = Path.cwd()
        self.save_location = self.cwd / "text_files"
        prefs = {'download.default_directory': str(self.save_location)}
        options = webdriver.ChromeOptions()
        options.add_experimental_option('prefs', prefs)
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)
        self.driver.get("https://lightpdf.com/ocr")

    def upload_file(self):
        choose_file = self.driver.find_element_by_class_name("file-input")
        roster_pic = self.cwd / "images/roster.jpg"
        choose_file.send_keys(str(roster_pic))
        upld_msg = self.driver.find_element_by_class_name("loading-msg")
        percentage = upld_msg.text
        print("Uploading file to LightPDF.com")
        while True:
            if "100%" in percentage: break

            upld_msg = self.driver.find_element_by_class_name("loading-msg")
            new_percentage = upld_msg.text
            if new_percentage!= percentage:
                print(new_percentage)
            percentage = new_percentage

    def convert_image(self):
        select_language_xpath = "/html/body/div[4]/div[1]/div/div[3]/div[2]/div/div/div[1]/div[1]/div"
        select_language = WebDriverWait(self.driver,60).until(EC.element_to_be_clickable((By.XPATH, select_language_xpath)))
        select_language.click()
        english_opt_xpath = "/html/body/div[9]/ul/li[9]/div/div[2]"
        english_opt = self.driver.find_element_by_xpath(english_opt_xpath)
        english_opt.click()
        convert_xpath = "/html/body/div[4]/div[1]/div/div[3]/div[2]/div/div/div[3]"
        convert = self.driver.find_element_by_xpath(convert_xpath)
        convert.click()
        print("Converting image")

    def download_text_file(self):
        download_xpath = "/html/body/div[4]/div[1]/div/div[4]/div[2]/div[4]/div[3]/a"
        download =  WebDriverWait(self.driver,60).until(EC.element_to_be_clickable((By.XPATH, download_xpath)))
        download.click()
        print("Downloading file")

    def run(self):
        self.upload_file()
        self.convert_image()
        self.download_text_file()

if __name__ == "__main__":
    ocr = OCR()
    ocr.run()