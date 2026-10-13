
import os
import requests
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI

app = FastAPI(title="AI Currency Converter")


@tool
def convert_currency(
    amount: float,
    from_currency: str,
    to_currency: str
) -> str:
    """Convert an amount using live exchange rates."""

    if amount <= 0:
        return "Amount must be greater than zero."

    base = from_currency.strip().upper()
    target = to_currency.strip().upper()

    try:
        response = requests.get(
            f"https://open.er-api.com/v6/latest/{base}",
            timeout=12
        )
        response.raise_for_status()
        data = response.json()

        if data.get("result") != "success":
            return f"Unsupported source currency: {base}"

        rates = data.get("rates", {})
        if target not in rates:
            return f"Unsupported target currency: {target}"

        rate = rates[target]
        converted = amount * rate

        return (
            f"{amount:,.2f} {base} = {converted:,.2f} {target}\n"
            f"Rate: 1 {base} = {rate:.6f} {target}\n"
            f"Rate updated: {data.get('time_last_update_utc', 'Unknown')}"
        )

    except requests.RequestException as exc:
        return f"Exchange-rate API error: {exc}"


api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    raise RuntimeError("Set OPENROUTER_API_KEY in Vercel Environment Variables.")

llm = ChatOpenAI(
    model="openai/gpt-4o-mini",
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
    temperature=0
)

agent = create_agent(
    model=llm,
    tools=[convert_currency],
    system_prompt=(
        "You are a currency conversion assistant. "
        "For every conversion request, use the convert_currency tool. "
        "Never invent exchange rates. Clearly explain the tool result."
    )
)


class ChatRequest(BaseModel):
    question: str


@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <title>AI Currency Converter</title>
      <style>
        body { font-family: Arial; max-width: 700px; margin: 40px auto;
               padding: 16px; background: #f4f6f8; }
        main { background: white; padding: 24px; border-radius: 14px; }
        textarea { width: 100%; box-sizing: border-box; padding: 12px;
                   margin: 12px 0; min-height: 90px; }
        button { padding: 12px 18px; cursor: pointer; }
        pre { white-space: pre-wrap; overflow-wrap: anywhere;
              background: #eef2f7; padding: 14px; border-radius: 8px; }
      </style>
    </head>
    <body>
      <main>
        <h2>💱 AI Currency Converter</h2>
        <p>Example: Convert 100 USD to INR</p>
        <textarea id="question"
          placeholder="Enter your conversion request"></textarea>
        <button id="send" onclick="sendMessage()">Convert</button>
        <h3>Result</h3>
        <pre id="answer">Your result will appear here.</pre>
      </main>
      <script>
        async function sendMessage() {
          const question = document.getElementById("question").value.trim();
          const answer = document.getElementById("answer");
          const button = document.getElementById("send");

          if (!question) {
            answer.textContent = "Please enter a conversion request.";
            return;
          }

          button.disabled = true;
          answer.textContent = "Converting...";

          try {
            const response = await fetch("/chat", {
              method: "POST",
              headers: {"Content-Type": "application/json"},
              body: JSON.stringify({question})
            });

            const data = await response.json();
            answer.textContent = response.ok
              ? data.answer
              : (data.detail || "Request failed.");
          } catch (error) {
            answer.textContent = "Request failed: " + error.message;
          } finally {
            button.disabled = false;
          }
        }
      </script>
    </body>
    </html>
    """


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat")
def chat(request: ChatRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Enter a question.")

    try:
        result = agent.invoke({
            "messages": [
                {"role": "user", "content": request.question.strip()}
            ]
        })

        for message in reversed(result["messages"]):
            if getattr(message, "type", "") == "ai" and message.content:
                return {"answer": str(message.content)}

        return {"answer": "No response generated."}

    except Exception:
        raise HTTPException(
            status_code=502,
            detail="AI request failed. Check your OpenRouter API key, model access and logs."
        )
