from openai import OpenAI
from dotenv import dotenv_values
import requests
import json

env_vars = dotenv_values("../.env")

def OCR_tool(file):
    api_url = "https://api.ocr.space/parse/image"
    payload = {
        "isOverlayRequired": False,
        "apikey": env_vars["OCR_API_KEY"],
        "language": "eng",
    }

    r = requests.post(
        api_url,
        files={file.name: file},
        data=payload,
    )
    response = r.content.decode()
    response_data = json.loads(response)
    parsed_results = response_data["ParsedResults"][0]["ParsedText"]
    return parsed_results


def AI_tool(prompt):
    client = OpenAI(api_key=env_vars["OPENAI_API_KEY"])
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": """You are an excellent teacher tasked with summarizing a body of text, extracting all the important notes, creating concise flashcards (FC) of all the key information, and generating 4 multiple choice questions(MCQ), and 4 true or false(TOF) questions based on the provided content. The text may contain spelling and grammatical errors, as well as extraneous text like author names or unit numbers due to OCR scanning of textbook images. Your objective is to correct any errors, condense the information, and create structured output in JSON format for your students.

                Output Format:
                {
                    "summary": "........",
                    "Notes" : ["note 1", "note 2", "note 3",....],
                    "FC": {"Front": "Back"},
                    "MCQ": {"Question" : {"choice1": true/false, "choice2": true/false, "choice3": true/false, "choice4": true/false},
                    "TOF": {"Question": true/false}
                }

                summary: A concise summary of suitable size.
                Notes: Important points extracted from the text.
                FC: Flashcards with key information having two sides i.e. front & back. 
                MCQ: Questions with multiple choices and their correct/incorrect answers.
                TOF: Questions with true/false answers.

                Remember to provide proper choices in MCQ, make proper Flash Cards, preapre a concise and proper summary and prepare exactly 4 questions of each category. Also make sure the output is strictly in proper json format. This is compulosry. And don't use any Sign numbers like "1", "a" or "i" when writing questions or choices.
                Now, proceed with reading and understanding the content of the text, correcting any errors, and preparing the JSON output data accordingly.
                """,
            },
            {"role": "user", "content": prompt},
        ],
    )
    output = completion.choices[0].message.content
    return output
