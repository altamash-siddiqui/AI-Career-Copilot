import os
import re


class ResumeAnalyzer:

    # ============================================================
    # INITIALIZATION
    # ============================================================

    def __init__(self):

        self.supported_extensions = [
            ".pdf",
            ".docx",
            ".txt"
        ]

        # --------------------------------------------------------
        # SKILL DATABASE
        # --------------------------------------------------------

        self.skill_database = [

            "Python",
            "Java",
            "JavaScript",
            "TypeScript",
            "C",
            "C++",
            "C#",
            "SQL",

            "HTML",
            "CSS",

            "React",
            "React.js",
            "Node.js",
            "Express.js",

            "Flask",
            "Django",
            "FastAPI",

            "Git",
            "GitHub",
            "GitLab",
            "GitHub Actions",

            "Machine Learning",
            "Deep Learning",
            "Artificial Intelligence",
            "AI",

            "Data Science",
            "Data Analytics",
            "Data Analysis",

            "Pandas",
            "NumPy",
            "Matplotlib",
            "Seaborn",

            "TensorFlow",
            "PyTorch",
            "Scikit-learn",

            "OpenCV",

            "NLP",
            "Natural Language Processing",

            "Power BI",
            "Excel",

            "MongoDB",
            "MySQL",
            "PostgreSQL",
            "SQLite",

            "AWS",
            "Azure",
            "Google Cloud",

            "Docker",
            "Kubernetes",

            "REST API",
            "API",

            "Linux",

            "Figma",
            "Canva",

            "Jupyter",
            "Jupyter Notebook",

            "Streamlit",

            "Generative AI",
            "LLM",
            "Large Language Models",
            "Prompt Engineering",

            "Computer Vision"

        ]

        # Remove duplicate skills while preserving order

        self.skill_database = list(
            dict.fromkeys(
                self.skill_database
            )
        )

        # --------------------------------------------------------
        # RESUME SECTION KEYWORDS
        # --------------------------------------------------------

        self.section_keywords = {

            "Summary": [
                "summary",
                "professional summary",
                "profile",
                "about me",
                "career profile"
            ],

            "Objective": [
                "objective",
                "career objective",
                "professional objective"
            ],

            "Education": [
                "education",
                "academic background",
                "academic qualifications",
                "qualifications",
                "educational background"
            ],

            "Experience": [
                "experience",
                "work experience",
                "professional experience",
                "employment history",
                "work history"
            ],

            "Internship": [
                "internship",
                "internships",
                "intern experience"
            ],

            "Projects": [
                "projects",
                "personal projects",
                "academic projects",
                "project experience"
            ],

            "Skills": [
                "skills",
                "technical skills",
                "key skills",
                "core skills",
                "technologies",
                "technical expertise"
            ],

            "Certifications": [
                "certifications",
                "certificates",
                "certification",
                "credentials"
            ],

            "Achievements": [
                "achievements",
                "awards",
                "honors",
                "accomplishments"
            ],

            "Languages": [
                "languages",
                "language proficiency"
            ],

            "Interests": [
                "interests",
                "hobbies",
                "activities"
            ]

        }

    # ============================================================
    # EXTRACT TEXT
    # ============================================================

    def extract_text(self, file_path):

        if not file_path:
            raise ValueError(
                "No resume file path provided."
            )

        if not os.path.exists(file_path):

            raise FileNotFoundError(
                "Resume file not found."
            )

        extension = os.path.splitext(
            file_path
        )[1].lower()

        if extension not in self.supported_extensions:

            raise ValueError(
                "Unsupported resume format. "
                "Use PDF, DOCX or TXT."
            )

        if extension == ".pdf":

            return self._extract_pdf_text(
                file_path
            )

        if extension == ".docx":

            return self._extract_docx_text(
                file_path
            )

        return self._extract_txt_text(
            file_path
        )

    # ============================================================
    # PDF EXTRACTION
    # ============================================================

    def _extract_pdf_text(self, file_path):

        try:

            import PyPDF2

            text_parts = []

            with open(
                file_path,
                "rb"
            ) as file:

                reader = PyPDF2.PdfReader(
                    file
                )

                if reader.is_encrypted:

                    try:
                        reader.decrypt("")
                    except Exception:
                        pass

                for page in reader.pages:

                    try:

                        page_text = (
                            page.extract_text()
                            or ""
                        )

                        if page_text.strip():

                            text_parts.append(
                                page_text
                            )

                    except Exception:

                        continue

            return "\n".join(
                text_parts
            )

        except ImportError:

            raise ImportError(
                "PyPDF2 is not installed. "
                "Run: pip install PyPDF2"
            )

        except Exception as error:

            raise Exception(
                f"PDF extraction failed: {error}"
            )

    # ============================================================
    # DOCX EXTRACTION
    # ============================================================

    def _extract_docx_text(self, file_path):

        try:

            from docx import Document

            document = Document(
                file_path
            )

            parts = []

            # ----------------------------------------------------
            # Paragraphs
            # ----------------------------------------------------

            for paragraph in document.paragraphs:

                text = (
                    paragraph.text
                    .strip()
                )

                if text:

                    parts.append(
                        text
                    )

            # ----------------------------------------------------
            # Tables
            # ----------------------------------------------------

            for table in document.tables:

                for row in table.rows:

                    row_text = []

                    for cell in row.cells:

                        cell_text = (
                            cell.text
                            .strip()
                        )

                        if cell_text:

                            row_text.append(
                                cell_text
                            )

                    if row_text:

                        parts.append(
                            " ".join(row_text)
                        )

            return "\n".join(
                parts
            )

        except ImportError:

            raise ImportError(
                "python-docx is not installed. "
                "Run: pip install python-docx"
            )

        except Exception as error:

            raise Exception(
                f"DOCX extraction failed: {error}"
            )

    # ============================================================
    # TXT EXTRACTION
    # ============================================================

    def _extract_txt_text(self, file_path):

        try:

            with open(
                file_path,
                "r",
                encoding="utf-8"
            ) as file:

                return file.read()

        except UnicodeDecodeError:

            try:

                with open(
                    file_path,
                    "r",
                    encoding="latin-1"
                ) as file:

                    return file.read()

            except Exception as error:

                raise Exception(
                    f"TXT reading failed: {error}"
                )

        except Exception as error:

            raise Exception(
                f"TXT reading failed: {error}"
            )

    # ============================================================
    # CLEAN TEXT
    # ============================================================

    def clean_text(self, text):

        if not text:

            return ""

        text = text.replace(
            "\x00",
            " "
        )

        text = text.replace(
            "\r\n",
            "\n"
        )

        text = text.replace(
            "\r",
            "\n"
        )

        # --------------------------------------------------------
        # Normalize bullets
        # --------------------------------------------------------

        bullet_characters = [
            "•",
            "▪",
            "●",
            "◦",
            "‣",
            "➢",
            "➤",
            "►"
        ]

        for bullet in bullet_characters:

            text = text.replace(
                bullet,
                " "
            )

        # --------------------------------------------------------
        # Normalize whitespace
        # --------------------------------------------------------

        text = re.sub(
            r"[ \t]+",
            " ",
            text
        )

        text = re.sub(
            r"\n[ \t]+",
            "\n",
            text
        )

        text = re.sub(
            r"\n{3,}",
            "\n\n",
            text
        )

        return text.strip()

    # ============================================================
    # DETECT NAME
    # ============================================================

    def detect_name(self, text):

        lines = [

            line.strip()

            for line in text.splitlines()

            if line.strip()

        ]

        ignored = {

            "resume",
            "curriculum vitae",
            "curriculum",
            "vitae",
            "cv",
            "profile",
            "contact",
            "contact information",
            "objective",
            "summary",
            "professional summary",
            "resume profile"

        }

        heading_words = {

            "education",
            "experience",
            "projects",
            "skills",
            "certifications",
            "achievements",
            "languages",
            "interests",
            "internship",
            "objective",
            "summary"

        }

        # Inspect first 15 meaningful lines

        for line in lines[:15]:

            clean_line = re.sub(
                r"\s+",
                " ",
                line
            ).strip()

            lower_line = (
                clean_line.lower()
            )

            if lower_line in ignored:

                continue

            if lower_line in heading_words:

                continue

            # Email line

            if "@" in clean_line:

                continue

            # URLs / social links

            if re.search(
                r"(linkedin|github|www\.|https?://)",
                lower_line
            ):

                continue

            # Contact labels

            if re.search(
                r"(phone|mobile|email|contact)",
                lower_line
            ):

                continue

            # Name should not contain numbers

            if re.search(
                r"\d",
                clean_line
            ):

                continue

            words = clean_line.split()

            if not (
                2 <= len(words) <= 5
            ):

                continue

            valid = True

            for word in words:

                if not re.match(
                    r"^[A-Za-z][A-Za-z.\-']*$",
                    word
                ):

                    valid = False

                    break

            if valid:

                return clean_line

        return ""

    # ============================================================
    # DETECT EMAIL
    # ============================================================

    def detect_email(self, text):

        pattern = (

            r"\b[A-Za-z0-9._%+\-]+"
            r"@[A-Za-z0-9.\-]+"
            r"\.[A-Za-z]{2,}\b"

        )

        match = re.search(
            pattern,
            text
        )

        if match:

            return match.group(0)

        return ""

    # ============================================================
    # DETECT PHONE
    # ============================================================

    def detect_phone(self, text):

        patterns = [

            # India

            r"\+91[\s\-]?[6-9]\d{9}",

            r"\+91[\s\-]?[6-9]\d{4}[\s\-]?\d{5}",

            r"\b[6-9]\d{9}\b",

            # International

            r"\+\d{1,3}[\s\-]?\d{7,12}",

            # US-like

            r"\b\d{3}[\s\-]\d{3}[\s\-]\d{4}\b",

            # Indian spaced

            r"\b\d{5}[\s\-]\d{5}\b"

        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                text
            )

            if match:

                return match.group(0)

        return ""

    # ============================================================
    # DETECT LINKEDIN
    # ============================================================

    def detect_linkedin(self, text):

        pattern = (

            r"(https?://)?"
            r"(www\.)?"
            r"linkedin\.com/[^\s|,;]+"

        )

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            return match.group(0).rstrip(
                ".,);]"
            )

        return ""

    # ============================================================
    # DETECT GITHUB
    # ============================================================

    def detect_github(self, text):

        pattern = (

            r"(https?://)?"
            r"(www\.)?"
            r"github\.com/[^\s|,;]+"

        )

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            return match.group(0).rstrip(
                ".,);]"
            )

        return ""

    # ============================================================
    # SKILL DATABASE
    # ============================================================

    def get_skill_database(self):

        return self.skill_database

    # ============================================================
    # DETECT SKILLS
    # ============================================================

    def detect_skills(self, text):

        detected_skills = []

        # --------------------------------------------------------
        # Longer skills first
        # --------------------------------------------------------

        skills_sorted = sorted(
            self.skill_database,
            key=len,
            reverse=True
        )

        for skill in skills_sorted:

            pattern = (

                r"(?<![A-Za-z0-9])"
                + re.escape(skill)
                + r"(?![A-Za-z0-9])"

            )

            if re.search(
                pattern,
                text,
                re.IGNORECASE
            ):

                if skill not in detected_skills:

                    detected_skills.append(
                        skill
                    )

        return detected_skills

    # ============================================================
    # SECTION DATABASE
    # ============================================================

    def get_section_keywords(self):

        return self.section_keywords

    # ============================================================
    # SECTION DETECTION
    # ============================================================

    def detect_sections(self, text):

        sections = []

        lower_text = text.lower()

        for section, keywords in (
            self.section_keywords.items()
        ):

            for keyword in keywords:

                pattern = (

                    r"(?<![a-z])"
                    + re.escape(
                        keyword.lower()
                    )
                    + r"(?![a-z])"

                )

                if re.search(
                    pattern,
                    lower_text
                ):

                    sections.append(
                        section
                    )

                    break

        return sections

    # ============================================================
    # CONTENT QUALITY
    # ============================================================

    def calculate_content_quality(
        self,
        text
    ):

        score = 0

        character_count = len(
            text
        )

        word_count = len(
            text.split()
        )

        # --------------------------------------------------------
        # Character quality
        # --------------------------------------------------------

        if character_count >= 1800:

            score += 20

        elif character_count >= 1400:

            score += 18

        elif character_count >= 1000:

            score += 16

        elif character_count >= 600:

            score += 12

        elif character_count >= 300:

            score += 8

        elif character_count >= 150:

            score += 4

        # --------------------------------------------------------
        # Word quality
        # --------------------------------------------------------

        if word_count >= 500:

            score += 10

        elif word_count >= 400:

            score += 9

        elif word_count >= 250:

            score += 8

        elif word_count >= 150:

            score += 6

        elif word_count >= 75:

            score += 3

        return min(
            score,
            30
        )

    # ============================================================
    # RESUME STRENGTH SCORE
    # ============================================================

    def calculate_strength_score(
        self,
        text,
        skills,
        sections,
        email,
        phone
    ):

        score = 0

        # --------------------------------------------------------
        # Content quality: 30
        # --------------------------------------------------------

        score += self.calculate_content_quality(
            text
        )

        # --------------------------------------------------------
        # Skills: 20
        # --------------------------------------------------------

        skill_count = len(
            skills
        )

        if skill_count >= 10:

            score += 20

        elif skill_count >= 7:

            score += 16

        elif skill_count >= 5:

            score += 13

        elif skill_count >= 3:

            score += 9

        elif skill_count >= 1:

            score += 5

        # --------------------------------------------------------
        # Sections: 25
        # --------------------------------------------------------

        section_count = len(
            sections
        )

        score += min(
            section_count * 3,
            18
        )

        important_sections = [

            "Education",
            "Skills",
            "Projects"

        ]

        for section in important_sections:

            if section in sections:

                score += 2

        # --------------------------------------------------------
        # Contact: 15
        # --------------------------------------------------------

        if email:

            score += 8

        if phone:

            score += 7

        # --------------------------------------------------------
        # Achievement language: 10
        # --------------------------------------------------------

        achievement_patterns = [

            r"\b\d+%",

            r"\b\d+\+",

            r"\b\d+\s*(users|clients|projects|students)",

            r"\b(increased|improved|reduced|optimized|"
            r"achieved|developed|built|created|"
            r"implemented|designed)\b"

        ]

        achievement_found = False

        for pattern in achievement_patterns:

            if re.search(
                pattern,
                text,
                re.IGNORECASE
            ):

                achievement_found = True

                break

        if achievement_found:

            score += 10

        return min(
            score,
            100
        )

    # ============================================================
    # ATS SCORE
    # ============================================================

    def calculate_ats_score(
        self,
        text,
        skills,
        sections,
        email,
        phone
    ):

        score = 0

        # --------------------------------------------------------
        # Contact: 20
        # --------------------------------------------------------

        if email:

            score += 10

        if phone:

            score += 10

        # --------------------------------------------------------
        # Core sections: 40
        # --------------------------------------------------------

        required_sections = [

            "Education",
            "Skills",
            "Projects",
            "Experience"

        ]

        for section in required_sections:

            if section in sections:

                score += 10

        # --------------------------------------------------------
        # Skills: 20
        # --------------------------------------------------------

        skill_count = len(
            skills
        )

        if skill_count >= 8:

            score += 20

        elif skill_count >= 5:

            score += 16

        elif skill_count >= 3:

            score += 12

        elif skill_count >= 1:

            score += 6

        # --------------------------------------------------------
        # Readability: 10
        # --------------------------------------------------------

        word_count = len(
            text.split()
        )

        if word_count >= 400:

            score += 10

        elif word_count >= 250:

            score += 8

        elif word_count >= 150:

            score += 6

        elif word_count >= 75:

            score += 4

        else:

            score += 2

        # --------------------------------------------------------
        # Achievement keywords: 10
        # --------------------------------------------------------

        keyword_signals = [

            "developed",
            "built",
            "created",
            "implemented",
            "designed",
            "managed",
            "optimized",
            "improved",
            "analyzed",
            "automated"

        ]

        signal_count = 0

        lower_text = text.lower()

        for signal in keyword_signals:

            if re.search(
                r"\b"
                + re.escape(signal)
                + r"\b",
                lower_text
            ):

                signal_count += 1

        if signal_count >= 5:

            score += 10

        elif signal_count >= 3:

            score += 7

        elif signal_count >= 1:

            score += 4

        return min(
            score,
            100
        )

    # ============================================================
    # SUGGESTIONS
    # ============================================================

    def generate_suggestions(
        self,
        text,
        skills,
        sections,
        email,
        phone
    ):

        suggestions = []

        # --------------------------------------------------------
        # Contact
        # --------------------------------------------------------

        if not email:

            suggestions.append(
                "Add a professional email address."
            )

        if not phone:

            suggestions.append(
                "Add a valid phone number."
            )

        # --------------------------------------------------------
        # Sections
        # --------------------------------------------------------

        if "Education" not in sections:

            suggestions.append(
                "Add a clear Education section."
            )

        if "Skills" not in sections:

            suggestions.append(
                "Add a dedicated Technical Skills section."
            )

        if "Projects" not in sections:

            suggestions.append(
                "Add relevant projects with technologies and outcomes."
            )

        if "Experience" not in sections:

            suggestions.append(
                "Add internship, work or practical experience if available."
            )

        if "Certifications" not in sections:

            suggestions.append(
                "Add relevant certifications and credentials."
            )

        # --------------------------------------------------------
        # Skills
        # --------------------------------------------------------

        if len(skills) < 5:

            suggestions.append(
                "Add more role-relevant technical skills."
            )

        # --------------------------------------------------------
        # Content
        # --------------------------------------------------------

        word_count = len(
            text.split()
        )

        if word_count < 250:

            suggestions.append(
                "Add more detail about projects, experience and achievements."
            )

        # --------------------------------------------------------
        # Achievement language
        # --------------------------------------------------------

        achievement_words = [

            "increased",
            "improved",
            "reduced",
            "optimized",
            "achieved",
            "developed",
            "built",
            "implemented",
            "designed",
            "automated"

        ]

        lower_text = text.lower()

        has_achievement_language = any(

            word in lower_text

            for word in achievement_words

        )

        if not has_achievement_language:

            suggestions.append(
                "Use measurable achievement language such as "
                "developed, improved, optimized or increased."
            )

        # --------------------------------------------------------
        # Final fallback
        # --------------------------------------------------------

        if not suggestions:

            suggestions.append(
                "Your resume has a strong structure. "
                "Tailor keywords and achievements for each job description."
            )

        return suggestions

    # ============================================================
    # RESUME QUALITY LABEL
    # ============================================================

    def get_score_label(self, score):

        if score >= 85:

            return "Excellent"

        if score >= 70:

            return "Strong"

        if score >= 55:

            return "Good"

        if score >= 40:

            return "Needs Improvement"

        return "Needs Optimization"

    # ============================================================
    # COMPLETE TEXT ANALYSIS
    # ============================================================

    def analyze_text(self, text):

        # --------------------------------------------------------
        # Clean text
        # --------------------------------------------------------

        text = self.clean_text(
            text
        )

        if not text:

            return {

                "success": False,

                "message":
                    "No readable text found in the resume."

            }

        # --------------------------------------------------------
        # Extract information
        # --------------------------------------------------------

        name = self.detect_name(
            text
        )

        email = self.detect_email(
            text
        )

        phone = self.detect_phone(
            text
        )

        linkedin = self.detect_linkedin(
            text
        )

        github = self.detect_github(
            text
        )

        skills = self.detect_skills(
            text
        )

        sections = self.detect_sections(
            text
        )

        # --------------------------------------------------------
        # Scores
        # --------------------------------------------------------

        strength_score = (
            self.calculate_strength_score(
                text,
                skills,
                sections,
                email,
                phone
            )
        )

        ats_score = (
            self.calculate_ats_score(
                text,
                skills,
                sections,
                email,
                phone
            )
        )

        # --------------------------------------------------------
        # Suggestions
        # --------------------------------------------------------

        suggestions = (
            self.generate_suggestions(
                text,
                skills,
                sections,
                email,
                phone
            )
        )

        # --------------------------------------------------------
        # Statistics
        # --------------------------------------------------------

        word_count = len(
            text.split()
        )

        character_count = len(
            text
        )

        # --------------------------------------------------------
        # Return result
        # --------------------------------------------------------

        return {

            "success": True,

            # Personal information

            "name": name,

            "detected_name": name,

            "email": email,

            "phone": phone,

            "linkedin": linkedin,

            "github": github,

            # Resume analysis

            "skills": skills,

            "sections": sections,

            # Scores

            "resume_strength_score":
                strength_score,

            "strength_score":
                strength_score,

            "ats_score":
                ats_score,

            # Labels

            "strength_label":
                self.get_score_label(
                    strength_score
                ),

            "ats_label":
                self.get_score_label(
                    ats_score
                ),

            # Suggestions

            "suggestions":
                suggestions,

            # Statistics

            "word_count":
                word_count,

            "character_count":
                character_count,

            "skill_count":
                len(skills),

            "section_count":
                len(sections)

        }

    # ============================================================
    # ANALYZE FILE
    # ============================================================

    def analyze_file(self, file_path):

        text = self.extract_text(
            file_path
        )

        result = self.analyze_text(
            text
        )

        result["resume_file"] = (
            os.path.basename(
                file_path
            )
        )

        return result


# ================================================================
# DIRECT TEST
# ================================================================

if __name__ == "__main__":

    analyzer = ResumeAnalyzer()

    print("=" * 60)

    print(
        "              AI CAREER COPILOT"
    )

    print(
        "                RESUME ANALYZER"
    )

    print("=" * 60)

    print(
        "Resume Analyzer module loaded successfully."
    )

    print(
        "Supported formats: PDF | DOCX | TXT"
    )

    print(
        f"Skills database: "
        f"{len(analyzer.skill_database)} skills"
    )

    print("=" * 60)