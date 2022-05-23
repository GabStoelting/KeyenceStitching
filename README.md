# KeyenceStitching
 Comfortable wrapper for the Fiji/ImageJ stitching routines

## Getting Started

This script has only been tested with Fiji (https://fiji.sc) on Windows and MacOS. 

### Dependencies

* Requires Fiji (which comes with the rolling ball background subtraction and Collection stitching plugins)
* It may run on baseline ImageJ if you install the plugins manually
 
### Installing

* Download the Keyence_stitching_automator.ijm.py script to a directory of your choice

### Preparing raw microscopy files
* My suggestion is to create a base folder that will contain the images from all samples (e.g. "Keyence Images")
* Within this folder, create a sub-folder for each sample (e.g. "Mouse 1234 Heart", "Mouse 1234 Adrenal"...)
* Put the microscopy images in that folder

### Executing program

* Run Fiji
* Open the script manager (File > New > Script) 
* Within the script manager, open the script file (File > Open)
* Press Ctrl+R or the "run" button
* In the popup window, select the folder which contains the files (e.g. "Keyence Images" in the example above).
* Stitching will take a while and at various times, images will be automatically opened and closed. Wait until the "Automated stitching is done." message appears in the "Log" screen. Please do not use your computer during stitching!

### Result
* You will end up with a "raw" and a "bkg_subtracted" folder in each of your sample directories. The raw files are just the originals, the files in the "bkg_subtracted" folder are background subtracted using the rolling ball algorithm (radius=50). The base directory should contain a "stitched.tif" with the resulting output.
