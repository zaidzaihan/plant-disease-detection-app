Here’s a clean, informative, and developer-friendly `README.md` for your GitHub project:

---

# 🌿 Plant Disease Detection App

An AI-powered web application that detects plant diseases from leaf images using a Convolutional Neural Network (CNN) model — all deployable with **Streamlit**.

🧪 Try it out: [Live Demo](https://plant-disease-detection-app-app-zya8ie.streamlit.app/)

📁 GitHub Repo: [github.com/zaidzaihan/plant-disease-detection-app](https://github.com/zaidzaihan/plant-disease-detection-app)

---

## 📸 What This App Does

Upload a **close-up image of a plant leaf**, and the app will:

* Detect if the plant is **healthy** or affected by a **specific disease**
* Show disease **name**, **severity**, **description**, and **treatment**
* Provide actionable tips, even when confidence is low

### 🧠 Trained to Recognize:

| Plant           | Diseases Detected                                                                                                                                  |
| --------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Tomato**      | Bacterial Spot, Early Blight, Late Blight, Leaf Mold, Septoria Leaf Spot, Target Spot, Yellow Leaf Curl Virus, Mosaic Virus, Spider Mites, Healthy |
| **Potato**      | Early Blight, Late Blight, Healthy                                                                                                                 |
| **Bell Pepper** | Bacterial Spot, Healthy                                                                                                                            |

> 💡 This system is ideal for farmers, agronomists, and agriculture students who want fast, visual diagnosis using a simple web interface.

---

## 🛠️ Installation & Deployment Guide

### 🔁 Clone the Repository

```bash
git clone https://github.com/zaidzaihan/plant-disease-detection-app.git
cd plant-disease-detection-app
```

### 🐍 Create a Virtual Environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

### 📥 Download the Model Automatically

The app uses `gdown` to fetch the pre-trained model from Google Drive if it's not present in the local directory. No extra steps required.

But if you'd like to manually download it:

* File ID: `1VHEHLSQ0d_QKvgeZjlheDixwLRwiBMCw`
* Link: [https://drive.google.com/uc?id=1VHEHLSQ0d\_QKvgeZjlheDixwLRwiBMCw](https://drive.google.com/uc?id=1VHEHLSQ0d_QKvgeZjlheDixwLRwiBMCw)
* Save it as: `best_model.h5` in the root directory

### ▶️ Run the App Locally

```bash
streamlit run app.py
```

> App will launch in your default browser at `http://localhost:8501`

---

## 🌐 Deploy to Streamlit Cloud

1. Fork or clone this repo.
2. Create a free account at [streamlit.io/cloud](https://streamlit.io/cloud).
3. Connect your GitHub and click **“New App”**.
4. Select your forked repo, and set `app.py` as the main file.
5. 🎉 Done! The app will auto-install requirements and deploy.

---

## 🧠 How the AI Model Works

* Input: 224x224 RGB images
* Framework: **TensorFlow / Keras**
* Architecture: CNN fine-tuned on a dataset of labeled plant leaf images
* Output: Disease class (e.g., `Tomato_Late_blight`) and confidence score
* Disease mapping is hardcoded in the `DISEASE_INFO` dictionary for detailed descriptions and treatment suggestions.

---

## 📂 Folder Structure

```
.
├── app.py                # Main Streamlit app
├── best_model.h5         # Trained Keras model (auto-downloaded if missing)
├── requirements.txt      # Dependencies
└── README.md             # You're here!
```

---

## 🤝 Contribution

Have an idea to improve the app?

* Add support for more plant types
* Improve the CNN model or training pipeline
* Add multilingual support

Feel free to open issues or PRs!

---

## 📄 License

This project is licensed under the MIT License.
Feel free to use it, modify it, and share it!

---

## 🙌 Credits

* Developed by [Zaid Zaihan](https://github.com/zaidzaihan)
* Powered by Streamlit and TensorFlow
* Trained on public plant disease datasets

---

Let me know if you'd like:

* A section on how to retrain the model
* Badges (for license, Streamlit app, etc.)
* Screenshots or GIF previews
  I can add them for you.
