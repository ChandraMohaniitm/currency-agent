
# 💱 FluxExchange – AI Currency Converter

An AI-powered currency conversion assistant that understands natural language queries and converts currencies using live exchange-rate data.

Instead of manually selecting currencies and entering values, simply ask questions like:

- Convert 100 USD to INR.
- How much is 500 EUR in USD?
- Convert 2500 JPY to INR.

FluxExchange uses a LangChain AI Agent with OpenRouter to understand requests and automatically call a currency conversion tool.

## ✨ Features

- 🤖 **AI-Powered Agent:** Natural language understanding using OpenRouter GPT-4o-mini.
- 💱 **Live Currency Conversion:** Fetches exchange rates through ExchangeRate API.
- 🛠️ **Tool Calling:** LangChain agent dynamically invokes the conversion tool.
- ⚡ **FastAPI Backend:** Lightweight REST API for handling requests.
- 🎨 **Modern UI:** Responsive dark-themed fintech dashboard.
- 📋 **Copy Results:** Easily copy conversion results.
- 🌐 **Cloud Deployment:** Deployable on Vercel.

## 🏗️ Architecture

```text
             User
              |
              v
       Frontend Dashboard
              |
              v
        FastAPI Backend
              |
              v
       LangChain AI Agent
              |
              v
       OpenRouter LLM
        GPT-4o-mini
              |
              v
       Tool Selection
              |
              v
     Currency Conversion Tool
              |
              v
      ExchangeRate API
              |
              v
       Live Exchange Rates
              |
              v
       Conversion Result
```

## 🧰 Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming |
| FastAPI | Backend API |
| LangChain | AI agent orchestration |
| OpenRouter | LLM access |
| GPT-4o-mini | Natural language understanding |
| ExchangeRate API | Currency exchange rates |
| Requests | HTTP API communication |
| HTML, CSS, JavaScript | Frontend |
| Vercel | Deployment |

## 📂 Project Structure

```text
FluxExchange/
│
├── api/
│   └── index.py
│
├── app.py
├── requirements.txt
├── vercel.json
├── .gitignore
└── README.md
```

*Adjust the structure according to your actual repository.*

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/FluxExchange.git
cd FluxExchange
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate it:

**Windows**
```bash
venv\Scripts\activate
```

**Linux / macOS**
```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file or configure the environment variable in your deployment platform.

```env
OPENROUTER_API_KEY=your_openrouter_api_key
```

Get your API key:

https://openrouter.ai/keys

Never commit your API key to GitHub.

### 5. Run Locally

```bash
uvicorn app:app --reload
```

Open:

http://127.0.0.1:8000

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Frontend dashboard |
| GET | `/health` | Health check |
| POST | `/chat` | Process currency conversion requests |

### Example API Request

```json
{
  "question": "Convert 100 USD to INR"
}
```

### Example Response

```json
{
  "answer": "100.00 USD = ... INR\nRate: 1 USD = ... INR"
}
```

*Actual values depend on the latest exchange-rate API response.*

## 🧠 How It Works

1. The user submits a currency conversion request in natural language.
2. FastAPI receives the request.
3. LangChain AI Agent interprets the query.
4. The agent selects the `convert_currency` tool.
5. The tool requests exchange-rate information from ExchangeRate API.
6. The conversion is calculated using the retrieved exchange rate.
7. The AI agent presents the result to the user.

## 🔮 Future Improvements

- Support for multiple conversion tools.
- Currency conversion history.
- Interactive exchange-rate charts.
- Historical exchange-rate analysis.
- Multi-currency comparison.
- Streaming AI responses.
- Improved input validation and error handling.

## ⚠️ Disclaimer

Exchange rates are retrieved from an external API and may change over time. Results are for informational purposes and should not be considered financial advice.

## 👨‍💻 Author

**Chandra Mohan**

IIT Madras | BS in Data Science and Applications

Interested in AI Engineering, Generative AI, Agentic AI, and LLM Applications.

---

⭐ If you find this project useful, consider giving it a star!
