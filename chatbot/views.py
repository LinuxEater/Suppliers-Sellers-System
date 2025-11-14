from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.clickjacking import xframe_options_exempt
import json
from .utils import call_gemini_api

@xframe_options_exempt # Allow embedding in iframe
def chatbot_view(request):
    return render(request, 'chatbot/chatbot.html')

@csrf_exempt
@login_required
def chatbot_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')

            if not user_message:
                return JsonResponse({'response': 'Por favor, digite uma mensagem.'}, status=400)

            # Call Gemini API
            ai_response, sources = call_gemini_api(user_message)

            # Format sources if any
            formatted_sources = ""
            if sources:
                formatted_sources = "\n\n**Fontes:**\n"
                for i, source in enumerate(sources):
                    formatted_sources += f"- [{source['title']}]({source['uri']})\n"
            
            full_response = ai_response + formatted_sources

            return JsonResponse({'response': full_response})
        except json.JSONDecodeError:
            return JsonResponse({'response': 'Requisição inválida.'}, status=400)
    return JsonResponse({'response': 'Método não permitido.'}, status=405)