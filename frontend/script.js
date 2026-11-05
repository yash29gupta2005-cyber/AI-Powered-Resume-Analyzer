
// ========================================
// DOM ELEMENTS
// ========================================

const analyzerForm = document.getElementById("analyzerForm");

const resumeInput = document.getElementById("resume");

const jobDescriptionInput =
    document.getElementById("jobDescription");

const analyzeBtn = document.getElementById("analyzeBtn");

const statusMessage = document.getElementById("statusMessage");

const resultsSection = document.getElementById("results");


// ========================================
// API URL
// ========================================

const API_URL = "http://127.0.0.1:8000/analyze";


// ========================================
// DISPLAY SKILLS
// ========================================

function displaySkills(elementId, skills) {

    const list = document.getElementById(elementId);

    list.replaceChildren();

    if (!skills || skills.length === 0) {

        const item = document.createElement("li");
        item.textContent = "No skills found";

        list.appendChild(item);

        return;
    }

    skills.forEach(skill => {

        const item = document.createElement("li");

        item.textContent = skill;

        list.appendChild(item);

    });
}


// ========================================
// DISPLAY ANALYSIS RESULTS
// ========================================

function displayResults(data) {

    document.getElementById("matchScore").textContent =
        data.match_score + "%";

    displaySkills(
        "resumeSkills",
        data.resume_skills
    );

    displaySkills(
        "requiredSkills",
        data.required_skills
    );

    displaySkills(
        "matchedSkills",
        data.matched_skills
    );

    displaySkills(
        "missingSkills",
        data.missing_skills
    );

    document.getElementById("resumeText").textContent =
        data.resume_text;

    resultsSection.classList.remove("hidden");

    resultsSection.scrollIntoView({
        behavior: "smooth"
    });

    // Skill Gap Chart
const chartCanvas = document.getElementById("skillGapChart");

if (window.skillGapChartInstance) {
    window.skillGapChartInstance.destroy();
}

window.skillGapChartInstance = new Chart(chartCanvas, {
    type: "doughnut",
    data: {
        labels: ["Matched Skills", "Missing Skills"],
        datasets: [{
            data: [
                data.matched_skills.length,
                data.missing_skills.length
            ],
            backgroundColor: ["#16a34a", "#ef4444"],
            borderWidth: 0
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: true,
        plugins: {
            legend: {
                position: "bottom"
            }
        }
    }
});
}


// ========================================
// FORM SUBMISSION
// ========================================

analyzerForm.addEventListener("submit", async function (event) {

    event.preventDefault();

    const resumeFile = resumeInput.files[0];

    const jobDescription =
        jobDescriptionInput.value.trim();


    // Validate resume

    if (!resumeFile) {

        statusMessage.textContent =
            "Please upload your resume.";

        return;
    }


    if (
        resumeFile.type !== "application/pdf" &&
        !resumeFile.name.toLowerCase().endsWith(".pdf")
    ) {

        statusMessage.textContent =
            "Please upload a PDF file.";

        return;
    }


    // Validate job description

    if (!jobDescription) {

        statusMessage.textContent =
            "Please enter a job description.";

        return;
    }


    // Prepare form data

    const formData = new FormData();

    formData.append("resume", resumeFile);

    formData.append(
        "job_description",
        jobDescription
    );


    // Show loading state

    analyzeBtn.disabled = true;

    analyzeBtn.textContent = "Analyzing...";

    statusMessage.textContent =
        "Analyzing your resume. Please wait...";

    resultsSection.classList.add("hidden");


    try {

        // Send request to FastAPI

        const response = await fetch(API_URL, {

            method: "POST",

            body: formData

        });


        const data = await response.json();


        // Handle API errors

        if (!response.ok) {

            throw new Error(
                data.detail || "Resume analysis failed."
            );

        }


        // Display results

        displayResults(data);

// Refresh analysis history after successful analysis
await loadAnalysisHistory();

statusMessage.textContent = "Resume analyzed successfully!";


    } catch (error) {

        console.error("Analysis Error:", error);

        statusMessage.textContent =
            "Error: " + error.message;

    } finally {

        // Restore button

        analyzeBtn.disabled = false;

        analyzeBtn.textContent = "Analyze Resume";

    }

});

// Analysis History Functionality

const loadHistoryBtn = document.getElementById("loadHistoryBtn");
const historyTableBody = document.getElementById("historyTableBody");
const historyStatus = document.getElementById("historyStatus");

async function loadAnalysisHistory() {
    loadHistoryBtn.disabled = true;
    loadHistoryBtn.textContent = "Loading...";
    historyStatus.textContent = "Fetching analysis history...";

    try {
        const response = await fetch("http://127.0.0.1:8000/history");

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Unable to load history.");
        }

        historyTableBody.replaceChildren();

        if (data.history.length === 0) {
            historyStatus.textContent = "No analysis history found.";
            return;
        }

        data.history.forEach(record => {
            const row = document.createElement("tr");

            const values = [
                record.id,
                record.filename,
                record.match_score + "%",
                record.matched_skills || "None",
                record.missing_skills || "None",
                new Date(record.created_at).toLocaleString()
            ];

           // Create normal table cells
values.forEach(value => {
    const cell = document.createElement("td");
    cell.textContent = value;
    row.appendChild(cell);
});

// Create Action cell
const actionCell = document.createElement("td");

const deleteBtn = document.createElement("button");
deleteBtn.textContent = "Delete";
deleteBtn.classList.add("delete-btn");

deleteBtn.addEventListener("click", function () {
    deleteAnalysis(record.id);
});

actionCell.appendChild(deleteBtn);
row.appendChild(actionCell);

historyTableBody.appendChild(row);
        });

        historyStatus.textContent =
            "Total analyses found: " + data.total_records;

    } catch (error) {
        console.error("History Error:", error);
        historyStatus.textContent = "Error: " + error.message;

    } finally {
        loadHistoryBtn.disabled = false;
        loadHistoryBtn.textContent = "Load Analysis History";
    }
}

loadHistoryBtn.addEventListener("click", loadAnalysisHistory);

// Automatically load analysis history when the page opens
loadAnalysisHistory();

// Delete an analysis record
async function deleteAnalysis(analysisId) {

    const confirmed = confirm(
        "Are you sure you want to delete this analysis?"
    );

    if (!confirmed) {
        return;
    }

    try {
        const response = await fetch(
            `http://127.0.0.1:8000/history/${analysisId}`,
            {
                method: "DELETE"
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Deletion failed.");
        }

        alert("Analysis deleted successfully!");

        // Refresh history after deletion
        await loadAnalysisHistory();

    } catch (error) {
        console.error("Delete Error:", error);
        alert("Error: " + error.message);
    }
}

// Dashboard Statistics
async function loadDashboardStats() {
    try {
        const response = await fetch(
            "http://127.0.0.1:8000/dashboard-stats"
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error("Unable to load dashboard statistics.");
        }

        const stats = data.stats;

        document.getElementById("totalAnalyses").textContent =
            stats.total_analyses;

        document.getElementById("averageScore").textContent =
            stats.average_score + "%";

        document.getElementById("bestScore").textContent =
            stats.best_score + "%";

        document.getElementById("analysesToday").textContent =
            stats.analyses_today;

    } catch (error) {
        console.error("Dashboard Statistics Error:", error);
    }
}

// Load statistics when the page opens
loadDashboardStats();
