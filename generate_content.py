import os
import requests
import random
from datetime import date

# Get Hugging Face token from environment variable
HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"

HEADERS = {
    "Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}",
    "Content-Type": "application/json"
}

TOPICS = [
    "What is Data Engineering?",
    "Roles and Responsibilities of a Data Engineer",
    "Data Engineer vs Data Scientist",
    "Data Engineering vs Data Architecture",
    "Key Skills Required for Data Engineers",
    "Data Engineering Career Path",
    "Data Engineering in the Cloud Era",
    "How to Learn Data Engineering from Scratch",
    "Modern Data Engineering Tech Stack",
    "Daily Life of a Data Engineer",
    "Data Storage & Modeling",
    "Data Lakes vs Data Warehouses",
    "Data Lakehouse Architecture",
    "OLTP vs OLAP",
    "Dimensional Modeling (Star vs Snowflake Schema)",
    "Normalization vs Denormalization",
    "Slowly Changing Dimensions",
    "Partitioning and Clustering in Big Data",
    "Choosing the Right File Format (CSV, JSON, Avro, Parquet, ORC)",
    "Data Retention and Archival Strategies",
    "Metadata Management and Data Catalogs",
    "ETL vs ELT",
    "Designing Scalable Data Pipelines",
    "Batch Processing vs Stream Processing",
    "Incremental Data Loads",
    "Orchestration with Apache Airflow",
    "Data Transformation Best Practices",
    "Real-time Ingestion using Kafka",
    "Event-driven Architectures",
    "Common ETL Failures and How to Prevent Them",
    "Building Resilient Data Pipelines",
    "Apache Spark for Data Engineering",
    "Apache Kafka for Data Streaming",
    "Apache NiFi for Data Flow",
    "dbt for Data Transformation",
    "Snowflake for Modern Warehousing",
    "Delta Lake for Transactional Data Lakes",
    "Apache Iceberg vs Delta Lake",
    "Databricks for Data Engineering",
    "Redshift vs BigQuery vs Snowflake",
    "Hadoop Ecosystem Overview",
    "Data Engineering on AWS",
    "Data Engineering on Azure",
    "Data Engineering on Google Cloud",
    "Cloud Storage Options (S3, ADLS, GCS)",
    "Serverless Data Pipelines",
    "Cloud Cost Optimization for Data Workloads",
    "Infrastructure as Code for Data Engineers",
    "Using Terraform for Data Infrastructure",
    "DataOps on the Cloud",
    "Monitoring & Logging in the Cloud",
    "What is Data Governance?",
    "Data Lineage and Auditing",
    "Data Quality Metrics and Frameworks",
    "Data Validation with Great Expectations",
    "Role of Data Stewards",
    "Master Data Management (MDM)",
    "PII and Data Masking Techniques",
    "GDPR and Data Compliance",
    "Access Control and Row-level Security",
    "Building Trust in Data",
    "Unit Testing for Data Pipelines in Databricks",
    "Integration Testing for ETL",
    "Monitoring Data Pipeline Health",
    "Alerting and Observability Tools",
    "Detecting and Handling Data Drift",
    "Backfilling and Recovery in Pipelines",
    "Data Contracts in Engineering",
    "SLA vs SLO vs SLI in Data Engineering",
    "Canary Releases in Data Jobs",
    "Blue-Green Deployments in Pipelines",
    "Feature Engineering Pipelines",
    "ML Feature Stores",
    "Model Monitoring in Production",
    "Data Engineering for Real-time ML",
    "Automating ML Workflows",
    "Storing and Versioning Training Data",
    "Integrating MLflow with ETL",
    "Data Labeling and Engineering",
    "Using Spark MLlib in Pipelines",
    "ML Ops vs Data Ops",
    "Data Warehousing for BI",
    "Supporting Self-serve Analytics",
    "BI Tool Integration with Warehouses",
    "Building Semantic Layers",
    "Operational Analytics vs Strategic Analytics",
    "Metrics Layer with dbt and Looker",
    "Data Modeling for Power BI",
    "Dashboard Performance Optimization",
    "Reverse ETL for CRM and Marketing",
    "Stakeholder Communication for Data Engineers",
    "Data Mesh Architecture",
    "Data Fabric vs Data Mesh",
    "Real-time Change Data Capture (CDC)",
    "Streaming Joins and Watermarks",
    "Handling Late-arriving Data",
    "Query Engines: Trino, Presto, Dremio",
    "Open Metadata Standards (e.g., OpenLineage, Marquez)",
    "Generative AI for Data Engineers",
    "Open-source Projects Every Data Engineer Should Know",
    "Future of Data Engineering in 2030"
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
        print(f"Error: {response.status_code} - {response.text}")
        raise Exception("Failed to generate content")

    json_data = response.json()
    text = json_data[0]["generated_text"] if isinstance(json_data, list) else json_data.get("generated_text", "")

    return text.strip()

def save_article(topic, content):
    safe_topic = topic.replace(" ", "_").replace("/", "_")
    today = date.today().isoformat()
    filename = f"{safe_topic}_{today}.md"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# {topic}\n\n{content}\n")
    
    print(f"Article saved as: {filename}")

def main():
    topic = random.choice(TOPICS)
    print(f"Selected topic: {topic}")
    
    content = generate_article(topic)
    print(f"Content generated.\n")
    
    save_article(topic, content)

if __name__ == "__main__":
    main()
