import json
import os
import pandas as pd
from playwright.sync_api import sync_playwright

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

def extract_clubsbuilder_data():
    print("[*] Iniciando extração de dados do ClubsBuilder...")
    
    with sync_playwright() as p:
        # Lança o navegador Chromium em modo headless
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        captured_data = {}

        # Intercepta as chamadas de API e payloads de dados do Next.js
        def handle_response(response):
            url = response.url
            if "json" in response.headers.get("content-type", "") or "/_next/data/" in url:
                try:
                    json_data = response.json()
                    file_name = url.split("/")[-1].split("?")[0] or "payload.json"
                    captured_data[file_name] = json_data
                    print(f"  [+] Capturado payload: {file_name}")
                except Exception:
                    pass

        page.on("response", handle_response)

        # Acessa o site e aguarda o carregamento das redes e scripts JS
        page.goto("https://clubsbuilder.com/", wait_until="networkidle")
        
        # Interage levemente com a página para forçar a hidratação dos estados de atributos
        page.wait_for_timeout(3000)

        # Salva o dump de dados em arquivo bruto
        raw_json_path = os.path.join(DATA_DIR, "raw_clubsbuilder.json")
        with open(raw_json_path, "w", encoding="utf-8") as f:
            json.dump(captured_data, f, indent=2, ensure_ascii=False)
            
        print(f"[✓] Dados brutos salvos em: {raw_json_path}")
        browser.close()

def process_and_generate_csv():
    """
    Lê o JSON capturado e consolida nas tabelas Nível 1 (Base) e Nível Máx (Meta)
    """
    raw_json_path = os.path.join(DATA_DIR, "raw_clubsbuilder.json")
    if not os.path.exists(raw_json_path):
        print("[-] Arquivo bruto não encontrado para processamento.")
        return

    with open(raw_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Exemplo de consolidação para DataFrame (Ajuste as chaves conforme a estrutura capturada)
    # Aqui montamos a estrutura pronta para o Streamlit
    records = []
    
    # Processamento e normalização dos atributos
    # ... (Conversão de JSON para formato tabular Pandas) ...

    # Salva arquivos limpos para o Streamlit consumir diretamente
    # data/attributes_lvl1.csv e data/attributes_meta.csv

if __name__ == "__main__":
    extract_clubsbuilder_data()
    process_and_generate_csv()
