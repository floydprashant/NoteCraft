from django.shortcuts import render, redirect
from django.http import HttpResponse
from .utils import OCR_tool, AI_tool
import time, json
# Create your views here.


def index(request):
    return render(request, "notecraft/index.html")


def image2text(request):
    result = ""
    if request.method == "POST":
        images = request.FILES.getlist("images")

        if len(images) > 0:
            for image in images:
                if image.size > 1000000:
                    return HttpResponse(
                        f"{image.name} is larger than 1 MB. Please upload a smaller image."
                    )
                text = OCR_tool(image)
                if text:
                    result += text
                    result += " "
                else:
                    return HttpResponse(f"Couldnt read the text from {image.name}")

        return render(request, "notecraft/OCR.html", {"text": result})
    return redirect("index")


def text2QNA(request):
    if request.method == "POST":
        prompt = request.POST.get("ai_prompt")
        response = AI_tool(prompt)
        output = response[0]
        count = 1
        while count <= 5:
            try:
                json_output = json.loads(output)
                first_key = next(iter(json_output["MCQ"]))
                if (
                    "A" in json_output["MCQ"][first_key]
                    or "a" in json_output["MCQ"][first_key]
                ):
                    raise ValueError("Invalid Output: Wrong MCQ choices")
                elif "Question1" in json_output["TOF"]:
                    raise ValueError("Invalid Output: Wrong TOF questions")
                break
            except Exception as e:
                count += 1
                json_output = None
                time.sleep(2)
                if "Wrong MCQ choices" in str(e):
                    output = AI_tool(
                        prompt
                        + "\nRemember the choices in MCQ should not contain any sign numbers like '1', 'a' or 'i'."
                    )
                elif "Wrong TOF questions" in str(e):
                    output = AI_tool(
                        prompt
                        + "\nRemember to provide proper questions in TOF and MCQ. DOn't mistakenly write just 'Question1' or 'QuestionA' instead of actual questions."
                    )
                else:
                    output = AI_tool(prompt)

        return render(
            request,
            "notecraft/text2QNA.html",
            {"questions": json_output, "count": count, "response": response[1]},
        )
    return redirect("index")
