from app.modules.ai.groq_service import GroqService

service = GroqService()

response = service.generate(
    "Say Hello from Groq."
)

print(response)