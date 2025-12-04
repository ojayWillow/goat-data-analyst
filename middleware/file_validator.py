import os
import re
import logging
import hashlib
import requests
from typing import Tuple, Optional
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class FileValidator:
    MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
    ALLOWED_EXTENSIONS = {'.csv'}
    
    def __init__(self):
        self.upload_log = []
        self.vt_api_key = os.getenv('VIRUSTOTAL_API_KEY')
        if not self.vt_api_key:
            logger.warning('VirusTotal API key not found. Malware scanning disabled.')
    
    def validate_file(self, file, filename: str, user_id: Optional[str] = None) -> Tuple[bool, str]:
        """Validate uploaded file. Returns (is_valid, error_message)"""
        
        if not filename:
            return False, 'No filename provided'
        
        ext = os.path.splitext(filename.lower())[1]
        if ext not in self.ALLOWED_EXTENSIONS:
            logger.warning(f'Invalid file type attempted: {ext} by user {user_id}')
            return False, f'Only CSV files allowed. Got: {ext}'
        
        safe_filename = self.sanitize_filename(filename)
        if safe_filename != filename:
            logger.info(f'Filename sanitized: {filename} -> {safe_filename}')
        
        try:
            file.seek(0, 2)
            size = file.tell()
            file.seek(0)
            
            if size > self.MAX_FILE_SIZE:
                logger.warning(f'File too large: {size} bytes by user {user_id}')
                return False, f'File too large. Max size: 100MB. Your file: {size / 1024 / 1024:.1f}MB'
            
            if size == 0:
                return False, 'File is empty'
        except Exception as e:
            logger.error(f'Error checking file size: {e}')
            return False, 'Error checking file size'
        
        if self.vt_api_key:
            is_safe, scan_msg = self.scan_file_virustotal(file)
            if not is_safe:
                logger.warning(f'Malware detected by user {user_id}: {scan_msg}')
                return False, f'Security alert: {scan_msg}'
            logger.info(f'VirusTotal scan: {scan_msg}')
        
        self.log_upload(user_id, safe_filename, size)
        return True, ''
    
    def sanitize_filename(self, filename: str) -> str:
        name, ext = os.path.splitext(filename)
        name = re.sub(r'[^a-zA-Z0-9_-]', '_', name)
        return f'{name}{ext}'
    
    def scan_file_virustotal(self, file) -> Tuple[bool, str]:
        """Scan file with VirusTotal using REST API. Returns (is_safe, message)"""
        try:
            file.seek(0)
            file_content = file.read()
            file.seek(0)
            
            file_hash = hashlib.sha256(file_content).hexdigest()
            
            headers = {'x-apikey': self.vt_api_key}
            url = f'https://www.virustotal.com/api/v3/files/{file_hash}'
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 404:
                logger.info(f'File hash {file_hash[:8]} not in VT database (likely safe)')
                return True, 'Not in database (likely safe)'
            
            if response.status_code == 200:
                data = response.json()
                stats = data.get('data', {}).get('attributes', {}).get('last_analysis_stats', {})
                malicious = stats.get('malicious', 0)
                suspicious = stats.get('suspicious', 0)
                
                if malicious > 0:
                    return False, f'File flagged by {malicious} security vendors'
                
                if suspicious > 2:
                    return False, f'File flagged as suspicious by {suspicious} vendors'
                
                logger.info(f'File hash {file_hash[:8]} clean (malicious: {malicious}, suspicious: {suspicious})')
                return True, f'Clean (checked by VT)'
            
            logger.warning(f'VT API returned {response.status_code}')
            return True, 'Scan unavailable'
        
        except requests.Timeout:
            logger.error('VirusTotal scan timeout')
            return True, 'Scan timeout'
        except Exception as e:
            logger.error(f'VirusTotal scan error: {e}')
            return True, 'Scan unavailable'
    
    def validate_csv_structure(self, df) -> Tuple[bool, str]:
        if df is None:
            return False, 'Failed to read CSV'
        if df.empty:
            return False, 'CSV file is empty'
        if len(df.columns) == 0:
            return False, 'CSV has no columns'
        if len(df) < 2:
            return False, 'CSV must have at least 2 rows'
        return True, ''
    
    def log_upload(self, user_id: Optional[str], filename: str, size: int):
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'user_id': user_id or 'anonymous',
            'filename': filename,
            'size_bytes': size
        }
        self.upload_log.append(log_entry)
        logger.info(f'File upload: {log_entry}')

file_validator = FileValidator()
