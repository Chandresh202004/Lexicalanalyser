from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List
from fastapi.responses import RedirectResponse

from lexer_no_ai import Lexer

app = FastAPI(title="Lexer (no AI)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
app.mount("/web", StaticFiles(directory="web", html=True), name="web")

# Optional: redirect root to /web
@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/web/")  # you can replace with a RedirectResponse if you want

class TokenOut(BaseModel):
    type: str
    value: str
    line: int
    column: int

class SourceIn(BaseModel):
    code: str

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/api/lex", response_model=List[TokenOut])
async def lex(source: SourceIn):
    lexer = Lexer(source.code)
    tokens = lexer.tokenize()
    return [
        TokenOut(type=t.type, value=t.value, line=t.line, column=t.column)
        for t in tokens if t.type != "NEWLINE"
    ]