# TODO: Add others supported models

PREM_MODELS = {"vicuna-7b": 8111, "gpt4all-lora-q4": 8222}

AI_PROVIDERS = ["openai", "premai"]
AUTH_METHODS = ["matador", "aperture"]
PROXIES = {
    'matador': ["http://localhost:8080", 'https://matador.cashai.space', "https://matador.kody.repl.co", "Add"],
    'aperture': ["https://localhost:8081", 'https://aperture.cashai.space:8081', "Add"]
}
MODELS = {
    "openai": ["gpt-3.5-turbo", "gpt-4"],
    "premai": ["gpt4all-lora-q4", "vicuna-7b"],
}

TOKEN_LIMIT = 512
