# 🌽 Corn Pathology AI — Maize Disease Classification

## Plant Health Maize Project

An image-based deep learning project for classifying maize leaf health conditions using Convolutional Neural Networks and MobileNetV2 transfer learning.

---

## 📌 Project Overview

Corn Pathology AI is a computer vision project designed to classify maize leaf images into four health conditions:

* **Blight**
* **Common Rust**
* **Gray Leaf Spot**
* **Healthy**

The project investigates whether deep learning can provide reliable image-based classification of maize leaf diseases and support users with useful plant-health information.

The project follows the **CRISP-DM (Cross-Industry Standard Process for Data Mining)** framework:

1. Business Understanding
2. Data Understanding
3. Data Preparation
4. Modeling
5. Evaluation
6. Deployment

---

## 🎯 Problem Statement

Maize production can be affected by diseases that reduce crop health and productivity. Identifying diseases from visual symptoms can be difficult because different diseases may produce visually similar patterns on leaves.

This project develops an image-classification system capable of analyzing maize leaf images and predicting the most likely health condition.

The system is intended as a **decision-support tool**, not as a replacement for professional agricultural diagnosis.

---

## ❓ Research Questions

The project is guided by two main questions:

1. Can maize leaf diseases be reliably classified using image-based deep learning?
2. Can a confidence-based prediction mechanism help identify uncertain predictions rather than presenting every prediction as definitive?

---

## 🎯 Project Objectives

### General Objective

To develop and evaluate an image-based machine learning system capable of classifying maize leaf health conditions.

### Specific Objectives

* Understand and verify the maize leaf image dataset.
* Clean and standardize image data.
* Analyze the distribution of the four target classes.
* Develop a Custom CNN baseline.
* Evaluate a tuned Custom CNN configuration.
* Apply MobileNetV2 transfer learning.
* Compare model performance using accuracy, precision, recall and F1-score.
* Investigate class-specific classification errors.
* Analyze prediction confidence.
* Introduce an uncertainty threshold for low-confidence predictions.
* Prepare the selected model for application deployment.

---

# 📊 Dataset

The cleaned dataset contains:

| Dataset component | Images |
| ----------------- | -----: |
| Total dataset     |  4,184 |
| Training          |  2,928 |
| Validation        |    628 |
| Test              |    628 |

The four classes are:

| Class          | Description                           |
| -------------- | ------------------------------------- |
| Blight         | Maize leaf affected by blight         |
| Common_Rust    | Maize leaf affected by common rust    |
| Gray_Leaf_Spot | Maize leaf affected by gray leaf spot |
| Healthy        | Healthy maize leaf                    |

The training data contains 2,928 images. Common Rust is the largest class with 914 images, while Gray Leaf Spot is the smallest with 400 images. The project uses class weighting to reduce the effect of this class imbalance during training.

---

# 🧹 Data Preparation

The image preparation pipeline includes:

1. Image integrity verification.
2. RGB conversion.
3. Image resizing.
4. Pixel normalization.
5. Training-only data augmentation.
6. Stratified train/validation/test splitting.
7. Class weighting during model training.

The project uses different preprocessing configurations depending on the model.

### Custom CNN

Images are resized and pixel values are scaled from:

```text
[0, 255] → [0, 1]
```

### MobileNetV2

The MobileNetV2 preprocessing function is used so that images are prepared according to the pretrained model's expected input representation.

---

# 🔄 Data Augmentation

Training data augmentation is used to increase the variety of training examples.

The project uses transformations including:

* Horizontal flipping
* Rotation
* Zoom
* Contrast adjustment

Augmentation is applied to training data only.

Validation and test data remain unaugmented so that model performance can be evaluated on data that has not been artificially transformed.

---

# 🧠 Machine Learning Models

Three main modeling approaches were evaluated.

## 1. Custom CNN Baseline

The Custom CNN was developed as the project's baseline deep learning model.

The architecture includes:

* Convolutional layers
* Batch normalization
* Max pooling
* Global average pooling
* Dense layer
* Dropout
* Four-class softmax output

The reconstructed baseline contains four convolutional blocks with increasing filter sizes.

---

## 2. Tuned Custom CNN

The second experiment modified the Custom CNN by:

* Increasing the image resolution from 256×256 to 320×320
* Applying moderate image augmentation

The experiment was designed to determine whether the additional resolution and augmentation would improve performance.

---

## 3. MobileNetV2 Transfer Learning

MobileNetV2 was introduced as a pretrained feature-extraction architecture.

Two stages were evaluated:

### Stage 1 — Frozen MobileNetV2

The pretrained base was used while the appropriate classification layers were trained.

Result:

**92.20% test accuracy**

### Stage 2 — Fine-Tuned MobileNetV2

Later MobileNetV2 layers were fine-tuned to adapt the pretrained representation to the maize disease classification problem.

Result:

**94.43% test accuracy**

Stage 2 produced the strongest result among the evaluated models.

---

# 📈 Model Performance

All models were evaluated using the held-out test set.

| Model                   | Test Accuracy |   Macro F1 |
| ----------------------- | ------------: | ---------: |
| Custom CNN Baseline     |        93.63% |     92.32% |
| Tuned Custom CNN        |        89.01% |     86.83% |
| MobileNetV2 Stage 1     |        92.20% |     90.30% |
| **MobileNetV2 Stage 2** |    **94.43%** | **92.97%** |

---

# 🏆 Final Model

The selected model is:

## MobileNetV2 Transfer Learning Stage 2

Performance on the held-out test set:

* **Accuracy:** 94.43%
* **Macro F1:** 92.97%
* **Weighted F1:** 94.42%
* **Correct predictions:** 593 / 628
* **Incorrect predictions:** 35 / 628

The model therefore achieved the highest test accuracy among the evaluated approaches.

---

# 🔍 Error Analysis

The analysis identified **Blight vs Gray Leaf Spot** as the most difficult classification boundary.

For the Custom CNN baseline:

* Blight → Gray Leaf Spot errors: 20
* Gray Leaf Spot → Blight errors: 8
* Combined errors: 28

For MobileNetV2 Stage 2:

* Combined Blight ↔ Gray Leaf Spot errors: 23

This represents a reduction of five errors compared with the Custom CNN baseline.

However, the remaining errors demonstrate that these two classes can still be visually difficult to distinguish.

---

# 📊 Class-Level Performance

The final MobileNetV2 model performed particularly strongly on Healthy and Common Rust images.

The project also identified Gray Leaf Spot as an important remaining weakness.

The final analysis reports:

* Blight recall: **90.70%**
* Gray Leaf Spot recall: **83.72%**
* Healthy F1-score: **99.71%**
* Common Rust F1-score: **97.22%**

These results demonstrate why overall accuracy alone is not sufficient for evaluating the system.

---

# ⚠️ Confidence and Uncertainty

The system incorporates confidence-based uncertainty handling.

A **70% confidence threshold** is used as the project's operating threshold.

The policy is:

```text
Confidence ≥ 70%
        ↓
Accept prediction

Confidence < 70%
        ↓
Flag as uncertain
```

The confidence mechanism is intended as a safety layer.

It does not guarantee that a high-confidence prediction is correct.

The model should therefore be interpreted as a **decision-support system rather than a confirmed agricultural diagnosis**.

---

# 🚀 Application and Deployment

The Plant Health application uses a FastAPI-based architecture.

The deployment architecture is:

```text
GitHub
   ↓
FastAPI
   ↓
Uvicorn
   ↓
Cloudflare Quick Tunnel
   ↓
Web Browser
```

The application also integrates with PostgreSQL for structured plant-health information.

The notebook documents the use of environment variables for database configuration so that sensitive credentials are not stored directly in the repository.

---

# 💬 Plant Health Chatbot

The project also includes a plant-health chatbot connected to the PostgreSQL knowledge base.

The chatbot provides plant-health information relating to:

* Maize
* Coffee
* Potato
* Tea

The chatbot is broader than the CNN image-classification component.

The CNN focuses on maize disease image classification, while the chatbot provides structured plant-health information.

---

# 🗄️ PostgreSQL Database

PostgreSQL is used to store structured plant-health information.

The database supports information used by the chatbot and plant-health application.

Database connectivity is handled through the project's database integration modules.

Database credentials should be supplied through environment variables rather than committed to GitHub.

---

# 📁 Project Structure

A representative project structure is:

```text
corn_pathology_ai/
│
├── cnn/
│   ├── model files
│   ├── preprocessing
│   └── prediction components
│
├── knowledge_base/
│   ├── chatbot.py
│   └── database_postgresql.py
│
├── templates/
│   └── frontend files
│
├── static/
│   └── static assets
│
├── corn_disease_cnn.ipynb
├── project.ipynb
├── render.yaml
├── requirements.txt
├── .gitignore
└── README.md
```

The exact repository structure may vary depending on the current deployment version.

---

# 💻 Technologies Used

* Python
* TensorFlow / Keras
* MobileNetV2
* NumPy
* Pandas
* Matplotlib
* Scikit-learn
* Pillow
* FastAPI
* Uvicorn
* PostgreSQL
* Git
* GitHub
* Cloudflare Quick Tunnel
* Render deployment configuration

---

# 🧪 Evaluation Metrics

The project uses several evaluation metrics:

### Accuracy

Measures the proportion of correctly classified images.

### Precision

Measures how reliable predictions for each class are.

### Recall

Measures how effectively the model identifies actual examples of a class.

### F1-score

Combines precision and recall.

### Confusion Matrix

Shows which classes are being confused with one another.

### Confidence

Measures the probability assigned to the predicted class and supports the project's uncertainty policy.

---

# 🔐 Security

Do not commit sensitive information to GitHub.

Never commit:

```text
.env
database passwords
API keys
secret tokens
private credentials
```

Use environment variables instead.

---

# ⚠️ Limitations

Although the final model achieved 94.43% test accuracy, it is not perfect.

Important limitations include:

* Some maize diseases have visually similar symptoms.
* Blight and Gray Leaf Spot remain an important source of classification errors.
* Gray Leaf Spot has lower recall than the strongest classes.
* High model confidence does not guarantee correctness.
* The model was evaluated using the available held-out test dataset and may behave differently on images from different environments.
* Image quality, lighting, camera characteristics and field conditions may affect predictions.

The system should therefore be treated as a decision-support tool.

---

# 🔮 Future Improvements

Possible future improvements include:

1. Expand the dataset with additional field images.
2. Increase representation of underrepresented disease classes.
3. Improve Blight vs Gray Leaf Spot classification.
4. Evaluate additional pretrained architectures.
5. Perform external validation using images from different environments.
6. Improve confidence calibration.
7. Add more comprehensive image-quality checks.
8. Optimize the TensorFlow model for production deployment.
9. Deploy the application on infrastructure with sufficient memory for reliable inference.
10. Extend the disease classification system to additional crops and diseases.

---

# 📌 Key Findings

The project demonstrates that:

* Maize leaf diseases can be classified using image-based deep learning.
* The Custom CNN established a strong baseline at 93.63% accuracy.
* The tuned Custom CNN did not improve performance and achieved 89.01%.
* Frozen MobileNetV2 achieved 92.20%.
* Fine-tuned MobileNetV2 achieved the strongest result at 94.43%.
* Blight and Gray Leaf Spot remain the most challenging classification boundary.
* Confidence-based uncertainty handling provides an additional safeguard for low-confidence predictions.
* The final system combines CNN-based image classification with a broader plant-health knowledge base.

---

# 👨‍💻 Project Status

**Status: Completed model development and evaluation; application prepared for deployment/demo.**

The project includes:

* Data understanding
* Data preparation
* CNN modeling
* Transfer learning
* Model comparison
* Error analysis
* Confidence analysis
* FastAPI application architecture
* PostgreSQL integration
* Chatbot functionality
* Deployment configuration

---

# ⚖️ Disclaimer

This system provides machine-learning predictions intended for decision support and educational/research purposes.

A model prediction should not be interpreted as a confirmed agricultural diagnosis. Professional agricultural expertise should be consulted when making important crop-management decisions.
