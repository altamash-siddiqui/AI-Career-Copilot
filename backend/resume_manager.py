import json
import os
from datetime import datetime


class ResumeManager:

    # ============================================================
    # INITIALIZATION
    # ============================================================

    def __init__(self):

        base_dir = os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        )

        self.resume_data_file = os.path.join(
            base_dir,
            "resume_analysis.json"
        )

    # ============================================================
    # LOAD DATA
    # ============================================================

    def load_resume_data(self):

        try:

            if not os.path.exists(
                self.resume_data_file
            ):

                return []

            with open(
                self.resume_data_file,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

            if not isinstance(data, list):

                return []

            return data

        except Exception as e:

            print(
                f"❌ Error loading resume data: {e}"
            )

            return []

    # ============================================================
    # SAVE DATA
    # ============================================================

    def save_resume_data(
        self,
        data
    ):

        try:

            with open(
                self.resume_data_file,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    data,
                    file,
                    indent=4
                )

            return True

        except Exception as e:

            print(
                f"❌ Error saving resume data: {e}"
            )

            return False

    # ============================================================
    # SAVE RESUME ANALYSIS
    # ============================================================

    def save_analysis(
        self,
        username,
        resume_name,
        detected_name,
        email,
        phone,
        skills,
        sections,
        strength_score,
        ats_score
    ):

        data = self.load_resume_data()

        record = {

            "user": username,

            "resume_file": resume_name,

            "name": detected_name,

            "email": email,

            "phone": phone,

            "skills": skills,

            "sections": sections,

            "resume_strength_score": strength_score,

            "ats_score": ats_score,

            "timestamp": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        }

        data.append(
            record
        )

        if self.save_resume_data(
            data
        ):

            print(
                "\n✅ Resume analysis saved successfully!"
            )

            return True

        return False

    # ============================================================
    # GET CURRENT USER'S RESUME HISTORY
    # ============================================================

    def get_user_resume_history(
        self,
        username
    ):

        data = self.load_resume_data()

        user_history = []

        for record in data:

            if (
                record.get("user", "").lower()
                ==
                username.lower()
            ):

                user_history.append(
                    record
                )

        return user_history

    # ============================================================
    # VIEW RESUME HISTORY
    # ============================================================

    def view_resume_history(
        self,
        username
    ):

        history = (
            self.get_user_resume_history(
                username
            )
        )

        print(
            "\n========== RESUME ANALYSIS HISTORY =========="
        )

        if not history:

            print(
                "❌ No resume analysis history found."
            )

            return

        for index, record in enumerate(
            history,
            start=1
        ):

            print(
                "\n----------------------------------------"
            )

            print(
                f"Analysis #{index}"
            )

            print(
                f"Resume File      : "
                f"{record.get('resume_file', '')}"
            )

            print(
                f"Detected Name    : "
                f"{record.get('name', '')}"
            )

            print(
                f"Email            : "
                f"{record.get('email', '')}"
            )

            print(
                f"Phone            : "
                f"{record.get('phone', '')}"
            )

            print(
                f"Skills           : "
                f"{len(record.get('skills', []))}"
            )

            print(
                f"Resume Strength  : "
                f"{record.get('resume_strength_score', 0)}/100"
            )

            print(
                f"ATS Score        : "
                f"{record.get('ats_score', 0)}/100"
            )

            print(
                f"Analyzed On      : "
                f"{record.get('timestamp', '')}"
            )

            print(
                "----------------------------------------"
            )

    # ============================================================
    # LATEST ANALYSIS
    # ============================================================

    def get_latest_analysis(
        self,
        username
    ):

        history = (
            self.get_user_resume_history(
                username
            )
        )

        if not history:

            return None

        return history[-1]