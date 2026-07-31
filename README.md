# 🤖 Teacher AI Platform

An AI-powered educational document intelligence platform that converts raw educational documents into a structured, classroom-ready **Teacher Knowledge Package (TKP)**.

The platform uses a modular AI pipeline to extract knowledge from educational documents, classify and chunk content, and generate structured teaching resources using a local LLM through **Ollama**.

---

## 📌 Overview

Teachers often work with large and unstructured educational materials such as:

* PDF textbooks
* Lecture notes
* Course documents
* Study materials
* Lesson plans
* Educational articles

Manually converting these materials into structured teaching resources can be time-consuming.

The **Teacher AI Platform** automates this process.

### Input

An educational document uploaded by the teacher.

### Processing

The system:

1. Extracts text from the document
2. Cleans and processes the extracted content
3. Splits the content into meaningful chunks
4. Classifies the document
5. Sends the relevant context to an LLM
6. Generates a structured Teacher Knowledge Package

### Output

A structured TKP containing information such as:

* Document title
* Summary
* Learning objectives
* Key concepts
* Teaching points
* Classroom activities
* Assessment questions
* Additional teaching guidance

---

# ✨ Features

## 📄 Document Upload

Upload educational documents through the web interface.

Supported document types depend on the configured parser and may include:

* PDF
* TXT
* DOCX

---

## 🔍 Document Intelligence

The backend extracts useful textual information from uploaded educational documents.

The extraction layer is separated from the AI generation layer, making the system easier to extend.

---

## 🧩 Intelligent Chunking

Large documents are divided into manageable chunks before being sent to the LLM.

This helps:

* Reduce context overload
* Improve processing reliability
* Handle large documents
* Preserve relevant educational context

---

## 🧠 Document Classification

The system can classify educational content before generating the Teacher Knowledge Package.

Classification information can be passed to the TKP generator to improve the relevance of the generated content.

---

## 🤖 Local LLM Processing

The platform uses **Ollama** to run the language model locally.

This provides:

* Local inference
* Better privacy for educational documents
* No mandatory external LLM API dependency
* Flexibility to switch between supported local models

---

## 📚 Teacher Knowledge Package

The final output is structured JSON containing classroom-ready educational information.

Example:

```json
{
  "title": "Introduction to Photosynthesis",
  "summary": "An introduction to the process of photosynthesis...",
  "learning_objectives": [
    "Understand the process of photosynthesis",
    "Identify the role of sunlight",
    "Explain the importance of chlorophyll"
  ],
  "key_concepts": [
    "Chlorophyll",
    "Glucose",
    "Carbon dioxide",
    "Oxygen"
  ],
  "teaching_points": [
    "Plants use sunlight to produce energy.",
    "Carbon dioxide and water are used during photosynthesis."
  ]
}
```

---

# 🏗️ System Architecture

```text
                    ┌──────────────────────┐
                    │      Teacher         │
                    │    Web Interface     │
                    └──────────┬───────────┘
                               │
                               │ Upload Document
                               ▼
                    ┌──────────────────────┐
                    │     React / Vite     │
                    │      Frontend        │
                    └──────────┬───────────┘
                               │
                               │ HTTP API
                               ▼
                    ┌──────────────────────┐
                    │       FastAPI        │
                    │       Backend        │
                    └──────────┬───────────┘
                               │
                 ┌─────────────┼─────────────┐
                 │             │             │
                 ▼             ▼             ▼
          ┌────────────┐ ┌────────────┐ ┌──────────────┐
          │  Document  │ │  Chunking  │ │Classification│
          │   Parser   │ │   Service  │ │   Service    │
          └─────┬──────┘ └──────┬─────┘ └──────┬───────┘
                │               │              │
                └───────────────┼──────────────┘
                                │
                                ▼
                      ┌────────────────────┐
                      │   TKP Generator    │
                      │     Service        │
                      └──────────┬─────────┘
                                 │
                                 │ Prompt + Context
                                 ▼
                      ┌────────────────────┐
                      │      Ollama        │
                      │      Local LLM     │
                      └──────────┬─────────┘
                                 │
                                 ▼
                      ┌────────────────────┐
                      │ Teacher Knowledge  │
                      │     Package        │
                      └────────────────────┘
```

---

# 🛠️ Technology Stack

## Backend

* Python
* FastAPI
* Uvicorn
* Pydantic
* Python document parsing libraries
* Ollama

## Frontend

* React
* Vite
* JavaScript
* Axios
* CSS

## AI / LLM

* Ollama
* Local Large Language Model
* Prompt-based structured generation

## Development

* GitHub
* Python virtual environment

---

# 📂 Project Structure

```text
teacher-ai-platform/
│
├── backend/
│   │
│   ├── app.py
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── upload.py
│   │   └── process.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── parser.py
│   │   ├── chunker.py
│   │   ├── classifier.py
│   │   ├── tkp_generator.py
│   │   └── llm.py
│   │
│   └── ...
│
├── frontend/
│   │
│   ├── src/
│   │   ├── components/
│   │   │   ├── FileUploader.jsx
│   │   │   ├── ResultViewer.jsx
│   │   │   └── LoadingSpinner.jsx
│   │   │
│   │   ├── services/
│   │   │   └── api.js
│   │   │
│   │   ├── App.jsx
│   │   └── main.jsx
│   │
│   ├── package.json
│   ├── package-lock.json
│   └── vite.config.js
│
├── files/
│   └── # Runtime/input files
│
├── requirements.txt
├── .gitignore
└── README.md
```

> The exact file structure may vary depending on the current implementation.

---

# ⚙️ Prerequisites

Before running the project, install:

### Python

Python 3.10+ is recommended.

Verify:

```bash
python --version
```

### Node.js

Node.js 18+ is recommended.

Verify:

```bash
node --version
npm --version
```

### Ollama

Install Ollama and verify:

```bash
ollama --version
```

The Ollama server must be running before processing documents.

---

# 🚀 Installation

## 1. Clone the Repository

```bash
git clone https://github.com/Nishtha-agarwal/Teacher-ai-platform.git
```

Move into the project:

```bash
cd Teacher-ai-platform
```

---

# 🐍 Backend Setup

## 2. Create a Virtual Environment

Windows:

```powershell
python -m venv venv
```

Activate it:

```powershell
venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

---

# 🤖 Ollama Setup

The platform uses Ollama for local LLM inference.

## 4. Start Ollama

Make sure the Ollama application/server is running.

You can verify the server by checking:

```text
http://127.0.0.1:11434
```

---

## 5. Download an LLM

Pull the model configured in your application.

For example:

```bash
ollama pull llama3.2
```

Verify installed models:

```bash
ollama list
```

> If your backend is configured to use a different model, replace `llama3.2` with that model name.

---

# ▶️ Running the Backend

From the project root:

```powershell
cd backend
```

Start FastAPI:

```powershell
uvicorn app:app --reload
```

The backend will normally be available at:

```text
http://127.0.0.1:8000
```

FastAPI automatically provides interactive API documentation at:

```text
http://127.0.0.1:8000/docs
```

---

# 💻 Running the Frontend

Open another terminal.

Navigate to the frontend:

```powershell
cd frontend
```

Install dependencies:

```powershell
npm install
```

Start Vite:

```powershell
npm run dev
```

The frontend will normally be available at:

```text
http://localhost:5173
```

---

# 🔄 Application Workflow

The complete application workflow is:

```text
1. Teacher uploads document
              ↓
2. React frontend sends document
              ↓
3. FastAPI receives upload
              ↓
4. Document is stored temporarily
              ↓
5. Parser extracts text
              ↓
6. Text is cleaned
              ↓
7. Content is divided into chunks
              ↓
8. Document is classified
              ↓
9. Context + classification sent to TKP generator
              ↓
10. TKP generator creates structured prompt
              ↓
11. Ollama processes the prompt
              ↓
12. LLM generates structured educational content
              ↓
13. FastAPI returns TKP JSON
              ↓
14. React displays the result
```

---

# 🔌 API Endpoints

## Health Check

```http
GET /
```

Used to verify that the backend is running.

---

## Upload Document

```http
POST /upload/
```

Uploads an educational document to the backend.

### Request

```text
multipart/form-data
```

Example:

```bash
curl -X POST \
  -F "file=@example.pdf" \
  http://127.0.0.1:8000/upload/
```

---

## Process Document

```http
POST /process/
```

Processes the uploaded document and generates the Teacher Knowledge Package.

The processing pipeline includes:

```text
Document
   ↓
Text Extraction
   ↓
Chunking
   ↓
Classification
   ↓
LLM Generation
   ↓
TKP
```

---

# 🧠 AI Pipeline

The AI architecture is intentionally modular.

## 1. Parser

Responsible for extracting text from the source document.

Example responsibility:

```text
PDF → Raw Text
```

---

## 2. Chunker

Splits large documents into smaller sections.

Example:

```text
Large Document
      ↓
Chunk 1
Chunk 2
Chunk 3
Chunk 4
```

This allows the LLM pipeline to process information more reliably.

---

## 3. Classifier

Determines useful information about the document, such as:

* Subject
* Topic
* Educational level
* Content type
* Difficulty
* Domain

The classification result can then be supplied to the TKP generator.

---

## 4. TKP Generator

The TKP generator combines:

```text
Document Context
        +
Classification
        +
Generation Instructions
        ↓
Structured TKP
```

The generator is designed to return structured JSON rather than unstructured text.

---

## 5. Ollama

Ollama provides the local inference layer.

The application sends the generated prompt to the Ollama API and receives the model response.

This keeps the LLM execution local and avoids requiring an external hosted LLM API.

---

# 📦 Teacher Knowledge Package

The generated TKP is designed to be machine-readable and teacher-friendly.

A typical package can contain:

```text
Title
│
├── Summary
│
├── Learning Objectives
│
├── Key Concepts
│
├── Teaching Points
│
├── Classroom Activities
│
├── Assessment Questions
│
└── Additional Guidance
```

This structure can be extended as the platform evolves.

---

# 🔐 Security & Privacy

The project is designed with local development and educational data privacy in mind.

### Local LLM

Ollama allows documents to be processed using a local model rather than automatically sending educational content to a third-party hosted LLM.

### Secrets

Sensitive configuration should be stored in environment variables.

Example:

```text
.env
```

Do not commit `.env` files to GitHub.

Instead, create:

```text
.env.example
```

with placeholder values.

---

# 🚫 Files Excluded from Git

The repository intentionally excludes generated and environment-specific files.

Examples:

```text
venv/
node_modules/
.env
uploads/
outputs/
*.gguf
*.safetensors
*.pt
*.pth
```

These files can be recreated locally and should not be committed to the repository.

---

# 🧪 Testing

Before submitting changes, verify the backend:

```powershell
cd backend
uvicorn app:app --reload
```

Then open:

```text
http://127.0.0.1:8000/docs
```

Test:

1. Health endpoint
2. Upload endpoint
3. Process endpoint
4. TKP generation

For the frontend:

```powershell
cd frontend
npm run dev
```

Verify:

1. Application loads
2. File upload works
3. Backend request succeeds
4. Loading state is displayed
5. Generated TKP is rendered

---

# 🐛 Troubleshooting

## Ollama connection error

Make sure Ollama is running.

Check:

```bash
ollama list
```

Then verify that the model used by the application is installed.

---

## FastAPI cannot start

Make sure you are inside the correct backend directory:

```powershell
cd backend
```

Then:

```powershell
uvicorn app:app --reload
```

---

## `ModuleNotFoundError`

Activate the virtual environment:

```powershell
venv\Scripts\activate
```

Then reinstall dependencies:

```powershell
pip install -r requirements.txt
```

---

## Frontend dependency error

From the frontend directory:

```powershell
npm install
```

Then:

```powershell
npm run dev
```

---

## Port 8000 already in use

Check the process:

```powershell
netstat -ano | findstr :8000
```

Stop the corresponding process if necessary, or run FastAPI on another port:

```powershell
uvicorn app:app --reload --port 8001
```

Update the frontend API URL accordingly.

---



# 🎯 Design Principles

The project follows several engineering principles:

### Modular Architecture

Document parsing, chunking, classification, and generation are separated into independent services.

### Separation of Concerns

The frontend handles presentation while the backend handles processing and AI orchestration.

### Extensibility

The LLM layer can be replaced without redesigning the entire application.

### Structured Outputs

The AI pipeline aims to generate structured JSON instead of relying only on free-form text.

### Local-First AI

Ollama provides a local inference option suitable for development and privacy-sensitive educational workflows.

---

# 👩‍💻 Development

To contribute:

```bash
git clone https://github.com/Nishtha-agarwal/Teacher-ai-platform.git
cd Teacher-ai-platform
```

Create a branch:

```bash
git checkout -b feature/your-feature
```

Make your changes and test them.

Then:

```bash
git add .
git commit -m "Add your feature"
git push origin feature/your-feature
```

---

# 📜 License

This project is intended for educational, research, and demonstration purposes.

Add an appropriate open-source license before distributing the project publicly.

---

# 👩‍💻 Author

**Nishtha Agarwal**

Teacher AI Platform — AI-powered educational document intelligence and Teacher Knowledge Package generation.

---

# ⭐ Project Goal

The goal of the Teacher AI Platform is to demonstrate how modern AI engineering techniques can be combined with a modular backend architecture to transform unstructured educational content into useful, structured, classroom-ready knowledge.

```text
Raw Educational Content
          ↓
   Document Intelligence
          ↓
    Knowledge Extraction
          ↓
      AI Reasoning
          ↓
 Structured Teacher Knowledge
          ↓
    Classroom Utility
```

**Built with Python, FastAPI, React, Vite, and Ollama.**
