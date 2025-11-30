"""
Comprehensive testing script for GOAT Data Analyst
Tests both FastAPI (main.py) and Streamlit integration (app.py)
UPDATED: Prioritizes 1M row test file
"""
import os
import sys
import time
import requests
import pandas as pd
from datetime import datetime
from pathlib import Path

# Color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_header(text):
    print(f"\n{BLUE}{'='*60}")
    print(f"{text}")
    print(f"{'='*60}{RESET}\n")

def print_success(text):
    print(f"{GREEN}✅ {text}{RESET}")

def print_error(text):
    print(f"{RED}❌ {text}{RESET}")

def print_warning(text):
    print(f"{YELLOW}⚠️  {text}{RESET}")

def print_info(text):
    print(f"{BLUE}ℹ️  {text}{RESET}")

class APITester:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.test_results = {
            "passed": 0,
            "failed": 0,
            "warnings": 0
        }
    
    def test_health(self):
        """Test health endpoint"""
        print_header("TEST 1: Health Check")
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print_success(f"Health endpoint responded: {response.status_code}")
                print_info(f"Status: {data.get('status')}")
                print_info(f"Version: {data.get('version')}")
                print_info(f"Timestamp: {data.get('timestamp')}")
                self.test_results["passed"] += 1
                return True
            else:
                print_error(f"Health check failed: {response.status_code}")
                self.test_results["failed"] += 1
                return False
        except Exception as e:
            print_error(f"Health check failed: {str(e)}")
            self.test_results["failed"] += 1
            return False
    
    def test_root(self):
        """Test root endpoint"""
        print_header("TEST 2: Root Endpoint")
        try:
            response = requests.get(f"{self.base_url}/", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print_success(f"Root endpoint responded: {response.status_code}")
                print_info(f"API Name: {data.get('name')}")
                print_info(f"Available endpoints: {', '.join(data.get('endpoints', {}).keys())}")
                self.test_results["passed"] += 1
                return True
            else:
                print_error(f"Root endpoint failed: {response.status_code}")
                self.test_results["failed"] += 1
                return False
        except Exception as e:
            print_error(f"Root endpoint failed: {str(e)}")
            self.test_results["failed"] += 1
            return False
    
    def test_analyze_json(self, csv_path):
        """Test /analyze endpoint (JSON response)"""
        print_header("TEST 3: /analyze Endpoint (Quick Mode)")
        try:
            if not os.path.exists(csv_path):
                print_error(f"Test CSV not found: {csv_path}")
                self.test_results["failed"] += 1
                return False
            
            # Get file size
            file_size_mb = os.path.getsize(csv_path) / (1024 * 1024)
            print_info(f"Testing with: {csv_path}")
            print_info(f"File size: {file_size_mb:.2f} MB")
            
            # Load CSV to get expected stats
            print_info("Loading CSV to validate...")
            df = pd.read_csv(csv_path)
            expected_rows = len(df)
            expected_cols = len(df.columns)
            print_info(f"Expected: {expected_rows:,} rows, {expected_cols} columns")
            
            with open(csv_path, 'rb') as f:
                start_time = time.time()
                response = requests.post(
                    f"{self.base_url}/analyze",
                    files={"file": (os.path.basename(csv_path), f, "text/csv")},
                    timeout=120
                )
                elapsed = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                
                # Validate response structure
                assert data.get("success") == True, "Success flag not True"
                assert data.get("row_count") == expected_rows, f"Row count mismatch: {data.get('row_count')} vs {expected_rows}"
                assert data.get("column_count") == expected_cols, f"Column count mismatch: {data.get('column_count')} vs {expected_cols}"
                assert "profile" in data, "Profile missing from response"
                assert "quality" in data, "Quality missing from response"
                
                print_success(f"Analysis completed in {elapsed:.2f}s")
                print_info(f"Rows: {data.get('row_count'):,}")
                print_info(f"Columns: {data.get('column_count')}")
                print_info(f"Quality Score: {data.get('quality', {}).get('quality_score', 'N/A')}")
                print_info(f"Profiled columns: {len(data.get('profile', {}))}")
                print_info(f"Throughput: {expected_rows/elapsed:,.0f} rows/second")
                
                self.test_results["passed"] += 1
                return True
            else:
                print_error(f"Analysis failed: {response.status_code}")
                print_error(f"Response: {response.text[:200]}")
                self.test_results["failed"] += 1
                return False
                
        except Exception as e:
            print_error(f"Analysis test failed: {str(e)}")
            self.test_results["failed"] += 1
            return False
    
    def test_analyze_html(self, csv_path):
        """Test /analyze/html endpoint (Full AI mode)"""
        print_header("TEST 4: /analyze/html Endpoint (Full AI Mode)")
        try:
            if not os.path.exists(csv_path):
                print_error(f"Test CSV not found: {csv_path}")
                self.test_results["failed"] += 1
                return False
            
            file_size_mb = os.path.getsize(csv_path) / (1024 * 1024)
            print_info(f"Testing with: {csv_path}")
            print_info(f"File size: {file_size_mb:.2f} MB")
            print_warning("This may take 30-90 seconds (AI insights + charts)...")
            
            with open(csv_path, 'rb') as f:
                start_time = time.time()
                response = requests.post(
                    f"{self.base_url}/analyze/html",
                    files={"file": (os.path.basename(csv_path), f, "text/csv")},
                    timeout=180
                )
                elapsed = time.time() - start_time
            
            if response.status_code == 200:
                html_content = response.text
                
                # Validate HTML structure
                assert "<html" in html_content.lower(), "Invalid HTML response"
                assert len(html_content) > 1000, "HTML too short"
                
                # Check for key sections
                checks = {
                    "Data Quality": "data quality" in html_content.lower(),
                    "Domain Detection": "domain" in html_content.lower(),
                    "AI Insights": "insight" in html_content.lower(),
                    "Charts": "plotly" in html_content.lower() or "chart" in html_content.lower()
                }
                
                print_success(f"HTML report generated in {elapsed:.2f}s")
                print_info(f"HTML size: {len(html_content):,} bytes")
                
                for check_name, passed in checks.items():
                    if passed:
                        print_success(f"Contains: {check_name}")
                    else:
                        print_warning(f"Missing: {check_name}")
                
                # Save HTML for manual inspection
                output_path = f"test_output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                print_info(f"Saved report to: {output_path}")
                
                self.test_results["passed"] += 1
                return True
            else:
                print_error(f"HTML generation failed: {response.status_code}")
                print_error(f"Response: {response.text[:200]}")
                self.test_results["failed"] += 1
                return False
                
        except Exception as e:
            print_error(f"HTML test failed: {str(e)}")
            self.test_results["failed"] += 1
            return False
    
    def test_performance(self, csv_path):
        """Test performance with multiple runs"""
        print_header("TEST 5: Performance Benchmark (3 runs)")
        try:
            if not os.path.exists(csv_path):
                print_error(f"Test CSV not found: {csv_path}")
                self.test_results["failed"] += 1
                return False
            
            runs = 3
            times = []
            
            print_info(f"Running {runs} iterations...")
            
            for i in range(runs):
                with open(csv_path, 'rb') as f:
                    start_time = time.time()
                    response = requests.post(
                        f"{self.base_url}/analyze",
                        files={"file": (os.path.basename(csv_path), f, "text/csv")},
                        timeout=120
                    )
                    elapsed = time.time() - start_time
                
                if response.status_code == 200:
                    times.append(elapsed)
                    print_info(f"Run {i+1}: {elapsed:.2f}s")
                else:
                    print_error(f"Run {i+1} failed")
            
            if times:
                avg_time = sum(times) / len(times)
                min_time = min(times)
                max_time = max(times)
                
                print_success(f"Performance Results:")
                print_info(f"Average: {avg_time:.2f}s")
                print_info(f"Min: {min_time:.2f}s")
                print_info(f"Max: {max_time:.2f}s")
                
                # Get dataset size
                df = pd.read_csv(csv_path)
                rows = len(df)
                print_info(f"Dataset: {rows:,} rows")
                print_info(f"Throughput: {rows/avg_time:,.0f} rows/second")
                
                # Performance check
                if rows >= 1000000:
                    target = 30.0
                    if avg_time < target:
                        print_success(f"✨ EXCELLENT: {avg_time:.2f}s < {target}s target for 1M rows!")
                    else:
                        print_warning(f"Performance: {avg_time:.2f}s (target: <{target}s for 1M rows)")
                
                self.test_results["passed"] += 1
                return True
            else:
                print_error("All performance runs failed")
                self.test_results["failed"] += 1
                return False
                
        except Exception as e:
            print_error(f"Performance test failed: {str(e)}")
            self.test_results["failed"] += 1
            return False
    
    def test_error_handling(self):
        """Test error handling with invalid inputs"""
        print_header("TEST 6: Error Handling")
        tests_passed = 0
        
        # Test 1: Non-CSV file
        try:
            response = requests.post(
                f"{self.base_url}/analyze",
                files={"file": ("test.txt", b"not a csv", "text/plain")},
                timeout=10
            )
            if response.status_code == 400:
                print_success("Rejected non-CSV file correctly")
                tests_passed += 1
            else:
                print_warning(f"Non-CSV rejection unclear: {response.status_code}")
        except Exception as e:
            print_error(f"Non-CSV test failed: {str(e)}")
        
        # Test 2: Empty file
        try:
            response = requests.post(
                f"{self.base_url}/analyze",
                files={"file": ("empty.csv", b"", "text/csv")},
                timeout=10
            )
            if response.status_code == 400:
                print_success("Rejected empty file correctly")
                tests_passed += 1
            else:
                print_warning(f"Empty file rejection unclear: {response.status_code}")
        except Exception as e:
            print_error(f"Empty file test failed: {str(e)}")
        
        # Test 3: Invalid CSV
        try:
            response = requests.post(
                f"{self.base_url}/analyze",
                files={"file": ("invalid.csv", b"not,valid\ncsv", "text/csv")},
                timeout=10
            )
            # Should either succeed (if parseable) or fail gracefully
            if response.status_code in [200, 400]:
                print_success("Handled invalid CSV gracefully")
                tests_passed += 1
            else:
                print_warning(f"Invalid CSV handling unclear: {response.status_code}")
        except Exception as e:
            print_error(f"Invalid CSV test failed: {str(e)}")
        
        if tests_passed >= 2:
            self.test_results["passed"] += 1
            return True
        else:
            self.test_results["failed"] += 1
            return False
    
    def print_summary(self):
        """Print test summary"""
        print_header("TEST SUMMARY")
        total = self.test_results["passed"] + self.test_results["failed"]
        print(f"{GREEN}Passed: {self.test_results['passed']}/{total}{RESET}")
        print(f"{RED}Failed: {self.test_results['failed']}/{total}{RESET}")
        if self.test_results["warnings"] > 0:
            print(f"{YELLOW}Warnings: {self.test_results['warnings']}{RESET}")
        
        if self.test_results["failed"] == 0:
            print_success("\n🎉 ALL TESTS PASSED!")
            return True
        else:
            print_error(f"\n❌ {self.test_results['failed']} TEST(S) FAILED")
            return False


def main():
    print_header("🐐 GOAT Data Analyst - Comprehensive Test Suite")
    
    # Check if API is running
    print_info("Checking if API is running on localhost:8000...")
    try:
        response = requests.get("http://localhost:8000/health", timeout=3)
        print_success("API is running!")
    except:
        print_error("API is NOT running on localhost:8000")
        print_info("\nTo start the API:")
        print_info("1. Open PowerShell in project root")
        print_info("2. Activate venv: venv\\Scripts\\Activate.ps1")
        print_info("3. Run: python main.py")
        print_info("\nThen run this test script again.")
        sys.exit(1)
    
    # Find test CSV - prioritize 1M row file
    test_files = [
        "sample_data/test/test.csv",           # 1M rows (if exists)
        "sample_data/test/*.csv",              # Any CSV in test folder
        "sample_data/sample_ecommerce.csv",    # 100K rows fallback
        "sample_data/20251127_084222_customers_50k.csv",  # 50K rows
    ]
    
    test_csv = None
    
    # Check for files in order of priority
    for pattern in test_files:
        if "*" in pattern:
            import glob
            matches = glob.glob(pattern)
            if matches:
                test_csv = matches[0]
                break
        elif os.path.exists(pattern):
            test_csv = pattern
            break
    
    if not test_csv:
        print_error("No test CSV files found!")
        print_info("Expected locations (in priority order):")
        for path in test_files:
            print_info(f"  - {path}")
        print_info("\nPlease ensure you have a CSV file in one of these locations.")
        sys.exit(1)
    
    # Show file info
    file_size_mb = os.path.getsize(test_csv) / (1024 * 1024)
    print_success(f"Using test file: {test_csv}")
    print_info(f"File size: {file_size_mb:.2f} MB")
    
    # Quick check of row count
    try:
        df_check = pd.read_csv(test_csv, nrows=1)
        df_full = pd.read_csv(test_csv)
        row_count = len(df_full)
        print_info(f"Dataset: {row_count:,} rows, {len(df_full.columns)} columns")
        
        if row_count >= 1000000:
            print_success("✨ Testing with 1M+ row dataset!")
    except Exception as e:
        print_warning(f"Could not preview dataset: {str(e)}")
    
    # Run tests
    tester = APITester()
    
    tester.test_health()
    tester.test_root()
    tester.test_analyze_json(test_csv)
    tester.test_analyze_html(test_csv)
    tester.test_performance(test_csv)
    tester.test_error_handling()
    
    # Summary
    success = tester.print_summary()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
