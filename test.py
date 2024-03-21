from playwright.sync_api import sync_playwright
from dataclasses import dataclass, asdict
import pandas as pd
import argparse
import os

@dataclass
class Business:
    name: str = None
    address: str = None
    website: str = None
    phone_number: str = None

@dataclass
class BusinessList:
    business_list=[]
    save_at = 'output'

    def dataframe(self):
        return pd.json_normalize((asdict(business) for business in self.business_list), sep="_")
    
    def save_to_excel(self, filename):
        if not os.path.exists(self.save_at):
            os.makedirs(self.save_at)
        self.dataframe().to_excel(f"{self.save_at}/{filename}.xlsx", index=False)

    def save_to_csv(self, filename):
        if not os.path.exists(self.save_at):
            os.makedirs(self.save_at)
        self.dataframe().to_csv(f"{self.save_at}/{filename}.csv", index=False)

def main():
     with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto("https://www.google.com", timeout=90000)
        page.wait_for_timeout(5000)
        
        #page.locator('//input[@id="searchboxinput"]').fill(search_for)
        page.locator('//textarea').nth(0).fill(search_for)
        page.wait_for_timeout(3000)

        page.keyboard.press("Enter")
        page.wait_for_timeout(5000)
        more_places_button = page.locator("//g-more-link/a")
        more_places_button.click()
        page.wait_for_timeout(5000)
        listings = page.locator('//div[contains(@class, "rllt__details")]').all()
        print(len(listings))
        print(listings)

        business_list = BusinessList()
        for listing in listings[:5]:
            listing.click()
            page.wait_for_timeout(3000)

            # name_xpath = '//h1[contains(@class, "fontHeadlineLarge")]/span[2]'
            address_xpath = '//div[@data-attrid="kc:/location/location:address"]'
            # website_xpath = '//a[@data-item-id="authority"]//div[contains(@class, "fontBodyMedium")]'
            # phone_number_xpath = '//button[contains(@data-item-id, "phone:tel:")]//div[contains(@class, "fontBodyMedium")]'

            business = Business()
        
            # # business.name = page.locator(name_xpath).inner_text()
            business.address = page.locator(address_xpath).inner_text()
            print(business.address)
            # # business.website = page.locator(website_xpath).inner_text()
            # # business.phone_number = page.locator(phone_number_xpath).inner_text()

            business_list.business_list.append(business)

        business_list.save_to_excel("google_maps_data")
        business_list.save_to_csv("google_maps_data")


        browser.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--search", type=str)
    parser.add_argument("-l", "--location", type=str) 
    args = parser.parse_args()

    if args.search and args.location:
        search_for = f'{args.search} {args.location}'
    else:
        search_for = 'dentist new york'
    
    main()
