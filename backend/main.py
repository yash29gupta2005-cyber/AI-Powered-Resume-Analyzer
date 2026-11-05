
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import tempfile
import os

from backend.resume_parser import extract_resume_text
from backend.skill_extractor import compare_skills
from backend.matcher import calculate_match_score
from backend.database import (
    save_analysis,
    get_analysis_history,
    delete_analysis,
    get_dashboard_stats
)


app = FastAPI(
    title="AI Resume Analyzer",
    description="Analyze resumes and match them with job descriptions.",
    version="1.0.0"
)


# Allow frontend requests during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "AI Resume Analyzer API is running!"
    }

@app.get("/history")
def analysis_history():
    """
    Retrieve previous resume analysis records.
    """
    history = get_analysis_history()

    return {
        "success": True,
        "total_records": len(history),
        "history": history
    }

@app.get("/dashboard-stats")
def dashboard_stats():
    """
    Retrieve dashboard statistics.
    """
    stats = get_dashboard_stats()

    if stats is None:
        raise HTTPException(
            status_code=500,
            detail="Unable to retrieve dashboard statistics."
        )

    return {
        "success": True,
        "stats": stats
    }

@app.delete("/history/{analysis_id}")
def delete_analysis_record(analysis_id: int):
    """
    Delete a specific analysis record.
    """
    result = delete_analysis(analysis_id)

    if result is None:
        raise HTTPException(
            status_code=500,
            detail="Database connection or deletion failed."
        )

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Analysis record not found."
        )

    return {
        "success": True,
        "message": "Analysis deleted successfully."
    }

@app.post("/analyze")
async def analyze_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    if not resume.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF resumes are supported."
        )

    if not job_description.strip():
        raise HTTPException(
            status_code=400,
            detail="Job description cannot be empty."
        )

    temp_path = None

    try:
        file_content = await resume.read()

        if not file_content:
            raise HTTPException(
                status_code=400,
                detail="Uploaded PDF is empty."
            )

        # Save uploaded PDF temporarily
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as temp_file:
            temp_file.write(file_content)
            temp_path = temp_file.name

        # Extract resume text
        resume_text = extract_resume_text(temp_path)

        if not resume_text:
            raise HTTPException(
                status_code=400,
                detail="No readable text found in the PDF."
            )

        # Extract and compare skills
        skill_result = compare_skills(
            resume_text,
            job_description
        )

        # Calculate ML similarity score
        match_score = calculate_match_score(
            resume_text,
            job_description
        )

        save_analysis(
    filename=resume.filename,
    match_score=match_score,
    resume_skills=skill_result["resume_skills"],
    required_skills=skill_result["required_skills"],
    matched_skills=skill_result["matched_skills"],
    missing_skills=skill_result["missing_skills"]
)

        return {
            "success": True,
            "filename": resume.filename,
            "match_score": match_score,
            "resume_skills": skill_result["resume_skills"],
            "required_skills": skill_result["required_skills"],
            "matched_skills": skill_result["matched_skills"],
            "missing_skills": skill_result["missing_skills"],
            "resume_text": resume_text
        }

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Resume analysis failed: {str(error)}"
        )

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
