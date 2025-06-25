import fs from 'fs';
import path from 'path';
import OpenAI from 'openai';

// Initialize OpenAI client with API key from environment variable
const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

// List of random data engineering topics
const topics = [
  "Data Lake Architecture",
  "ETL vs ELT",
  "Apache Airflow Basics",
  "Data Partitioning Strategies",
  "Streaming Data with Apache Kafka",
  "Data Quality Best Practices",
  "Building Scalable Data Pipelines",
  "Data Warehouse vs Data Lakehouse",
  "Schema Evolution in Big Data",
  "Data Orchestration with Prefect",
];

// Function to pick a random topic
function getRandomTopic() {
  const index = Math.floor(Math.random() * topics.length);
  return topics[index];
}

async function generateContent() {
  const topic = getRandomTopic();
  const prompt = `Write a detailed, technical article about the topic: "${topic}" in data engineering. Include explanations and examples where relevant.`;

  try {
    const response = await openai.chat.completions.create({
      model: "gpt-3.5-turbo",
      messages: [
        { role: "system", content: "You are an expert data engineer and technical writer." },
        { role: "user", content: prompt },
      ],
    });

    const content = response.choices[0].message.content.trim();

    // Prepare filename with topic and timestamp
    const safeTopic = topic.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');
    const timestamp = new Date().toISOString().split('T')[0];
    const filename = path.join('content', `${timestamp}-${safeTopic}.md`);

    // Ensure content directory exists
    if (!fs.existsSync('content')) {
      fs.mkdirSync('content');
    }

    // Write content to file
    fs.writeFileSync(filename, `# ${topic}\n\n${content}`);

    console.log(`Content generated and saved to ${filename}`);
  } catch (error) {
    console.error("Error generating content:", error);
    process.exit(1);
  }
}

generateContent();
