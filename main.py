# main.py
import os
import uvicorn
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Dict
from database import questions_collection, save_feedback
from utils.web_scraper import fetch_and_save_web_data  # Asegúrate de que esta función esté importada
from transformers import pipeline

app = FastAPI()

# Inicializa el pipeline de QA
qa_pipeline = pipeline('question-answering', model="mrm8488/bert-base-spanish-wwm-cased-finetuned-spa-squad2-es")

class QuestionRequest(BaseModel):
    question: str

class FeedbackRequest(BaseModel):
    question: str
    chosen_answer: str

@app.on_event("startup")
async def startup_event():
    print("Inicio de la aplicación: ejecutando scraping de datos de la web...")
    await fetch_and_save_web_data()  # Ejecuta el scraping y guarda en MongoDB si no hay duplicados
    print("Datos de la web procesados.")

def get_ranked_answers(question: str, context_list: List[str]):
    ranked_answers = []
    for context in context_list:
        result = qa_pipeline(question=question, context=context)
        ranked_answers.append({'answer': result['answer'], 'score': result['score']})
    return sorted(ranked_answers, key=lambda x: x['score'], reverse=True)

@app.post("/ask")
async def ask_question(request: QuestionRequest):
    question = request.question
    all_answers = []

    # Recupera todas las respuestas en MongoDB
    docs = await questions_collection.find().to_list(length=100)  # Obtiene los documentos en formato de lista
    for doc in docs:
        if "answer" in doc:
            all_answers.append(doc["answer"])

    if not all_answers:
        raise HTTPException(status_code=404, detail="No se encontraron respuestas en la base de datos.")

    # Clasifica las respuestas usando el modelo de QA
    ranked_answers = get_ranked_answers(question, all_answers)
    return {
        "question": question,
        "answers": [{"answer": ans["answer"], "score": ans["score"]} for ans in ranked_answers[:5]],
        "next_page": 1
    }

@app.post("/feedback")
async def feedback(request: FeedbackRequest):
    await save_feedback(request.question, request.chosen_answer)
    return {"message": "Feedback guardado con éxito"}

@app.get("/")
async def home():
    return {"message": "Hola"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
