from imports import *
from modules.setup import setup, grant_access
from modules.page import sticky_header
from modules.image_processing import *






def get_generated_image(image, mask, prompt):
    _, img_encoded = cv2.imencode('.png', image)
    img_bytes = io.BytesIO(img_encoded)

    # Convert mask image to bytes without saving to disk
    _, mask_img_encoded = cv2.imencode('.png', mask)

    mask_img_bytes = io.BytesIO(mask_img_encoded)
    response = openai.Image.create_edit(
        image=img_bytes,
        mask=mask_img_bytes,
        prompt=prompt,
        n=1,
        size="256x256"
    )
    image_url = response['data'][0]['url']

    result_image = requests.get(image_url)
    return result_image, image_url


def main():
    image = st.file_uploader("upload the image", type=[".jpg", ".png"])
    if image is not None:

        img = st.session_state.images.get(image.name, False)

        if not img:
            st.write("not in the database")
            file_bytes = np.asarray(bytearray(image.read()), dtype=np.uint8)
            image_decoded = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
            cropped_image = crop_image_to_square(image_decoded)

            resized_image = resize_image(cropped_image)

            grayscale_image = convert_to_grayscale(resized_image)

            optimal_threshold, optimal_mask = get_mask(grayscale_image)

            st.session_state.images[image.name] = {"image_decoded": image_decoded,
                                                   "resized": resized_image,
                                                   "optimal_threshold": optimal_threshold,
                                                   "grayscale_image": grayscale_image,

                                                   }
        else:
            image_decoded = st.session_state.images[image.name]["image_decoded"]
            resized_image = st.session_state.images[image.name]["resized"]
            optimal_threshold = st.session_state.images[image.name]["optimal_threshold"]

            grayscale_image = st.session_state.images[image.name]["grayscale_image"]

        col1, col2, col3, col4 = st.columns(4)











        reset_threshold_button, invert_mask_button = st.columns(2)

        th = st.slider(f"choose the threshold for the mask{st.session_state.threshold_reset_counter}",
                       min_value=0.0,
                       label_visibility="collapsed",
                       max_value=255.0,
                       value=optimal_threshold)

        if reset_threshold_button.button("reset to optimal threshold", disabled=th == optimal_threshold, use_container_width=True):
            st.session_state.threshold_reset_counter += 1
            st.rerun()

        if invert_mask_button.button("invert the mask", use_container_width=True):
            st.session_state.inverted = not st.session_state.inverted



        threshold, mask = get_mask(grayscale_image, threshold=th)

        if st.session_state.inverted:
            mask = invert_bitwise(mask)

        #with col1:
        #    st.write("original")
        #    st.image(image_decoded, channels="BGR", use_column_width=True)

        with col2:
            st.write("resized")
            st.image(resized_image, channels="BGR", use_column_width=True)

        with col3:
            st.write("mask")
            st.image(mask, channels="RGBA", use_column_width=True)

        if prompt := st.chat_input("Give the DALLE prompt"):
            st.session_state.prompt = prompt
            transparent_mask = create_transparent_mask(mask)

            #st.image(transparent_mask, caption='Generated Image',width=300, channels='BGRA')

            with st.spinner("waiting for the image to be generated"):
                st.session_state.generated_image, st.session_state.image_url = get_generated_image(resized_image, transparent_mask, prompt)


    if st.session_state.generated_image:
        st.header(st.session_state.prompt)
        st.image(st.session_state.generated_image.content, caption='Generated Image',width=300, channels='BGR')
        st.write(st.session_state.image_url)












if __name__ == '__main__':
    load_dotenv()
    setup()

    sticky_header()

    # st.write(st.session_state.access_key in allowed_access_keys)
    # st.write("allowed access keys:", allowed_access_keys)
    # st.write("access key:", st.session_state.access_key)

    if grant_access():
        main()