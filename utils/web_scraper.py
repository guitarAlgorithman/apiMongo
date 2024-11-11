# utils/web_scraper.py
import requests
from bs4 import BeautifulSoup
from database import questions_collection  # Asegúrate de importar la colección desde database.py

def fetch_and_save_web_data():
    url = "https://www.billetesymonedas.cl/home/preguntasfrecuentes"
    response = requests.get(url)
    if response.status_code != 200:
        print("Error al acceder a la página:", response.status_code)
        return

    soup = BeautifulSoup(response.content, 'html.parser')
    questions = soup.find_all('p', class_='pregunta')
    answers = soup.find_all('blockquote', class_='respuesta')
    min_len = min(len(questions), len(answers))

    web_data = []
    for i in range(min_len):
        question_text = questions[i].text.strip()
        answer_text = answers[i].text.strip()

        # Revisa si la pregunta ya existe en MongoDB
        existing_question = questions_collection.find_one({"question": question_text})
        if not existing_question:
            # Solo guarda si la pregunta no está en la base de datos
            questions_collection.insert_one({"question": question_text, "answer": answer_text})
            print(f"Insertado en MongoDB: {question_text}")
        else:
            print(f"Pregunta ya existe en MongoDB: {question_text}")

# Ejecuta el scraping y guarda los datos si no son duplicados
if __name__ == "__main__":
    fetch_and_save_web_data()
