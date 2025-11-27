"""
CSV Handler - Robust CSV file loading with auto-detection
Handles multiple encodings, delimiters, and edge cases
"""

import pandas as pd
import chardet
from pathlib import Path
from typing import Tuple, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CSVHandler:
    """Handles CSV file loading with automatic format detection"""
    
    COMMON_DELIMITERS = [',', ';', '\t', '|']
    COMMON_ENCODINGS = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
    
    def __init__(self):
        self.data = None
        self.metadata = {}
    
    def detect_encoding(self, file_path: str) -> str:
        """Detect file encoding using chardet"""
        try:
            with open(file_path, 'rb') as f:
                raw_data = f.read(10000)  # Read first 10KB
                result = chardet.detect(raw_data)
                encoding = result['encoding']
                confidence = result['confidence']
                
                logger.info(f"Detected encoding: {encoding} (confidence: {confidence:.2%})")
                
                # If confidence is low, try common encodings
                if confidence < 0.7:
                    logger.warning("Low confidence in encoding detection, will try common encodings")
                    return 'utf-8'  # Default fallback
                
                return encoding
        except Exception as e:
            logger.error(f"Error detecting encoding: {e}")
            return 'utf-8'  # Safe fallback
    
    def detect_delimiter(self, file_path: str, encoding: str) -> str:
        """Detect CSV delimiter by testing common ones"""
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                first_lines = [f.readline() for _ in range(5)]
            
            # Count occurrences of each delimiter in first lines
            delimiter_counts = {}
            for delimiter in self.COMMON_DELIMITERS:
                counts = [line.count(delimiter) for line in first_lines if line.strip()]
                if counts and all(c > 0 for c in counts):
                    # Good delimiter has consistent count across lines
                    delimiter_counts[delimiter] = sum(counts) / len(counts)
            
            if delimiter_counts:
                best_delimiter = max(delimiter_counts, key=delimiter_counts.get)
                logger.info(f"Detected delimiter: '{best_delimiter}'")
                return best_delimiter
            
            return ','  # Default fallback
        except Exception as e:
            logger.error(f"Error detecting delimiter: {e}")
            return ','
    
    def load_csv(self, file_path: str, encoding: Optional[str] = None, 
                 delimiter: Optional[str] = None) -> pd.DataFrame:
        """
        Load CSV file with automatic detection of encoding and delimiter
        
        Args:
            file_path: Path to CSV file
            encoding: Optional encoding (auto-detected if not provided)
            delimiter: Optional delimiter (auto-detected if not provided)
        
        Returns:
            pandas DataFrame
        """
        file_path = str(Path(file_path))
        
        # Auto-detect if not provided
        if encoding is None:
            encoding = self.detect_encoding(file_path)
        
        if delimiter is None:
            delimiter = self.detect_delimiter(file_path, encoding)
        
        # Try to load with detected settings
        try:
            df = pd.read_csv(
                file_path,
                encoding=encoding,
                delimiter=delimiter,
                low_memory=False
            )
            
            logger.info(f"✅ Successfully loaded CSV: {df.shape[0]} rows, {df.shape[1]} columns")
            
            # Store metadata
            self.metadata = {
                'file_path': file_path,
                'encoding': encoding,
                'delimiter': delimiter,
                'rows': df.shape[0],
                'columns': df.shape[1],
                'column_names': df.columns.tolist()
            }
            
            self.data = df
            return df
            
        except Exception as e:
            logger.error(f"Failed to load with encoding={encoding}, delimiter={delimiter}: {e}")
            
            # Try fallback: common encoding/delimiter combinations
            for enc in self.COMMON_ENCODINGS:
                for delim in self.COMMON_DELIMITERS:
                    try:
                        df = pd.read_csv(file_path, encoding=enc, delimiter=delim, low_memory=False)
                        logger.info(f"✅ Loaded with fallback: encoding={enc}, delimiter={delim}")
                        
                        self.metadata = {
                            'file_path': file_path,
                            'encoding': enc,
                            'delimiter': delim,
                            'rows': df.shape[0],
                            'columns': df.shape[1],
                            'column_names': df.columns.tolist()
                        }
                        
                        self.data = df
                        return df
                    except:
                        continue
            
            raise ValueError(f"Could not load CSV file: {file_path}")
    
    def get_metadata(self) -> dict:
        """Return metadata about loaded file"""
        return self.metadata


# Convenience function
def load_csv(file_path: str) -> pd.DataFrame:
    """Quick function to load CSV"""
    handler = CSVHandler()
    return handler.load_csv(file_path)
