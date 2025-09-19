from huggingface_hub import InferenceClient

client = InferenceClient(model="HuggingFaceH4/zephyr-7b-beta")

response = client.text_generation("What is loamy soil?")
print("Bot says:", response)
