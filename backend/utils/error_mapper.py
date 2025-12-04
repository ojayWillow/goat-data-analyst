"""
Error message mapper: Converts technical errors to user-friendly messages
"""

ERROR_MESSAGES = {
    # File errors
    'KeyError': 'Missing required column: {key}',
    'FileNotFoundError': 'File not found. Please check the file path.',
    'PermissionError': 'Permission denied. Cannot access the file.',
    'IsADirectoryError': 'Expected a file, but got a directory.',
    
    # CSV parsing errors
    'EmptyDataError': 'CSV file is empty or has no data.',
    'ParserError': 'CSV parsing error. Please check file format.',
    'UnicodeDecodeError': 'File encoding issue. Please save as UTF-8 CSV.',
    
    # Data errors
    'ValueError': 'Invalid data format: {details}',
    'TypeError': 'Data type mismatch: {details}',
    'IndexError': 'Data index out of range.',
    
    # Memory errors
    'MemoryError': 'File too large to process. Try a smaller file.',
    
    # Timeout
    'TimeoutError': 'Analysis took too long. Try a smaller file or simpler data.',
    
    # Default
    'default': 'An unexpected error occurred. Please try again.'
}

def get_user_friendly_error(exception: Exception) -> str:
    """
    Convert technical exception to user-friendly message
    
    Args:
        exception: The caught exception
        
    Returns:
        User-friendly error message
    """
    error_type = type(exception).__name__
    error_msg = str(exception)
    
    # Get template
    template = ERROR_MESSAGES.get(error_type, ERROR_MESSAGES['default'])
    
    # Fill in details
    if '{key}' in template and error_type == 'KeyError':
        key = error_msg.strip("'").strip('"')
        return template.format(key=key)
    elif '{details}' in template:
        return template.format(details=error_msg[:100])
    
    return template
