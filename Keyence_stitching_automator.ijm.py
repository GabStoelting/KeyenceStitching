from ij import IJ, WindowManager

import os
import shutil
import re

def create_filelist(files):
	"""
	Extracts a list of TIF files from a given list.
	
	
	Parameters
	----------
	files : list
	    List of files as given by os.walk()
	
	Returns
	-------
	list
	    The list of TIF files
	
	"""

	filelist = []
	
	for file in files:
		# Only add TIF files to the list of files
		if file.endswith(".tif") or file.endswith(".tiff") or file.endswith(".TIF"):
			filelist.append(file) # append to filelist	
            
	return filelist

def move_files_to_raw(subdir, filelist):
    """
    Creates "raw" and "bkg_subtracted" subfolders and moves TIF files from
    the main to the "raw" subdirectory.


    Parameters
    ----------
    subdir: string
        This is the base directory that contains the TIF files and subdirectories
    filelist: list
    	This contains a list of the TIF files in the base directory

    Returns
    -------
    nothing
    """

    if(len(filelist)>1):
    	# if the files are not in a "raw" subdirectory, create "raw"
    	# and "bkg_subtracted" folders and move files there
	
		os.mkdir(subdir+os.sep+"raw")
		os.mkdir(subdir+os.sep+"bkg_subtracted")
		for file in filelist:
			IJ.log("Moving "+subdir+os.sep+file+" to raw folder")
			shutil.move(subdir+os.sep+file, subdir+os.sep+"raw"+os.sep+file)    	

def background_subtraction(subdir, filelist):
	"""
	This is a wrapper for the rolling ball background subtraction routine
	in Fiji/ImageJ.
	
	
	Parameters
	----------
	subdir: string
	    This is the directory that contains the raw TIF files (and subdirectories).
	filelist: list
		This contains a list of the TIF files in the raw directory.
	
	Returns
	-------
	nothing
	"""	
	IJ.log("Subtracting background in "+subdir+" and moving to bkg_subtracted")
	print("bkg", subdir, filelist)
	for file in filelist:
		img = IJ.openImage(subdir+os.sep+file) # Open individual image
		IJ.run(img, "Subtract Background...", "rolling=50 light") # Subtract background
		# Save individual image
		IJ.saveAs(img, file, subdir+os.sep+".."+os.sep+"bkg_subtracted"+os.sep+file)
			
def stitch_images(subdir, filelist):
	"""
	This is a wrapper for the rolling ball background subtraction routine
	in Fiji/ImageJ.
	
	The function first extracts the x- and y-coordinates of individual images from
	their filenames. Afterwards, the maximum x- and y-coordinates are determined and
	forwarded to the "Collection stitching" plugin of Fiji/ImageJ
	
	
	Parameters
	----------
	subdir: string
	    This is the directory that contains the raw TIF files (and subdirectories).
	filelist: list
		This contains a list of the TIF files in the raw directory.
	
	Returns
	-------
	nothing
	"""
	# Stitch images
	x_list = []
	y_list = []
	# Extract the x and y coordinates from each file name
	for file in filelist:			
		coordinate_num = re.findall(r'\d+', file)
		x_list.append(int(coordinate_num[1]))
		y_list.append(int(coordinate_num[0]))
		IJ.log("Stitching "+file)
		
	# Get the maximum coordinates in x- and y-direction
	coordinate_num = [max(y_list), max(x_list)]

	# Start stitching via the Collection stitiching plugin
	IJ.run("Grid/Collection stitching", 
	"type=[Filename defined position] order=[Defined by filename         ] grid_size_x="+
	str(coordinate_num[1]+1)+" grid_size_y="+str(coordinate_num[0]+1)+
	" tile_overlap=20 first_file_index_x=0 first_file_index_y=0 directory=["+subdir+
	"] file_names=Image_R{yy}C{xx}_CH4.tif output_textfile_name=TileConfiguration.txt \
	fusion_method=[Linear Blending] regression_threshold=0.30 max/avg_displacement_threshold=2.50 \
	absolute_displacement_threshold=3.50 compute_overlap computation_parameters=[Save memory (but be slower)] \
	image_output=[Fuse and display]")
	
	img = WindowManager.getCurrentImage()
	IJ.run("RGB Color") # Convert to RGB
	img.close()
	img = WindowManager.getCurrentImage()
	# Save as TIF
	IJ.saveAs(img, "Tiff", subdir+os.sep+".."+os.sep+"stitched.tif")
	img.close()
			

# Ask for directory
directory = IJ.getDirectory("Input_directory")

IJ.log("Scanning directory "+directory+" and subdirectories")

# Iterate over all files and (sub-)directories
for subdir, dirs, files in os.walk(directory):


    filelist = create_filelist(files)      
	
    if(len(filelist)>1):
    	# if the files are not in a "raw" subdirectory, move them there
		if not (subdir.endswith("raw") or subdir.endswith("bkg_subtracted")):
			move_files_to_raw(subdir, filelist) # Move files to raw folder
			# Create a new list of files in the raw subfolder and process
			# with background subtraction and stitching
			for subdir_raw, dirs_raw, files_raw in os.walk(subdir+os.sep+"raw"):
				filelist_raw = create_filelist(files_raw) # Create list of files
				background_subtraction(subdir_raw, filelist_raw) # Subtract background
				stitch_images(subdir+os.sep+"bkg_subtracted", filelist_raw) # Stitch images
	
		# If they are already in a "raw" directory, proceed with background subtraction
		elif subdir.endswith("raw"):
			background_subtraction(subdir, filelist) # Subtract background
			stitch_images(subdir, filelist) # Stitch images
			
		# If they are already in a "raw" directory, proceed with background subtraction	
		elif subdir.endswith("bkg_subtracted"):
			stitch_images(subdir, filelist) # Stitch images
			

			
			
IJ.log("Automated stitching is done.")
