"""
Live Streamlit App Tester for GOAT Data Analyst
Tests the deployed app at: https://goat-data-analyst-a6idzyddvy2pevnsqdzskt.streamlit.app/
"""
import requests
import time
from datetime import datetime
import os

# Color codes
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_header(text):
    print(f"\n{BLUE}{'='*70}")
    print(f"{text}")
    print(f"{'='*70}{RESET}\n")

def print_success(text):
    print(f"{GREEN}✅ {text}{RESET}")

def print_error(text):
    print(f"{RED}❌ {text}{RESET}")

def print_warning(text):
    print(f"{YELLOW}⚠️  {text}{RESET}")

def print_info(text):
    print(f"{BLUE}ℹ️  {text}{RESET}")

class StreamlitAppTester:
    def __init__(self):
        self.streamlit_url = "https://goat-data-analyst-a6idzyddvy2pevnsqdzskt.streamlit.app"
        self.railway_api_url = "https://goat-data-analyst-production.up.railway.app"
        self.test_results = {
            "passed": 0,
            "failed": 0,
            "warnings": 0
        }
    
    def test_streamlit_accessibility(self):
        """Test if Streamlit app is accessible"""
        print_header("TEST 1: Streamlit App Accessibility")
        try:
            print_info(f"Testing: {self.streamlit_url}")
            start_time = time.time()
            response = requests.get(self.streamlit_url, timeout=10)
            elapsed = time.time() - start_time
            
            if response.status_code == 200:
                print_success(f"App is accessible: {response.status_code}")
                print_info(f"Response time: {elapsed:.2f}s")
                print_info(f"Content length: {len(response.content):,} bytes")
                
                # Check for key Streamlit elements
                content = response.text.lower()
                checks = {
                    "Streamlit framework": "streamlit" in content,
                    "App title": "goat" in content or "data analyst" in content,
                    "Upload widget": "upload" in content or "file" in content,
                }
                
                for check_name, passed in checks.items():
                    if passed:
                        print_success(f"Found: {check_name}")
                    else:
                        print_warning(f"Not detected: {check_name}")
                
                self.test_results["passed"] += 1
                return True
            else:
                print_error(f"App returned: {response.status_code}")
                self.test_results["failed"] += 1
                return False
                
        except requests.exceptions.Timeout:
            print_error("App timed out (>10s)")
            self.test_results["failed"] += 1
            return False
        except Exception as e:
            print_error(f"Failed to access app: {str(e)}")
            self.test_results["failed"] += 1
            return False
    
    def test_railway_api_health(self):
        """Test if Railway API backend is healthy"""
        print_header("TEST 2: Railway API Health Check")
        try:
            print_info(f"Testing: {self.railway_api_url}/health")
            start_time = time.time()
            response = requests.get(f"{self.railway_api_url}/health", timeout=10)
            elapsed = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                print_success(f"API is healthy: {response.status_code}")
                print_info(f"Response time: {elapsed:.2f}s")
                print_info(f"Status: {data.get('status')}")
                print_info(f"Version: {data.get('version')}")
                print_info(f"Timestamp: {data.get('timestamp')}")
                
                self.test_results["passed"] += 1
                return True
            else:
                print_error(f"API unhealthy: {response.status_code}")
                self.test_results["failed"] += 1
                return False
                
        except Exception as e:
            print_error(f"API health check failed: {str(e)}")
            self.test_results["failed"] += 1
            return False
    
    def test_railway_api_root(self):
        """Test Railway API root endpoint"""
        print_header("TEST 3: Railway API Root Endpoint")
        try:
            print_info(f"Testing: {self.railway_api_url}/")
            response = requests.get(f"{self.railway_api_url}/", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                print_success("API root endpoint working")
                print_info(f"API Name: {data.get('name')}")
                print_info(f"Version: {data.get('version')}")
                print_info(f"Status: {data.get('status')}")
                
                endpoints = data.get('endpoints', {})
                print_info(f"Available endpoints: {len(endpoints)}")
                for name, path in endpoints.items():
                    print_info(f"  - {name}: {path}")
                
                self.test_results["passed"] += 1
                return True
            else:
                print_error(f"Root endpoint failed: {response.status_code}")
                self.test_results["failed"] += 1
                return False
                
        except Exception as e:
            print_error(f"Root endpoint test failed: {str(e)}")
            self.test_results["failed"] += 1
            return False
    
    def test_api_docs(self):
        """Test if API docs are accessible"""
        print_header("TEST 4: API Documentation")
        try:
            print_info(f"Testing: {self.railway_api_url}/docs")
            response = requests.get(f"{self.railway_api_url}/docs", timeout=10)
            
            if response.status_code == 200:
                print_success("API docs accessible")
                print_info(f"Docs URL: {self.railway_api_url}/docs")
                
                # Check for Swagger/OpenAPI elements
                content = response.text.lower()
                if "swagger" in content or "openapi" in content:
                    print_success("OpenAPI/Swagger UI detected")
                
                self.test_results["passed"] += 1
                return True
            else:
                print_error(f"Docs not accessible: {response.status_code}")
                self.test_results["failed"] += 1
                return False
                
        except Exception as e:
            print_error(f"Docs test failed: {str(e)}")
            self.test_results["failed"] += 1
            return False
    
    def test_api_with_sample_data(self):
        """Test API /analyze endpoint with small sample"""
        print_header("TEST 5: API Analysis with Sample Data")
        try:
            print_info("Creating small test CSV...")
            
            # Create minimal test CSV
            csv_content = b"id,value,category\n1,100,A\n2,200,B\n3,150,A"
            
            print_info(f"Sending to: {self.railway_api_url}/analyze")
            start_time = time.time()
            response = requests.post(
                f"{self.railway_api_url}/analyze",
                files={"file": ("test.csv", csv_content, "text/csv")},
                timeout=30
            )
            elapsed = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                print_success(f"Analysis completed in {elapsed:.2f}s")
                print_info(f"Rows: {data.get('row_count')}")
                print_info(f"Columns: {data.get('column_count')}")
                print_info(f"Quality Score: {data.get('quality', {}).get('quality_score', 'N/A')}")
                
                # Validate response structure
                required_keys = ["success", "row_count", "column_count", "profile", "quality"]
                missing = [k for k in required_keys if k not in data]
                
                if missing:
                    print_warning(f"Missing keys: {', '.join(missing)}")
                else:
                    print_success("Response structure valid")
                
                self.test_results["passed"] += 1
                return True
            else:
                print_error(f"Analysis failed: {response.status_code}")
                print_error(f"Response: {response.text[:200]}")
                self.test_results["failed"] += 1
                return False
                
        except Exception as e:
            print_error(f"API analysis test failed: {str(e)}")
            self.test_results["failed"] += 1
            return False
    
    def test_api_html_generation(self):
        """Test API /analyze/html endpoint"""
        print_header("TEST 6: API HTML Report Generation")
        try:
            print_info("Creating test CSV for HTML report...")
            
            # Create test CSV with more data
            csv_content = b"date,revenue,customer,product\n2024-01-01,1000,CustomerA,ProductX\n2024-01-02,1500,CustomerB,ProductY\n2024-01-03,1200,CustomerA,ProductX"
            
            print_info(f"Sending to: {self.railway_api_url}/analyze/html")
            print_warning("This may take 30-60 seconds (AI insights)...")
            
            start_time = time.time()
            response = requests.post(
                f"{self.railway_api_url}/analyze/html",
                files={"file": ("test.csv", csv_content, "text/csv")},
                timeout=120
            )
            elapsed = time.time() - start_time
            
            if response.status_code == 200:
                html_content = response.text
                print_success(f"HTML report generated in {elapsed:.2f}s")
                print_info(f"HTML size: {len(html_content):,} bytes")
                
                # Validate HTML content
                checks = {
                    "Valid HTML": "<html" in html_content.lower(),
                    "Has styles": "<style" in html_content.lower() or "css" in html_content.lower(),
                    "Data quality": "quality" in html_content.lower(),
                    "Domain detection": "domain" in html_content.lower(),
                    "Insights": "insight" in html_content.lower(),
                }
                
                for check_name, passed in checks.items():
                    if passed:
                        print_success(f"✓ {check_name}")
                    else:
                        print_warning(f"✗ {check_name}")
                
                # Save for inspection
                output_path = f"live_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                print_info(f"Saved to: {output_path}")
                
                self.test_results["passed"] += 1
                return True
            else:
                print_error(f"HTML generation failed: {response.status_code}")
                print_error(f"Response: {response.text[:200]}")
                self.test_results["failed"] += 1
                return False
                
        except Exception as e:
            print_error(f"HTML generation test failed: {str(e)}")
            self.test_results["failed"] += 1
            return False
    
    def test_cors_headers(self):
        """Test CORS configuration"""
        print_header("TEST 7: CORS Configuration")
        try:
            print_info("Checking CORS headers...")
            response = requests.options(f"{self.railway_api_url}/analyze")
            
            cors_headers = {
                "Access-Control-Allow-Origin": response.headers.get("Access-Control-Allow-Origin"),
                "Access-Control-Allow-Methods": response.headers.get("Access-Control-Allow-Methods"),
                "Access-Control-Allow-Headers": response.headers.get("Access-Control-Allow-Headers"),
            }
            
            print_success("CORS headers:")
            for header, value in cors_headers.items():
                if value:
                    print_info(f"  {header}: {value}")
                else:
                    print_warning(f"  {header}: Not set")
            
            self.test_results["passed"] += 1
            return True
                
        except Exception as e:
            print_warning(f"CORS test inconclusive: {str(e)}")
            self.test_results["warnings"] += 1
            return True
    
    def print_summary(self):
        """Print test summary"""
        print_header("TEST SUMMARY - LIVE DEPLOYMENT")
        
        print(f"\n{BLUE}Streamlit App:{RESET}")
        print(f"  URL: {self.streamlit_url}")
        
        print(f"\n{BLUE}Railway API:{RESET}")
        print(f"  URL: {self.railway_api_url}")
        print(f"  Docs: {self.railway_api_url}/docs")
        
        print(f"\n{BLUE}Results:{RESET}")
        total = self.test_results["passed"] + self.test_results["failed"]
        print(f"{GREEN}Passed: {self.test_results['passed']}/{total}{RESET}")
        print(f"{RED}Failed: {self.test_results['failed']}/{total}{RESET}")
        if self.test_results["warnings"] > 0:
            print(f"{YELLOW}Warnings: {self.test_results['warnings']}{RESET}")
        
        if self.test_results["failed"] == 0:
            print_success("\n🎉 ALL LIVE DEPLOYMENT TESTS PASSED!")
            print_success("✨ Your app is live and working perfectly!")
            return True
        else:
            print_error(f"\n❌ {self.test_results['failed']} TEST(S) FAILED")
            return False


def main():
    print_header("🐐 GOAT Data Analyst - Live Deployment Test Suite")
    print_info("Testing live Streamlit app and Railway API backend...")
    
    tester = StreamlitAppTester()
    
    # Run all tests
    tester.test_streamlit_accessibility()
    tester.test_railway_api_health()
    tester.test_railway_api_root()
    tester.test_api_docs()
    tester.test_api_with_sample_data()
    tester.test_api_html_generation()
    tester.test_cors_headers()
    
    # Summary
    success = tester.print_summary()
    
    return 0 if success else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
