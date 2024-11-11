# Video Summary Tool

## Introduction

This Streamlit-based application automatically generates structured summaries of YouTube videos, offering a fast and efficient way to grasp key points without watching the entire video. The tool leverages LLMs via the Groq API and applies advanced prompt engineering techniques to produce clear, well-organized summaries.

## Key Features
- **Prompt-Driven Structure**: Uses prompt engineering to create summaries with distinct sections like Overview, Details, and Key Takeaways ensuring clarity and coherence.
- **Real-Time Video Parsing**: Retrieves and displays video metadata and captions as the content is processed.
- **Flexible Model Selection**: Choose from a list of available models
- **Adjustable Chunk Length**: Control the length of each chunk from the video captions for the model to process and summarize individually before creating a cohesive final summary.
- **Simple URL Input**: Paste the video URL into the text box and click the button to generate your summary instantly.

## Instruction For Use

### 1. Export your Groq API Key

```terminal
setx GROQ_API_KEY ***
```

### 2. Install libraries

```terminal
pip install -r requirements.txt
```

### 3. Run Streamlit App

```terminal
streamlit run app.py
```

- Open [localhost:8501](http://localhost:8501) to view your Video Summary App

> Note: For best results, please use videos in English. Other languages are currently not supported and may yield incomplete or inaccurate summaries.
