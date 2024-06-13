import os
import cv2
import glob
import numpy as np
import pandas as pd

current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.dirname(os.path.dirname(current_directory))
datasets_directory = os.path.join(parent_directory, 'datasets')

def slow_horizontal_variance(im):
    '''Return average variance of horizontal lines of a grayscale image'''
    height, width = im.shape
    if not width or not height: return 0
    vars = []
    for y in range(height):
        row = im[y, :]
        mean = np.mean(row)
        variance = np.mean((row - mean) ** 2)
        vars.append(variance)
    return np.mean(vars)

def extract_hsv_value(im):
    hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
    mean_hue = np.mean(hsv[:, :, 0])
    mean_sat = np.mean(hsv[:, :, 1])
    mean_val = np.mean(hsv[:, :, 2])

    mean_hue = round(mean_hue, 4)
    mean_sat = round(mean_sat, 4)
    mean_val = round(mean_val, 4)

    return mean_hue, mean_sat, mean_val

def create_data_frame(variance, hue, sat, val, classif):
    # Check if CSV file exists
    if os.path.exists('mean_rgb_values.csv'):
        # Load existing DataFrame
        df = pd.read_csv('mean_rgb_values.csv')
    else:
        # Create new DataFrame if CSV file doesn't exist
        df = pd.DataFrame(columns=['Hue', 'Sat', 'Val', 'Variance', 'Class'])
        df = df.astype({'Hue': float, 'Sat': float, 'Val': float, 'Variance': int, 'Class': int})

    # Create DataFrame for the new row
    new_row_df = pd.DataFrame({'Hue': [hue], 'Sat': [sat], 'Val': [val], 'Variance': [variance], 'Class': [classif]})

    # Concatenate the new row DataFrame with the existing DataFrame
    df = pd.concat([df, new_row_df], ignore_index=True)

    # Save to CSV
    df.to_csv('mean_rgb_values.csv', index=False)

# Patterns for the image files
patterns = ['*.png', '*.jpeg', '*.jpg']

# Retrieve all files matching the patterns
files = []
for pattern in patterns:
    files_found = glob.glob(os.path.join(datasets_directory, pattern))
    files.extend(files_found)

for fn in files:
    # Read image in grayscale for variance calculation
    im_gray = cv2.imread(fn, cv2.IMREAD_GRAYSCALE)
    if im_gray is None:
        print(f"Failed to load image {fn}")
        continue

    var = slow_horizontal_variance(im_gray)
    var = round(var, 0)
    fog_status = 1 if var < 200 else 0

    # Read image in color for HSV extraction
    im_color = cv2.imread(fn)
    if im_color is None:
        print(f"Failed to load image {fn}")
        continue

    mean_hue, mean_sat, mean_val = extract_hsv_value(im_color)

    # Print the required details alongside the image name
    # create_data_frame(var, mean_hue, mean_sat, mean_val, fog_status)
    print(f"{os.path.basename(fn)} - Variance: {var:.0f}, Fog: {fog_status}, H={mean_hue}, S={mean_sat}, V={mean_val}")
