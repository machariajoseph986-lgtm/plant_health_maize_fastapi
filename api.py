import os
import uuid

from fastapi import FastAPI, File, UploadFile, HTTPException, Request, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

# Disable TensorFlow XLA JIT for deployment stability.
os.environ["TF_XLA_FLAGS"] = "--tf_xla_auto_jit=0"


class ChatRequest(BaseModel):
    message: str


app = FastAPI(
    title="Plant Health Maize API",
    description="API for the Plant Health Maize Project.",
    version="1.0.0"
)


# ============================================================
# FRONTEND CONFIGURATION
# ============================================================

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

templates = Jinja2Templates(
    directory="templates"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:8000",
        "http://localhost:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# UPLOAD CONFIGURATION
# ============================================================

UPLOAD_FOLDER = "static/uploads"

ALLOWED_EXTENSIONS = {
    "jpg",
    "jpeg",
    "png",
    "webp"
}

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


def allowed_file(filename):
    """
    Check whether the uploaded file has an allowed image extension.
    """

    return (
        "." in filename
        and filename.rsplit(
            ".",
            1
        )[1].lower() in ALLOWED_EXTENSIONS
    )


# ============================================================
# FRONTEND ROUTES
# ============================================================

@app.get(
    "/",
    response_class=HTMLResponse,
    name="home"
)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


@app.get(
    "/diagnosis",
    response_class=HTMLResponse,
    name="diagnosis"
)
async def diagnosis_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="diagnosis.html",
        context={
            "result": None
        }
    )


@app.get(
    "/chatbot",
    response_class=HTMLResponse,
    name="chatbot"
)
async def chatbot_page(
    request: Request,
    health_problem_id: str | None = None
):
    diagnosis_profile = None

    if health_problem_id:
        from knowledge_base.database_postgresql import get_disease_profile
        diagnosis_profile = get_disease_profile(health_problem_id)

    return templates.TemplateResponse(
        request=request,
        name="chatbot.html",
        context={
            "response": None,
            "health_problem_id": health_problem_id,
            "diagnosis_profile": diagnosis_profile
        }
    )


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health_check():
    """
    Confirm that the API is running.
    """

    return {
        "status": "ok",
        "service": "Plant Health Maize API"
    }


# ============================================================
# CNN PREDICTION API
# ============================================================

@app.post("/predict")
async def predict(
    image: UploadFile = File(...)
):
    """
    Run the V3 MobileNetV2 model on an uploaded image.
    """

    from cnn.predictor import predict_image

    if not image.filename:
        raise HTTPException(
            status_code=400,
            detail="No image filename was provided."
        )

    if not allowed_file(image.filename):
        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported image format. "
                "Use JPG, JPEG, PNG, or WEBP."
            )
        )

    file_extension = os.path.splitext(
        image.filename
    )[1].lower()

    filename = (
        f"{uuid.uuid4().hex}"
        f"{file_extension}"
    )

    image_path = os.path.join(
        UPLOAD_FOLDER,
        filename
    )

    image_bytes = await image.read()

    with open(
        image_path,
        "wb"
    ) as file:

        file.write(
            image_bytes
        )

    try:

        result = predict_image(
            image_path
        )

    except Exception as error:

        if os.path.exists(image_path):
            os.remove(image_path)

        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(error)}"
        )

    return {
        "class_index":
            result["class_index"],

        "class_name":
            result["class_name"],

        "confidence":
            result["confidence"],

        "confidence_threshold":
            result["confidence_threshold"],

        "confidence_status":
            result["confidence_status"],

        "caution_required":
            result["caution_required"],

        "caution_reason":
            result["caution_reason"],

        "health_problem_id":
            result["health_problem_id"],

        "is_healthy":
            result["is_healthy"]
    }


# ============================================================
# DIAGNOSIS API
# ============================================================

@app.post("/diagnose")
async def diagnose_api(
    image: UploadFile = File(...)
):
    """
    Run the complete maize-health diagnosis pipeline and
    return the result as JSON.
    """

    if not image.filename:
        raise HTTPException(
            status_code=400,
            detail="No image filename was provided."
        )

    if not allowed_file(image.filename):
        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported image format. "
                "Use JPG, JPEG, PNG, or WEBP."
            )
        )

    file_extension = os.path.splitext(
        image.filename
    )[1].lower()

    filename = (
        f"{uuid.uuid4().hex}"
        f"{file_extension}"
    )

    image_path = os.path.join(
        UPLOAD_FOLDER,
        filename
    )

    image_bytes = await image.read()

    with open(
        image_path,
        "wb"
    ) as file:

        file.write(
            image_bytes
        )

    try:

        from cnn.database_integration_postgresql import (
            diagnose_from_image
        )

        result = diagnose_from_image(
            image_path
        )

    except Exception as error:

        if os.path.exists(image_path):
            os.remove(image_path)

        raise HTTPException(
            status_code=500,
            detail=f"Diagnosis failed: {str(error)}"
        )

    return {
        "class_index":
            result["class_index"],

        "class_name":
            result["class_name"],

        "confidence":
            result["confidence"],

        "confidence_status":
            result["confidence_status"],

        "caution_required":
            result["caution_required"],

        "caution_reason":
            result["caution_reason"],

        "health_problem_id":
            result["health_problem_id"],

        "is_healthy":
            result["is_healthy"],

        "disease_profile":
            result.get("disease_profile")
    }


# ============================================================
# DIAGNOSIS WEB FORM
# ============================================================

@app.post(
    "/diagnose-page",
    response_class=HTMLResponse,
    name="diagnose"
)
async def diagnose_page(
    request: Request,
    images: list[UploadFile] = File(...)
):
    """
    Process up to 5 diagnosis images and render the diagnosis page.
    """

    MAX_IMAGES = 5
    MAX_TOTAL_BYTES = 30 * 1024 * 1024

    if not images:
        raise HTTPException(
            status_code=400,
            detail="Please upload at least one image."
        )

    if len(images) > MAX_IMAGES:
        raise HTTPException(
            status_code=400,
            detail="You can analyze a maximum of 5 images per case."
        )

    allowed_extensions = {
        ".jpg",
        ".jpeg",
        ".png",
        ".webp"
    }

    total_bytes = 0

    for image in images:

        if not image.filename:
            raise HTTPException(
                status_code=400,
                detail="One of the uploaded files has no filename."
            )

        extension = os.path.splitext(
            image.filename
        )[1].lower()

        if extension not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Unsupported image format. "
                    "Use JPG, JPEG, PNG, or WEBP."
                )
            )

    saved_paths = []

    try:

        for image in images:

            image_bytes = await image.read()

            total_bytes += len(image_bytes)

            if total_bytes > MAX_TOTAL_BYTES:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        "The total size of the uploaded images "
                        "must not exceed 30 MB per case."
                    )
                )

            file_extension = os.path.splitext(
                image.filename
            )[1].lower()

            filename = (
                f"{uuid.uuid4().hex}"
                f"{file_extension}"
            )

            image_path = os.path.join(
                UPLOAD_FOLDER,
                filename
            )

            with open(
                image_path,
                "wb"
            ) as file:

                file.write(
                    image_bytes
                )

            saved_paths.append(image_path)


        from cnn.database_integration_postgresql import (
            diagnose_from_images
        )

        result = diagnose_from_images(
            saved_paths
        )

        result["image_paths"] = saved_paths

    except HTTPException:
        for saved_path in saved_paths:
            if os.path.exists(saved_path):
                os.remove(saved_path)
        raise

    except Exception as error:

        for saved_path in saved_paths:
            if os.path.exists(saved_path):
                os.remove(saved_path)

        raise HTTPException(
            status_code=500,
            detail=f"Diagnosis failed: {str(error)}"
        )

    return templates.TemplateResponse(
        request=request,
        name="diagnosis.html",
        context={
            "result": result
        }
    )


# ============================================================
# CHATBOT API
# ============================================================

@app.post("/chat")
async def chat(
    payload: ChatRequest
):
    """
    Send a user question to the PostgreSQL-backed
    Plant Health chatbot.
    """

    question = payload.message

    if not question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    try:

        from knowledge_base.chatbot import (
            chatbot_response
        )

        response = chatbot_response(
            question,
            health_problem_id
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Chatbot request failed: {str(error)}"
        )

    return {
        "question": question,
        "response": response
    }


# ============================================================
# CHATBOT WEB FORM
# ============================================================

@app.post(
    "/chatbot",
    response_class=HTMLResponse,
    name="chatbot_submit"
)
async def chatbot_submit(
    request: Request,
    question: str = Form(""),
    health_problem_id: str | None = Form(None)
):
    """
    Process the chatbot web form and render the response.
    """

    if not question.strip():
        return templates.TemplateResponse(
            request=request,
            name="chatbot.html",
            context={
                "response": "Please enter a question.",
                "health_problem_id": health_problem_id,
                "diagnosis_profile": None
            },
            status_code=400
        )

    try:

        from knowledge_base.chatbot import (
            chatbot_response
        )

        response = chatbot_response(
            question,
            health_problem_id
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Chatbot request failed: {str(error)}"
        )

    return templates.TemplateResponse(
        request=request,
        name="chatbot.html",
        context={
            "response": response,
            "health_problem_id": health_problem_id,
            "diagnosis_profile": None
        }
    )


# ============================================================
# DATABASE TEST
# ============================================================

@app.get("/db-test")
def db_test():
    """
    Test the PostgreSQL knowledge-base connection independently
    from the CNN and diagnosis pipeline.
    """

    from knowledge_base.database_postgresql import (
        get_disease_profile
    )

    profile = get_disease_profile(
        "HP_MAIZE_BLIGHT"
    )

    return {
        "status": "ok",
        "database": "postgresql",
        "profile_found": profile is not None,
        "health_problem_id":
            profile.get("health_problem_id")
            if profile
            else None
    }
