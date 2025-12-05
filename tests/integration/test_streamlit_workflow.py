import pytest
import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

@pytest.mark.integration
@pytest.mark.skipif(True, reason="Requires Selenium and Chrome - manual test only")
class TestStreamlitWorkflow:
    """Test Streamlit UI workflow end-to-end"""
    
    @pytest.fixture
    def driver(self):
        """Setup Chrome driver for testing"""
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(options=options)
        yield driver
        driver.quit()
    
    def test_login_and_upload_workflow(self, driver):
        """Test: Login → Upload CSV → View report → Download"""
        # Navigate to Streamlit app
        driver.get("http://localhost:8501")
        
        # Wait for page load
        wait = WebDriverWait(driver, 10)
        
        # Login
        email_input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']"))
        )
        email_input.send_keys("og.vitols@gmail.com")
        
        password_input = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
        password_input.send_keys("Twitter92!")
        
        login_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]")
        login_button.click()
        
        # Wait for redirect to main app
        time.sleep(2)
        
        # Upload CSV
        file_input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
        )
        test_file = Path("tests/fixtures/clean.csv").absolute()
        file_input.send_keys(str(test_file))
        
        # Wait for analysis to complete
        time.sleep(5)
        
        # Check report is displayed
        report = driver.find_element(By.CSS_SELECTOR, ".stMarkdown")
        assert "Data Quality Report" in report.text or "Executive Summary" in report.text
        
        # Check download button exists
        download_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Download')]")
        assert download_btn.is_displayed()

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
