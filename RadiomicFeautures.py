
!pip install nibabel SimpleITK pyradiomics

import SimpleITK as sitk
import numpy as np
import matplotlib.pyplot as plt
from radiomics import featureextractor
import nibabel as nib
import six

from google.colab import drive
drive.mount('/content/drive')

template = '/content/drive/My Drive/nifti/ProstateX-0000/'
data1 = '/content/drive/My Drive/nifti/ProstateX-0001/'

# Load images for the ProstateX-0001 dataset
T2W_t1 = nib.load(template + 'T2W.nii.gz').get_fdata()
CM_t1 = nib.load(template + 'LS1.nii.gz').get_fdata()
T2W_s1 = nib.load(data1 + 'T2W.nii.gz').get_fdata()
CM_s1 = nib.load(data1 + 'LS1.nii.gz').get_fdata()
ADC_s1 = nib.load(data1 + 'ADC.nii.gz').get_fdata()
ADC_t1 = nib.load(template + 'ADC.nii.gz').get_fdata()

# Standardize T2W_s1 using T2W_t
mean_t2w1 = np.mean(T2W_t1)
std_t2w1 = np.std(T2W_t1) + 1e-8
T2W_s1_standardized = (T2W_s1 - np.mean(T2W_s1)) / np.std(T2W_s1) * std_t2w1 + mean_t2w1

# Standardize ADC_s1 using ADC_t
mean_ADC1 = np.mean(ADC_t1)
std_ADC1 = np.std(ADC_t1) + 1e-8
ADC_s1_standardized = (ADC_s1 - np.mean(ADC_s1)) / np.std(ADC_s1) * std_ADC1 + mean_ADC1

# Get the middle slice index for both volumes
middle_slice_index_T2W = T2W_t1.shape[2] // 2
middle_slice_index_ADC = ADC_t1.shape[2] // 2

# Get the middle slices
T2W_slice_t = T2W_t1[:, :, middle_slice_index_T2W].astype(np.float32)
T2W_slice_s = T2W_s1_standardized[:, :, middle_slice_index_T2W].astype(np.float32)

# Get the middle slices
ADC_slice_t = ADC_t1[:, :, middle_slice_index_ADC].astype(np.float32)
ADC_slice_s = ADC_s1_standardized[:, :, middle_slice_index_ADC].astype(np.float32)

T2W_slice_t_rotated = np.rot90(T2W_slice_t)
T2W_slice_s_rotated = np.rot90(T2W_slice_s)
ADC_slice_t_rotated = np.rot90(ADC_slice_t)
ADC_slice_s_rotated = np.rot90(ADC_slice_s)

# Display the slices with a 2x2 grid
fig, axes = plt.subplots(2, 2, figsize=(20, 20))

# T2W original slice
axes[0, 0].imshow(T2W_slice_t_rotated, cmap='gray', origin='lower')
axes[0, 0].set_title('T2W from ProstateX-0000 (Middle Slice)')
axes[0, 0].axis('off')

# T2W standardized slice
axes[0, 1].imshow(T2W_slice_s_rotated, cmap='gray', origin='lower')
axes[0, 1].set_title('Standardized T2W from ProstateX-0001 (Middle Slice)')
axes[0, 1].axis('off')

# ADC original slice
axes[1, 0].imshow(ADC_slice_t_rotated, cmap='gray', origin='lower')
axes[1, 0].set_title('ADC from ProstateX-0000 (Middle Slice)')
axes[1, 0].axis('off')

# ADC standardized slice
axes[1, 1].imshow(ADC_slice_s_rotated, cmap='gray', origin='lower')
axes[1, 1].set_title('Standardized ADC from ProstateX-0001 (Middle Slice)')
axes[1, 1].axis('off')

plt.tight_layout()
plt.show()

# Convert to SimpleITK images
T2W_s1_sitk = sitk.GetImageFromArray(T2W_s1_standardized)
ADC_s1_sitk = sitk.GetImageFromArray(ADC_s1_standardized)
CM_s1_sitk = sitk.GetImageFromArray(CM_s1)

from google.colab import files

# Upload the params.yaml file
uploaded = files.upload()

# Set up Radiomics extractor with config file
extractor = featureextractor.RadiomicsFeatureExtractor('params.yaml')

# Convert them to numpy arrays for plotting.
T2W_array = sitk.GetArrayFromImage(T2W_s1_sitk)
ADC_array = sitk.GetArrayFromImage(ADC_s1_sitk)
CM_array = sitk.GetArrayFromImage(CM_s1_sitk)

# Display the middle slice of the CM image
slice_index = CM_array.shape[2] // 2  # Choose the middle slice

plt.figure(figsize=(5, 5))  #

# Plot the middle slice of the contrast-enhanced image
plt.imshow(CM_array[:, :, slice_index], cmap='gray')
plt.title('CM')
plt.axis('off')  # Hide the axes
plt.show()

# Extract features using the same extractor
features_P1_T2W = extractor.execute(T2W_s1_sitk, CM_s1_sitk, label=1, voxelBased=True)
features_P1_ADC = extractor.execute(ADC_s1_sitk, CM_s1_sitk, label=1, voxelBased=True)

import pandas as pd

# Convert the features dictionary to a DataFrame
features_df = pd.DataFrame.from_dict(features_P1_T2W, orient='index', columns=['Value'])

# Export the DataFrame to a CSV file
features_df.to_csv('features_P1_T2W.csv', index_label='Feature Name')

print("Features have been exported to features_P1_T2W.csv")
from google.colab import files
files.download("features_P1_T2W.csv")

import pandas as pd

# Convert the features dictionary to a DataFrame
features_df = pd.DataFrame.from_dict(features_P1_ADC, orient='index', columns=['Value'])

# Export the DataFrame to a CSV file
features_df.to_csv('features_P1_ADC.csv', index_label='Feature Name')

print("Features have been exported to features_P1_ADC.csv")
from google.colab import files
files.download("features_P1_ADC.csv")

"""Patient 2

"""

data2 = '/content/drive/My Drive/nifti/ProstateX-0002/'

T2W_t2 = nib.load(template + 'T2W.nii.gz').get_fdata()
CM_t2 = nib.load(template + 'LS1.nii.gz').get_fdata()
T2W_s2 = nib.load(data2 + 'T2W.nii.gz').get_fdata()
CM_s2 = nib.load(data2 + 'LS1.nii.gz').get_fdata()
ADC_s2 = nib.load(data2 + 'ADC.nii.gz').get_fdata()
ADC_t2 = nib.load(template + 'ADC.nii.gz').get_fdata()

mean_t2w2 = np.mean(T2W_t2)
std_t2w2 = np.std(T2W_t2) + 1e-8
T2W_s2_standardized = (T2W_s2 - np.mean(T2W_s2)) / np.std(T2W_s2) * std_t2w2 + mean_t2w2


mean_ADC2 = np.mean(ADC_t2)
std_ADC2 = np.std(ADC_t2) + 1e-8
ADC_s2_standardized = (ADC_s2 - np.mean(ADC_s2)) / np.std(ADC_s2) * std_ADC2 + mean_ADC2

middle_slice_index_T2W_2 = T2W_t2.shape[2] // 2
middle_slice_index_ADC_2 = ADC_t2.shape[2] // 2

# Get the middle slices
T2W_slice_t_2 = T2W_t2[:, :, middle_slice_index_T2W_2].astype(np.float32)
T2W_slice_s_2 = T2W_s2_standardized[:, :, middle_slice_index_T2W_2].astype(np.float32)

# Get the middle slices
ADC_slice2_t = ADC_t2[:, :, middle_slice_index_ADC_2].astype(np.float32)
ADC_slice2_s = ADC_s2_standardized[:, :, middle_slice_index_ADC_2].astype(np.float32)


T2W_slice_t_rotated_2 = np.rot90(T2W_slice_t_2)
T2W_slice_s_rotated_2 = np.rot90(T2W_slice_s_2)
ADC_slice_t_rotated_2 = np.rot90(ADC_slice2_t)
ADC_slice_s_rotated_2 = np.rot90(ADC_slice2_s)

# Display the slices with a 2x2 grid
fig, axes = plt.subplots(2, 2, figsize=(20, 20))

# T2W original slice
axes[0, 0].imshow(T2W_slice_t_rotated_2, cmap='gray', origin='lower')
axes[0, 0].set_title('T2W from ProstateX-0000 (Middle Slice)')
axes[0, 0].axis('off')

# T2W standardized slice
axes[0, 1].imshow(T2W_slice_s_rotated_2, cmap='gray', origin='lower')
axes[0, 1].set_title('Standardized T2W from ProstateX-0002 (Middle Slice)')
axes[0, 1].axis('off')

# ADC original slice
axes[1, 0].imshow(ADC_slice_t_rotated_2, cmap='gray', origin='lower')
axes[1, 0].set_title('ADC from ProstateX-0000 (Middle Slice)')
axes[1, 0].axis('off')

# ADC standardized slice
axes[1, 1].imshow(ADC_slice_s_rotated_2, cmap='gray', origin='lower')
axes[1, 1].set_title('Standardized ADC from ProstateX-0002 (Middle Slice)')
axes[1, 1].axis('off')

plt.tight_layout()
plt.show()

# Convert to SimpleITK images
T2W_s2_sitk = sitk.GetImageFromArray(T2W_s2_standardized)
ADC_s2_sitk = sitk.GetImageFromArray(ADC_s2_standardized)
CM_s1_sitk = sitk.GetImageFromArray(CM_s1)

# Extract features using the same extractor
features_P2_T2W = extractor.execute(T2W_s2_sitk, CM_s1_sitk, label=1, voxelBased=True)
features_P2_ADC = extractor.execute(ADC_s2_sitk, CM_s1_sitk, label=1, voxelBased=True)

import pandas as pd

# Convert the features dictionary to a DataFrame
features_df = pd.DataFrame.from_dict(features_P2_T2W, orient='index', columns=['Value'])

# Export the DataFrame to a CSV file
features_df.to_csv('features_P2_T2W.csv', index_label='Feature Name')

print("Features have been exported to ffeatures_P2_T2W.csv")
from google.colab import files
files.download("features_P2_T2W.csv")

import pandas as pd

# Convert the features dictionary to a DataFrame
features_df = pd.DataFrame.from_dict(features_P2_ADC, orient='index', columns=['Value'])

# Export the DataFrame to a CSV file
features_df.to_csv('features_P2_ADC.csv', index_label='Feature Name')

print("Features have been exported to features_P2_ADC.csv")
from google.colab import files
files.download("features_P2_ADC.csv")

import pandas as pd

# extracting features for different patients and modalities
features_P1_T2W = extractor.execute(T2W_s1_sitk, CM_s1_sitk, label=1, voxelBased=False)
features_P1_ADC = extractor.execute(ADC_s1_sitk, CM_s1_sitk, label=1, voxelBased=False)
features_P2_T2W = extractor.execute(T2W_s2_sitk, CM_s1_sitk, label=1, voxelBased=False)
features_P2_ADC = extractor.execute(ADC_s2_sitk, CM_s1_sitk, label=1, voxelBased=False)

# Assuming the features extracted are dictionaries with feature names as keys and values as the feature values
def organize_data_in_neat_table(ratios_T2W_patient1, ratios_T2W_patient2, ratios_ADC_patient1, ratios_ADC_patient2):
    # Collect all feature names and sort by modality to list T2W features first, then ADC
    T2W_features = list(ratios_T2W_patient1.keys())
    ADC_features = list(ratios_ADC_patient1.keys())

    # Start filtering from the feature 'original_shape_Elongation' onwards
    start_feature = 'original_shape_Elongation'

    # Initialize a dictionary to store data with multi-level columns, organized by modality
    data = {}
    for feature in T2W_features:
        if feature >= start_feature:  # Only include features starting from 'original_shape_Elongation'
            data[(feature, 'T2W')] = [ratios_T2W_patient1.get(feature, None), ratios_T2W_patient2.get(feature, None)]
    for feature in ADC_features:
        if feature >= start_feature:  # Only include features starting from 'original_shape_Elongation'
            data[(feature, 'ADC')] = [ratios_ADC_patient1.get(feature, None), ratios_ADC_patient2.get(feature, None)]

    # Create DataFrame with multi-level column headers and P1/P2 as rows
    df_table = pd.DataFrame(data, index=['P1', 'P2'])
    df_table.columns.names = ['Feature', 'Modality']

    return df_table

ratios_patient1_T2W = features_P1_T2W
ratios_patient2_T2W = features_P2_T2W
ratios_patient1_ADC = features_P1_ADC
ratios_patient2_ADC = features_P2_ADC

# Create the organized table
df_neat_feature_table = organize_data_in_neat_table(ratios_patient1_T2W, ratios_patient2_T2W, ratios_patient1_ADC, ratios_patient2_ADC)

# Display the table
print(df_neat_feature_table)

# Save the DataFrame as an Excel file
df_neat_feature_table.to_excel("feature_ratios_table.xlsx", index=True)

from google.colab import files
files.download("feature_ratios_table.xlsx")
