#!/usr/bin/env python3

import argparse
import os
from pathlib import Path
from dewatermark import DeWatermark

def main():
    parser = argparse.ArgumentParser(description='Remove watermarks from images using dewatermark.ai')
    parser.add_argument('input', help='Input image file path')
    parser.add_argument('-o', '--output', help='Output image file path (default: input filename with _dewatermarked suffix)')
    parser.add_argument('-a', '--api-key', help='API key for dewatermark.ai service')
    
    args = parser.parse_args()
    
    # Prepare input/output paths
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file '{input_path}' does not exist.")
        return 1
    
    # If output path not provided, create one based on input filename
    if not args.output:
        output_path = input_path.with_stem(f"{input_path.stem}_dewatermarked")
    else:
        output_path = Path(args.output)
    
    # Create output directory if it doesn't exist
    output_dir = output_path.parent
    if not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)
    
    # Initialize DeWatermark with API key if provided
    dewatermark = DeWatermark(api_key=args.api_key)
    
    # Read the image file
    with open(input_path, 'rb') as f:
        image_bytes = f.read()
    
    print(f"Processing {input_path}...")
    
    try:
        # Process the image
        result_bytes = dewatermark.erase_watermark(image_bytes)
        
        # Save the result
        with open(output_path, 'wb') as f:
            f.write(result_bytes)
        
        print(f"Watermark removed successfully! Result saved as '{output_path}'")
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

if __name__ == "__main__":
    exit(main())