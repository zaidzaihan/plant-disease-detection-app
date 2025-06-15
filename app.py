import streamlit as st
from PIL import Image
import numpy as np
import tensorflow as tf
import time
import os

# Page configuration
st.set_page_config(
    page_title="Plant Disease Detection",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Minimal CSS styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        margin-bottom: 2rem;
    }
    .stButton > button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #45a049;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_model():
    """Load the trained model with error handling"""
    try:
        model_path = "best_model.h5"

        if not os.path.exists(model_path):
            import gdown
            file_id = "1VHEHLSQ0d_QKvgeZjlheDixwLRwiBMCw"
            url = f"https://drive.google.com/uc?id={file_id}"
            gdown.download(url, model_path, quiet=False)

        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file {model_path} was not downloaded.")

        return tf.keras.models.load_model(model_path)
    
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        st.stop()


# Disease information database
DISEASE_INFO = {
    "Pepper__bell___Bacterial_spot": {
        "plant": "Bell Pepper",
        "disease": "Bacterial Spot",
        "severity": "Moderate",
        "description": "A bacterial infection causing dark spots on leaves and fruits.",
        "treatment": "Remove affected parts, apply copper-based fungicides, improve air circulation."
    },
    "Pepper__bell___healthy": {
        "plant": "Bell Pepper",
        "disease": "Healthy",
        "severity": "None",
        "description": "Your plant appears healthy with no signs of disease.",
        "treatment": "Continue regular care and monitoring."
    },
    "Potato___Early_blight": {
        "plant": "Potato",
        "disease": "Early Blight",
        "severity": "Moderate",
        "description": "Fungal disease causing brown spots with concentric rings.",
        "treatment": "Apply fungicides, remove infected foliage, ensure proper spacing."
    },
    "Potato___Late_blight": {
        "plant": "Potato",
        "disease": "Late Blight",
        "severity": "Severe",
        "description": "Serious fungal disease that can destroy entire crops quickly.",
        "treatment": "Immediate fungicide application, remove infected plants, improve drainage."
    },
    "Potato___healthy": {
        "plant": "Potato",
        "disease": "Healthy",
        "severity": "None",
        "description": "Your potato plant appears healthy with no signs of disease.",
        "treatment": "Continue regular care and monitoring."
    },
    "Tomato_Bacterial_spot": {
        "plant": "Tomato",
        "disease": "Bacterial Spot",
        "severity": "Moderate",
        "description": "Bacterial infection causing small dark spots on leaves and fruits.",
        "treatment": "Use copper-based sprays, improve air circulation, avoid overhead watering."
    },
    "Tomato_Early_blight": {
        "plant": "Tomato",
        "disease": "Early Blight",
        "severity": "Moderate",
        "description": "Fungal disease causing brown spots with target-like patterns.",
        "treatment": "Apply fungicides preventively, prune lower leaves, mulch around plants."
    },
    "Tomato_Late_blight": {
        "plant": "Tomato",
        "disease": "Late Blight",
        "severity": "Severe",
        "description": "Devastating fungal disease that can kill plants rapidly.",
        "treatment": "Emergency fungicide treatment, remove infected plants immediately."
    },
    "Tomato_Leaf_Mold": {
        "plant": "Tomato",
        "disease": "Leaf Mold",
        "severity": "Moderate",
        "description": "Fungal infection causing yellow patches and fuzzy growth on leaves.",
        "treatment": "Increase ventilation, reduce humidity, apply appropriate fungicides."
    },
    "Tomato_Septoria_leaf_spot": {
        "plant": "Tomato",
        "disease": "Septoria Leaf Spot",
        "severity": "Moderate",
        "description": "Fungal disease causing small circular spots with dark borders.",
        "treatment": "Remove affected leaves, apply fungicides, avoid overhead watering."
    },
    "Tomato_Spider_mites_Two_spotted_spider_mite": {
        "plant": "Tomato",
        "disease": "Spider Mites",
        "severity": "Moderate",
        "description": "Tiny pests causing stippling and webbing on leaves.",
        "treatment": "Increase humidity, use insecticidal soap, introduce beneficial predators."
    },
    "Tomato__Target_Spot": {
        "plant": "Tomato",
        "disease": "Target Spot",
        "severity": "Moderate",
        "description": "Fungal disease causing concentric ring patterns on leaves.",
        "treatment": "Apply fungicides, improve air circulation, practice crop rotation."
    },
    "Tomato__Tomato_YellowLeaf__Curl_Virus": {
        "plant": "Tomato",
        "disease": "Yellow Leaf Curl Virus",
        "severity": "Severe",
        "description": "Viral disease causing yellow, curled leaves and stunted growth.",
        "treatment": "Remove infected plants, control whiteflies, use resistant varieties."
    },
    "Tomato__Tomato_mosaic_virus": {
        "plant": "Tomato",
        "disease": "Mosaic Virus",
        "severity": "Severe",
        "description": "Viral infection causing mottled, distorted leaves.",
        "treatment": "Remove infected plants, disinfect tools, avoid tobacco products."
    },
    "Tomato_healthy": {
        "plant": "Tomato",
        "disease": "Healthy",
        "severity": "None",
        "description": "Your tomato plant appears healthy with no signs of disease.",
        "treatment": "Continue regular care and monitoring."
    }
}

def preprocess_image(image):
    """Preprocess image for model prediction"""
    # Convert to RGB if needed (handles RGBA and other formats)
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Resize image to model input size with high-quality resampling
    img_resized = image.resize((224, 224), Image.Resampling.LANCZOS)
    
    # Convert to array and normalize
    img_array = np.array(img_resized, dtype=np.float32) / 255.0
    
    # Add batch dimension
    img_array = np.expand_dims(img_array, axis=0)
    
    return img_array

def predict_disease(model, image):
    """Make prediction on the processed image"""
    try:
        img_array = preprocess_image(image)
        predictions = model.predict(img_array, verbose=0)
        confidence_scores = tf.nn.softmax(predictions[0]).numpy()
        predicted_class_index = np.argmax(confidence_scores)
        confidence = float(confidence_scores[predicted_class_index])
        
        return predicted_class_index, confidence
    except Exception as e:
        st.error(f"Error during prediction: {str(e)}")
        return None, None

# Load model
model = load_model()
class_names = list(DISEASE_INFO.keys())

# Debug: Print model input shape
# if model:
#     st.sidebar.write(f"**Model Info:**")
#     st.sidebar.write(f"Expected input shape: {model.input_shape}")
#     st.sidebar.write(f"Number of classes: {len(class_names)}")

# Main header
st.markdown("""
<div class="main-header">
    <h1>🌿 Plant Disease Detection</h1>
    <p>Upload a photo of your plant leaf to detect diseases and get treatment recommendations</p>
</div>
""", unsafe_allow_html=True)

# Sidebar for image upload
with st.sidebar:
    st.header("📸 Image Upload")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose a plant image",
        type=['png', 'jpg', 'jpeg'],
        help="Upload a clear image of a plant leaf for best results"
    )
    
    if uploaded_file:
        st.success("Image uploaded successfully!")

# Main content area
if uploaded_file:
    # Display the uploaded image
    st.subheader("🖼️ Uploaded Image")
    image = Image.open(uploaded_file)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(image, caption="Plant Image", use_container_width=True)
        
        # Prediction button
        if st.button("🔬 Analyze Plant Health", type="primary"):
            with st.spinner("Analyzing your plant image..."):
                # Add a small delay for better UX
                time.sleep(1)
                
                predicted_index, confidence = predict_disease(model, image)
                
                if predicted_index is not None and predicted_index < len(class_names):
                    predicted_class = class_names[predicted_index]
                    disease_info = DISEASE_INFO[predicted_class]
                    
                    # Display results - minimalist style
                    st.subheader("📋 Analysis Results")
                    
                    # Basic information
                    st.write(f"**Plant:** {disease_info['plant']}")
                    st.write(f"**Status:** {disease_info['disease']}")
                    st.write(f"**Severity:** {disease_info['severity']}")
                    st.write(f"**Confidence:** {confidence*100:.1f}%")
                    
                    st.write("---")
                    
                    # Description and treatment
                    st.write("**Description:**")
                    st.write(disease_info['description'])
                    
                    st.write("**Recommended Treatment:**")
                    st.write(disease_info['treatment'])
                    
                    # Confidence warning
                    if confidence < 0.7:
                        st.warning("⚠️ **Note:** The confidence level is below 70%. Consider taking another photo with better lighting or a clearer view of the affected area.")
                    
                    # Additional recommendations for diseased plants
                    if disease_info['disease'] != 'Healthy':
                        st.info("💡 **General Tips:** Always consult with a local agricultural expert for severe cases. Early detection and treatment are key to plant health.")
                
                else:
                    st.error("Unable to classify the image. Please try with a clearer image of a plant leaf.")

else:
    # Welcome screen
    st.markdown("""
    ## 🚀 How to Use This Tool
    
    1. **Upload** a clear image of your plant leaf using the sidebar
    2. **Click** the "Analyze Plant Health" button
    3. **Get** instant disease detection and treatment recommendations
    
    ### 📱 Tips for Best Results
    - Use good lighting when taking photos
    - Focus on leaves that show clear symptoms
    - Ensure the leaf fills most of the image frame
    - Avoid blurry or low-resolution images
    
    ### 🌾 Supported Plants
    This tool can detect diseases in:
    - **Tomatoes** (7 different conditions)
    - **Potatoes** (3 different conditions) 
    - **Bell Peppers** (2 different conditions)
    
    ---
    *Made with ❤️ for farmers and gardeners worldwide*
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>🌿 Plant Disease Detection System | Powered by AI Technology</p>
    <p><small>For educational and advisory purposes. Always consult agricultural experts for critical decisions.</small></p>
</div>
""", unsafe_allow_html=True)