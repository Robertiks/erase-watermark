# DeWatermark
USING API IS OPTIONAL. Script bypass dewatermark and can be used without API key. 
I have made API implemention only for future buletproofing because i have no plans to update this tool.
Originally it was TS script which bypassed API and it worked fine.
But i decided to make it in Python because i wanted to use it in my own projects.
I have made it in Python because i wanted to use it in my own projects.
This is a powerful tool to remove watermarks from images using the dewatermark.ai API. Available in both Python and TypeScript implementations.


## Features
- Can be used without an API key
- Supports both Python and TypeScript implementations
- Easy-to-use API for removing watermarks from images
- Batch processing of multiple images
- Supports JWT authentication (TypeScript version only)
- Removes watermarks from images using advanced AI technology
- Preserves image quality and details
- Available in both Python and TypeScript
- Simple and easy-to-use API
- Supports batch processing of multiple images

## Requirements
- Python 3.6+ or Node.js 12+
- OPTIONAL: API key from [dewatermark.ai] an API key
- Supports both Python and TypeScript implementations
- Easy-to-use API for removing watermarks from images
- Batch processing of multiple images
- Supports JWT authentication (TypeScript version only)
## Installation

### Python

```bash
# Clone the repository
git clone https://github.com/yourusername/erase-watermark.git
cd erase-watermark

# Install dependencies
pip install -r requirements.txt
```

### TypeScript

```bash
# Clone the repository
git clone https://github.com/yourusername/erase-watermark.git
cd erase-watermark

# Install dependencies using npm
npm install
# OR using Bun
bun install
```

## API Key

To use the dewatermark.ai service, you need an API key. You can either:

1. Get an API key from [dewatermark.ai](https://dewatermark.ai/)
2. Use the library's built-in JWT authentication (TypeScript version only)

## Usage
python batch_process.py --input wfoto --output proc 

OR

python batch_process.py --input wfoto --output proc -- workers 5

## Example
Here's a simple example of how to use the library to remove watermarks from an image using the dewatermark.ai API:
```bash
python batch_process.py --input wfoto --output proc --workers 5
```

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Disclaimer

This tool is meant for legitimate use cases where you have the right to remove watermarks. Please respect copyright and intellectual property laws.

---

*Note: This library is not affiliated with dewatermark.ai.*
