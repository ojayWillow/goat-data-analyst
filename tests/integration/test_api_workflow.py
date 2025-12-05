import pytest
import requests
import os
from pathlib import Path

# API base URL
API_BASE = os.getenv("API_URL", "http://localhost:8000")

@pytest.mark.integration
class TestAPIWorkflow:
    """Test full API workflow end-to-end"""
    
    def test_health_endpoint(self):
        """Test API health check (no auth required)"""
        response = requests.get(f"{API_BASE}/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
    
    def test_analyze_csv_workflow_no_auth(self):
        """Test: Upload CSV without auth → 401 Unauthorized"""
        test_file = Path("tests/fixtures/clean.csv")
        assert test_file.exists(), "Test fixture missing"
        
        with open(test_file, "rb") as f:
            files = {"file": ("clean.csv", f, "text/csv")}
            response = requests.post(
                f"{API_BASE}/analyze/html",
                files=files,
                timeout=30
            )
        
        # Should require authentication
        assert response.status_code == 401
    
    def test_invalid_file_rejection_no_auth(self):
        """Test: Upload .txt file without auth → 401 (auth checked first)"""
        # Create temp txt file
        temp_file = Path("tests/fixtures/test.txt")
        temp_file.write_text("This is not a CSV")
        
        try:
            with open(temp_file, "rb") as f:
                files = {"file": ("test.txt", f, "text/plain")}
                response = requests.post(
                    f"{API_BASE}/analyze/html",
                    files=files,
                    timeout=10
                )
            
            # Auth is checked before file validation
            assert response.status_code == 401
        finally:
            if temp_file.exists():
                temp_file.unlink()

@pytest.mark.integration
@pytest.mark.skipif(not os.getenv("TEST_AUTH_TOKEN"), reason="No auth token provided")
class TestAPIWorkflowAuthenticated:
    """Test API workflows with authentication"""
    
    @pytest.fixture
    def auth_headers(self):
        """Provide auth headers for authenticated tests"""
        token = os.getenv("TEST_AUTH_TOKEN")
        return {"Authorization": f"Bearer {token}"}
    
    def test_analyze_csv_with_auth(self, auth_headers):
        """Test: Upload CSV with auth → Receive HTML report"""
        test_file = Path("tests/fixtures/clean.csv")
        assert test_file.exists()
        
        with open(test_file, "rb") as f:
            files = {"file": ("clean.csv", f, "text/csv")}
            response = requests.post(
                f"{API_BASE}/analyze/html",
                files=files,
                headers=auth_headers,
                timeout=30
            )
        
        assert response.status_code == 200
        assert "text/html" in response.headers.get("content-type", "")
        assert len(response.content) > 1000
    
    def test_analyze_messy_csv_with_auth(self, auth_headers):
        """Test: Upload messy CSV with auth → Detect issues"""
        test_file = Path("tests/fixtures/messy.csv")
        assert test_file.exists()
        
        with open(test_file, "rb") as f:
            files = {"file": ("messy.csv", f, "text/csv")}
            response = requests.post(
                f"{API_BASE}/analyze/html",
                files=files,
                headers=auth_headers,
                timeout=30
            )
        
        assert response.status_code == 200
    
    def test_large_file_with_auth(self, auth_headers):
        """Test: Upload large CSV with auth → Completes"""
        test_file = Path("tests/fixtures/large_10k.csv")
        assert test_file.exists()
        
        with open(test_file, "rb") as f:
            files = {"file": ("large_10k.csv", f, "text/csv")}
            response = requests.post(
                f"{API_BASE}/analyze/html",
                files=files,
                headers=auth_headers,
                timeout=60
            )
        
        assert response.status_code == 200

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
