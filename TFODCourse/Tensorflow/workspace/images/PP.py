import os
import glob
import xml.etree.ElementTree as ET

# Set the path to the folder containing the images and XML files
folder_path = "C:\\Users\\User\\Desktop\\local\\TFODCourse\\Tensorflow\\workspace\\images\\train"

# Loop through all the JPG files in the folder
for jpg_file in glob.glob(os.path.join(folder_path, "*.png")):
    
    # Get the name of the file (without extension)
    file_name = os.path.splitext(os.path.basename(jpg_file))[0]
    
    # Rename the JPG file to PNG
    os.rename(jpg_file, os.path.join(folder_path, file_name + ".jpeg"))
    
    # Update the XML file with the new file name
    xml_file = os.path.join(folder_path, file_name + ".xml")
    tree = ET.parse(xml_file)
    root = tree.getroot()
    root.find("filename").text = file_name + ".jpeg"
    tree.write(xml_file)