import os
from pathlib import Path
import uuid
import base64
import mimetypes
import tempfile
import shutil
from io import BytesIO

from PIL import Image, UnidentifiedImageError

from fastapi import (
    FastAPI,
    File,
    UploadFile,
    HTTPException,
    Request,
    Form
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

ENVIRONMENT = os.getenv("ENVIRONMENT", "development").lower()

if ENVIRONMENT not in {"development", "production"}:
    raise RuntimeError(
        "ENVIRONMENT must be either 'development' or 'production'."
    )

# Disable TensorFlow XLA JIT for deployment stability.
os.environ["TF_XLA_FLAGS"] = "--tf_xla_auto_jit=0"


class ChatRequest(BaseModel):
    message: str


app = FastAPI(
    title="Plant Health Maize API",
    description="API for the Plant Health Maize Project.",
    version="1.0.0",
    docs_url="/docs" if ENVIRONMENT == "development" else None,
    redoc_url="/redoc" if ENVIRONMENT == "development" else None,
    openapi_url="/openapi.json" if ENVIRONMENT == "development" else None,
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

if ENVIRONMENT == "production":
    cors_origins = [
        origin.strip()
        for origin in os.getenv("CORS_ORIGINS", "").split(",")
        if origin.strip()
    ]

    if not cors_origins:
        raise RuntimeError(
            "CORS_ORIGINS must be set when ENVIRONMENT=production."
        )
else:
    cors_origins = [
        "http://127.0.0.1:8000",
        "http://localhost:8000",
    ]


app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)

    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

    return response


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

MAX_IMAGE_BYTES = 10 * 1024 * 1024
MAX_DIAGNOSIS_IMAGES = 5
MAX_TOTAL_DIAGNOSIS_BYTES = 30 * 1024 * 1024

ALLOWED_IMAGE_FORMATS = {
    "JPEG",
    "PNG",
    "WEBP"
}

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


def cleanup_uploaded_files(file_paths):
    """
    Delete temporary uploaded files.
    """

    for file_path in file_paths:

        if os.path.exists(file_path):

            try:
                os.remove(file_path)

            except OSError:
                pass


def embed_result_images(result):
    """
    Replace temporary image paths in the diagnosis result
    with data URLs.

    This allows diagnosis.html to display the images after
    the temporary files have been deleted.
    """

    def convert_path(image_path):

        if not image_path:
            return image_path

        if not os.path.exists(image_path):
            return image_path

        mime_type, _ = mimetypes.guess_type(
            image_path
        )

        if not mime_type:
            mime_type = "application/octet-stream"

        with open(
            image_path,
            "rb"
        ) as image_file:

            encoded = base64.b64encode(
                image_file.read()
            ).decode("ascii")

        return (
            f"data:{mime_type};base64,{encoded}"
        )

    def process(value):

        if isinstance(value, dict):

            processed = {}

            for key, item in value.items():

                if key == "image_path":

                    processed[key] = convert_path(
                        item
                    )

                elif key == "image_paths":

                    processed[key] = [
                        convert_path(path)
                        for path in item
                    ]

                else:

                    processed[key] = process(
                        item
                    )

            return processed

        if isinstance(value, list):

            return [
                process(item)
                for item in value
            ]

        return value

    return process(result)


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


def validate_uploaded_image(
    image_bytes,
    filename
):
    """
    Validate uploaded image size, extension,
    and actual image content.
    """

    if not filename:
        raise HTTPException(
            status_code=400,
            detail="No image filename was provided."
        )

    if not allowed_file(filename):
        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported image format. "
                "Use JPG, JPEG, PNG, or WEBP."
            )
        )

    if not image_bytes:
        raise HTTPException(
            status_code=400,
            detail="The uploaded image is empty."
        )

    if len(image_bytes) > MAX_IMAGE_BYTES:
        raise HTTPException(
            status_code=400,
            detail=(
                "Each image must not exceed 10 MB."
            )
        )

    try:
        with Image.open(
            BytesIO(image_bytes)
        ) as image:

            image.verify()

            image_format = image.format

    except (
        UnidentifiedImageError,
        OSError
    ):
        raise HTTPException(
            status_code=400,
            detail=(
                "The uploaded file is not a valid image."
            )
        )

    if image_format not in ALLOWED_IMAGE_FORMATS:
        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported image format. "
                "Use JPG, JPEG, PNG, or WEBP."
            )
        )

    extension = Path(filename).suffix.lower().lstrip(".")

    expected_format = {
        "jpg": "JPEG",
        "jpeg": "JPEG",
        "png": "PNG",
        "webp": "WEBP",
    }[extension]

    if image_format != expected_format:
        raise HTTPException(
            status_code=400,
            detail=(
                "The file extension does not match "
                "the actual image format."
            )
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

        from knowledge_base.database_postgresql import (
            get_disease_profile
        )

        diagnosis_profile = get_disease_profile(
            health_problem_id
        )

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

    The uploaded image is stored temporarily and deleted
    after prediction.
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

    temp_directory = tempfile.mkdtemp(
        prefix="plant_health_predict_"
    )

    image_path = os.path.join(
        temp_directory,
        f"{uuid.uuid4().hex}{file_extension}"
    )

    try:

        image_bytes = await image.read()

        validate_uploaded_image(
            image_bytes,
            image.filename
        )

        with open(
            image_path,
            "wb"
        ) as file:

            file.write(
                image_bytes
            )

        result = predict_image(
            image_path
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

    except HTTPException:
        raise

    except Exception:

        raise HTTPException(
            status_code=500,
            detail=(
                "Prediction failed. "
                "Please try again with a valid image."
            )
        )

    finally:

        shutil.rmtree(
            temp_directory,
            ignore_errors=True
        )


# ============================================================
# DIAGNOSIS API
# ============================================================

@app.post("/diagnose")
async def diagnose_api(
    image: UploadFile = File(...)
):
    """
    Run the complete maize-health diagnosis pipeline
    and return the result as JSON.

    The uploaded image is stored temporarily and deleted
    after diagnosis.
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

    temp_directory = tempfile.mkdtemp(
        prefix="plant_health_diagnose_"
    )

    image_path = os.path.join(
        temp_directory,
        f"{uuid.uuid4().hex}{file_extension}"
    )

    try:

        image_bytes = await image.read()

        validate_uploaded_image(
            image_bytes,
            image.filename
        )

        with open(
            image_path,
            "wb"
        ) as file:

            file.write(
                image_bytes
            )

        from cnn.database_integration_postgresql import (
            diagnose_from_image
        )

        result = diagnose_from_image(
            image_path
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

    except HTTPException:
        raise

    except Exception as error:
        print(
            "DIAGNOSE_PAGE_ERROR:",
            repr(error)
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Diagnosis failed. One or more uploaded images "
                "could not be processed. Please try again."
            )
        )

    finally:

        shutil.rmtree(
            temp_directory,
            ignore_errors=True
        )


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

    Uploaded images are stored in a temporary directory outside
    static/uploads. Result images are embedded into the response
    as data URLs, then the temporary directory is deleted.
    """

    if not images:

        raise HTTPException(
            status_code=400,
            detail="Please upload at least one image."
        )

    if len(images) > MAX_DIAGNOSIS_IMAGES:

        raise HTTPException(
            status_code=400,
            detail=(
                "You can analyze a maximum of 5 images per case."
            )
        )

    total_bytes = 0

    for image in images:

        if not image.filename:

            raise HTTPException(
                status_code=400,
                detail=(
                    "One of the uploaded files "
                    "has no filename."
                )
            )

    temp_directory = tempfile.mkdtemp(
        prefix="plant_health_web_"
    )

    saved_paths = []

    try:

        for image in images:

            image_bytes = await image.read()

            validate_uploaded_image(
                image_bytes,
                image.filename
            )

            total_bytes += len(image_bytes)

            if total_bytes > MAX_TOTAL_DIAGNOSIS_BYTES:

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
                temp_directory,
                filename
            )

            with open(
                image_path,
                "wb"
            ) as file:

                file.write(
                    image_bytes
                )

            saved_paths.append(
                image_path
            )

        from cnn.database_integration_postgresql import (
            diagnose_from_images
        )

        result = diagnose_from_images(
            saved_paths
        )

        result["image_paths"] = saved_paths

        result = embed_result_images(
            result
        )

        return templates.TemplateResponse(
            request=request,
            name="diagnosis.html",
            context={
                "result": result
            }
        )

    except HTTPException:

        raise

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=(
                "Diagnosis failed. One or more uploaded images "
                "could not be processed. Please upload valid "
                "JPG, JPEG, PNG, or WEBP images."
            )
        )

    finally:

        shutil.rmtree(
            temp_directory,
            ignore_errors=True
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
            None
        )

    except Exception:

        raise HTTPException(
            status_code=500,
            detail=(
                "Chatbot request failed. "
                "Please try again later."
            )
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

    except Exception:

        raise HTTPException(
            status_code=500,
            detail=(
                "Chatbot request failed. "
                "Please try again later."
            )
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

if ENVIRONMENT == "development":

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