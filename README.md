# AI-Powered Resume Analyzer & Job Matcher

An AI-powered web application that analyzes resumes, extracts technical
skills, compares them against job descriptions, and calculates a
resume-job similarity score using Machine Learning.

## Features

- PDF Resume Parsing
- Automatic Technical Skill Extraction
- Skill Matching and Gap Analysis
- TF-IDF Based Resume-Job Similarity
- Match Score Visualization
- Analysis History Management
- Delete Previous Analyses
- Dashboard Statistics
- MySQL Database Integration

## Technology Stack

### Backend
- Python
- FastAPI
- Scikit-learn
- PyPDF
- MySQL Connector

### Frontend
- HTML5
- CSS3
- JavaScript
- Chart.js

### Database
- MySQL

## Project Structure

Resume-Analyzer/
- backend/
  - main.py
  - resume_parser.py
  - skill_extractor.py
  - matcher.py
  - database.py
- frontend/
  - index.html
  - style.css
  - script.js
- tests/
- requirements.txt
- .gitignore
- README.md

## Installation and Setup

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd Resume-Analyzer
