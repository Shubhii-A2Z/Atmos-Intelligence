# AtmosAI 🌤️

AtmosAI is an AI-powered weather agent that fetches **live weather data for any city or location** using **Open-Meteo tool calling**. It supports multiple LLM providers and lets you interact with weather information using natural language.

## ✨ Features

- 🤖 AI-powered weather agent
- 🌍 Weather information for cities and locations worldwide
- 🔧 Tool calling with the Open-Meteo API
- ⚡ Live weather data
- 🔌 Multi-provider LLM support (Currently uses Groq)
- 💬 Natural-language weather queries
- 🐍 Built with Python
- 🎈 Streamlit frontend

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd AtmosAI
```

### 2. Install dependencies

This project uses **uv** for Python dependency management.

Make sure `uv` is installed, then run:

```bash
uv sync
```

This will create the project's virtual environment and install the required dependencies.

### 3. Configure environment variables

Create your `.env` file based on the provided example:

```bash
cp .env.example .env
```

Then open `.env` and add the required API keys/configuration.

> **Note:** `.env.example` is provided to show which environment variables are required. Never commit your actual `.env` file or API keys to GitHub.

### 4. Run the application

Start the Streamlit frontend with:

```bash
uv run streamlit run frontend/app.py
```

Streamlit will provide a local URL where you can open AtmosAI in your browser.

## 💬 Example Queries

Once the application is running, you can ask questions such as:

```text
What's the weather in Delhi?
```

```text
Will it rain in London today?
```

```text
What's the current temperature in Tokyo?
```

```text
Give me the weather forecast for New York.
```

AtmosAI uses the weather tool to retrieve live data and then uses the configured LLM provider to generate a natural-language response.

## 🛠️ Tech Stack

- **Python**
- **Streamlit**
- **uv**
- **Open-Meteo API**
- **Groq LLM Tool Calling**
- **Jinja2**

## 🔐 Environment Variables

API keys and other configuration are loaded through environment variables.

Use:

```text
.env.example
```

as the reference for configuring your local `.env` file.

**Do not commit secrets or API keys to the repository.**

## 📁 Project Structure

```text
AtmosAI/
├── frontend/
│   └── app.py
├── src/
│   ├── client/
│   ├── prompts/
│   ├── tools/
│   └── ...
├── .env.example
├── pyproject.toml
├── uv.lock
└── README.md
```

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Test the application locally
5. Commit your changes
6. Open a pull request

Please keep API keys and other secrets out of commits.