from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename

import json
import os

from datetime import datetime

from services.resume_service import resume_service
from resume_manager import ResumeManager


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
            "AI Career Copilot API is running 🚀",

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

    # ========================================================
    # NO CAREER
    # ========================================================

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

    # ========================================================
    # CURRENT CAREER
    # ========================================================

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

    # ========================================================
    # UPDATE EXISTING CAREER
    # ========================================================

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

    # ========================================================
    # CREATE NEW CAREER
    # ========================================================

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

        # ----------------------------------------------------
        # USERNAME
        # ----------------------------------------------------

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

        # ----------------------------------------------------
        # FILE CHECK
        # ----------------------------------------------------

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

        # ----------------------------------------------------
        # FILE EXTENSION
        # ----------------------------------------------------

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

        # ----------------------------------------------------
        # SECURE FILE NAME
        # ----------------------------------------------------

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

        # ----------------------------------------------------
        # UNIQUE FILE NAME
        # ----------------------------------------------------

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

        # ----------------------------------------------------
        # SAVE FILE
        # ----------------------------------------------------

        resume_file.save(
            file_path
        )

        # ----------------------------------------------------
        # ANALYZE RESUME
        # ----------------------------------------------------

        analysis = resume_service.analyze_resume(file_path)

        # ----------------------------------------------------
        # SAVE ANALYSIS
        # ----------------------------------------------------

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

        # ----------------------------------------------------
        # RESPONSE
        # ----------------------------------------------------

        # Return the complete analyzer payload so the frontend can
        # render all available resume intelligence data.
        analysis_payload = dict(analysis)
        analysis_payload["resume_file"] = final_filename

        return jsonify({
            "success": True,
            "message": "Resume analyzed successfully.",
            "username": username,
            "resume_file": final_filename,
            "analysis": analysis_payload
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

            "/api/resume/history/<username>",

            "/api/resume/latest/<username>"

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

    }), 500


# ============================================================
# RUN SERVER
# ============================================================

if __name__ == "__main__":

    print("=" * 50)

    print(
        "       AI CAREER COPILOT API"
    )

    print("=" * 50)

    print(
        "API Server: http://127.0.0.1:5000"
    )

    print(
        "Status: ONLINE 🚀"
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

    app.run(

        host="127.0.0.1",

        port=5000,

        debug=True

    )