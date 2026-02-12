import re
import json
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    "extract-customer-questions",
    instructions=(
        "This server extracts customer questions from call transcripts. "
        "Pass a raw transcript and it returns structured questions with "
        "sentiment and urgency classification."
    ),
)


QUESTION_PATTERN = re.compile(
    r"\[(\d{2}:\d{2})\]\s*(.+?):\s*\n(.*?\?.*?)(?=\n\n|\Z)",
    re.DOTALL,
)

URGENCY_KEYWORDS_HIGH = [
    "critical", "urgent", "blocker", "blocked", "immediately", "asap",
    "downtime", "outage", "failing", "broken", "deadline", "compliance",
    "audit", "security", "breach", "cost", "million", "revenue",
]
URGENCY_KEYWORDS_MEDIUM = [
    "concern", "worried", "timeline", "schedule", "risk", "challenge",
    "important", "priority", "need", "must", "require", "when",
]

NEGATIVE_SENTIMENT_KEYWORDS = [
    "problem", "issue", "fail", "broken", "frustrated", "difficult",
    "struggling", "pain", "slow", "stale", "wrong", "loss", "losing",
    "cost", "expensive", "complex", "manual", "workaround", "escalation",
    "can't", "cannot", "unable", "impossible",
]
POSITIVE_SENTIMENT_KEYWORDS = [
    "great", "excellent", "impressive", "powerful", "love", "excited",
    "confident", "productive", "flexible", "good", "works well",
    "straightforward", "elegant", "efficient",
]


def classify_urgency(text: str) -> str:
    lower = text.lower()
    if any(kw in lower for kw in URGENCY_KEYWORDS_HIGH):
        return "high"
    if any(kw in lower for kw in URGENCY_KEYWORDS_MEDIUM):
        return "medium"
    return "low"


def classify_sentiment(text: str) -> str:
    lower = text.lower()
    neg = sum(1 for kw in NEGATIVE_SENTIMENT_KEYWORDS if kw in lower)
    pos = sum(1 for kw in POSITIVE_SENTIMENT_KEYWORDS if kw in lower)
    if neg > pos:
        return "negative"
    if pos > neg:
        return "positive"
    return "neutral"


def extract_questions_from_text(transcript: str) -> list[dict]:
    """Parse a transcript and pull out lines that contain questions."""
    results = []
    # Split into individual utterances
    blocks = re.split(r"(?=\[\d{2}:\d{2}\])", transcript)

    for block in blocks:
        block = block.strip()
        if not block:
            continue

        # Parse timestamp + speaker + text
        header_match = re.match(
            r"\[(\d{2}:\d{2})\]\s*(.+?):\s*\n(.*)",
            block,
            re.DOTALL,
        )
        if not header_match:
            continue

        timestamp = header_match.group(1)
        speaker = header_match.group(2).strip()
        text = header_match.group(3).strip()

        # Only keep utterances that contain a question
        if "?" not in text:
            continue

        # Extract individual questions from the text
        sentences = re.split(r"(?<=[.!?])\s+", text)
        questions = [s.strip() for s in sentences if "?" in s and len(s.strip()) > 10]

        for q in questions:
            results.append(
                {
                    "timestamp": timestamp,
                    "speaker": speaker,
                    "question": q,
                    "urgency": classify_urgency(q),
                    "sentiment": classify_sentiment(q),
                }
            )

    return results


@mcp.tool()
def extract_customer_questions(transcript: str) -> str:
    """Extract customer questions from a call transcript with sentiment and urgency classification.

    Args:
        transcript: Raw call transcript text with timestamps in [MM:SS] format
                    and speaker labels followed by their dialogue.

    Returns:
        JSON string containing an array of extracted questions, each with:
        - timestamp: when the question was asked (MM:SS)
        - speaker: who asked the question
        - question: the question text
        - urgency: high | medium | low
        - sentiment: positive | neutral | negative
    """
    questions = extract_questions_from_text(transcript)

    summary = {
        "total_questions": len(questions),
        "urgency_breakdown": {
            "high": sum(1 for q in questions if q["urgency"] == "high"),
            "medium": sum(1 for q in questions if q["urgency"] == "medium"),
            "low": sum(1 for q in questions if q["urgency"] == "low"),
        },
        "sentiment_breakdown": {
            "positive": sum(1 for q in questions if q["sentiment"] == "positive"),
            "neutral": sum(1 for q in questions if q["sentiment"] == "neutral"),
            "negative": sum(1 for q in questions if q["sentiment"] == "negative"),
        },
        "questions": questions,
    }

    return json.dumps(summary, indent=2)


@mcp.tool()
def extract_customer_questions_from_file(file_path: str) -> str:
    """Extract customer questions from a transcript file on disk.

    Args:
        file_path: Path to the transcript file to analyze.

    Returns:
        JSON string with extracted questions, urgency, and sentiment.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        transcript = f.read()
    return extract_customer_questions(transcript)


if __name__ == "__main__":
    mcp.run(transport="sse")
