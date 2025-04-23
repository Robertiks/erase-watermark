#!/usr/bin/env python3

from dewatermark import DeWatermark
import os

def main():
    # Create an instance of DeWatermark
    dewatermark = DeWatermark()
    
    # Read the image file
    with open("./shutterstock_image.jpg", "rb") as f:
        image_bytes = f.read()
    
    # Process the image to remove watermark
    try:
        result_bytes = dewatermark.erase_watermark(image_bytes)
        
        # Save the result
        with open("./result.jpg", "wb") as f:
            f.write(result_bytes)
            
        print("Watermark removed successfully! Result saved as 'result.jpg'")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()