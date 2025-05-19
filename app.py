import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
from streamlit_image_coordinates import streamlit_image_coordinates

# Load color dataset
@st.cache_data
def load_colors():
    return pd.read_csv("colors.csv")

color_data = load_colors()
st.title("🎨 Color Detection from Image (No OpenCV)")
st.markdown("Upload an image and click on it to detect the nearest color name.")

# Display dataset sample
with st.expander("🔍 View Sample Color Dataset"):
    st.dataframe(color_data.head())

# Find closest color name using Euclidean distance
def get_color_name(R, G, B, color_data):
    min_dist = float('inf')
    closest_color = None
    for _, row in color_data.iterrows():
        try:
            d = ((R - int(row['R'])) ** 2 +
                 (G - int(row['G'])) ** 2 +
                 (B - int(row['B'])) ** 2) ** 0.5
            if d < min_dist:
                min_dist = d
                closest_color = row
        except Exception as e:
            st.write(f"Error processing row: {e}")
    return closest_color

# Upload image
uploaded_file = st.file_uploader("C:\Users\user\Pictures\beautiful_yellow_roses_flowers_green_leaves_blur_background_hd_yellow-HD.jpg", type=["jpg"])

