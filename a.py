import os

import matplotlib.image as mpimg
import streamlit as st

PATH_TO_TEST_IMAGES = './images'
NO_CHOICE = '---'

st.sidebar.title('Contrast Enhancement')


def get_opened_image(image_file):
    if isinstance(image_file, str):
        image_path = os.path.join(PATH_TO_TEST_IMAGES, image_file)
        return mpimg.imread(image_path)
    return image_file


def get_list_of_images():
    file_list = os.listdir(PATH_TO_TEST_IMAGES)
    return [NO_CHOICE]+[str(filename) for filename in file_list if str(filename).endswith('.png')]


def get_processed_image(raw_image):
    return get_opened_image(raw_image)


def main():
    st.sidebar.subheader('Load Image')
    image_file_uploaded = st.sidebar.file_uploader(
        'Upload an image', type='png')
    st.sidebar.text('OR')
    image_file_chosen = st.sidebar.selectbox(
        "Select an existing image", get_list_of_images())
    button = st.sidebar.button('Load')

    st.sidebar.subheader('Parameter Tunning')
    p1 = st.sidebar.slider('p1', min_value=0, max_value=100)
    p2 = st.sidebar.slider('p2', min_value=0, max_value=100)

    image_file = None
    if image_file_uploaded:
        image_file = image_file_uploaded
    elif image_file_uploaded and image_file_chosen != NO_CHOICE:
        image_file = image_file_uploaded
    else:
        image_file = image_file_chosen

    if image_file_uploaded and image_file and button:
        image = get_opened_image(image_file)
        with st.beta_expander('Selected Image', expanded=True):
            st.image(image, use_column_width=True)
    elif image_file_chosen != NO_CHOICE and image_file and button:
        image = get_opened_image(image_file)
        with st.beta_expander('Selected Image', expanded=True):
            st.image(image, use_column_width=True)

    if image_file and button:
        st.markdown(f"Ahora viene la talla")
        st.image(get_processed_image(image_file))
        st.markdown(f"## Metrics results:")
        st.markdown(f"### PSNR: **{12.32}**")
    else:
        st.markdown(f"# First load an image")


main()
