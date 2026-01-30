"""Interview data parser."""

import json
from pathlib import Path

from llm_ta.models.interview import Interview, InterviewResponse, InterviewCollection


class InterviewParser:
    """Parser for interview JSON data."""
    
    @staticmethod
    def parse_file(path: Path) -> InterviewCollection:
        """Parse interview data from a JSON file."""
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    return InterviewCollection(interviews=[])
                data = json.loads(content)
        except json.JSONDecodeError:
            # Return empty collection or could raise proper error
            print(f"Warning: Failed to decode JSON from {path}")
            return InterviewCollection(interviews=[])
        
        interviews = []
        
        # Handle list of interviews
        if isinstance(data, list):
            for item in data:
                interview = InterviewParser._parse_interview(item)
                interviews.append(interview)
        # Handle single interview
        elif isinstance(data, dict):
            interview = InterviewParser._parse_interview(data)
            interviews.append(interview)
        
        return InterviewCollection(interviews=interviews)
    
    @staticmethod
    def _parse_interview(data: dict) -> Interview:
        """Parse a single interview from dict."""
        participant_id = data.get("participant_id", "P00")
        
        responses = []
        raw_responses = data.get("responses", [])
        
        for resp in raw_responses:
            responses.append(InterviewResponse(
                question=resp.get("question", ""),
                answer=resp.get("answer", ""),
            ))
        
        return Interview(
            participant_id=participant_id,
            responses=responses,
        )
    
    @staticmethod
    def save_collection(collection: InterviewCollection, path: Path) -> None:
        """Save interview collection to JSON file."""
        data = []
        for interview in collection.interviews:
            data.append({
                "participant_id": interview.participant_id,
                "responses": [
                    {"question": r.question, "answer": r.answer}
                    for r in interview.responses
                ]
            })
        
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
