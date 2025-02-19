import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from PIL import Image

# Load the API key from .env file
load_dotenv()

# Set up the Google Gemini AI with your API key
genai.configure(api_key="AIzaSyCuf5UbF_E22S4PxgXt7WS9sNC1Dj4pRiI")

# Function to prepare the uploaded image for AI processing
def prepare_image(uploaded_file):
    """Convert uploaded image to format required by Google's AI"""
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        return None

# Function to get AI response about the food image
def get_gemini_response(image, prompt):
    """Send image to Google's AI and get calorie information"""
    try:
        model = genai.GenerativeModel('gemini-1.5-pro')
        response = model.generate_content([image[0], prompt])
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# Main web app
def main():
    st.set_page_config(page_title="Calorie Advisor", page_icon="🍽️")
    
    st.title("🍽️ Calorie Advisor")
    st.write("Upload a photo of your food to get calorie information!")

    uploaded_file = st.file_uploader(
        "Upload your food image (jpg, jpeg, or png)",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Your Food Image", use_container_width=True)

        if st.button("Calculate Calories"):
            with st.spinner("Analyzing your food..."):
                prompt = """
                Please analyze this food image and provide:
                1. List each food item and its calories
                2. Total calories
                3. Simple health advice

                Format like this:
                FOOD ITEMS:
                1. [Food Item] - [Calories]
                2. [Food Item] - [Calories]

                TOTAL CALORIES: [Number]

                HEALTH TIPS:
                • [Tip 1]
                • [Tip 2]
                """

                image_data = prepare_image(uploaded_file)
                if image_data is not None:
                    response = get_gemini_response(image_data, prompt)
                    st.success("Analysis Complete!")
                    st.write(response)
                else:
                    st.error("Please upload an image first!")

if __name__ == "__main__":
    main()