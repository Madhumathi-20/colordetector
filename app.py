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
uploaded_file = st.file_uploader("📁 Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.write("🖱️ Click on the image below to detect a color:")
    coords = streamlit_image_coordinates(image, key="click_image")

    if coords:
        x, y = int(coords["x"]), int(coords["y"])
        st.write(f"📍 Clicked Coordinates: ({x}, {y})")

        image_np = np.array(image)
        if y < image_np.shape[0] and x < image_np.shape[1]:  # ensure within bounds
            r, g, b = image_np[y, x]
            st.write(f"🎨 RGB: ({r}, {g}, {b})")

            color_info = get_color_name(r, g, b, color_data)

            if color_info is not None:
                hex_color = color_info['hex']
                name = color_info['color_name']

                st.markdown(f"""
                ### 🎯 Detected Color: {name}
                - RGB: ({r}, {g}, {b})
                - HEX: `{hex_color}`
                """)
                st.markdown(f"""
                <div style="width:100px; height:50px; background-color:{hex_color}; border:1px solid #000;"></div>
                """, unsafe_allow_html=True)
            else:
                st.error("❌ No closest color found.")
        else:
            st.warning("⚠️ Clicked outside the image bounds.")
