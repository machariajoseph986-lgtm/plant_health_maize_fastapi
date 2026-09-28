# 🌽 Plant Health Maize AI

A FastAPI-based plant health application that combines **maize disease image classification**, **maize-domain/OOD detection**, **PostgreSQL disease information**, and a **plant-health knowledge-base chatbot**.

The system is designed to reduce false disease predictions by first determining whether an uploaded image appears to contain maize before sending it to the maize disease classifier.

---

## 📌 Project Overview

Plant Health Maize AI provides two main AI-assisted capabilities:

1. **Image-based maize disease diagnosis**
2. **Plant-health knowledge-base chatbot**

The diagnosis pipeline uses a two-stage architecture:

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
          PostgreSQL Knowledge Base
                  │
                  ▼
            Diagnosis Result
                  │
                  ▼
          Context-aware Chatbot
```

---

## 🧠 AI Components

### 1. Maize Disease Classifier

The disease classifier is based on **MobileNetV2** and recognizes four dataset classes:

- Blight
- Common Rust
- Gray Leaf Spot
- Healthy

Input images are resized to:

```text
320 × 320 × 3
```

The deployed application runs the trained disease model using **LiteRT** rather than the full TensorFlow runtime. This reduces deployment overhead and helps the application operate within the memory constraints of the production environment.

### 2. Maize Gate / OOD Detection

A dedicated binary gate is executed before disease classification. Its purpose is to determine whether an uploaded image is sufficiently similar to the maize domain.

The gate was trained using:

- 500 maize images
- 800 non-maize plant images
- 300 non-plant object images

Total:

```text
1,600 images
```

The non-maize examples include other crops and unrelated objects.

#### Maize Gate Architecture

```text
Input Image
     │
     ▼
Image preprocessing
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

The gate therefore does not replace the disease classifier. It acts as a domain-validation layer before it.

#### Gate decision

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

When an image is rejected, the disease classifier is not run. The user instead receives a message explaining that the uploaded image does not appear to contain maize.

---

## 🎯 Confidence and Uncertainty

The disease classifier uses a confidence threshold of:

```text
70%
```

Predictions are therefore separated into two confidence states:

- **Accepted** — confidence ≥ 70%
- **Uncertain** — confidence < 70%

The system does not treat model confidence as absolute certainty.

### Finding status

For multiple uploaded images, contributing predictions are grouped by disease. The final finding status is determined as follows:

| Condition | Finding status |
|---|---|
| All contributing predictions are accepted | Identified |
| At least one contributing prediction is uncertain | Identified with uncertainty |
| No usable accepted/uncertain prediction status | Possible |

This allows the application to communicate uncertainty instead of presenting every model prediction as equally reliable.

---

## 🖼️ Multi-Image Diagnosis

The application supports diagnosis using multiple images from the same submission.

Limits are:

```text
Maximum images per diagnosis: 5
Maximum size per image:       10 MB
Maximum total upload size:    30 MB
```

Each uploaded image keeps its original image number throughout the diagnosis process.

For example:

```text
Image 1 → Accepted → Disease analysis
Image 2 → Rejected → Non-maize
Image 3 → Accepted → Disease analysis
```

Rejected images are displayed separately so that users can understand which images were excluded and why.

The application can also identify the same disease across multiple contributing images and calculate the average confidence for that finding.

---

## 🗄️ PostgreSQL Knowledge Base

The application uses PostgreSQL to store structured plant-health information.

The current knowledge base contains the following tables:

- `plants`
- `species`
- `health_problems`
- `pathogens`
- `symptoms`
- `conditions`
- `management`
- `chemical_management`
- `transmission`
- `sources`

The database connects diseases to their associated:

- plant hosts
- species
- pathogens
- symptoms
- favourable conditions
- management practices
- chemical-management information
- transmission mechanisms
- information sources

Foreign-key and orphan-record checks were performed on the production database.

---

## 💬 Knowledge-Base Chatbot

The chatbot allows users to ask natural-language questions about plant health information contained in the knowledge base.

Examples include:

- *What are the symptoms of Common Rust?*
- *How do I manage maize blight?*
- *What conditions favour Common Rust?*
- *How does Common Rust spread?*
- *What chemical treatments are available?*

The chatbot searches the structured knowledge base and returns information associated with the relevant plant disease.

### Unsupported Questions

The chatbot is designed to avoid inventing information outside the available knowledge base.

For example, a question such as:

> What is the price of maize in Nairobi?

returns an unavailable-information response rather than attempting to provide an unrelated answer.

Similarly, unsupported diseases are not automatically mapped to a similarly named disease. For example:

> What are the symptoms of banana bacterial wilt?

does **not** get incorrectly mapped to Potato Bacterial Wilt.

A supported query such as:

> What are the symptoms of potato bacterial wilt?

returns the corresponding Potato Bacterial Wilt information.

---

## 🔗 Diagnosis-Aware Chatbot

The chatbot can be opened directly from a diagnosis result.

When the user selects **Ask about this diagnosis**, the application carries the relevant diagnosis context into the chatbot.

For example:

```text
Diagnosis
   │
   ▼
Maize Blight identified
   │
   ▼
Ask about this diagnosis
   │
   ▼
Context-aware chatbot
```

The user can then ask follow-up questions such as:

- *What should I do to manage this disease?*
- *What conditions can make this disease worse?*
- *How does this disease spread?*

The chatbot continues using the active diagnosis context.

### ↩️ Return to Diagnosis

The diagnosis-aware chatbot also provides a **Back to your diagnosis** action.

The original diagnosis case is preserved temporarily in application memory so that the user can:

```text
Diagnosis Results
      ↓
Chatbot
      ↓
Question 1
      ↓
Question 2
      ↓
Question 3
      ↓
Back to your diagnosis
      ↓
Same Diagnosis Results
```

This return path is maintained even after multiple chatbot questions.

A general chatbot session that was not opened from a diagnosis does not receive the diagnosis return button.

---

## 🕘 Conversation History

The chatbot provides a temporary **Conversation history** feature.

The history stores:

- The user's questions
- The associated disease context, when applicable
- The associated diagnosis case, when applicable

The chatbot stores **questions only**, not chatbot responses.

### History limit

The maximum history length is:

```text
10 questions
```

When an 11th question is added, the oldest question is removed automatically.

Users can also manually clear their history using **Clear history**. A confirmation prompt is displayed before the history is cleared.

### Repeating previous questions

Selecting an existing question from the history reruns that question.

Repeating a previous question:

- does not create a duplicate history entry
- replaces the currently displayed answer
- preserves the existing history list
- preserves diagnosis context when applicable

Conversation history is maintained temporarily in application memory using a session identifier. It is **not** stored permanently in PostgreSQL.

---

## 🔐 Upload Validation and Security

The application applies several validation and security controls to uploaded images.

### Supported image formats

- JPEG
- PNG
- WEBP

The application checks both the filename extension and the actual detected image format. Uploaded images are also verified using Pillow before they are processed.

### Upload limits

```text
Maximum image size:       10 MB
Maximum diagnosis images: 5
Maximum total upload:     30 MB
```

The application also applies a Pillow image-pixel limit to reduce the risk of excessively large image decompression.

### Security headers

Production responses include security headers such as:

```text
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Referrer-Policy: strict-origin-when-cross-origin
```

These headers provide additional protection against common browser-based attack techniques.

### Environment variables

Database credentials and other environment-specific configuration are not hard-coded into the application. Production configuration is supplied through environment variables. The `.env` file is excluded from Git tracking.

A security review was also performed for accidentally exposed credentials and database connection strings. No critical exposed secrets were identified.

---

## 🖼️ Image Storage and Privacy

The application follows a process-and-diagnose approach rather than maintaining a permanent archive of uploaded user images.

The principle is:

> Diagnose the image, retain the diagnostic result — not the user's original image permanently.

Uploaded images are processed temporarily for diagnosis. The application does not intentionally maintain a permanent image database of users' diagnosis uploads.

For the diagnosis-to-chatbot workflow, the application temporarily keeps the diagnosis case in memory so that the user can move between the diagnosis result and its associated chatbot conversation.

The temporary diagnosis-case store is limited to:

```text
50 diagnosis cases
```

Older cases are removed when the limit is exceeded.

This in-memory approach is suitable for the current demonstration deployment but would require further consideration for a larger multi-instance production system.

---

## 🚀 Production Deployment

The application is deployed using the following architecture:

```text
GitHub
   │
   ▼
Render
   │
   ▼
Docker Container
   │
   ├── FastAPI
   ├── LiteRT inference
   └── PostgreSQL connection
```

Production application:

<https://plant-health-maize-fastapi.onrender.com>

The deployment uses Docker to provide a consistent runtime environment. The production disease and feature-extraction models use LiteRT to reduce runtime memory requirements compared with loading the full TensorFlow stack.

---

## 🧪 Runtime Validation

The LiteRT migration was validated against the original TensorFlow/TFLite pipeline.

### Disease model

Using the same input tensor:

```text
TensorFlow output:
[0.983679354, 0.004437326, 0.011881880, 0.000001449]

LiteRT output:
[0.983679354, 0.004437326, 0.011881880, 0.000001449]

Maximum absolute difference:
0.0
```

Both runtimes produced:

```text
Class index: 0
Confidence: 98.3679%
```

### Feature extractor

```text
TensorFlow shape: (1, 1280)
LiteRT shape:     (1, 1280)

Mean absolute difference:    0.0
Maximum absolute difference: 0.0
```

These tests confirmed that the deployed LiteRT models reproduce the corresponding model outputs when given the same input tensor.

---

## ⚡ Performance Validation

Performance testing was performed against the deployed application.

Representative warm-request results included:

```text
Homepage:
Approximately 0.37–0.51 seconds

Average warm homepage response:
Approximately 0.426 seconds

Single-image diagnosis:
Approximately 2 seconds

Five-image diagnosis:
Approximately 4 seconds

1.96 MB image diagnosis:
Approximately 4 seconds
```

During diagnosis testing, observed application memory usage was approximately:

```text
226.7 MB
```

This remained below the Render Free instance memory limit of:

```text
512 MB
```

Cold requests can take considerably longer because the application may need to initialize the machine-learning models.

---

## ✅ Functional Validation

The following major application flows were tested:

| Test | Result |
|---|---|
| Production homepage | PASSED |
| High-confidence maize diagnosis | PASSED |
| Non-maize image rejection | PASSED |
| Invalid image-content rejection | PASSED |
| Multi-image diagnosis | PASSED |
| Uncertain prediction handling | PASSED |
| Diagnosis → chatbot context | PASSED |
| Chatbot → same diagnosis result | PASSED |
| Common Rust chatbot query | PASSED |
| Diagnosis-aware management query | PASSED |
| Chemical-management query | PASSED |
| Transmission query | PASSED |
| Unsupported information query | PASSED |
| Unsupported disease query | PASSED |
| Supported Potato Bacterial Wilt regression | PASSED |
| Chatbot conversation history | PASSED |
| Database integrity checks | PASSED |
| Security review | PASSED |
| Production performance review | PASSED |

---

## ⚠️ Limitations

The application is a research and demonstration system and has several important limitations.

### Disease coverage

The current disease classifier is limited to the classes represented in its training dataset:

- Blight
- Common Rust
- Gray Leaf Spot
- Healthy

It should not be assumed to recognize every maize disease or plant health problem.

### Model confidence

A confidence score represents the model's output probability, not medical-style certainty. Predictions below the 70% threshold are explicitly marked as uncertain.

### Maize gate

The maize gate was evaluated using a constructed dataset containing maize, other plants, and non-plant objects. Its evaluation results should therefore not be interpreted as universal real-world accuracy.

### Image quality

Poor lighting, unusual viewpoints, severe blur, occlusion, damaged leaves, or backgrounds that differ substantially from the training data may affect predictions.

### Knowledge base coverage

Chatbot answers depend on information available in the PostgreSQL knowledge base. The system should not be expected to answer arbitrary agricultural, market, financial, or other unrelated questions.

### Chemical management

Chemical-management information should be interpreted together with applicable local regulations, product labels, crop requirements, and professional agricultural guidance.

### Temporary in-memory state

Diagnosis cases and chatbot history are currently maintained in application memory. This approach is appropriate for the current demonstration but is not a durable storage architecture for a large multi-instance production system.

---

## 💻 Local Development

### Requirements

Recommended environment:

- Python 3.11
- PostgreSQL
- Git
- Docker (optional)
- Windows, Linux, or macOS

### Clone the repository

```bash
git clone https://github.com/machariajoseph986-lgtm/plant_health_maize_fastapi.git
cd plant_health_maize_fastapi
```

### Create a virtual environment

**Windows Git Bash:**

```bash
python -m venv nn-env
source nn-env/Scripts/activate
```

**Linux/macOS:**

```bash
python3 -m venv nn-env
source nn-env/bin/activate
```

### Install dependencies

For the production-compatible environment:

```bash
pip install -r requirements-render.txt
```

### Configure environment variables

Create a local `.env` file containing the required PostgreSQL configuration.

Example variable names:

```text
POSTGRES_HOST
POSTGRES_PORT
POSTGRES_DATABASE
POSTGRES_USER
POSTGRES_PASSWORD
ENVIRONMENT
CORS_ORIGINS
```

> ⚠️ Do not commit credentials or other secrets to Git.

### Run the application

```bash
uvicorn api:app --reload
```

The local application can then be accessed through the address printed by Uvicorn.

---

## 📁 Project Structure

A simplified view of the project is:

```text
plant_health_maize_fastapi/
│
├── api.py
├── Dockerfile
├── render.yaml
├── requirements-render.txt
├── README.md
│
├── cnn/
│   ├── predictor.py
│   └── database_integration_postgresql.py
│
├── knowledge_base/
│   ├── chatbot.py
│   ├── schema.sql
│   └── seed/
│
├── templates/
│   ├── diagnosis.html
│   └── chatbot.html
│
├── static/
│   └── ...
│
├── training_output/
│   └── v3/
│       ├── maize_disease.tflite
│       └── maize_feature_extractor.tflite
│
└── data/
    └── ...
```

---

## 🌐 Main Application Routes

| Route | Purpose |
|---|---|
| `/` | Application homepage |
| `/diagnosis` | Diagnosis interface/results |
| `/diagnose-page` | Processes diagnosis submissions |
| `/chatbot` | Plant-health knowledge-base chatbot |
| `/chatbot/clear-history` | Clears temporary chatbot question history |

The exact available methods and supporting API behavior are defined in `api.py`.

---

## 🛠️ Technology Stack

**Backend**

- FastAPI
- Uvicorn
- Python

**Machine Learning**

- TensorFlow/Keras for model development
- MobileNetV2
- LiteRT for production inference
- Scikit-learn
- Logistic Regression
- Joblib
- NumPy
- Pillow

**Database**

- PostgreSQL
- psycopg

**Frontend**

- HTML
- Jinja2 templates
- CSS
- JavaScript

**Deployment**

- GitHub
- Docker
- Render

---

## 📊 Database Integrity

The production database was checked for:

- Expected tables
- Expected row counts
- Foreign-key relationships
- Orphaned health problems
- Orphaned pathogens
- Orphaned symptoms
- Orphaned conditions
- Orphaned management records
- Orphaned chemical-management records
- Orphaned transmission records
- Orphaned sources
- Orphaned species

All tested integrity checks passed during final validation.

---

## 🔍 Testing Summary

The final validation covered the application's major components:

- ✅ Database integrity
- ✅ Disease diagnosis
- ✅ Maize gate
- ✅ Multi-image diagnosis
- ✅ Uncertainty handling
- ✅ Knowledge-base chatbot
- ✅ Diagnosis context
- ✅ Conversation history
- ✅ Upload validation
- ✅ Security review
- ✅ Performance review
- ✅ Production deployment

The application was tested using both normal and intentionally invalid or unsupported inputs.

---

## 🎓 Project Purpose

Plant Health Maize AI was developed as a practical demonstration of how machine learning, computer vision, structured agricultural knowledge, databases, and web APIs can be combined into a single plant-health decision-support application.

The project focuses on making model predictions more transparent by:

1. Checking the input domain before disease classification.
2. Communicating prediction confidence.
3. Separating uncertain predictions from accepted predictions.
4. Supporting multiple images in one diagnosis.
5. Connecting predictions to structured disease information.
6. Providing contextual follow-up through a knowledge-base chatbot.
7. Avoiding permanent storage of users' original diagnosis images.

---

## 🚦 Project Status

**Current status: Deployed and functionally validated.**

The production application has completed:

- Production deployment
- Database integration
- AI inference migration to LiteRT
- Maize-domain validation
- Disease diagnosis testing
- Multi-image testing
- Uncertainty testing
- Chatbot testing
- Diagnosis-aware chatbot testing
- Conversation-history testing
- Security review
- Performance review
- Final application validation

The system is suitable as a research/demo application and provides a foundation for future improvements such as broader disease coverage, larger real-world validation datasets, persistent session infrastructure, improved monitoring, and expanded agricultural knowledge.

---

## 📄 License

This project is developed for academic and demonstration purposes.

---

## 👤 Author

**Plant Health Maize AI**

Built as a data science and machine-learning project combining computer vision, FastAPI, PostgreSQL, and knowledge-based agricultural assistance.
