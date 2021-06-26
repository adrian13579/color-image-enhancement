import numpy as np
import pywt
import streamlit as st
from PIL import Image

import metrics
from color import enhance_image

st.sidebar.title("Contrast Enhancement")


def fix_channels(array):
    return array[:, :, :3]


def get_opened_image(image_file):
    return fix_channels(np.array(Image.open(image_file)))


@st.cache(allow_output_mutation=True)
def get_upload_status():
    return {"image": None}


def save_image(image):
    im = Image.fromarray(image)
    im.save(f'./result.jpg')


def upload_image():
    image_dict = get_upload_status()
    st.sidebar.subheader("Load Image")
    image = st.sidebar.file_uploader("Upload an image", type="jpg")
    image_dict.update({"image": image})


def main():
    upload_image()
    image_file = get_upload_status()["image"]

    if image_file is None:
        return

    save_button = st.sidebar.button('Save Result')

    st.sidebar.subheader("Parameter Tunning")

    alpha = st.sidebar.slider(
        "alpha", min_value=0.0, max_value=1.0, step=0.01, value=0.1
    )
    wj = st.sidebar.slider("wj", min_value=0.0, max_value=8.0, value=0.8)
    K = st.sidebar.slider("K", min_value=0, max_value=80, value=10)
    wavl = st.sidebar.selectbox("Select a wavelet", pywt.wavelist())

    image = get_opened_image(image_file)
    with st.beta_expander("Selected Image", expanded=True):
        st.image(image, use_column_width=True)

    st.markdown(f"Processed image")
    processed_image = enhance_image(image, alpha, wj, K, wavl)
    st.image(processed_image)
    st.markdown(f"## Metrics results:")
    st.markdown(
        f"### PSNR: **{metrics.calculate_psnr(image, processed_image)}**")
    st.markdown(
        f"### SSIM: **{metrics.calculate_ssim(image, processed_image)}**")

    if save_button and processed_image is not None:
        save_image(processed_image)


if __name__ == "__main__":
    main()
