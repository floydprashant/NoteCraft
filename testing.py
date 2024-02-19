import requests
import json
from openai import OpenAI
from dotenv import dotenv_values
import time

env_vars = dotenv_values("./.env")


def OCR_tool(file):
    api_url = "https://api.ocr.space/parse/image"
    api_key = "bdae3e26c988957"
    payload = {
        "isOverlayRequired": False,
        "apikey": api_key,
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
                "content": """You are tasked with summarizing a body of text, extracting all the important notes, creating concise flashcards (FC) of all the key information, and generating 4 multiple choice questions(MCQ), and 4 true or false(TOF) questions based on the provided content. The text may contain spelling and grammatical errors, as well as extraneous text like author names or unit numbers due to OCR scanning of textbook images. Your objective is to correct any errors, condense the information, and create structured output in JSON format.

                Output Format:
                {
                    "summary": "........",
                    "Notes" : ["note 1", "note 2", "note 3", "..."],
                    "FC": {"Front": "Back"},
                    "MCQ": {"Question" : {"choice1": true/false, "choice2": true/false, "..."}},
                    "TOF": {"Question": true/false}
                }

                summary: A concise summary having approximately 1/4th size of the body of text.
                Notes: Important points extracted from the text.
                FC: Flashcards with key information having two sides i.e. front & back. 
                MCQ: Questions with multiple choices and their correct/incorrect answers.
                TOF: Questions with true/false answers.

                Remember top provide proper choices in MCQ, maintain the length of summary and prepare exactly 4 questions of each category. Also make sure the output is strictly in proper json format. This is compulosry. And don't use any Sign numbers like "1", "a" or "i" when writing questions or choices.
                Now, proceed with reading and understanding the content of the text, correcting any errors, and preparing the JSON output data accordingly.
                """,
            },
            {"role": "user", "content": prompt},
        ],
    )
    count = 1
    output = completion.choices[0].message.content
    while(count <= 5):
        try:
            json_output = json.loads(output)
            first_key = next(iter(json_output['MCQ']))
            if "A" in json_output['MCQ'][first_key] or "a" in json_output['MCQ'][first_key]:
                raise Exception
            break
        except:

            count+=1
            time.sleep(2) 
    print([json_output, count])

AI_tool(''' CHAPTER 1. Down the Rabbit-Hole
Alice was beginning to get very tired of sitting by her sister on the
bank, and of having nothing to do: once or twice she had peeped
into the book her sister was reading, but it had no pictures or
conversations in it, 'and what is the use of a book,' thought Alice
'without pictures or conversation?'
So she was considering in her own mind (as well as she could, for
the hot day made her feel very sleepy and stupid), whether the
pleasure of making a daisy-chain would be worth the trouble of
getting up and picking the daisies, when suddenly a White Rabbit
with pink eyes ran close by her.
There was nothing so VERY remarkable in that; nor did Alice think
it so VERY much out of the way to hear the Rabbit say to itself, 'Oh
dear! Oh dear! I shall be late!' (when she thought it over
afterwards, it occurred to her that she ought to have wondered at
this, but at the time it all seemed quite natural); but when the
Rabbit actually TOOK A WATCH OUT OF ITS WAISTCOAT-POCKET,
and looked at it, and then hurried on, Alice started to her feet, for
it flashed across her mind that she had never before seen a rabbit
with either a waistcoat-pocket, or a watch to take out of it, and
burning with curiosity, she ran across the field after it, and
fortunately was just in time to see it pop down a large rabbit-hole
under the hedge.
In another moment down went Alice after it, never once
considering how in the world she was to get out again.
The rabbit-hole went straight on like a tunnel for some way, and
then dipped suddenly down, so suddenly that Alice had not a
moment to think about stopping herself before she found herself
falling down a very deep well.
 ''')