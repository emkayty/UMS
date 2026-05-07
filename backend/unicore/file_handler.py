"""
File Handling for UMS

Provides secure file upload, download, and management
for documents, images, and other files.
"""
import os
import uuid
import hashlib
from typing import Optional, Tuple
from datetime import datetime
from django.conf import settings
from django.core.files.storage import default_storage
import logging

logger = logging.getLogger(__name__)


# Allowed file extensions by category
ALLOWED_EXTENSIONS = {
    'image': ['jpg', 'jpeg', 'png', 'gif', 'webp'],
    'document': ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'txt'],
    'archive': ['zip', 'tar', 'gz', 'rar'],
    'video': ['mp4', 'webm', 'avi'],
    'audio': ['mp3', 'wav', 'ogg'],
}

# Maximum file size (50MB)
MAX_FILE_SIZE = 50 * 1024 * 1024


class FileHandler:
    """Handle file operations"""
    
    def __init__(self, upload_dir: str = 'uploads'):
        self.upload_dir = upload_dir
        self.max_file_size = MAX_FILE_SIZE
    
    def get_file_extension(self, filename: str) -> str:
        """Get file extension"""
        return filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
    
    def validate_file(self, filename: str, file_size: int) -> Tuple[bool, str]:
        """
        Validate file
        
        Args:
            filename: Name of the file
            file_size: Size of the file in bytes
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        ext = self.get_file_extension(filename)
        
        # Check file size
        if file_size > self.max_file_size:
            return False, f"File size exceeds {self.max_file_size} bytes"
        
        # Check extension
        allowed = sum(ALLOWED_EXTENSIONS.values(), [])
        if ext not in allowed:
            return False, f"File extension .{ext} not allowed"
        
        return True, ""
    
    def generate_filename(self, original_filename: str) -> str:
        """Generate unique filename"""
        ext = self.get_file_extension(original_filename)
        unique_id = uuid.uuid4().hex[:12]
        timestamp = datetime.now().strftime('%Y%m%d')
        return f"{timestamp}_{unique_id}.{ext}"
    
    def calculate_checksum(self, file_path: str) -> str:
        """Calculate file checksum (MD5)"""
        hash_md5 = hashlib.md5()
        with default_storage.open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    def save_file(self, uploaded_file, subdir: str = '') -> Tuple[Optional[str], str]:
        """
        Save uploaded file
        
        Args:
            uploaded_file: UploadedFile from request.FILES
            subdir: Subdirectory for the file
            
        Returns:
            Tuple of (file_path, error_message)
        """
        # Validate
        is_valid, error = self.validate_file(
            uploaded_file.name,
            uploaded_file.size
        )
        if not is_valid:
            return None, error
        
        # Generate unique filename
        filename = self.generate_filename(uploaded_file.name)
        
        # Build path
        if subdir:
            file_path = os.path.join(self.upload_dir, subdir, filename)
        else:
            file_path = os.path.join(self.upload_dir, filename)
        
        # Save
        try:
            saved_path = default_storage.save(file_path, uploaded_file)
            logger.info(f"File saved: {saved_path}")
            return saved_path, ""
        except Exception as e:
            logger.error(f"File save error: {e}")
            return None, str(e)
    
    def delete_file(self, file_path: str) -> Tuple[bool, str]:
        """
        Delete file
        
        Args:
            file_path: Path to the file
            
        Returns:
            Tuple of (success, error_message)
        """
        try:
            if default_storage.exists(file_path):
                default_storage.delete(file_path)
                logger.info(f"File deleted: {file_path}")
                return True, ""
            return False, "File not found"
        except Exception as e:
            logger.error(f"File delete error: {e}")
            return False, str(e)
    
    def get_file_url(self, file_path: str) -> str:
        """Get public URL for file"""
        return default_storage.url(file_path)


def handle_upload(uploaded_file, subdir: str = '') -> Tuple[Optional[str], str]:
    """Convenience function for file upload"""
    handler = FileHandler()
    return handler.save_file(uploaded_file, subdir)


def handle_delete(file_path: str) -> Tuple[bool, str]:
    """Convenience function for file deletion"""
    handler = FileHandler()
    return handler.delete_file(file_path)