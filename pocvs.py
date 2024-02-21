import streamlit as st
import cv2
import os
import webbrowser

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "poc-vision001-b627d17bdf81.json"


def detect_image(path):
    from google.cloud import vision

    client = vision.ImageAnnotatorClient()

    with open(path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.object_localization(image=image)
    objects = response.localized_object_annotations

    object_descriptions = []
    max_confidence = 0.0
    max_object = None

    for obj in objects:
        if obj.score > max_confidence:
            max_confidence = obj.score
            max_object = obj.name

    if max_object is not None:
        object_descriptions.append(max_object)
    

    response = client.logo_detection(image=image)
    logos = response.logo_annotations

    max_confidence = 0.0
    max_logo = None
    for logo in logos:
        if logo.score > max_confidence:
            max_confidence = logo.score
            max_logo = logo.description

    logo_descriptions = []
    if max_logo is not None:
        logo_descriptions.append(max_logo)


    response = client.label_detection(image=image)
    labels = response.label_annotations

    max_confidence = 0.0
    max_label = None

    for label in labels:
        if label.score > max_confidence:
            max_confidence = label.score
            max_label = label.description

    label_descriptions = []
    if max_label is not None:
        label_descriptions.append(max_label)


    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )
   # additional code to open the browser and search for the detected object
    if max_logo is not None:
        webbrowser.open('https://www.safeway.com/shop/search-results.html?q='+ max_logo)
    elif max_label is not None:
        webbrowser.open('https://www.safeway.com/shop/search-results.html?q='+ max_label)
    elif max_object is not None:
        webbrowser.open('https://www.safeway.com/shop/search-results.html?q='+ max_object)
    # additional code to open the browser and search for the detected object
    return object_descriptions, label_descriptions, logo_descriptions
#

def image_upload():
    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        # Save the uploaded file to a temporary path
        temp_path = "output/" + uploaded_file.name
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getvalue())
            st.image(cv2.imread(temp_path), channels="BGR")
        return temp_path
    else:
        return None


def open_camera():
    import cv2
    import streamlit as st
    import tempfile

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        st.error("Unable to open camera")
        return None

    st.title("Webcam Live Feed")
    run = st.checkbox("Run")
    FRAME_WINDOW = st.image([])

    cap = cv2.VideoCapture(0)
    
    while run:
        _, frame = cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        FRAME_WINDOW.image(frame)
    
    
    if st.button("Capture"):
        ret, frame = cap.read()
        if ret:
            temp_path = "C:/Users/jrazo09/OneDrive - Safeway, Inc/Desktop/Copilot Docs/image search/temp/" + "/camera_image.jpg"
            cv2.imwrite(temp_path, frame)
            st.image(frame, channels="BGR")
            
            return temp_path
        else:
            st.error("Failed to capture image")

    cap.release()
    return None


def main():
    st.title("Visual Search POC")

    #if st.button("Upload Image"):
    file_path = image_upload()
    if file_path is None:
        st.error("Please upload an image")
        
        camera_path = open_camera()
        if camera_path is None:
            st.error("Please capture an image")
            return
        else:
            camImage = detect_image(camera_path)
            for i in range(len(camImage)):
                st.write(camImage[i])
        return
    else:
        image = detect_image(file_path)
        for i in range(len(image)):
            st.write(image[i])

    if st.button("Clear Display"):
        st.empty()
    
        
if __name__ == "__main__":
    main()
