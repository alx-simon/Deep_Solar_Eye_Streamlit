import streamlit as st
import requests
from io import BytesIO
from PIL import Image
import numpy as np
import base64
import ipdb

#App title/ description
st.header(':mostly_sunny: Solar Panel Power Loss Estimator :mostly_sunny:')


st.markdown('####')

uploaded_file = st.file_uploader("Select you solar panel image to be analyzed...	:frame_with_picture:", type=["jpg"])


if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)

    # Convert image to byte stream
    byte_arr = BytesIO()
    image.save(byte_arr, format='JPEG')
    byte_arr = byte_arr.getvalue()

    # Prepare data to send to FastAPI endpoint
    file = {"file": (uploaded_file.name, byte_arr, "image/jpeg")}

    response = requests.post("https://mask-image-linux-xzsdeienxq-ew.a.run.app/predict", files=file)

    if response.status_code == 200:
        #ipdb.set_trace()
        if response.json()['inferred_img']:
            # get response and convert from base64 to byte stream
            image_base64 = response.json()['inferred_img']
            # Decode the base64 byte stream
            image_bytes = base64.b64decode(image_base64)
            inferred_img = Image.open(BytesIO(image_bytes))
            # Display the image on Streamlit
            st.image(inferred_img, output_format='jpeg', caption='Analysed Image', use_column_width=True)

        response_regression = requests.post("https://deep-solar-eye-linux-xzsdeienxq-ew.a.run.app/predict", files=file)
        if response_regression.status_code == 200:
            st.write("	:crystal_ball:")
            prediction_result = response_regression.json()
            percent_loss = round(float(prediction_result['power_loss']) * 100, 2)
            if percent_loss < 0:
                percent_loss = 0
            st.write("Power Loss Prediction:")
            st.write(f"Power Loss: {percent_loss}%")

        else:
            st.write("No solar panel detected. Consider changing the angle or lighting.")

    else:
        st.write("  :construction:")
        st.write("Failed to get prediction result")
