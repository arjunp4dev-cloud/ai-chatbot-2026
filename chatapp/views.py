import json
import requests
from django.http import JsonResponse, StreamingHttpResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


def home(request):
    return HttpResponse(
        "<h2>✅ Local AI Chatbot backend running</h2>"
        "<p>Open <code>/chat/</code></p>"
    )


def chat_page(request):
    return render(request, "chatapp/chat.html")


@csrf_exempt
def chat_api(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)

    try:
        body = json.loads(request.body.decode())
        message = body.get("message", "").strip()
        model = body.get("model", "qwen3:4b")
        system_prompt = body.get("system_prompt", "")
    except Exception:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    if not message:
        return JsonResponse({"error": "Empty message"}, status=400)

    def stream():
        payload = {
            "model": model,
            "stream": True,
            "messages": []
        }

        if system_prompt:
            payload["messages"].append({
                "role": "system",
                "content": system_prompt
            })

        payload["messages"].append({
            "role": "user",
            "content": message
        })

        with requests.post(
            "http://localhost:11434/api/chat",
            json=payload,
            stream=True,
            timeout=300
        ) as r:
            for line in r.iter_lines():
                if line:
                    data = json.loads(line.decode("utf-8"))
                    if "message" in data:
                        yield data["message"]["content"]

    return StreamingHttpResponse(stream(), content_type="text/plain")
