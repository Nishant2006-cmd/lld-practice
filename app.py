import pdfplumber

from flask import Flask, request, render_template, jsonify
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
app = Flask(__name__)
def evaluate_design(submission):
    reference = "class interface manager controller extends implements strategy pattern"
    documents = [reference, submission]
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(documents)
    score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()[0]
    percentage = round(float(score) * 100, 2)

    deterministic = []
    if "class" in submission.lower():
        deterministic.append("✅ Classes defined")
    else:
        deterministic.append("⚠️ No classes found")

    if "interface" in submission.lower():
        deterministic.append("✅ Interfaces used")
    else:
        deterministic.append("⚠️ No interfaces found")

    if "manager" in submission.lower() or "controller" in submission.lower():
        deterministic.append("✅ Separation of responsibilities")
    else:
        deterministic.append("⚠️ Consider adding a Manager/Controller class")

    ai_feedback = "💡 Suggestion: Use Strategy pattern for fee calculation."

    return {"score": percentage, "deterministic": deterministic, "aiFeedback": ai_feedback}

def extract_text_from_pdf(file):
    """
    Safely extract text from a PDF.
    Returns empty string if the PDF cannot be read.
    """
    try:
        text = ""

        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

        return text
    except Exception as e:
        print("PDF ERROR:", e)
        return ""
def filter_resume_text(text):
    """
    Keep important resume sections for comparison.
    """

    keep_sections = []

    keywords = [
        "education",
        "cgpa",
        "technical skills",
        "skills",
        "projects",
        "experience",
        "internship",
        "certification",
        "achievements"
    ]

    for line in text.splitlines():

        line_lower = line.lower()

        if any(keyword in line_lower for keyword in keywords):
            keep_sections.append(line)

    return " ".join(keep_sections)
@app.route("/attempt", methods=["POST"])
def submit_attempt():
    submission = request.form.get("submissionContent", "").strip()
    if not submission:
        return render_template("index.html", results=None, error="Please enter your design/code.")

    feedback = evaluate_design(submission)
    return render_template("index.html", results=feedback)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            # Get learner submission from form
            problem_id = request.form.get("problemId", "").strip()
            submission = request.form.get("submissionContent", "").strip()

            if not submission:
                return render_template("index.html", results=None, error="Please enter your design/code.")

            # Run evaluator
            feedback = evaluate_design(submission)

            # Attach problem info if needed
            feedback["problemId"] = problem_id

            return render_template("index.html", results=feedback)

        except Exception as e:
            print("\n================================")
            print("SERVER ERROR:")
            print(e)
            print("================================\n")
            return render_template("index.html", results=None, error="Something went wrong while processing the submission. Please try again.")

    return render_template("index.html", results=None)



    return render_template(
             "index.html",
        results=None
    )# actully i build same project before ai-hr requirter so i enhanced it for lld project 

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000)) 
    app.run(host="0.0.0.0", port=port, debug=True)
