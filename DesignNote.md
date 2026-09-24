# Design Note

## User Flow
1. Select problem.
2. Submit design/code.
3. Receive feedback (score + checks + AI suggestion).
4. Retry and improve.

## Evaluator Logic
- Deterministic checks: keyword presence.
- Score: TF-IDF similarity against reference keywords.
- AI feedback: mocked suggestions.

## Data Model
- Problems: id, title, description.
- Submissions: learnerId, problemId, content, feedback.
- Feedback: deterministic checks, score, AI suggestion.
