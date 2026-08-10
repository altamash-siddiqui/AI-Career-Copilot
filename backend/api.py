from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime

# ============================================================
# FLASK APP
# ============================================================

app = Flask(__name__)
CORS(app)

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

    except Exception:

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
            indent=4
        )


# ============================================================
# HEALTH CHECK
# ============================================================

@app.route("/api/status", methods=["GET"])
def status():

    return jsonify({
        "success": True,
        "message": "AI Career Copilot API is running 🚀",
        "system": "online"
    })


# ============================================================
# REGISTER
# ============================================================

@app.route("/api/register", methods=["POST"])
def register():

    data = request.get_json(silent=True) or {}

    username = str(
        data.get("username", "")
    ).strip()

    password = str(
        data.get("password", "")
    ).strip()

    if not username or not password:

        return jsonify({
            "success": False,
            "message": "Username and password are required."
        }), 400

    users = load_json(
        USERS_FILE,
        []
    )

    if not isinstance(users, list):

        users = []

    for user in users:

        if (
            str(user.get("name", "")).lower()
            ==
            username.lower()
        ):

            return jsonify({
                "success": False,
                "message": "Username already exists."
            }), 409

    users.append({
        "name": username,
        "password": password
    })

    save_json(
        USERS_FILE,
        users
    )

    return jsonify({
        "success": True,
        "message": "Registration successful.",
        "username": username
    })


# ============================================================
# LOGIN
# ============================================================

@app.route("/api/login", methods=["POST"])
def login():

    data = request.get_json(silent=True) or {}

    username = str(
        data.get("username", "")
    ).strip()

    password = str(
        data.get("password", "")
    ).strip()

    if not username or not password:

        return jsonify({
            "success": False,
            "message": "Username and password are required."
        }), 400

    users = load_json(
        USERS_FILE,
        []
    )

    if not isinstance(users, list):

        users = []

    for user in users:

        if (
            str(user.get("name", "")).lower()
            ==
            username.lower()
            and
            str(user.get("password", ""))
            ==
            password
        ):

            return jsonify({
                "success": True,
                "message": f"Welcome back, {username}!",
                "username": user.get("name")
            })

    return jsonify({
        "success": False,
        "message": "Invalid username or password."
    }), 401


# ============================================================
# USER DASHBOARD
# ============================================================

@app.route("/api/dashboard/<username>", methods=["GET"])
def dashboard(username):

    username = username.strip()

    careers = load_json(
        DATA_FILE,
        []
    )

    if not isinstance(careers, list):

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

            user_records.append(record)

    if not user_records:

        return jsonify({
            "success": True,
            "username": username,
            "has_career": False,
            "message": "No career selected yet.",
            "careers": []
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

    total_steps = len(roadmap)

    completed_count = len(
        completed_steps
    )

    if total_steps > 0:

        progress = int(
            (
                completed_count
                /
                total_steps
            ) * 100
        )

    else:

        progress = int(
            current.get(
                "progress",
                0
            )
        )

    return jsonify({
        "success": True,
        "username": username,
        "has_career": True,

        "career": career.title(),

        "progress": progress,

        "favorite": bool(
            current.get(
                "favorite",
                False
            )
        ),

        "completed_steps": completed_steps,

        "total_steps": total_steps,

        "remaining_steps": max(
            0,
            total_steps - completed_count
        ),

        "roadmap": roadmap,

        "timestamp": current.get(
            "timestamp",
            ""
        )
    })


# ============================================================
# CAREER ROADMAP
# ============================================================

@app.route("/api/roadmap/<career>", methods=["GET"])
def roadmap(career):

    career = career.strip().lower()

    steps = ROADMAPS.get(
        career,
        []
    )

    if not steps:

        return jsonify({
            "success": False,
            "message": "Career roadmap not available."
        }), 404

    return jsonify({
        "success": True,
        "career": career.title(),
        "steps": steps,
        "total_steps": len(steps)
    })


# ============================================================
# SELECT / SAVE CAREER
# ============================================================

@app.route("/api/career", methods=["POST"])
def select_career():

    data = request.get_json(silent=True) or {}

    username = str(
        data.get("username", "")
    ).strip()

    career = str(
        data.get("career", "")
    ).strip().lower()

    if not username or not career:

        return jsonify({
            "success": False,
            "message": "Username and career are required."
        }), 400

    if career not in ROADMAPS:

        return jsonify({
            "success": False,
            "message": "Career roadmap not available."
        }), 400

    careers = load_json(
        DATA_FILE,
        []
    )

    if not isinstance(careers, list):

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

    # --------------------------------------------------------
    # UPDATE EXISTING CAREER
    # --------------------------------------------------------

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

        existing["timestamp"] = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    # --------------------------------------------------------
    # CREATE NEW CAREER
    # --------------------------------------------------------

    else:

        careers.append({

            "name": username,

            "career": career,

            "user": username,

            "progress": 0,

            "favorite": False,

            "completed_steps": [],

            "timestamp": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

        })

    save_json(
        DATA_FILE,
        careers
    )

    return jsonify({
        "success": True,
        "message": "Career saved successfully.",
        "username": username,
        "career": career.title(),
        "progress": 0
    })


# ============================================================
# COMPLETE ROADMAP STEP
# ============================================================

@app.route("/api/complete-step", methods=["POST"])
def complete_step():

    data = request.get_json(silent=True) or {}

    username = str(
        data.get("username", "")
    ).strip()

    step = str(
        data.get("step", "")
    ).strip()

    if not username or not step:

        return jsonify({
            "success": False,
            "message": "Username and step are required."
        }), 400

    careers = load_json(
        DATA_FILE,
        []
    )

    if not isinstance(careers, list):

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
            "success": False,
            "message": "Career record not found."
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

    if step not in roadmap_steps:

        return jsonify({
            "success": False,
            "message": "Invalid roadmap step."
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
            "success": False,
            "message": "This step is already completed."
        }), 409

    completed_steps.append(
        step
    )

    selected["completed_steps"] = completed_steps

    total_steps = len(
        roadmap_steps
    )

    progress = int(
        (
            len(completed_steps)
            /
            total_steps
        ) * 100
    )

    selected["progress"] = progress

    save_json(
        DATA_FILE,
        careers
    )

    return jsonify({

        "success": True,

        "message": "Roadmap step completed.",

        "step": step,

        "progress": progress,

        "completed_steps": completed_steps,

        "remaining_steps": max(
            0,
            total_steps - len(completed_steps)
        )

    })


# ============================================================
# CAREER HISTORY
# ============================================================

@app.route("/api/history/<username>", methods=["GET"])
def history(username):

    username = username.strip()

    careers = load_json(
        DATA_FILE,
        []
    )

    if not isinstance(careers, list):

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

            user_records.append(record)

    return jsonify({
        "success": True,
        "username": username,
        "count": len(user_records),
        "careers": user_records
    })


# ============================================================
# RUN SERVER
# ============================================================

if __name__ == "__main__":

    print("=" * 50)
    print("       AI CAREER COPILOT API")
    print("=" * 50)
    print("API Server: http://127.0.0.1:5000")
    print("Status: ONLINE 🚀")
    print("=" * 50)

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )