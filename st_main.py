import os

import matplotlib.image as mpimg
import pywt
import streamlit as st
from PIL import Image
import numpy as np
from color import enhance_image

import metrics

PATH_TO_TEST_IMAGES = "./images"
NO_CHOICE = "---"

st.sidebar.title("Contrast Enhancement")


def fix_channels(array):
    return array[:, :, :3]


def get_opened_image(image_file):
    if isinstance(image_file, str):
        image_path = os.path.join(PATH_TO_TEST_IMAGES, image_file)
        return fix_channels(np.array(Image.open(image_path)))
    return fix_channels(np.array(Image.open(image_file)))


def get_list_of_images():
    file_list = os.listdir(PATH_TO_TEST_IMAGES)
    return [NO_CHOICE] + [
        str(filename) for filename in file_list if str(filename).endswith(".png")
    ]


def get_processed_image(raw_image):
    original = get_opened_image(raw_image)
    # Put enhancement method here
    return enhance_image(original)


def main():
    st.sidebar.subheader("Load Image")
    image_file_uploaded = st.sidebar.file_uploader(
        "Upload an image", type="png")
    st.sidebar.text("OR")
    image_file_chosen = st.sidebar.selectbox(
        "Select an existing image", get_list_of_images()
    )
    button = st.sidebar.button("Load")

    st.sidebar.subheader("Parameter Tunning")
    alpha = st.sidebar.slider("alpha", min_value=0.0, max_value=1.0, step=0.01)
    wj = st.sidebar.slider("wj", min_value=0, max_value=8)
    K = st.sidebar.slider("K", min_value=0, max_value=80)
    wavl = st.sidebar.selectbox('Select a wavelet', pywt.wavelist())

    image_file = None
    if image_file_uploaded:
        image_file = image_file_uploaded
    elif image_file_uploaded and image_file_chosen != NO_CHOICE:
        image_file = image_file_uploaded
    else:
        image_file = image_file_chosen

    if image_file_uploaded and image_file and button:
        image = get_opened_image(image_file)
        print("uploaded", type(image))
        with st.beta_expander("Selected Image", expanded=True):
            st.image(image, use_column_width=True)
    elif image_file_chosen != NO_CHOICE and image_file and button:
        image = get_opened_image(image_file)
        print("chosen", type(image))
        with st.beta_expander("Selected Image", expanded=True):
            st.image(image, use_column_width=True)

    if image_file and button:
        st.markdown(f"Processed image")
        original_image = get_opened_image(image_file)
        processed_image = get_processed_image(image_file)
        st.image(processed_image)
        st.markdown(f"## Metrics results:")
        st.markdown(
            f"### PSNR: **{metrics.calculate_psnr(original_image, processed_image)}**"
        )
        st.markdown(
            f"### SSIM: **{metrics.calculate_ssim(original_image, processed_image)}**"
        )
    else:
        st.markdown(f"# First load an image")


if __name__ == "__main__":
    main()
