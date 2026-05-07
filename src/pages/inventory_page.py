from selenium.webdriver.common.by import By

from src.pages.base_page import BasePage


class InventoryPage(BasePage):
    TITLE = (By.CSS_SELECTOR, ".title")

    def get_title(self) -> str:
        return self.get_text(self.TITLE)
