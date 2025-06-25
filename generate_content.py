import os
import requests
import random
from datetime import date

# ✅ Get Hugging Face token from environment variable
HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct"

HEADERS = {
    "Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}",
    "Content-Type": "application/json"
}

TOPICS = [
    "Data Lake vs Data Warehouse",
    "ETL vs ELT",
    "Stream Processing vs Batch Processing",
    "Data Pipeline Best Practices",
    "Data Quality in Engineering",
    "Metadata Management",
    "Data Orchestration Tools",
    "Cloud Data Engineering Trends",
    "Data Engineering for Machine Learning",
    "Scaling Data Pipelines"
]

def generate_article(topic):
    prompt = f"Write a detailed article about the following Data Engineering topic:\n\n{topic}"
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 700,
            "temperature": 0.7,
            "do_sample": True
        }
    }

    response = requests.post(API_URL, headers=HEADERS, json=payload)

    if response.status_code != 200:
        print(f"❌ Error: {response.status_code} - {response.text}")
        raise Exception("Failed to generate content")

    json_data = response.json()
    text = json_data[0]["generated_text"] if isinstance(json_data, list) else json_data.get("generated_text", "")

    return text.strip()

def save_article(topic, content):
    safe_topic = topic.replace(" ", "_").replace("/", "_")
    today = date.today().isoformat()
    filename = f"Data_Engineering_{safe_topic}_{today}.md"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# {topic}\n\n{content}\n")
    
    print(f"✅ Article saved as: {filename}")

def main():
    topic = random.choice(TOPICS)
    print(f"🧠 Selected topic: {topic}")
    
    content = generate_article(topic)
    print(f"✅ Content generated.\n")
    
    save_article(topic, content)

if __name__ == "__main__":
    main()
