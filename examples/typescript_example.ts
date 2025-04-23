/**
 * TypeScript example for DeWatermark
 */

import DeWatermark from "../index";
import fs from "fs/promises";
import path from "path";

async function main() {
    // Initialize DeWatermark
    const dewatermark = new DeWatermark();
    
    // Path to input and output images
    const inputPath = "input_image.jpg";
    const outputPath = "output_image.jpg";
    
    console.log(`Processing ${inputPath}...`);
    
    try {
        // Read the image file
        console.log("Reading image file...");
        const imageBuffer = await fs.readFile(inputPath);
        
        // Process the image to remove watermark
        console.log("Removing watermark...");
        const resultBuffer = await dewatermark.eraseWatermark(imageBuffer);
        
        // Save the result
        console.log(`Saving result to ${outputPath}...`);
        await fs.writeFile(outputPath, resultBuffer);
        
        console.log(`Watermark removed successfully! Result saved as '${outputPath}'`);
    } catch (error) {
        console.error(`Error: ${error.message}`);
    }
}

main();