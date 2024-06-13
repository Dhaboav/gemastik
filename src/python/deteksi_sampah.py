import cv2
import numpy as np
import pandas as pd


img = cv2.imread('test.jpg')
tester = cv2.resize(img, (640,480))
cv2.rectangle(tester, (180,170), (370, 190), (0,255,0), 1)
roi = tester[170:190, 180:370]

# Calculate mean RGB values
mean_blue = np.mean(roi[:,:,0])
mean_green = np.mean(roi[:,:,1])
mean_red = np.mean(roi[:,:,2])

mean_blue = round(mean_blue, 4)
mean_green = round(mean_green, 4)
mean_red = round(mean_red, 4)

# Create a DataFrame
df = pd.DataFrame({'Mean_RGB': ['Blue', 'Green', 'Red'],
                   'Value': [mean_blue, mean_green, mean_red]})

# Transpose the DataFrame
df_transposed = df.set_index('Mean_RGB').T

# Save to CSV
df_transposed.to_csv('mean_rgb_values.csv', index=False)

print("Mean RGB values saved to 'mean_rgb_values.csv'")
