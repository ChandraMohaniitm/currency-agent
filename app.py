
import os
import requests
import gradio as gr

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI


@tool
def convert_currency(
    amount: float,
    from_currency: str,
    to_currency: str
) -> str:
    """Convert currencies using the latest available exchange rates."""

    if amount <= 0:
        return "Error: Amount must be positive."

    base = from_currency.upper().strip()
    target = to_currency.upper().strip()

    try:
        url = f"https://open.er-api.com/v6/latest/{base}"
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()

        if data.get("result") != "success":
            return f"Error: Invalid or unsupported currency: {base}"

        rates = data.get("rates", {})

        if target not in rates:
            return f"Error: Unsupported target currency: {target}"

        rate = rates[target]
        converted = amount * rate

        return (
            f"Amount: {amount:.2f} {base}\n"
            f"Exchange rate: 1 {base} = {rate:.6f} {target}\n"
            f"Converted amount: {converted:.2f} {target}\n"
            f"Rate date: {data.get('time_last_update_utc', 'Not provided')}"
        )

    except requests.RequestException:
        return "Currency API request failed. Please try again."


api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    raise ValueError("Please configure OPENROUTER_API_KEY in Space Secrets.")

llm = ChatOpenAI(
    model="openai/gpt-3.5-turbo",
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
    temperature=0
)

agent = create_agent(
    model=llm,
    tools=[convert_currency],
    system_prompt=(
        "You are a currency conversion assistant. "
        "For every conversion request, call the currency tool. "
        "Never guess exchange rates. Explain the returned amount, "
        "exchange rate and rate date clearly."
    )
)


def chat_with_agent(question):
    if not question.strip():
        return "Please enter a question."

    try:
        result = agent.invoke({
            "messages": [
                {"role": "user", "content": question}
            ]
        })
        return str(result["messages"][-1].content)

    except Exception as e:
        print(f"Agent error: {e}")
        return "Something went wrong. Check the API key, model access, and Space logs."


demo = gr.Interface(
    fn=chat_with_agent,
    inputs=gr.Textbox(
        label="Ask Currency Conversion",
        placeholder="Convert 1 USD to INR"
    ),
    outputs=gr.Textbox(label="Result"),
    title="💱 AI Currency Converter",
    description="Convert currencies using live exchange-rate data and an AI agent.",
    examples=[
        "Convert 1 USD to INR",
        "Convert 100 EUR to INR",
        "Convert 5000 INR to USD"
    ]
)

if __name__ == "__main__":
    demo.launch()
