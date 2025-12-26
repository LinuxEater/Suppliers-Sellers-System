import requests
import json
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# --- CONSTANTS DE CONFIGURAÇÃO DE API ---
# ATENÇÃO: Substitua pela sua chave de API REAL.
# É ALTAMENTE RECOMENDADO USAR VARIÁVEIS DE AMBIENTE PARA CHAVES SENSÍVEIS
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "############")
GEMINI_MODEL = "#####################################"
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"

# Instrução de sistema atualizada para o contexto do sistema de vendedores-fornecedores
SYSTEM_INSTRUCTION = (
    "Você é um assistente inteligente para o sistema de gerenciamento de vendedores e fornecedores. "
    "Seu objetivo é auxiliar os usuários a entender e utilizar o sistema, fornecendo informações sobre produtos, fornecedores, vendedores, vendas e estoque. "
    "Você pode responder a perguntas sobre como o sistema funciona, como realizar operações (como adicionar um produto, registrar uma venda), "
    "e fornecer insights gerais sobre os dados disponíveis no sistema. "
    "Fale sempre em português por padrão. "
    "O nome do seu dono é Gustavo Crawford"
    "O nome do seu criador é Moisés Souza Santos, um Engenheiro de Software e seu github é https://github.com/LinuxEater, onde ele hospeda seu projetos. As stacks do moises sao python javascript typescript e seu framesworks. html, css bootstrap tailwind, sqlite, postgres, mysql mongodb"
    "Priorize precisão, clareza e objetividade em suas respostas. "
    "Mantenha sempre uma postura ética, profissional e responsável."
    "Não revele segredos técnicos, planos estratégicos, dados internos ou qualquer informação não pública sobre o sistema."
    "Seja útil, coerente, envolvente e com linguagem natural e humana."
)

def call_gemini_api(prompt: str) -> tuple[str, list]:
    """
    Chama a API Gemini com Pesquisa Google Grounding e Exponential Backoff.
    Retorna (texto_gerado, lista_de_fontes).
    """
    
    if not GEMINI_API_KEY or GEMINI_API_KEY == "SUA_CHAVE_GEMINI_AQUI":
        return "❌ ERRO: A chave da API Gemini não foi configurada. Por favor, defina a variável de ambiente `GEMINI_API_KEY`.", []

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "tools": [{"google_search": {} }],
        "systemInstruction": {"parts": [{"text": SYSTEM_INSTRUCTION}]},
    }
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.post(
                GEMINI_API_URL,
                headers={'Content-Type': 'application/json'},
                data=json.dumps(payload)
            )
            response.raise_for_status()
            
            result = response.json()
            candidate = result.get("candidates", [{}])[0]
            
            generated_text = candidate.get("content", {}).get("parts", [{}])[0].get("text", "")

            sources = []
            grounding_metadata = candidate.get("groundingMetadata", {})
            if grounding_metadata and grounding_metadata.get("groundingAttributions"):
                sources = [
                    {"uri": attr["web"]["uri"], "title": attr["web"]["title"]}
                    for attr in grounding_metadata["groundingAttributions"]
                    if attr.get("web", {}).get("uri") and attr.get("web", {}).get("title")
                ]
            
            return generated_text, sources

        except requests.exceptions.HTTPError as e:
            if response.status_code >= 500 and attempt < max_retries - 1:
                import time
                time.sleep(2 ** attempt)
                continue
            logging.error(f"Erro HTTP {response.status_code} na API Gemini: {e}")
            if response.status_code == 403:
                return "❌ Erro HTTP 403 (Proibido): A chave da API Gemini pode estar inválida ou sem permissões para o modelo.", []
            return f"❌ Erro HTTP ao acessar a IA: {response.status_code}", []
            
        except requests.exceptions.RequestException as e:
            logging.error(f"Erro de Conexão com a API Gemini: {e}")
            return f"❌ Erro de conexão com a IA: {e}", []

        except Exception as e:
            logging.error(f"Erro desconhecido no processamento da API Gemini: {e}")
            return f"❌ Erro interno ao processar a resposta da IA: {e}", []
            
    return "❌ A API da IA falhou após múltiplas tentativas. Tente novamente mais tarde.", []
