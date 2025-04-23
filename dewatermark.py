import requests
import base64
from io import BytesIO
from PIL import Image
import json
from typing import Optional, Dict, Any, Union

class DeWatermark:
    def __init__(self, proxy: Optional[Dict[str, Any]] = None, api_key: Optional[str] = None, use_api: bool = True):
        """Initialize DeWatermark with optional proxy settings and API key.
        
        Args:
            proxy: Optional proxy settings
            api_key: API key for authentication
            use_api: Whether to use the API for watermark removal
        """
        self.proxy = proxy
        self.api_key = api_key
        self.use_api = use_api
    
    def erase_watermark(self, image_bytes: bytes) -> bytes:
        """Remove watermark from an image.
        
        Args:
            image_bytes: Binary image data
            
        Returns:
            Processed image without watermark as bytes
        """
        # If API usage is disabled, return original image
        if not self.use_api or not self.api_key:
            return image_bytes
        
        # Resize image if needed (max dimension 1408px as per API docs)
        resized_image = self.resize_image(image_bytes, 1408)
        
        # Prepare form data for API request
        files = {
            'original_preview_image': ('image.jpg', resized_image, 'image/jpeg'),
            'remove_text': (None, 'true', 'text/plain')
        }
        
        # Set headers for API request with X-API-KEY authentication
        headers = {
            "X-API-KEY": self.api_key,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        }
        
        # Make API request to remove watermark
        response = requests.post(
            "https://platform.dewatermark.ai/api/object_removal/v1/erase_watermark",
            files=files,
            headers=headers,
            proxies=self.proxy
        )
        
        # Check if the request was successful
        if response.status_code != 200:
            raise Exception(f"API Error: {response.text}")
        
        # Parse response
        try:
            result = response.json()
            
            if not result.get('edited_image') or not result['edited_image'].get('image'):
                raise Exception(f"API Error: {json.dumps(result)}")
            
            # Return processed image
            return base64.b64decode(result['edited_image']['image'])
            
        except json.JSONDecodeError:
            raise Exception(f"Invalid JSON response from API: {response.text}")
    
    # Note: Previous JWT authentication methods have been removed as they are no longer needed
    # with the X-API-KEY header authentication approach
    
    def resize_image(self, image_bytes: bytes, target_width: int) -> bytes:
        """Resize image to target width while maintaining aspect ratio."""
        # Open image from bytes
        img = Image.open(BytesIO(image_bytes))
        width, height = img.size
        
        # Return original if already smaller than target
        if width <= target_width:
            return image_bytes
        
        # Calculate new height maintaining aspect ratio
        target_height = int((target_width / width) * height)
        
        # Resize image
        resized_img = img.resize((target_width, target_height), Image.LANCZOS)
        
        # Convert back to bytes
        buffer = BytesIO()
        resized_img.save(buffer, format=img.format or "PNG")
        
        return buffer.getvalue()