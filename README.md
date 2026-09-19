# 🌽 Plant Health Maize AI

A FastAPI-based plant health application that combines **maize disease image classification**, **out-of-distribution (OOD) / maize-gate detection**, **PostgreSQL disease information**, and a **plant-health knowledge-base chatbot**.

The system is designed to prevent the maize disease classifier from blindly assigning a maize disease to images that are not actually maize.

---

## 📌 Project Overview

The application provides two main AI-assisted capabilities:

1. **Image-based maize disease diagnosis**
2. **Plant-health knowledge-base chatbot**

The image diagnosis pipeline uses a two-stage architecture:

```text
Uploaded Image
      │
      ▼
┌─────────────────────┐
│   Maize Gate / OOD  │
│   "Is this maize?"  │
└──────────┬──────────┘
           │
      ┌────┴────┐
      │         │
   Reject     Accept
      │         │
      ▼         ▼
   Not Maize   Disease Classifier
                  │
                  ▼
          Disease Information
                  │
                  ▼
              PostgreSQL
```

This additional gate addresses an important limitation of ordinary multi-class classifiers: when an image does not belong to any of the training classes, the classifier may still select the class with the highest probability.

---

## 🧠 Current AI Components

### 1. Maize Disease Classifier

The disease model is based on **MobileNetV2** and classifies maize images into four categories:

* Blight
* Common Rust
* Gray Leaf Spot
* Healthy

The model accepts images resized to:

```text
320 × 320 × 3
```

and uses MobileNetV2 preprocessing.

---

### 2. Maize Gate / OOD Detection

A dedicated binary gate was added before disease classification.

Its purpose is:

> Determine whether an uploaded image is sufficiently similar to the maize domain before allowing it to reach the disease classifier.

The gate was trained using:

* **500 maize images**
* **800 non-maize plant images**
* **300 non-plant object images**

Total:

```text
1,600 images
```

The non-maize examples include other crops such as apple, blueberry, grape, potato, pepper, soybean, tomato and strawberry, together with unrelated objects.

---

## 🔬 Maize Gate Architecture

The gate reuses the feature representation produced by the existing MobileNetV2 model.

```text
Input Image
     │
     ▼
MobileNetV2 preprocessing
     │
     ▼
MobileNetV2 feature extractor
     │
     ▼
Global Average Pooling
     │
     ▼
1280-dimensional feature vector
     │
     ▼
Logistic Regression
     │
     ▼
Maize Probability
     │
     ▼
Threshold = 0.45
```

The gate therefore does not replace the disease classifier.

It acts as a **domain-validation layer** before it.

---

## 🚦 Gate Decision

The current gate threshold is:

```text
0.45
```

Conceptually:

```text
P(maize) < 0.45
        │
        ▼
     Reject

P(maize) ≥ 0.45
        │
        ▼
   Run disease model
```

When an image is rejected, the disease classifier is not executed.

The user receives a message explaining that the image does not appear to contain maize.

---

## 🧪 Gate Evaluation

The gate dataset was divided into training, validation and test sets:

| Split      |   Maize | Non-Maize |
| ---------- | ------: | --------: |
| Training   |     350 |       770 |
| Validation |      75 |       165 |
| Test       |      75 |       165 |
| **Total**  | **500** | **1,100** |

The constructed validation and test sets achieved:

```text
Validation accuracy: 100%
Test accuracy:       100%
```

These results apply to the constructed evaluation dataset and **should not be interpreted as proof of 100% real-world accuracy**.

Further evaluation using a larger and more representative real-world dataset is still required.

---

## 🧪 Example Behaviour

### Non-maize image

An Apple-scab image was tested through the gate.

Example result:

```text
Maize probability: approximately 2.16%
Threshold:         45%
Gate status:       Rejected
```

The disease classifier was not run.

The applica
