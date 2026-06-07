from datetime import datetime
from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel, Field, field_validator

app = FastAPI(
    title="Notes API",
    description="Week 1 Cloud DevSec Foundation Checkpoint — Modernized Python 3.12 Syntax",
    version="1.2.0"
)

# --------------------------------------------------------
# 1. DATA MODELS & VALIDATORS
# --------------------------------------------------------

class NoteCreate(BaseModel):
    title: str = Field(..., description="The title of the note")
    content: str = Field(..., description="The body content of the note")
    tag: str = Field(default="general", description="Optional filter tag")

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        stripped_value = value.strip()
        if len(stripped_value) < 3:
            raise ValueError("title must be at least 3 characters")
        return stripped_value

    @field_validator("content")
    @classmethod
    def validate_content(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("content cannot be empty")
        return value


class NoteResponse(BaseModel):
    id: int
    title: str
    content: str
    tag: str
    created_at: str

# --------------------------------------------------------
# 2. IN-MEMORY DATABASE & STATE
# --------------------------------------------------------
notes_db: dict[int, NoteResponse] = {}
current_id: int = 1

# --------------------------------------------------------
# 3. API ROUTES (Using Built-in Type Hints)
# --------------------------------------------------------

@app.post(
    "/notes", 
    response_model=NoteResponse, 
    status_code=status.HTTP_201_CREATED,
    summary="Create a new note"
)
def create_note(note_data: NoteCreate):
    global current_id
    
    timestamp = datetime.now().isoformat()
    
    new_note = NoteResponse(
        id=current_id,
        title=note_data.title,
        content=note_data.content,
        tag=note_data.tag,
        created_at=timestamp
    )
    
    notes_db[current_id] = new_note
    current_id += 1
    return new_note


@app.get(
    "/notes", 
    response_model=list[NoteResponse],
    summary="Retrieve all notes"
)
def get_notes(tag: str | None = None):
    # Using python 3.10+ native 'str | None' union representation
    if tag:
        return [note for note in notes_db.values() if note.tag.lower() == tag.lower()]
    return list(notes_db.values())


@app.get(
    "/notes/{note_id}", 
    response_model=NoteResponse,
    summary="Get a single note by ID"
)
def get_note(note_id: int):
    if note_id in notes_db:
        return notes_db[note_id]
            
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"Note with ID {note_id} not found"
    )


@app.delete(
    "/notes/{note_id}", 
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a note by ID"
)
def delete_note(note_id: int):
    if note_id in notes_db:
        notes_db.pop(note_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
            
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"Note with ID {note_id} not found"
    )