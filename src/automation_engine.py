"""
Automation Engine Module
Handles browser automation and form filling using Selenium.
"""
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

logger = logging.getLogger(__name__)

class AutomationEngine:
    """Handle browser automation and giveaway participation"""
    
    def __init__(self, headless=False):
        """Initialize automation engine
        
        Args:
            headless: Run browser in headless mode
        """
        self.driver = None
        self.headless = headless
        self._init_driver()
        logger.info("Automation Engine initialized")
    
    def _init_driver(self):
        """Initialize Selenium WebDriver"""
        try:
            options = webdriver.ChromeOptions()
            if self.headless:
                options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            self.driver = webdriver.Chrome(options=options)
            logger.info("Chrome WebDriver initialized")
        except Exception as e:
            logger.error(f"Error initializing WebDriver: {e}")
            self.driver = None
    
    def participate_in_giveaway(self, email_data):
        """Participate in giveaway from email
        
        Args:
            email_data: Email dictionary with giveaway information
            
        Returns:
            True if successful, False otherwise
        """
        if not self.driver:
            logger.error("WebDriver not initialized")
            return False
        
        try:
            # Extract giveaway link from email
            giveaway_url = self._extract_link(email_data.get('body', ''))
            if not giveaway_url:
                logger.warning("No giveaway link found")
                return False
            
            logger.info(f"Navigating to giveaway: {giveaway_url}")
            self.driver.get(giveaway_url)
            
            # Wait and fill form
            self._fill_form(email_data)
            
            # Submit form
            self._submit_form()
            logger.info("Successfully participated in giveaway")
            return True
            
        except Exception as e:
            logger.error(f"Error during giveaway participation: {e}")
            return False
    
    def _extract_link(self, text):
        """Extract URL from text
        
        Args:
            text: Text containing URL
            
        Returns:
            URL string or None
        """
        import re
        urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
        return urls[0] if urls else None
    
    def _fill_form(self, email_data):
        """Fill giveaway form
        
        Args:
            email_data: Email data for form filling
        """
        try:
            # Find and fill email field
            email_fields = self.driver.find_elements(By.CSS_SELECTOR, 'input[type="email"]')
            if email_fields:
                email_fields[0].send_keys(email_data.get('from', ''))
                logger.info("Email field filled")
            
            # Find and fill name field
            name_fields = self.driver.find_elements(By.CSS_SELECTOR, 'input[type="text"]')
            if name_fields:
                name_fields[0].send_keys("Participant")
                logger.info("Name field filled")
                
        except Exception as e:
            logger.warning(f"Error filling form: {e}")
    
    def _submit_form(self):
        """Submit the form"""
        try:
            # Look for submit button
            submit_buttons = self.driver.find_elements(By.CSS_SELECTOR, 'button[type="submit"], input[type="submit"]')
            if submit_buttons:
                submit_buttons[0].click()
                logger.info("Form submitted")
        except Exception as e:
            logger.warning(f"Error submitting form: {e}")
    
    def close(self):
        """Close browser"""
        if self.driver:
            self.driver.quit()
            logger.info("Browser closed")
    
    def __del__(self):
        """Destructor"""
        self.close()
