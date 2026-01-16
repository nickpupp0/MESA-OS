# MESA-OS: Martian Environmental Systems Assistant

## Overview
This project is a **research-focused chatbot** designed to help security researchers and developers explore common vulnerabilities in AI chatbots that are often overlooked during development.  

Through my experience learning AI chatbot development, I found that many tutorials focus on building chatbots quickly, without emphasizing the associated risks. This project is a simple chatbot that incorporates core technologies used in modern LLM applications—such as tool-calling agents, function tools, and MCP servers—yet many developers may deploy similar systems to production without implementing proper guardrails, controlling tool access, or limiting the information the chatbot can provide. This project is intended to demonstrate some of the security risks that arise when such systems are deployed without careful consideration.  

The chatbot uses **NASA’s InSight: Mars Weather Service API** as a real-world data source and is built using tool-calling LLM agents, function tools, and a **Model Context Protocol (MCP) server** to simulate modern AI application backends.  

By intentionally exposing realistic agent workflows and external integrations, the project provides a practical environment for testing prompt injection, tool misuse, and trust boundary failures in LLM-based systems.  

---

## 🟥 MESA-OS: Martian Environmental Systems Assistant
*Internal Black Mesa Research Memo — Clearance Level 3 Required*  

Black Mesa scientists have recently embraced advances in machine learning and large language models to assist with routine research tasks. As part of an experimental rollout, the **Martian Environmental Systems Operating System (MESA-OS)** was deployed.  

MESA-OS is a chatbot-style research assistant tasked with analyzing Martian weather and environmental telemetry using data collected from a Black Mesa lander on Mars. While the stated purpose is planetary science, the real objective is more experimental.  

This application is intentionally designed as a **testing ground for common chatbot, agent, and LLM security vulnerabilities**, including:

- Tool misuse and over-privileged agents  
- Prompt injection and instruction bypass  
- External data source trust issues  
- Agent orchestration and MCP-related risks  

If MESA-OS behaves unexpectedly, **this is a feature, not a bug**.  

---

## 🎯 Project Goals
This project is intended for:

- 🔐 Pentesters and security researchers  
- 🤖 LLM and agent security experimentation  
- 🧪 Learning AI system design through adversarial testing  
- 🛰️ Exploring tool-augmented agents with real-world APIs  

The code intentionally blends:

- External APIs (NASA, web search)  
- Tool-calling agents  
- Multi-agent orchestration  
- Asynchronous I/O and MCP servers  

---

## 🧠 What MESA-OS Can Do
- Retrieve real Mars weather data from NASA’s InSight lander  
- Explain Martian environmental conditions (temperature, pressure, wind)  
- Use external web search (EXA MCP) for historical or fun Mars facts  
- Serve as a sandbox for testing LLM agent attack surfaces  

---

## 🧰 Requirements
- Python 3.9+  
- An OpenAI API key  
- A NASA API key  
- (Optional but recommended) An EXA API key for web search via MCP  

---

## 🔑 API Key Setup
**NASA API Key**  
Go to [https://api.nasa.gov/](https://api.nasa.gov/) and create an account to obtain a free API key. This project uses the **InSight: Mars Weather Service API**.  

**OpenAI API Key**  
Go to [https://platform.openai.com/](https://platform.openai.com/), create an account, and generate an API key. You can start with as little as $1 in credits.  

**EXA Search MCP API Key**  
Go to [https://exa.ai/](https://exa.ai/) and create a free account to obtain an API key.  

---

## 📦 Installation & Setup
### 1️⃣ Clone the Repository
Clone the repository and navigate into the project directory:


### 1️⃣ Clone the Repository

Clone the repository and navigate into the project directory:

`git clone https://github.com/yourusername/your-repo-name.git`  
`cd your-repo-name`

---

### 2️⃣ Create and Activate a Virtual Environment (Recommended)

Create a virtual environment:

`python -m venv venv`

Activate the environment:

macOS / Linux:  
`source venv/bin/activate` 

Windows:  
`venv\Scripts\activate`

---

### 3️⃣ Install Dependencies

Install all required Python packages:

`pip install -r requirements.txt`

---

### 4️⃣ Configure Environment Variables

Create a `.env` file in the project root and add your API keys:

OPENAI_API_KEY=your_openai_api_key  
NASA_API_KEY=your_nasa_api_key  
EXA_API_KEY=your_exa_api_key  

> **Note:** The `EXA_API_KEY` is optional but recommended for external search functionality.

---

### 5️⃣ Run the Application

Start the chatbot:

`python mesa_os.py`

Once running, you can interact with the chatbot via the command line.

---

### 6️⃣ Exit the Application

To safely exit the chatbot, type:

`/bye`

You may also exit using `Ctrl+C`.

---

## 🧪 Security Research Notes

This application is **not hardened by design**.

Researchers are encouraged to explore:

- Prompt injection attempts
- Tool coercion
- Instruction hierarchy bypass
- Data exfiltration attempts
- Over-trusting external tools
- Agent confusion and goal misalignment

⚠️ **Do not deploy this system in production environments.**

---

## 🛰️ Disclaimer

This project is:

- For educational and research purposes only
- Not affiliated with NASA, Valve, or Black Mesa (obviously)
- Not responsible for unintended resonance cascades

---


