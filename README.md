# 🤖 AI Career Copilot

An AI-powered career development platform that helps users analyze resumes, check ATS compatibility, optimize resumes, match jobs with skills, generate personalized learning roadmaps, explore career insights, and practice interviews with AI.

AI Career Copilot combines Python, Flask, AI APIs, resume analysis, career intelligence, authentication, interview preparation, and a modern web interface into a single career-focused application.

---

## 🚀 Features

### 🔐 User Authentication

The application includes user authentication and protected API access.

Users can:

- Register a new account
- Log in securely
- Access protected API routes
- Use authentication tokens
- Access user-specific career and resume data
- Maintain authenticated sessions

---

## 📄 AI Resume Analysis

The Resume Analyzer helps users understand the quality and structure of their resume.

Features include:

- Resume file upload
- Resume text extraction
- Skills extraction
- Resume section detection
- Resume strength analysis
- ATS score estimation
- Content quality analysis
- Achievement analysis
- Missing section detection
- Resume improvement insights
- Resume history

Supported file processing includes PDF and DOCX resume analysis through the configured backend modules.

---

## 🎯 ATS Resume Analysis

The application evaluates resumes from an Applicant Tracking System perspective.

The analysis can provide insights related to:

- Resume structure
- Relevant skills
- Keywords
- Missing sections
- Content quality
- ATS compatibility
- Resume strength

---

## ✨ AI Resume Optimization

Users can optimize their resumes using AI-powered recommendations.

The system supports:

- Resume improvement suggestions
- Content optimization
- Job-focused resume optimization
- AI-generated improvements
- Optimized resume approval
- Resume history and version management

---

## 💼 Job Matching

Users can compare their resume with job requirements.

The Job Matching system can analyze:

- Matching skills
- Missing skills
- Resume relevance
- Skill gaps
- Job compatibility
- Overall match results

---

## 🧠 Career Intelligence

The Career Intelligence module provides AI-powered insights related to career development.

It can help users explore:

- Career direction
- Skill development priorities
- Career opportunities
- Learning recommendations
- Career growth insights
- Personalized career guidance

---

## 🗺️ Personalized Learning Roadmaps

Users can select career paths and follow structured learning roadmaps.

Features include:

- Career selection
- Personalized learning steps
- Step completion tracking
- Progress percentage
- Completed steps
- Remaining steps
- Career progress visualization
- Career completion tracking

Example career areas include:

- 🤖 Artificial Intelligence
- 🐍 Python Development
- 🌐 Web Development
- 📊 Data Science

---

## 📊 Career Dashboard

The Dashboard provides a centralized view of user progress.

It can display:

- Career information
- Roadmap progress
- Completed steps
- Remaining steps
- Career statistics
- Progress indicators
- User-specific data

---

## 🎤 AI Interview Intelligence

The Interview module helps users prepare for technical and career-focused interviews.

Features include:

- Interview session creation
- Career-focused interview questions
- Mock interview experience
- AI-generated interview questions
- Answer evaluation
- AI feedback
- Interview reports
- Interview session history

---

## 🎙️ Voice Interview Features

The project includes voice-related interview capabilities.

Depending on API configuration, the application can support:

- AI interviewer voice responses
- Speech generation
- Audio transcription
- Voice-based interview interaction

Voice functionality can use configured AI services such as ElevenLabs.

---

## 🎥 Learning Resources

The application includes learning resource support through YouTube search integration.

Users can search for relevant educational content based on:

- Career paths
- Skills
- Learning goals
- Interview preparation topics

---

# 🛠️ Technologies Used

## Backend

- Python
- Flask
- Flask-CORS
- Python Dotenv
- Werkzeug
- Requests

## AI and APIs

- Google Gemini API
- Google GenAI SDK
- ElevenLabs API

## Resume Processing

- PyPDF2
- python-docx

## Frontend

- HTML5
- CSS3
- JavaScript

## Development Tools

- Git
- GitHub
- Visual Studio Code

---

# 📂 Project Structure

```text
AI-Career-Copilot/
│
├── backend/
│   │
│   ├── api.py
│   ├── app.py
│   ├── career_features.py
│   ├── career_intelligence.py
│   ├── interview_engine.py
│   ├── job_matcher.py
│   ├── person.py
│   ├── resume_analyzer.py
│   ├── resume_manager.py
│   ├── resume_optimizer.py
│   ├── utils.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   └── resume_service.py
│   │
│   └── requirements.txt
│
├── frontend/
│   │
│   ├── index.html
│   ├── dashboard.html
│   ├── resume.html
│   ├── roadmap.html
│   ├── career-intelligence.html
│   ├── interview.html
│   ├── script.js
│   └── style.css
│
├── uploads/
│
├── notes/
│
├── .env.example
├── .gitignore
├── README.md
│
└── other project files
```

---

# ⚙️ Environment Setup

Create a `.env` file in the project root.

Use `.env.example` as a reference.

Example:

```env
GEMINI_API_KEY=your_gemini_api_key

GEMINI_MODEL=your_configured_gemini_model

ELEVENLABS_API_KEY=your_elevenlabs_api_key

ELEVENLABS_VOICE_NAME=Sarah

ELEVENLABS_VOICE_ID=your_voice_id

ELEVENLABS_MODEL_ID=eleven_multilingual_v2

ELEVENLABS_STT_MODEL_ID=scribe_v2

SECRET_KEY=your_strong_secret_key

AUTH_TOKEN_MAX_AGE=3600

CORS_ORIGINS=http://127.0.0.1:5500,http://localhost:5500

FLASK_DEBUG=false
```

> ⚠️ Never upload your real `.env` file or API keys to GitHub.

---

# ▶️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/altamash-siddiqui/AI-Career-Copilot.git
```

---

## 2. Open the Project

```bash
cd AI-Career-Copilot
```

---

## 3. Create a Virtual Environment

### Windows

```powershell
python -m venv venv
```

Activate it:

```powershell
venv\Scripts\activate
```

---

## 4. Install Dependencies

```bash
pip install -r backend/requirements.txt
```

---

## 5. Configure Environment Variables

Create a file named:

```text
.env
```

Use:

```text
.env.example
```

as a reference.

Then add your actual API keys and secret values.

---

# 🖥️ Running the Application Locally

## Start the Backend API

From the project root:

```powershell
cd backend
python api.py
```

The backend runs locally at:

```text
http://127.0.0.1:5000
```

---

## Start the Frontend

Open the project with a local development server.

For example, using VS Code Live Server, run:

```text
frontend/index.html
```

The frontend can run on:

```text
http://127.0.0.1:5500
```

Make sure the frontend API URL matches the running backend URL during local development.

---

# 🔗 Main API Functionality

The backend provides functionality for:

```text
API Status
User Registration
User Login
Dashboard
Career Creation
Career Roadmaps
Roadmap Step Completion
Career History
Resume Analysis
Job Matching
Resume Optimization
Resume Optimization Approval
Resume History
Latest Resume
Career Intelligence
Interview Intelligence
YouTube Learning Resource Search
```

The project also includes additional API routes registered through the Career Intelligence and Interview Engine modules.

---

# 🔒 Security

The project includes several security-focused configurations:

- Environment variables for API keys
- Secret key configuration
- Authentication token expiration
- Protected API requests
- Authorization header support
- CORS configuration
- File upload validation
- File size restrictions
- Password hashing

For production deployment, secret values should always be stored in the hosting platform's environment variable settings.

Never expose:

```text
GEMINI_API_KEY
ELEVENLABS_API_KEY
SECRET_KEY
```

in frontend code or public repositories.

---

# 📊 Application Flow

```text
User
 │
 ▼
Authentication
 │
 ▼
Dashboard
 │
 ├──────────────────┬──────────────────────┬──────────────────────┐
 ▼                  ▼                      ▼                      ▼
Resume            Roadmap            Career Intelligence       Interview
Analysis            │                      │                      │
 │                  ▼                      ▼                      ▼
 ▼               Progress              AI Insights          Mock Interview
ATS Score         Tracking                 │                      │
 │                  │                      ▼                      ▼
 ▼                  ▼               Recommendations         Evaluation
Job Match        Dashboard                                     │
 │                                                        ▼
 ▼                                                     Report
Resume
Optimization
```

---

# 🧩 Core Modules

## Resume Modules

```text
resume_analyzer.py
resume_manager.py
resume_optimizer.py
services/resume_service.py
```

These modules handle resume analysis, processing, optimization, and related functionality.

---

## Career Modules

```text
career_features.py
career_intelligence.py
```

These modules provide career analysis and intelligence functionality.

---

## Interview Module

```text
interview_engine.py
```

This module handles AI interview functionality, including interview generation, answer evaluation, feedback, and reports.

---

## API Layer

```text
api.py
```

The Flask API acts as the main backend layer connecting:

- Frontend
- Authentication
- Resume features
- Career features
- Interview features
- AI services
- External APIs

---

# 📈 Development Journey

| Day | Development Focus |
|---|---|
| Day 1 | Python Fundamentals |
| Day 2 | Variables and Data Types |
| Day 3 | If-Else and Conditional Statements |
| Day 4 | Loops and Control Statements |
| Day 5 | Python Practice Programs |
| Day 6 | Lists and Tuples |
| Day 7 | Functions |
| Day 8 | Dictionaries and Sets |
| Day 9 | Strings |
| Day 10 | File Handling |
| Day 11 | Functions Practice |
| Day 12 | Object-Oriented Programming |
| Day 13 | Inheritance and Method Overriding |
| Day 14 | Multiple Classes and Composition |
| Day 15 | Modules and Project Structure |
| Day 16 | Exception Handling and Logging |
| Day 17 | JSON Data Storage |
| Day 18 | Advanced File Handling and Search |
| Day 19 | User Authentication |
| Day 20 | Project Refactoring |
| Day 21 | Mini Features and Testing |
| Day 22 | Resume and ATS Improvements |
| Day 23 | AI Career Copilot Features |
| Day 24 | Bug Fixing and Code Cleanup |
| Day 25 | Career Dashboard Enhancement |
| Day 26 | Documentation and GitHub README |
| Day 27 | Deployment Preparation |
| Day 28+ | Web Application Development |
| Day 33 | Career Intelligence |
| Day 34 | Personalized Learning Roadmap |
| Day 35-36 | Interview Intelligence and Mock Interview |
| Day 38 | Interview Intelligence and API Improvements |
| Day 39 | Production Deployment |

---

# 🚀 Future Improvements

Possible future improvements include:

- Cloud database integration
- Persistent production storage
- Advanced user profiles
- More career paths
- More AI models
- Advanced job recommendations
- Improved analytics
- Interview scoring improvements
- Better resume templates
- Mobile application
- Admin dashboard
- Email verification
- Password reset
- Production monitoring
- CI/CD automation

---

# 🎯 Project Goal

The goal of AI Career Copilot is to build a practical AI-powered career development platform while improving skills in:

- Python
- Backend Development
- REST APIs
- Artificial Intelligence
- Authentication
- Resume Analysis
- Career Analytics
- Web Development
- Software Architecture
- Git and GitHub
- Production Deployment

---

# 👨‍💻 Author

**Altamash Siddiqui**

BCA Student | Python and AI Enthusiast

---

# ⭐ Project Status

🚀 **Actively Developed and Continuously Improving**

The project currently includes:

- AI-powered resume analysis
- ATS insights
- Job matching
- Resume optimization
- Career intelligence
- Personalized learning roadmaps
- Career dashboard
- User authentication
- Interview intelligence
- Mock interview functionality
- Voice-based interview capabilities

---

# 📜 License

This project is created for:

- Learning
- Practice
- Portfolio development
- Educational purposes