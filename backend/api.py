from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename

import json
import os

from datetime import datetime
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

from services.resume_service import resume_service
from resume_manager import ResumeManager
from resume_optimizer import ResumeOptimizer

# ============================================================
# DAY 33 - CAREER INTELLIGENCE
# ============================================================
from career_intelligence import register_day33_routes

# ============================================================
# DAY 31 - ATS JOB MATCHER
# ============================================================

from job_matcher import match_resume_to_job


# ============================================================
# FLASK APP
# ============================================================

app = Flask(__name__)

CORS(app)

# Maximum upload size: 10 MB
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024


# ============================================================
# FILE PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

USERS_FILE = os.path.join(
    BASE_DIR,
    "users.json"
)

DATA_FILE = os.path.join(
    BASE_DIR,
    "career_data.json"
)


# ============================================================
# RESUME CONFIGURATION
# ============================================================

RESUME_UPLOAD_DIR = os.path.join(
    BASE_DIR,
    "uploads",
    "resumes"
)

os.makedirs(
    RESUME_UPLOAD_DIR,
    exist_ok=True
)

OPTIMIZED_RESUME_DIR = os.path.join(
    RESUME_UPLOAD_DIR,
    "optimized"
)
os.makedirs(
    OPTIMIZED_RESUME_DIR,
    exist_ok=True
)

resume_optimizer = ResumeOptimizer()


ALLOWED_RESUME_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".txt"
}


resume_manager = ResumeManager()


# ============================================================
# CAREER ROADMAPS
# ============================================================

ROADMAPS = {

    "ai": [
        "Learn Python",
        "Learn Machine Learning",
        "Build AI Projects"
    ],

    "web": [
        "Learn HTML",
        "Learn CSS",
        "Learn JavaScript"
    ],

    "python": [
        "Learn Python Basics",
        "Learn Object-Oriented Programming",
        "Build Python Projects"
    ],

    "data science": [
        "Learn Python",


        "Learn Pandas",


        "Learn SQL"
    ]
}


# ============================================================
# JSON HELPERS
# ============================================================

def load_json(file_path, default):

    try:

        if not os.path.exists(file_path):
            return default

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        return data

    except Exception as e:

        print(
            f"JSON load error: {e}"
        )

        return default


def save_json(file_path, data):

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )


# ============================================================
# HEALTH CHECK
# ============================================================

@app.route(
    "/api/status",
    methods=["GET"]
)
def status():

    return jsonify({

        "success": True,

        "message":
            "AI Career Copilot API is running ■",

        "system":
            "online"

    })


# ============================================================
# REGISTER
# ============================================================

@app.route(
    "/api/register",
    methods=["POST"]
)
def register():

    data = request.get_json(
        silent=True
    ) or {}

    username = str(
        data.get(
            "username",
            ""
        )
    ).strip()

    password = str(
        data.get(
            "password",
            ""
        )
    ).strip()

    if not username or not password:
        return jsonify({


            "success": False,

            "message":
                "Username and password are required."

        }), 400

    users = load_json(
        USERS_FILE,
        []
    )

    if not isinstance(
        users,
        list
    ):

        users = []

    for user in users:

        saved_username = str(
            user.get(
                "name",
                ""
            )
        ).strip()

        if (
            saved_username.lower()
            ==
            username.lower()
        ):

            return jsonify({

                "success": False,

                "message":
                    "Username already exists."

            }), 409

    users.append({

        "name":
            username,

        "password":
            password

    })

    save_json(
        USERS_FILE,
        users
    )

    return jsonify({

        "success":
            True,

        "message":
            "Registration successful.",

        "username":
            username

    })


# ============================================================
# LOGIN
# ============================================================

@app.route(
    "/api/login",
    methods=["POST"]
)
def login():

    data = request.get_json(
        silent=True
    ) or {}

    username = str(
        data.get(
            "username",
            ""
        )
    ).strip()

    password = str(
        data.get(
            "password",
            ""
        )
    ).strip()

    if not username or not password:

        return jsonify({


            "success": False,

            "message":
                "Username and password are required."

        }), 400

    users = load_json(
        USERS_FILE,
        []
    )

    if not isinstance(
        users,
        list
    ):

        users = []

    for user in users:

        saved_username = str(
            user.get(
                "name",
                ""
            )
        ).strip()

        saved_password = str(
            user.get(
                "password",
                ""
            )
        )

        if (
            saved_username.lower()
            ==
            username.lower()
            and
            saved_password
            ==
            password
        ):

            return jsonify({

                "success":
                    True,

                "message":
                    f"Welcome back, {saved_username}!",

                "username":
                    saved_username

            })

    return jsonify({

        "success":
            False,

        "message":
            "Invalid username or password."

    }), 401


# ============================================================
# DASHBOARD
# ============================================================

@app.route(
    "/api/dashboard/<username>",
    methods=["GET"]
)
def dashboard(username):

    username = username.strip()

    careers = load_json(
        DATA_FILE,
        []
    )

    if not isinstance(
        careers,
        list
    ):

        careers = []

    user_records = []

    for record in careers:

        record_user = record.get(
            "user",
            record.get(
                "name",
                ""
            )
        )


        if (
            str(record_user).lower()
            ==
            username.lower()
        ):

            user_records.append(
                record
            )

    if not user_records:

        return jsonify({

            "success":
                True,

            "username":
                username,

            "has_career":
                False,

            "message":
                "No career selected yet.",

            "careers":
                []

        })

    current = user_records[-1]

    career = str(
        current.get(
            "career",
            ""
        )
    ).lower()

    completed_steps = current.get(
        "completed_steps",
        []
    )

    if not isinstance(
        completed_steps,
        list
    ):

        completed_steps = []

    roadmap = ROADMAPS.get(
        career,
        []
    )

    total_steps = len(
        roadmap
    )

    valid_completed_steps = [

        step

        for step in completed_steps

        if step in roadmap

    ]

    completed_count = len(
        valid_completed_steps
    )

    if total_steps > 0:

        progress = int(

            (
                    completed_count
                    /
                    total_steps
            )
            *
            100

        )

    else:

        progress = int(
            current.get(
                "progress",
                0
            )
        )

    return jsonify({

        "success":
            True,

        "username":


            username,


        "has_career":
            True,

        "career":
            career.title(),

        "progress":
            progress,

        "favorite":
            bool(
                current.get(
                    "favorite",
                    False
                )
            ),

        "completed_steps":
            valid_completed_steps,

        "total_steps":
            total_steps,

        "remaining_steps":
            max(
                0,
                total_steps
                -
                completed_count
            ),

        "roadmap":
            roadmap,

        "timestamp":
            current.get(
                "timestamp",
                ""
            )

    })


# ============================================================
# CAREER ROADMAP
# ============================================================

@app.route(
    "/api/roadmap/<career>",
    methods=["GET"]
)
def roadmap(career):

    career = career.strip().lower()

    steps = ROADMAPS.get(
        career,
        []
    )

    if not steps:

        return jsonify({

            "success":
                False,

            "message":
                "Career roadmap not available."

        }), 404

    return jsonify({

        "success":
            True,

        "career":
            career.title(),

        "steps":
            steps,

        "total_steps":
            len(steps)

    })


# ============================================================
# SELECT / SAVE CAREER
# ============================================================

@app.route(
    "/api/career",
    methods=["POST"]
)
def select_career():

    data = request.get_json(
        silent=True
    ) or {}

    username = str(


        data.get(
            "username",
            ""
        )
    ).strip()

    career = str(
        data.get(
            "career",
            ""
        )
    ).strip().lower()

    if not username or not career:

        return jsonify({

            "success":
                False,

            "message":
                "Username and career are required."

        }), 400

    if career not in ROADMAPS:

        return jsonify({

            "success":
                False,

            "message":
                "Career roadmap not available."

        }), 400

    careers = load_json(
        DATA_FILE,
        []
    )

    if not isinstance(
        careers,
        list
    ):

        careers = []

    existing = None

    for record in careers:

        record_user = record.get(
            "user",
            record.get(
                "name",
                ""
            )
        )

        if (
            str(record_user).lower()
            ==
            username.lower()
        ):

            existing = record

            break

    if existing:

        existing["career"] = career

        existing["user"] = username

        existing["name"] = username

        existing["progress"] = 0

        existing["completed_steps"] = []

        existing["favorite"] = bool(
            existing.get(
                "favorite",
                False
            )
        )

        existing["timestamp"] = (
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        )

    else:

        careers.append({

            "name":
                username,

            "career":


                career,


            "user":
                username,

            "progress":
                0,

            "favorite":
                False,

            "completed_steps":
                [],

            "timestamp":
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )

        })

    save_json(
        DATA_FILE,
        careers
    )

    return jsonify({

        "success":
            True,

        "message":
            "Career saved successfully.",

        "username":
            username,

        "career":
            career.title(),

        "progress":
            0

    })


# ============================================================
# COMPLETE ROADMAP STEP
# ============================================================

@app.route(
    "/api/complete-step",
    methods=["POST"]
)
def complete_step():

    data = request.get_json(
        silent=True
    ) or {}

    username = str(
        data.get(
            "username",
            ""
        )
    ).strip()

    step = str(
        data.get(
            "step",
            ""
        )
    ).strip()

    if not username or not step:

        return jsonify({

            "success":
                False,

            "message":
                "Username and step are required."

        }), 400

    careers = load_json(
        DATA_FILE,
        []
    )

    if not isinstance(
        careers,
        list
    ):

        careers = []

    selected = None

    for record in careers:

        record_user = record.get(
            "user",
            record.get(
                "name",


                ""
            )
        )

        if (
            str(record_user).lower()
            ==
            username.lower()
        ):

            selected = record

            break

    if not selected:

        return jsonify({

            "success":
                False,

            "message":
                "Career record not found."

        }), 404

    career = str(
        selected.get(
            "career",
            ""
        )
    ).lower()

    roadmap_steps = ROADMAPS.get(
        career,
        []
    )

    if not roadmap_steps:

        return jsonify({

            "success":
                False,

            "message":
                "Career roadmap not found."

        }), 404

    if step not in roadmap_steps:

        return jsonify({

            "success":
                False,

            "message":
                "Invalid roadmap step."

        }), 400

    completed_steps = selected.get(
        "completed_steps",
        []
    )

    if not isinstance(
        completed_steps,
        list
    ):

        completed_steps = []

    if step in completed_steps:

        return jsonify({

            "success":
                False,

            "message":
                "This step is already completed."

        }), 409

    completed_steps.append(
        step
    )

    selected[
        "completed_steps"
    ] = completed_steps

    total_steps = len(
        roadmap_steps
    )

    progress = int(

        (
            len(completed_steps)
            /
            total_steps


        )


        *
        100

    )

    selected[
        "progress"
    ] = progress

    save_json(
        DATA_FILE,
        careers
    )

    return jsonify({

        "success":
            True,

        "message":
            "Roadmap step completed.",

        "step":
            step,

        "progress":
            progress,

        "completed_steps":
            completed_steps,

        "remaining_steps":
            max(
                0,
                total_steps
                -
                len(completed_steps)
            )

    })


# ============================================================
# CAREER HISTORY
# ============================================================

@app.route(
    "/api/history/<username>",
    methods=["GET"]
)
def history(username):

    username = username.strip()

    careers = load_json(
        DATA_FILE,
        []
    )

    if not isinstance(
        careers,
        list
    ):

        careers = []

    user_records = []

    for record in careers:

        record_user = record.get(
            "user",
            record.get(
                "name",
                ""
            )
        )

        if (
            str(record_user).lower()
            ==
            username.lower()
        ):

            user_records.append(
                record
            )

    return jsonify({

        "success":
            True,

        "username":
            username,

        "count":
            len(user_records),

        "careers":
            user_records

    })


# ============================================================
# RESUME UPLOAD + ANALYSIS
# ============================================================

@app.route(
    "/api/resume/analyze",
    methods=["POST"]
)
def analyze_resume():

    try:

        username = str(
            request.form.get(
                "username",
                ""
            )
        ).strip()

        if not username:

            return jsonify({

                "success":
                    False,

                "message":
                    "Username is required."

            }), 400

        if "resume" not in request.files:

            return jsonify({

                "success":
                    False,

                "message":
                    "Please upload a resume."

            }), 400

        resume_file = request.files[
            "resume"
        ]

        if not resume_file.filename:

            return jsonify({

                "success":
                    False,

                "message":
                    "No resume file selected."

            }), 400

        original_filename = (
            resume_file.filename
        )

        extension = os.path.splitext(
            original_filename
        )[1].lower()

        if (
            extension
            not in
            ALLOWED_RESUME_EXTENSIONS
        ):

            return jsonify({

                "success":
                    False,

                "message":
                    "Unsupported file format. "
                    "Only PDF, DOCX and TXT are allowed."

            }), 400

        safe_filename = secure_filename(
            original_filename
        )

        if not safe_filename:

            return jsonify({

                "success":
                    False,

                "message":
                    "Invalid resume filename."

            }), 400

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S_%f"
        )
        filename_without_extension = (


            os.path.splitext(
                safe_filename
            )[0]
        )

        final_filename = (

            f"{username}_"
            f"{timestamp}_"
            f"{filename_without_extension}"
            f"{extension}"

        )

        file_path = os.path.join(
            RESUME_UPLOAD_DIR,
            final_filename
        )

        resume_file.save(
            file_path
        )

        analysis = resume_service.analyze_resume(
            file_path
        )

        resume_manager.save_analysis(

            username=username,

            resume_name=final_filename,

            detected_name=analysis.get(
                "name",
                ""
            ),

            email=analysis.get(
                "email",
                ""
            ),

            phone=analysis.get(
                "phone",
                ""
            ),

            skills=analysis.get(
                "skills",
                []
            ),

            sections=analysis.get(
                "sections",
                []
            ),

            strength_score=analysis.get(
                "resume_strength_score",
                0
            ),

            ats_score=analysis.get(
                "ats_score",
                0
            )

        )

        analysis_payload = dict(
            analysis
        )

        analysis_payload[
            "resume_file"
        ] = final_filename

        return jsonify({

            "success":
                True,

            "message":
                "Resume analyzed successfully.",

            "username":
                username,

            "resume_file":
                final_filename,

            "analysis":
                analysis_payload

        }), 200

    except Exception as e:

        print(
            f"Resume analysis error: {e}"
        )

        return jsonify({


            "success":
                False,

            "message":
                f"Resume analysis failed: {str(e)}"

        }), 500


# ============================================================
# DAY 31
# ATS JOB MATCHING ENGINE
# ============================================================

def extract_resume_text_for_job_match(file_path):
    """Extract resume text for the ATS job matching engine."""

    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".pdf":
        try:
            import PyPDF2
        except ImportError as error:
            raise ImportError(
                "PyPDF2 is required for PDF job matching. Run: pip install PyPDF2"
            ) from error

        text_parts = []

        with open(file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)

            for page in reader.pages:
                try:
                    text_parts.append(page.extract_text() or "")
                except Exception:
                    continue

        return "\n".join(text_parts).strip()

    if extension == ".docx":
        try:
            from docx import Document
        except ImportError as error:
            raise ImportError(
                "python-docx is required for DOCX job matching. Run: pip install python-docx"
            ) from error

        document = Document(file_path)
        parts = []

        for paragraph in document.paragraphs:
            if paragraph.text.strip():
                parts.append(paragraph.text.strip())

        for table in document.tables:
            for row in table.rows:
                values = [
                    cell.text.strip()
                    for cell in row.cells
                    if cell.text.strip()
                ]
                if values:
                    parts.append(" ".join(values))

        return "\n".join(parts).strip()

    if extension == ".txt":
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read().strip()
        except UnicodeDecodeError:
            with open(file_path, "r", encoding="latin-1") as file:
                return file.read().strip()

    raise ValueError(
        "Unsupported resume format. Use PDF, DOCX or TXT."
    )


@app.route(
    "/api/job-match",
    methods=["POST"]
)
def job_match():

    try:

        data = request.get_json(
            silent=True
        ) or {}

        username = str(
            data.get(
                "username",
                ""
            )
        ).strip()

        job_description = str(
            data.get(
                "job_description",
                ""
            )


        ).strip()


        resume_text = str(
            data.get(
                "resume_text",
                ""
            )
        ).strip()

        resume_file = str(
            data.get(
                "resume_file",
                ""
            )
        ).strip()

        # --------------------------------------------------------
        # VALIDATION
        # --------------------------------------------------------

        if not job_description:

            return jsonify({

                "success": False,

                "message":
                    "Job description is required."

            }), 400

        if len(job_description) < 30:

            return jsonify({

                "success": False,

                "message":
                    "Job description is too short. Paste the complete job description."

            }), 400

        # --------------------------------------------------------
        # RESUME TEXT SOURCE
        # --------------------------------------------------------
        # Preferred browser flow: the frontend sends the filename
        # returned by /api/resume/analyze. The server extracts the
        # original resume text locally, so the browser never needs
        # to expose the full resume text.

        if not resume_text and resume_file:

            safe_resume_file = os.path.basename(
                resume_file
            )

            file_path = os.path.join(
                RESUME_UPLOAD_DIR,
                safe_resume_file
            )

            if not os.path.isfile(file_path):

                return jsonify({

                    "success": False,

                    "message":
                        "The analyzed resume file could not be found. Please analyze the resume again."

                }), 404

            resume_text = extract_resume_text_for_job_match(
                file_path
            )

        if not resume_text:

            return jsonify({

                "success": False,

                "message":
                    "No resume text available. Analyze a resume first."

            }), 400

        # --------------------------------------------------------
        # MATCH ENGINE
        # --------------------------------------------------------

        result = match_resume_to_job(
            resume_text,
            job_description
        )

        # --------------------------------------------------------
        # RESPONSE
        # --------------------------------------------------------

        return jsonify({

            "success": True,

            "username": username,


            "resume_file": resume_file,

            "job_description_length": len(job_description),

            "job_match": result.get(
                "job_match",
                {}
            ),

            "scores": result.get(
                "scores",
                {}
            ),

            "skills": result.get(
                "skills",
                {}
            ),

            "keywords": result.get(
                "keywords",
                {}
            ),

            "experience": result.get(
                "experience",
                {}
            ),

            "analysis": result.get(
                "analysis",
                {}
            ),

            "summary": result.get(
                "summary",
                {}
            )

        }), 200

    except Exception as e:

        print(
            f"Job matching error: {e}"
        )

        return jsonify({

            "success": False,

            "message":
                f"Job matching failed: {str(e)}"

        }), 500


# ============================================================
# DAY 32 - RESUME OPTIMIZATION
# ============================================================

@app.route(
    "/api/resume/optimize",
    methods=["POST"]
)
def optimize_resume():

    try:

        username = str(
            request.form.get(
                "username",
                "user"
            )
        ).strip() or "user"

        target_role = str(
            request.form.get(
                "target_role",
                ""
            )
        ).strip()

        job_description = str(
            request.form.get(
                "job_description",
                ""
            )
        ).strip()

        resume_file = request.files.get(
            "resume"
        )

        # --------------------------------------------------------
        # VALIDATION
        # --------------------------------------------------------

        if not resume_file:
            return jsonify({
                "success": False,
                "message": "Resume file is required."
            }), 400

        original_filename = secure_filename(
            resume_file.filename or "resume"
        )

        if not original_filename:
            original_filename = "resume"

        extension = os.path.splitext(
            original_filename
        )[1].lower()

        if extension not in ALLOWED_RESUME_EXTENSIONS:
            return jsonify({
                "success": False,
                "message":
                    "Unsupported resume format. "
                    "Use PDF, DOCX or TXT."
            }), 400

        # --------------------------------------------------------
        # SAVE ORIGINAL RESUME
        # --------------------------------------------------------

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S_%f"
        )

        saved_name = (
            f"{username}_{timestamp}_{original_filename}"
        )

        original_path = os.path.join(
            RESUME_UPLOAD_DIR,
            saved_name
        )

        resume_file.save(
            original_path
        )

        # --------------------------------------------------------
        # ANALYZE RESUME
        # --------------------------------------------------------
        # ResumeOptimizer needs the same analysis data
        # that the normal /api/resume/analyze endpoint produces.

        analysis = resume_service.analyze_resume(
            original_path
        )

        if not isinstance(
            analysis,
            dict
        ):
            analysis = {}

        # --------------------------------------------------------
        # DETECT TARGET ROLE IF FRONTEND DID NOT SEND ONE
        # --------------------------------------------------------

        if not target_role:

            target_role = (
                resume_optimizer.detect_target_role(
                    analysis=analysis,
                    job_description=job_description
                )
            )

        # --------------------------------------------------------
        # OPTIMIZE
        # --------------------------------------------------------

        result = resume_optimizer.optimize(
            original_text=(
                resume_service.analyzer.extract_text(
                    original_path
                )
            ),
            analysis=analysis,
            target_role=target_role,
            job_description=job_description
        )

        if not result.get("success"):
            return jsonify(result), 400

        # --------------------------------------------------------
        # ADD FILE / USER INFORMATION
        # --------------------------------------------------------

        result["username"] = username

        result["original_filename"] = (
            original_filename
        )

        result["stored_original_filename"] = (
            saved_name
        )

        result["resume_file"] = saved_name

        result["analysis"] = analysis

        # --------------------------------------------------------
        # RESPONSE
        # --------------------------------------------------------

        return jsonify(
            result
        ), 200

    except Exception as error:

        print(
            f"Resume optimization error: {error}"
        )

        return jsonify({

            "success": False,

            "message":
                f"Resume optimization failed: {error}"

        }), 500
        
# ============================================================
# DAY 32 - APPROVE OPTIMIZED RESUME
# ============================================================

@app.route(
    "/api/resume/optimize/approve",
    methods=["POST"]
)
def approve_optimized_resume():

    try:

        data = request.get_json(
            silent=True
        ) or {}

        # --------------------------------------------------------
        # GET DATA
        # --------------------------------------------------------

        username = str(
            data.get(
                "username",
                "user"
            )
        ).strip() or "user"

        optimized_text = str(
            data.get(
                "optimized_text",
                ""
            )
        ).strip()

        original_filename = str(
            data.get(
                "original_filename",
                "resume.txt"
            )
        ).strip() or "resume.txt"

        # --------------------------------------------------------
        # VALIDATION
        # --------------------------------------------------------

        if not optimized_text:

            return jsonify({

                "success": False,

                "message":
                    "Optimized resume text is required."

            }), 400

        # --------------------------------------------------------
        # SAVE APPROVED COPY
        # --------------------------------------------------------

        saved_filename = (
            resume_optimizer.save_approved_copy(

                optimized_text=optimized_text,

                original_filename=original_filename,

                username=username,

                output_directory=OPTIMIZED_RESUME_DIR

            )
        )

        optimized_path = os.path.join(
            OPTIMIZED_RESUME_DIR,
            saved_filename
        )

        # --------------------------------------------------------
        # RESPONSE
        # --------------------------------------------------------

        return jsonify({

            "success": True,

            "message":
                "Optimized resume approved and saved successfully.",

            "username":
                username,

            "original_filename":
                original_filename,

            "optimized_filename":
                saved_filename,

            "optimized_resume":
                optimized_text,

            "file_path":
                optimized_path

        }), 200

    except Exception as error:

        print(
            f"Resume approval error: {error}"
        )

        return jsonify({

            "success": False,

            "message":
                f"Unable to save approved resume: {str(error)}"

        }), 500


# ============================================================
# RESUME HISTORY
# ============================================================

@app.route(
    "/api/resume/history/<username>",
    methods=["GET"]
)
def resume_history(username):

    try:

        username = username.strip()

        if not username:

            return jsonify({

                "success":
                    False,

                "message":
                    "Username is required."

            }), 400

        history = (
            resume_manager.get_user_resume_history(
                username
            )
        )

        return jsonify({

            "success":
                True,

            "username":
                username,

            "count":
                len(history),

            "history":
                history

        }), 200


    except Exception as e:

        return jsonify({

            "success":
                False,

            "message":
                f"Unable to load resume history: {str(e)}"

        }), 500


# ============================================================
# LATEST RESUME ANALYSIS
# ============================================================

@app.route(
    "/api/resume/latest/<username>",
    methods=["GET"]
)
def latest_resume(username):

    try:

        username = username.strip()

        if not username:

            return jsonify({

                "success":
                    False,

                "message":
                    "Username is required."

            }), 400

        latest = (
            resume_manager.get_latest_analysis(
                username
            )
        )

        if latest is None:

            return jsonify({

                "success":
                    True,

                "username":
                    username,

                "has_analysis":
                    False,

                "analysis":
                    None

            }), 200

        return jsonify({

            "success":
                True,

            "username":
                username,

            "has_analysis":
                True,

            "analysis":
                latest

        }), 200

    except Exception as e:

        return jsonify({

            "success":
                False,

            "message":
                f"Unable to load latest analysis: {str(e)}"

        }), 500


# ============================================================
# DAY 33 - CAREER INTELLIGENCE ROUTES
# ============================================================
# Uses the same ResumeManager instance as the existing resume
# analysis endpoints, so Day 33 reads the latest resume analysis.
register_day33_routes(
    app,
    resume_manager
)




# ============================================================
# DAY 34 - YOUTUBE STUDY MATERIAL
# ============================================================

YOUTUBE_API_KEY = os.getenv(
    "YOUTUBE_API_KEY",
    ""
).strip()


@app.route(
    "/api/youtube/search",
    methods=["GET"]
)
def youtube_search():

    skill = str(
        request.args.get(
            "skill",
            ""
        )
    ).strip()

    if not skill:
        return jsonify({
            "success": False,
            "message": "Skill is required."
        }), 400

    query = (
        f"{skill} tutorial course for beginners"
    )

    # No API key: keep the product usable and return a safe YouTube search
    # URL. The frontend opens this immediately, so users never get blocked.
    if not YOUTUBE_API_KEY:
        return jsonify({
            "success": True,
            "source": "youtube_search_fallback",
            "video_url": (
                "https://www.youtube.com/results?"
                + urlencode({"search_query": query})
            ),
            "message": "YOUTUBE_API_KEY is not configured; using YouTube search."
        }), 200

    params = urlencode({
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": 1,
        "safeSearch": "moderate",
        "key": YOUTUBE_API_KEY
    })

    url = (
        "https://www.googleapis.com/youtube/v3/search?"
        + params
    )

    try:

        req = Request(
            url,
            headers={
                "Accept": "application/json",
                "User-Agent": "AI-Career-Copilot/1.0"
            }
        )

        with urlopen(
            req,
            timeout=8
        ) as response:

            payload = json.loads(
                response.read().decode("utf-8")
            )

        items = payload.get(
            "items",
            []
        )

        if not items:
            return jsonify({
                "success": True,
                "source": "youtube_api",
                "video_url": (
                    "https://www.youtube.com/results?"
                    + urlencode({"search_query": query})
                ),
                "message": "No direct video result found; using YouTube search."
            }), 200

        first = items[0]
        video_id = (
            first.get("id", {})
                .get("videoId", "")
        )
        snippet = first.get(
            "snippet",
            {}
        )

        if not video_id:
            return jsonify({
                "success": True,
                "source": "youtube_api",
                "video_url": (
                    "https://www.youtube.com/results?"
                    + urlencode({"search_query": query})
                )
            }), 200

        return jsonify({
            "success": True,
            "source": "youtube_api",
            "video_url":
                f"https://www.youtube.com/watch?v={video_id}",
            "video_id": video_id,
            "title": snippet.get("title", ""),
            "channel": snippet.get("channelTitle", "")
        }), 200

    except (HTTPError, URLError, TimeoutError, ValueError) as error:

        return jsonify({
            "success": True,
            "source": "youtube_search_fallback",
            "video_url": (
                "https://www.youtube.com/results?"
                + urlencode({"search_query": query})
            ),
            "message":
                f"YouTube API unavailable; using search fallback: {str(error)}"
        }), 200


# ============================================================
# FILE TOO LARGE
# ============================================================

@app.errorhandler(413)
def file_too_large(error):

    return jsonify({

        "success":
            False,
        "message":


            "Resume file is too large. Maximum allowed size is 10 MB."

    }), 413


# ============================================================
# ERROR HANDLER - 404
# ============================================================

@app.errorhandler(404)
def page_not_found(error):

    return jsonify({

        "success":
            False,

        "message":
            "API endpoint not found.",

        "available_endpoints": [

            "/api/status",

            "/api/register",

            "/api/login",

            "/api/dashboard/<username>",

            "/api/roadmap/<career>",

            "/api/career",

            "/api/complete-step",

            "/api/history/<username>",

            "/api/resume/analyze",
            "/api/resume/optimize",
            "/api/resume/optimize/approve",

            "/api/job-match",

            "/api/resume/history/<username>",

            "/api/resume/latest/<username>",

            "/api/career-intelligence/<username>",

            "/api/career-intelligence/saved/<username>",

            "/api/career-intelligence/careers",

            "/api/youtube/search?skill=<skill>"

        ]

    }), 404


# ============================================================
# ERROR HANDLER - SERVER ERROR
# ============================================================

@app.errorhandler(500)
def internal_server_error(error):

    return jsonify({

        "success":
            False,

        "message":
            "Internal server error."

    })


# ============================================================
# RUN SERVER
# ============================================================

if __name__ == "__main__":

    print("=" * 50)

    print(
        "         AI CAREER COPILOT API"
    )

    print("=" * 50)

    print(
        "API Server: http://127.0.0.1:5000"
    )

    print(
        "Status: ONLINE ■"
    )

    print("=" * 50)

    print(
        "Resume Upload: ENABLED"
    )

    print(
        "Supported: PDF | DOCX | TXT"
    )

    print(
        "Maximum Upload: 10 MB"
    )


    print("=" * 50)

    print(
        "YouTube Study Material: ENABLED"
    )

    print(
        "Endpoint: GET /api/youtube/search?skill=<skill>"
    )

    print(
        "YouTube API Key: " + ("CONFIGURED" if YOUTUBE_API_KEY else "OPTIONAL / FALLBACK")
    )

    print(
        "ATS Job Matching: ENABLED"
    )

    print(
        "Endpoint: POST /api/job-match"
    )

    print("=" * 50)

    app.run(

        host="127.0.0.1",

        port=5000,

        debug=True

    )