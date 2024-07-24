from fastapi import FastAPI, UploadFile, File
import openai
from pypdf import PdfReader
import io


openai.api_key = 'sk-proj-OkHHllUSWWFRlwHpOzw3T3BlbkFJfIwZKGT9xHMvAoaSM3Uv'


app = FastAPI()
@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    contents = await file.read()
    pdf_reader = PdfReader(io.BytesIO(contents))
    text = ""
    for page in pdf_reader.pages:
        text = text + page.extract_text()
    return {"content": text}


@app.post("/query/")
async def query(question: str, pdf_content: str):
    response = openai.Completion.create(
        engine="davinci",
        reading_data=f"Context: {pdf_content}\nQuestion: {question}\nAnswer:",
        max_tokens=150
    )
    return {"response": response.choices[0].text.strip()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
