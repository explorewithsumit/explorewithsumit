// generate-content.js

import { config } from 'dotenv';
import fs from 'fs';
import { HfInference } from '@huggingface/inference';

config(); // Load HUGGINGFACE_API_TOKEN from .env

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

// Select a random topic
const topic = topics[Math.floor(Math.random() * topics.length)];
const prompt = `Write a detailed article about the following Data Engineering topic:\n\n${topic}`;
const safeFilename = topic.replace(/[^a-zA-Z0-9]/g, '_');
const filename = `Data_Engineering_${safeFilename}_${new Date().toISOString().split('T')[0]}.md`;

async function generateContent() {
  try {
    const hf = new HfInference(process.env.HUGGINGFACE_API_TOKEN);

    const response = await hf.textGeneration({
      model: "tiiuae/falcon-7b-instruct",  // model known to work
      inputs: prompt,
      parameters: {
        max_new_tokens: 700,
        temperature: 0.7,
        do_sample: true
      }
    });

    const content = response.generated_text || (Array.isArray(response) ? response[0]?.generated_text : '');
    if (!content) throw new Error("No text was generated.");

    fs.writeFileSync(filename, `# ${topic}\n\n${content}`);
    console.log(`✅ Article written to ${filename}`);
  } catch (error) {
    console.error("❌ Generation failed:", error.message || error);
    process.exit(1);
  }
}

generateContent();
