#!/usr/bin/env python3

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dewatermark import DeWatermark
from PIL import Image
from io import BytesIO

def main():
    # Initialize DeWatermark
    dewatermark = DeWatermark()
    
    # Path to input and output images
    input_path = "input_image.jpg"
    output_path = "output_image.jpg"
    
    print(f"Processing {input_path}...")
    
    # Read the image file
    with open(input_path, "rb") as f:
        image_bytes = f.read()
    
    # Process the image to remove watermark
    try:
        print("Removing watermark...")
        result_bytes = dewatermark.erase_watermark(image_bytes)
        
        # Save the result
        with open(output_path, "wb") as f:
            f.write(result_bytes)
            
        print(f"Watermark removed successfully! Result saved as '{output_path}'")
        
        # Display before/after (if in interactive environment)
        try:
            print("Displaying before/after images...")
            before_img = Image.open(BytesIO(image_bytes))
            after_img = Image.open(BytesIO(result_bytes))
            
            # Show images side by side if using in a notebook or GUI environment
            # In console, this will just open two image windows
            before_img.show(title="Before")
            after_img.show(title="After")
        except Exception as e:
            print(f"Could not display images: {e}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()