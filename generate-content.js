// generate-content.js

import { config } from 'dotenv';
import fs from 'fs';
import { HfInference } from '@huggingface/inference';

config(); // Load .env

const topics = [
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
];

// 1. Pick a random topic
const topic = topics[Math.floor(Math.random() * topics.length)];
const prompt = `Write a detailed article about the following Data Engineering topic:\n\n${topic}`;

const safeFilename = topic.replace(/[^a-zA-Z0-9]/g, '_');
const filename = `Data_Engineering_${safeFilename}_${new Date().toISOString().split('T')[0]}.md`;

async function generateContent() {
  try {
    const hf = new HfInference(process.env.HUGGINGFACE_API_TOKEN);

    const result = await hf.textGeneration({
      model: "tiiuae/falcon-7b-instruct", 
      inputs: prompt,
      parameters: {
        max_new_tokens: 700,
        temperature: 0.7,
        do_sample: true
      },
    });

    const content = result.generated_text;

    fs.writeFileSync(filename, `# ${topic}\n\n${content}`);
    console.log(`Content written to ${filename}`);
  } catch (error) {
    console.error("❌ Failed to generate content:", error.message || error);
    process.exit(1);
  }
}

generateContent();
