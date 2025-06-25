// generate-content.js
import { config } from 'dotenv';
import fs from 'fs';
import fetch from 'node-fetch';

config();

const topics = [ /* ... your topics array ... */ ];
const topic = topics[Math.floor(Math.random() * topics.length)];
const prompt = `Write a detailed article about the following Data Engineering topic with 2 or 3 subtopics and bullet points:\n\n${topic}`;
const safeFilename = topic.replace(/[^a-zA-Z0-9]/g, '_');
const filename = `Data_Engineering_${safeFilename}_${new Date().toISOString().split('T')[0]}.md`;

async function generateContent() {
  try {
    const res = await fetch(
      'https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct',
      {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${process.env.HUGGINGFACE_API_TOKEN}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          inputs: prompt,
          parameters: {
            max_new_tokens: 700,
            temperature: 0.7,
            do_sample: true
          }
        })
      }
    );

    if (!res.ok) {
      const err = await res.text();
      throw new Error(`Response ${res.status}: ${err}`);
    }

    const json = await res.json();
    const content = json.generated_text || json[0]?.generated_text;
    if (!content) throw new Error('No text was generated.');

    fs.writeFileSync(filename, `# ${topic}\n\n${content}`);
    console.log(`✅ Article written to ${filename}`);

  } catch (error) {
    console.error("❌ Generation failed:", error.message);
    process.exit(1);
  }
}

generateContent();
