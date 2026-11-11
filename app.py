
import os
import requests

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI


# --------------------------------------------------
# APP CONFIGURATION
# --------------------------------------------------

app = FastAPI(
    title="FluxExchange - AI Currency Converter",
    description="AI-powered currency conversion assistant"
)


# --------------------------------------------------
# CURRENCY CONVERSION TOOL
# --------------------------------------------------

@tool
def convert_currency(
    amount: float,
    from_currency: str,
    to_currency: str
) -> str:
    """Convert an amount from one currency to another using the latest available exchange rates."""

    if amount <= 0:
        return "Error: Amount must be greater than zero."

    from_currency = from_currency.strip().upper()
    to_currency = to_currency.strip().upper()

    try:
        url = f"https://open.er-api.com/v6/latest/{from_currency}"

        response = requests.get(url, timeout=12)
        response.raise_for_status()

        data = response.json()

        if data.get("result") != "success":
            return f"Error: Could not find exchange rates for {from_currency}."

        rates = data.get("rates", {})

        if to_currency not in rates:
            return f"Error: Unsupported currency code {to_currency}."

        rate = rates[to_currency]
        converted_amount = amount * rate

        return (
            f"Conversion successful!\n"
            f"{amount:,.2f} {from_currency} = "
            f"{converted_amount:,.2f} {to_currency}\n"
            f"Exchange rate: 1 {from_currency} = {rate:,.6f} {to_currency}\n"
            f"Rate date: {data.get('time_last_update_utc', 'Not available')}"
        )

    except requests.RequestException as e:
        return f"Currency API error: {str(e)}"


# --------------------------------------------------
# AI AGENT CONFIGURATION
# --------------------------------------------------

api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    raise RuntimeError("OPENROUTER_API_KEY environment variable is missing.")

llm = ChatOpenAI(
    model="openai/gpt-4o-mini",
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
    temperature=0
)

agent = create_agent(
    model=llm,
    tools=[convert_currency],
    system_prompt="""
You are FluxExchange, a professional AI currency conversion assistant.

Your responsibilities:
1. Help users convert currencies.
2. Identify the amount, source currency and target currency.
3. Always use the convert_currency tool for actual conversions.
4. Never invent exchange rates or conversion results.
5. If important information is missing, ask the user for clarification.
6. Explain the conversion in simple language.
7. Keep responses clear, friendly and concise.
8. Support common international currency codes.
"""
)


# --------------------------------------------------
# REQUEST MODEL
# --------------------------------------------------

class ChatRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2000)


# --------------------------------------------------
# FRONTEND
# --------------------------------------------------

HTML_PAGE = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>FluxExchange | AI Currency Converter</title>

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">

<style>
:root {
    --bg: #080d18;
    --panel: #101827;
    --panel-light: #141f31;
    --border: rgba(148, 163, 184, 0.13);
    --text: #f1f5f9;
    --muted: #8996aa;
    --blue: #3984ff;
    --cyan: #43d9e8;
    --green: #41d9a0;
    --danger: #ff6b78;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    min-height: 100vh;
    background:
        radial-gradient(ellipse at 15% 5%, rgba(42, 105, 220, .13), transparent 35%),
        radial-gradient(ellipse at 90% 75%, rgba(35, 198, 215, .08), transparent 30%),
        var(--bg);
    color: var(--text);
    font-family: 'DM Sans', sans-serif;
}

button, input, select {
    font: inherit;
}

button {
    cursor: pointer;
}

.container {
    max-width: 1160px;
    margin: auto;
    padding: 0 25px;
}

/* NAVBAR */

.navbar {
    height: 82px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid var(--border);
}

.logo {
    display: flex;
    align-items: center;
    gap: 11px;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 22px;
    font-weight: 700;
    letter-spacing: -.8px;
}

.logo-icon {
    width: 39px;
    height: 39px;
    border-radius: 12px;
    display: grid;
    place-items: center;
    background: linear-gradient(135deg, #3984ff, #39d7dc);
    color: #06101d;
    font-size: 23px;
    font-weight: 800;
}

.logo span {
    color: var(--cyan);
}

.nav-right {
    display: flex;
    align-items: center;
    gap: 9px;
    color: var(--muted);
    font-size: 12px;
    font-weight: 600;
}

.status-dot {
    width: 8px;
    height: 8px;
    background: var(--green);
    border-radius: 50%;
    box-shadow: 0 0 12px rgba(65, 217, 160, .7);
}

/* HERO */

.hero {
    text-align: center;
    padding: 64px 0 40px;
}

.eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 8px 13px;
    border: 1px solid rgba(67, 217, 232, .2);
    background: rgba(67, 217, 232, .06);
    border-radius: 30px;
    color: var(--cyan);
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.3px;
    text-transform: uppercase;
}

.hero h1 {
    font-family: 'Space Grotesk', sans-serif;
    font-size: clamp(35px, 5vw, 57px);
    letter-spacing: -2.5px;
    margin-top: 22px;
    line-height: 1.13;
}

.hero h1 span {
    background: linear-gradient(90deg, #4c91ff, #48dce0);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}

.hero p {
    max-width: 540px;
    margin: 17px auto 0;
    color: var(--muted);
    font-size: 15px;
    line-height: 1.8;
}

/* MAIN GRID */

.main-grid {
    display: grid;
    grid-template-columns: 1.05fr .95fr;
    gap: 22px;
    align-items: start;
    padding-bottom: 70px;
}

.panel {
    background: linear-gradient(145deg, rgba(20, 31, 49, .96), rgba(13, 22, 36, .98));
    border: 1px solid var(--border);
    border-radius: 22px;
    padding: 27px;
    box-shadow: 0 20px 60px rgba(0, 0, 0, .18);
}

.panel-heading {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 25px;
}

.panel-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 19px;
    font-weight: 700;
}

.panel-subtitle {
    font-size: 12px;
    color: var(--muted);
    margin-top: 5px;
}

.live-label {
    color: var(--green);
    background: rgba(65, 217, 160, .08);
    border: 1px solid rgba(65, 217, 160, .17);
    padding: 6px 10px;
    border-radius: 20px;
    font-size: 10px;
    font-weight: 700;
}

/* CONVERTER */

.field-label {
    display: block;
    font-size: 12px;
    font-weight: 600;
    color: #aebbd0;
    margin-bottom: 10px;
}

.amount-input {
    width: 100%;
    height: 58px;
    background: rgba(5, 12, 24, .6);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 0 16px;
    color: white;
    font-size: 22px;
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 600;
    outline: none;
    transition: .2s;
    margin-bottom: 21px;
}

.amount-input:focus,
.currency-select:focus,
.chat-input:focus {
    border-color: var(--blue);
    box-shadow: 0 0 0 3px rgba(57, 132, 255, .10);
}

.currency-row {
    display: grid;
    grid-template-columns: 1fr 42px 1fr;
    gap: 10px;
    align-items: end;
}

.currency-select {
    width: 100%;
    height: 56px;
    padding: 0 12px;
    background: rgba(5, 12, 24, .6);
    color: white;
    border: 1px solid var(--border);
    border-radius: 12px;
    outline: none;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
}

.currency-select option {
    background: #101827;
    color: white;
}

.swap-wrap {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 56px;
}

.swap-btn {
    width: 38px;
    height: 38px;
    border-radius: 50%;
    background: rgba(57, 132, 255, .12);
    border: 1px solid rgba(57, 132, 255, .25);
    color: #65a2ff;
    font-size: 20px;
    transition: .25s;
}

.swap-btn:hover {
    transform: rotate(180deg);
    background: rgba(57, 132, 255, .25);
}

.convert-btn {
    width: 100%;
    height: 55px;
    margin-top: 25px;
    border: none;
    border-radius: 12px;
    color: #06101d;
    background: linear-gradient(100deg, #448dff, #42d8dc);
    font-weight: 800;
    font-size: 14px;
    letter-spacing: .2px;
    transition: .2s;
    box-shadow: 0 8px 25px rgba(57, 132, 255, .18);
}

.convert-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 30px rgba(57, 132, 255, .28);
}

.convert-btn:disabled {
    opacity: .6;
    cursor: not-allowed;
    transform: none;
}

.result-box {
    display: none;
    margin-top: 22px;
    padding: 19px;
    border-radius: 14px;
    background: rgba(65, 217, 160, .055);
    border: 1px solid rgba(65, 217, 160, .18);
}

.result-label {
    color: var(--green);
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
}

.result-amount {
    font-family: 'Space Grotesk', sans-serif;
    font-size: clamp(24px, 4vw, 33px);
    font-weight: 700;
    margin: 10px 0;
    overflow-wrap: anywhere;
}

.result-rate {
    font-size: 12px;
    color: var(--muted);
    line-height: 1.7;
}

.result-actions {
    display: flex;
    justify-content: flex-end;
    margin-top: 12px;
}

.copy-btn {
    background: rgba(65, 217, 160, .10);
    border: 1px solid rgba(65, 217, 160, .18);
    color: var(--green);
    border-radius: 8px;
    padding: 8px 12px;
    font-size: 11px;
    font-weight: 700;
}

/* QUICK PAIRS */

.quick-section {
    margin-top: 26px;
}

.quick-title {
    color: var(--muted);
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 12px;
}

.quick-pairs {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}

.pair-btn {
    padding: 8px 11px;
    background: rgba(148, 163, 184, .06);
    border: 1px solid var(--border);
    color: #cbd5e1;
    border-radius: 9px;
    font-size: 11px;
    font-weight: 600;
    transition: .2s;
}

.pair-btn:hover {
    border-color: rgba(67, 217, 232, .4);
    color: var(--cyan);
}

/* AI ASSISTANT */

.ai-panel {
    min-height: 480px;
    display: flex;
    flex-direction: column;
}

.ai-heading-icon {
    width: 38px;
    height: 38px;
    display: grid;
    place-items: center;
    border-radius: 12px;
    background: linear-gradient(135deg, rgba(57, 132, 255, .2), rgba(67, 217, 232, .15));
    color: var(--cyan);
    font-size: 19px;
}

.ai-title-row {
    display: flex;
    align-items: center;
    gap: 12px;
}

.ai-output {
    flex: 1;
    min-height: 230px;
    padding: 17px;
    background: rgba(5, 12, 24, .43);
    border: 1px solid var(--border);
    border-radius: 14px;
    overflow-wrap: anywhere;
}

.welcome-message {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    min-height: 195px;
    color: var(--muted);
}

.welcome-icon {
    font-size: 30px;
    margin-bottom: 14px;
}

.welcome-message strong {
    color: #e2e8f0;
    font-size: 14px;
    margin-bottom: 8px;
}

.welcome-message p {
    font-size: 12px;
    line-height: 1.7;
    max-width: 270px;
}

.ai-response {
    white-space: pre-wrap;
    color: #dce6f5;
    font-size: 13px;
    line-height: 1.85;
}

.chat-input-area {
    margin-top: 16px;
}

.chat-input {
    width: 100%;
    min-height: 54px;
    resize: vertical;
    padding: 15px;
    background: rgba(5, 12, 24, .6);
    color: white;
    border: 1px solid var(--border);
    border-radius: 12px;
    outline: none;
    font-size: 13px;
}

.chat-bottom {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 10px;
    margin-top: 12px;
}

.input-hint {
    color: var(--muted);
    font-size: 10px;
}

.ask-btn {
    border: none;
    padding: 12px 20px;
    border-radius: 10px;
    background: linear-gradient(100deg, #3984ff, #3acbdc);
    color: #06101d;
    font-weight: 800;
    font-size: 12px;
    transition: .2s;
}

.ask-btn:hover {
    transform: translateY(-1px);
}

.ask-btn:disabled {
    opacity: .6;
    cursor: not-allowed;
}

/* LOADING */

.loading {
    display: flex;
    align-items: center;
    gap: 10px;
    color: var(--cyan);
    font-size: 12px;
}

.spinner {
    width: 17px;
    height: 17px;
    border: 2px solid rgba(67, 217, 232, .2);
    border-top-color: var(--cyan);
    border-radius: 50%;
    animation: spin .7s linear infinite;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

/* INFO */

.info-strip {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 15px;
    padding: 22px;
    border: 1px solid var(--border);
    border-radius: 17px;
    background: rgba(16, 24, 39, .55);
    margin-bottom: 55px;
}

.info-item {
    text-align: center;
    padding: 8px;
}

.info-item strong {
    display: block;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 15px;
    margin-bottom: 6px;
}

.info-item span {
    color: var(--muted);
    font-size: 11px;
}

/* FOOTER */

footer {
    border-top: 1px solid var(--border);
    padding: 23px 0;
    color: var(--muted);
    font-size: 11px;
}

.footer-inner {
    display: flex;
    justify-content: space-between;
    gap: 15px;
    flex-wrap: wrap;
}

.toast {
    position: fixed;
    bottom: 25px;
    left: 50%;
    transform: translateX(-50%) translateY(20px);
    background: #18263a;
    border: 1px solid var(--border);
    color: white;
    padding: 12px 18px;
    border-radius: 10px;
    font-size: 12px;
    opacity: 0;
    pointer-events: none;
    transition: .25s;
    z-index: 10;
}

.toast.show {
    opacity: 1;
    transform: translateX(-50%) translateY(0);
}

/* RESPONSIVE */

@media (max-width: 850px) {
    .main-grid {
        grid-template-columns: 1fr;
    }

    .ai-panel {
        min-height: 430px;
    }
}

@media (max-width: 520px) {
    .container {
        padding: 0 15px;
    }

    .navbar {
        height: 70px;
    }

    .logo {
        font-size: 19px;
    }

    .hero {
        padding: 45px 0 32px;
    }

    .hero h1 {
        letter-spacing: -1.5px;
    }

    .hero p {
        font-size: 13px;
    }

    .panel {
        padding: 19px;
        border-radius: 17px;
    }

    .currency-row {
        grid-template-columns: 1fr 36px 1fr;
        gap: 6px;
    }

    .currency-select {
        font-size: 12px;
        padding: 0 7px;
    }

    .info-strip {
        grid-template-columns: 1fr;
        gap: 5px;
    }

    .info-item {
        border-bottom: 1px solid var(--border);
    }

    .info-item:last-child {
        border: none;
    }
}
</style>
</head>

<body>

<div class="container">

    <nav class="navbar">
        <div class="logo">
            <div class="logo-icon">↗</div>
            Flux<span>Exchange</span>
        </div>

        <div class="nav-right">
            <div class="status-dot"></div>
            AI SYSTEM ONLINE
        </div>
    </nav>


    <section class="hero">

        <div class="eyebrow">
            ✦ AI POWERED CURRENCY INTELLIGENCE
        </div>

        <h1>
            Exchange smarter.<br>
            <span>Move globally.</span>
        </h1>

        <p>
            Convert currencies instantly and get intelligent answers
            with your personal AI-powered currency assistant.
        </p>

    </section>


    <main class="main-grid">

        <!-- CURRENCY CONVERTER -->

        <section class="panel">

            <div class="panel-heading">
                <div>
                    <div class="panel-title">Currency Converter</div>
                    <div class="panel-subtitle">Simple. Fast. Intelligent.</div>
                </div>

                <div class="live-label">● LIVE RATES</div>
            </div>


            <label class="field-label" for="amount">AMOUNT</label>

            <input
                type="number"
                id="amount"
                class="amount-input"
                value="100"
                min="0.01"
                step="any"
                placeholder="Enter amount"
            >


            <div class="currency-row">

                <div>
                    <label class="field-label" for="fromCurrency">FROM</label>

                    <select id="fromCurrency" class="currency-select">
                        <option value="USD">🇺🇸 USD - US Dollar</option>
                        <option value="INR" selected>🇮🇳 INR - Indian Rupee</option>
                        <option value="EUR">🇪🇺 EUR - Euro</option>
                        <option value="GBP">🇬🇧 GBP - British Pound</option>
                        <option value="JPY">🇯🇵 JPY - Japanese Yen</option>
                        <option value="AED">🇦🇪 AED - UAE Dirham</option>
                        <option value="CAD">🇨🇦 CAD - Canadian Dollar</option>
                        <option value="AUD">🇦🇺 AUD - Australian Dollar</option>
                        <option value="SGD">🇸🇬 SGD - Singapore Dollar</option>
                        <option value="CHF">🇨🇭 CHF - Swiss Franc</option>
                    </select>
                </div>

                <div class="swap-wrap">
                    <button class="swap-btn" id="swapBtn" title="Swap currencies">⇄</button>
                </div>

                <div>
                    <label class="field-label" for="toCurrency">TO</label>

                    <select id="toCurrency" class="currency-select">
                        <option value="USD" selected>🇺🇸 USD - US Dollar</option>
                        <option value="INR">🇮🇳 INR - Indian Rupee</option>
                        <option value="EUR">🇪🇺 EUR - Euro</option>
                        <option value="GBP">🇬🇧 GBP - British Pound</option>
                        <option value="JPY">🇯🇵 JPY - Japanese Yen</option>
                        <option value="AED">🇦🇪 AED - UAE Dirham</option>
                        <option value="CAD">🇨🇦 CAD - Canadian Dollar</option>
                        <option value="AUD">🇦🇺 AUD - Australian Dollar</option>
                        <option value="SGD">🇸🇬 SGD - Singapore Dollar</option>
                        <option value="CHF">🇨🇭 CHF - Swiss Franc</option>
                    </select>
                </div>

            </div>


            <button class="convert-btn" id="convertBtn">
                ⇄ &nbsp; Convert Currency
            </button>


            <div class="result-box" id="resultBox">

                <div class="result-label">CONVERSION RESULT</div>

                <div class="result-amount" id="resultAmount">--</div>

                <div class="result-rate" id="resultRate"></div>

                <div class="result-actions">
                    <button class="copy-btn" id="copyBtn">▢ Copy Result</button>
                </div>

            </div>


            <div class="quick-section">

                <div class="quick-title">Popular currency pairs</div>

                <div class="quick-pairs">
                    <button class="pair-btn" data-from="USD" data-to="INR">USD → INR</button>
                    <button class="pair-btn" data-from="EUR" data-to="INR">EUR → INR</button>
                    <button class="pair-btn" data-from="GBP" data-to="USD">GBP → USD</button>
                    <button class="pair-btn" data-from="USD" data-to="EUR">USD → EUR</button>
                    <button class="pair-btn" data-from="AED" data-to="INR">AED → INR</button>
                    <button class="pair-btn" data-from="INR" data-to="USD">INR → USD</button>
                </div>

            </div>

        </section>


        <!-- AI ASSISTANT -->

        <section class="panel ai-panel">

            <div class="panel-heading">

                <div class="ai-title-row">

                    <div class="ai-heading-icon">✧</div>

                    <div>
                        <div class="panel-title">AI Assistant</div>
                        <div class="panel-subtitle">Powered by FluxExchange AI</div>
                    </div>

                </div>

                <div class="live-label">GPT-4o MINI</div>

            </div>


            <div class="ai-output" id="aiOutput">

                <div class="welcome-message" id="welcomeMessage">

                    <div class="welcome-icon">✧</div>

                    <strong>How can I help you today?</strong>

                    <p>
                        Ask me to convert currencies, explain exchange rates
                        or calculate international payments.
                    </p>

                </div>

            </div>


            <div class="chat-input-area">

                <textarea
                    class="chat-input"
                    id="question"
                    rows="2"
                    placeholder="e.g. Convert 500 USD to INR..."
                ></textarea>


                <div class="chat-bottom">

                    <span class="input-hint">Enter to send · Shift + Enter for new line</span>

                    <button class="ask-btn" id="askBtn">
                        Ask AI &nbsp; →
                    </button>

                </div>

            </div>

        </section>

    </main>


    <section class="info-strip">

        <div class="info-item">
            <strong>AI Powered</strong>
            <span>Intelligent currency assistance</span>
        </div>

        <div class="info-item">
            <strong>Global Currencies</strong>
            <span>International currency support</span>
        </div>

        <div class="info-item">
            <strong>Simple & Secure</strong>
            <span>No account required</span>
        </div>

    </section>

</div>


<footer>
    <div class="container footer-inner">
        <span>© 2026 FluxExchange. Built with AI.</span>
        <span>Exchange rates are indicative and may be delayed.</span>
    </div>
</footer>


<div class="toast" id="toast"></div>


<script>

const amountInput = document.getElementById("amount");
const fromCurrency = document.getElementById("fromCurrency");
const toCurrency = document.getElementById("toCurrency");

const convertBtn = document.getElementById("convertBtn");
const resultBox = document.getElementById("resultBox");
const resultAmount = document.getElementById("resultAmount");
const resultRate = document.getElementById("resultRate");

const questionInput = document.getElementById("question");
const askBtn = document.getElementById("askBtn");
const aiOutput = document.getElementById("aiOutput");
const welcomeMessage = document.getElementById("welcomeMessage");

let lastResult = "";


function showToast(message) {
    const toast = document.getElementById("toast");

    toast.textContent = message;
    toast.classList.add("show");

    setTimeout(() => {
        toast.classList.remove("show");
    }, 2200);
}


function formatNumber(value) {
    return Number(value).toLocaleString("en-US", {
        minimumFractionDigits: 2,
        maximumFractionDigits: 4
    });
}


// SWAP CURRENCIES

document.getElementById("swapBtn").addEventListener("click", () => {

    const previousFrom = fromCurrency.value;

    fromCurrency.value = toCurrency.value;
    toCurrency.value = previousFrom;

    resultBox.style.display = "none";

});


// QUICK PAIRS

document.querySelectorAll(".pair-btn").forEach(button => {

    button.addEventListener("click", () => {

        fromCurrency.value = button.dataset.from;
        toCurrency.value = button.dataset.to;

        resultBox.style.display = "none";

    });

});


// CURRENCY CONVERSION THROUGH AI AGENT

convertBtn.addEventListener("click", async () => {

    const amount = Number(amountInput.value);
    const from = fromCurrency.value;
    const to = toCurrency.value;

    if (!Number.isFinite(amount) || amount <= 0) {
        showToast("Please enter a valid amount.");
        return;
    }

    const question =
        `Convert ${amount} ${from} to ${to}. ` +
        `Use the currency conversion tool and provide the exchange rate.`;

    convertBtn.disabled = true;
    convertBtn.textContent = "⟳  Converting...";

    resultBox.style.display = "none";

    try {

        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ question })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Conversion failed.");
        }

        const answer = data.answer || "No response received.";

        // Extract conversion result and exchange rate from AI response.
        const conversionMatch = answer.match(
            /([\d,]+(?:\.\d+)?)\s+([A-Z]{3})\s*=\s*([\d,]+(?:\.\d+)?)\s+([A-Z]{3})/i
        );

        const rateMatch = answer.match(
            /Exchange rate:\s*1\s+([A-Z]{3})\s*=\s*([\d,.]+)\s+([A-Z]{3})/i
        );

        if (conversionMatch) {

            const originalAmount = conversionMatch[1];
            const originalCurrency = conversionMatch[2];
            const convertedAmount = conversionMatch[3];
            const convertedCurrency = conversionMatch[4];

            resultAmount.textContent =
                `${convertedAmount} ${convertedCurrency}`;

            resultRate.textContent = rateMatch
                ? `1 ${rateMatch[1]} = ${rateMatch[2]} ${rateMatch[3]}`
                : `${originalAmount} ${originalCurrency} converted successfully.`;

            lastResult =
                `${originalAmount} ${originalCurrency} = ` +
                `${convertedAmount} ${convertedCurrency}\n` +
                `${resultRate.textContent}`;

            resultBox.style.display = "block";

        } else {

            // Show the full agent response if it uses a different format.
            resultAmount.textContent = "See AI response";
            resultRate.textContent = answer;
            lastResult = answer;
            resultBox.style.display = "block";

        }

    } catch (error) {

        showToast(error.message || "Something went wrong.");

    } finally {

        convertBtn.disabled = false;
        convertBtn.textContent = "⇄  Convert Currency";

    }

});


// COPY RESULT

document.getElementById("copyBtn").addEventListener("click", async () => {

    if (!lastResult) return;

    try {
        await navigator.clipboard.writeText(lastResult);
        showToast("Conversion copied!");
    } catch {
        showToast("Unable to copy result.");
    }

});


// AI ASSISTANT

askBtn.addEventListener("click", sendMessage);


questionInput.addEventListener("keydown", (event) => {

    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }

});


async function sendMessage() {

    const question = questionInput.value.trim();

    if (!question) {
        showToast("Please enter a question.");
        return;
    }

    askBtn.disabled = true;
    askBtn.textContent = "Thinking...";

    welcomeMessage?.remove();

    const loading = document.createElement("div");
    loading.className = "loading";

    const spinner = document.createElement("div");
    spinner.className = "spinner";

    const loadingText = document.createElement("span");
    loadingText.textContent = "FluxExchange AI is thinking...";

    loading.appendChild(spinner);
    loading.appendChild(loadingText);

    aiOutput.replaceChildren(loading);

    questionInput.value = "";

    try {

        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ question })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "AI request failed.");
        }

        const answer = document.createElement("div");
        answer.className = "ai-response";

        // textContent prevents HTML injection from model output.
        answer.textContent = data.answer || "No response received.";

        aiOutput.replaceChildren(answer);

    } catch (error) {

        const errorMessage = document.createElement("div");
        errorMessage.className = "ai-response";
        errorMessage.style.color = "#ff8791";
        errorMessage.textContent = "Error: " + error.message;

        aiOutput.replaceChildren(errorMessage);

    } finally {

        askBtn.disabled = false;
        askBtn.textContent = "Ask AI  →";

    }

}

</script>

</body>
</html>
"""


# --------------------------------------------------
# ROUTES
# --------------------------------------------------

@app.get("/", response_class=HTMLResponse)
async def home():
    return HTMLResponse(content=HTML_PAGE)


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "app": "FluxExchange",
        "message": "AI Currency Converter is running"
    }


@app.post("/chat")
async def chat(request: ChatRequest):

    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    try:

        result = agent.invoke({
            "messages": [
                {
                    "role": "user",
                    "content": question
                }
            ]
        })

        messages = result.get("messages", [])

        answer = None

        for message in reversed(messages):

            content = getattr(message, "content", None)

            if getattr(message, "type", None) == "ai" and content:
                answer = content
                break

        if isinstance(answer, list):
            answer = "\n".join(
                str(item.get("text", item)) if isinstance(item, dict)
                else str(item)
                for item in answer
            )

        if not answer:
            answer = "Sorry, I could not generate a response."

        return {
            "success": True,
            "answer": answer
        }

    except Exception as e:

        print(f"AI Agent Error: {str(e)}")

        raise HTTPException(
            status_code=502,
            detail="AI service is temporarily unavailable. Please try again."
        )
