#!/usr/bin/env python3
import os
import sys
import time
from pathlib import Path
import concurrent.futures
import argparse
from typing import List, Tuple, Optional

from dewatermark import DeWatermark


def process_image(input_path: str, output_path: str, dewatermark_instance: DeWatermark, using_api: bool = True) -> Tuple[str, bool, Optional[str]]:
    """Process a single image to remove watermark.
    
    Args:
        input_path: Path to the input image
        output_path: Path where the processed image will be saved
        dewatermark_instance: Instance of DeWatermark class
        using_api: Whether this image is being processed with API
        
    Returns:
        Tuple containing: filename, success status, and error message if any
    """
    try:
        # Read the image file
        with open(input_path, 'rb') as f:
            image_bytes = f.read()
        
        # Process the image
        if using_api:
            print(f"Processing {os.path.basename(input_path)} with API...")
        else:
            print(f"Processing {os.path.basename(input_path)} without API (original will be returned)...")
            
        # Set API usage flag on the dewatermark instance
        dewatermark_instance.use_api = using_api
        
        result_bytes = dewatermark_instance.erase_watermark(image_bytes)
        
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Save the resulting image
        with open(output_path, 'wb') as f:
            f.write(result_bytes)
            
        return os.path.basename(input_path), True, None
    except Exception as e:
        return os.path.basename(input_path), False, str(e)


def main():
    """Main function to process a batch of images."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Remove watermarks from a batch of images')
    parser.add_argument('-i', '--input', default='wfoto', help='Input directory containing images with watermarks')
    parser.add_argument('-o', '--output', default='processed', help='Output directory for processed images')
    parser.add_argument('-w', '--workers', type=int, default=3, help='Number of worker threads')
    parser.add_argument('-a', '--api-key', default='0f0a0891de8fa067b0a3903f1640736a77b389f795a85761f8b773416b3b8c43', help='API key for dewatermark.ai service')
    parser.add_argument('-l', '--limit', type=int, default=210, help='Maximum number of images to process using API (default: 210)')
    
    args = parser.parse_args()
    
    # Get absolute paths
    script_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    input_dir = script_dir / args.input
    output_dir = script_dir / args.output
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Get list of image files
    image_extensions = ('.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG')
    image_files = [f for f in os.listdir(input_dir) 
                 if os.path.isfile(os.path.join(input_dir, f)) and 
                 f.lower().endswith(image_extensions)]
    
    if not image_files:
        print(f"No image files found in {input_dir}")
        return
    
    # Create an instance of DeWatermark with API key
    api_key = args.api_key
    api_limit = args.limit
    dewatermark_instance = DeWatermark(api_key=api_key)
    
    # Process images with a progress counter
    total_images = len(image_files)
    print(f"Found {total_images} images to process")
    print(f"Using API key: {api_key}")
    print(f"API usage limit: {api_limit} images")
    
    successful = 0
    failed = 0
    api_used = 0  # Counter for API usage
    start_time = time.time()
    
    # Process images using thread pool
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = []
        
        for img_file in image_files:
            input_path = os.path.join(input_dir, img_file)
            output_path = os.path.join(output_dir, img_file)
            
            # Determine if this image should use API based on our limit
            use_api = api_used < api_limit
            
            # If this is the first image beyond the limit, notify user
            if not use_api and api_used == api_limit:
                print(f"\nAPI limit of {api_limit} images reached. Processing remaining images without API.")
            
            future = executor.submit(
                process_image, 
                input_path, 
                output_path, 
                dewatermark_instance,
                use_api  # Pass the API usage flag
            )
            futures.append(future)
            
            # Count this toward API usage if we're using API
            if use_api:
                api_used += 1
        
        # Process results as they complete
        for i, future in enumerate(concurrent.futures.as_completed(futures), 1):
            filename, success, error_msg = future.result()
            
            if success:
                successful += 1
                print(f"[{i}/{total_images}] ✓ {filename}")
            else:
                failed += 1
                print(f"[{i}/{total_images}] ✗ {filename} - Error: {error_msg}")
    
    # Print summary
    elapsed_time = time.time() - start_time
    print(f"\nProcessing complete!")
    print(f"Time taken: {elapsed_time:.2f} seconds")
    print(f"Images processed: {successful} successful, {failed} failed")
    print(f"API usage: {min(api_used, api_limit)}/{api_limit} images processed with API")
    print(f"Processed images saved to: {output_dir}")


if __name__ == "__main__":
    main()