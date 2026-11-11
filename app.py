
@app.get("/", response_class=HTMLResponse)
def home():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Flux | AI Currency Converter</title>

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">

<style>
:root {
    --bg: #080d18;
    --panel: #111a2b;
    --panel2: #172338;
    --border: rgba(255,255,255,.09);
    --text: #f1f5ff;
    --muted: #8998b3;
    --accent: #8b9cff;
    --green: #43dfad;
}

* { box-sizing: border-box; }

body {
    margin: 0;
    min-height: 100vh;
    background:
        radial-gradient(ellipse at 10% 0%, #263b6838, transparent 40%),
        radial-gradient(ellipse at 90% 90%, #45307c25, transparent 40%),
        var(--bg);
    color: var(--text);
    font-family: 'DM Sans', sans-serif;
}

button, textarea { font: inherit; }

.container {
    width: min(1120px, 92%);
    margin: auto;
}

nav {
    height: 78px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid var(--border);
}

.logo {
    display: flex;
    align-items: center;
    gap: 11px;
    font: 700 24px 'Space Grotesk', sans-serif;
}

.logo-icon {
    width: 39px;
    height: 39px;
    display: grid;
    place-items: center;
    border-radius: 12px;
    background: linear-gradient(135deg,#8b9cff,#a78bfa);
    color: #101629;
    font-size: 22px;
}

.nav-right {
    display: flex;
    align-items: center;
    gap: 10px;
    color: var(--muted);
    font-size: 13px;
}

.status-dot {
    width: 8px;
    height: 8px;
    background: var(--green);
    border-radius: 50%;
    box-shadow: 0 0 12px var(--green);
}

.hero {
    text-align: center;
    padding: 68px 0 38px;
}

.tag {
    display: inline-flex;
    gap: 8px;
    align-items: center;
    padding: 7px 13px;
    border: 1px solid #8b9cff45;
    background: #8b9cff12;
    color: #aab8ff;
    border-radius: 30px;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1px;
}

h1 {
    font: 700 clamp(34px,5vw,56px) 'Space Grotesk', sans-serif;
    margin: 19px 0 12px;
    letter-spacing: -2px;
}

.gradient {
    background: linear-gradient(90deg,#8ea4ff,#c3a0ff,#54dfc0);
    -webkit-background-clip: text;
    color: transparent;
}

.subtitle {
    color: var(--muted);
    font-size: 15px;
    line-height: 1.7;
}

.dashboard {
    display: grid;
    grid-template-columns: 1.15fr .85fr;
    gap: 22px;
    align-items: start;
}

.card {
    background: linear-gradient(145deg,#151f33,#101827);
    border: 1px solid var(--border);
    border-radius: 22px;
    padding: 26px;
    box-shadow: 0 20px 60px #00000025;
}

.card-heading {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24px;
}

.card-heading h2 {
    font: 600 19px 'Space Grotesk';
    margin: 0;
}

.live {
    color: var(--green);
    font-size: 11px;
    font-weight: 700;
    letter-spacing: .8px;
}

label {
    display: block;
    color: var(--muted);
    font-size: 12px;
    margin-bottom: 10px;
    font-weight: 600;
}

textarea {
    width: 100%;
    min-height: 125px;
    resize: vertical;
    border: 1px solid var(--border);
    outline: none;
    border-radius: 14px;
    background: #0b1424;
    color: white;
    padding: 17px;
    font-size: 15px;
    line-height: 1.6;
    transition: .2s;
}

textarea:focus {
    border-color: var(--accent);
    box-shadow: 0 0 0 3px #8b9cff16;
}

textarea::placeholder { color: #64728b; }

.examples {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    margin: 16px 0 22px;
}

.example {
    padding: 8px 11px;
    background: #ffffff08;
    border: 1px solid var(--border);
    color: #bac6db;
    border-radius: 9px;
    font-size: 11px;
    cursor: pointer;
    transition: .2s;
}

.example:hover {
    border-color: var(--accent);
    color: white;
    background: #8b9cff16;
}

.convert-btn {
    width: 100%;
    padding: 15px;
    border: 0;
    border-radius: 12px;
    color: #101629;
    font-weight: 800;
    font-size: 14px;
    background: linear-gradient(100deg,#9aabff,#b7a2ff);
    cursor: pointer;
    transition: .2s;
}

.convert-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px #9aabff30;
}

.convert-btn:disabled {
    opacity: .55;
    cursor: wait;
    transform: none;
}

.result-card {
    min-height: 340px;
    position: relative;
    overflow: hidden;
}

.result-card::before {
    content: "";
    position: absolute;
    width: 190px;
    height: 190px;
    background: #8b9cff13;
    filter: blur(65px);
    right: -70px;
    top: -80px;
    pointer-events: none;
}

.result-label {
    color: var(--muted);
    font-size: 12px;
    font-weight: 600;
    letter-spacing: .8px;
}

.result-placeholder {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    min-height: 245px;
    color: var(--muted);
}

.result-placeholder .icon {
    font-size: 42px;
    margin-bottom: 15px;
}

.result-placeholder p {
    font-size: 13px;
    line-height: 1.7;
    max-width: 250px;
}

.result-content {
    margin-top: 24px;
    position: relative;
    z-index: 1;
}

.result-value {
    font: 700 clamp(29px,4vw,43px) 'Space Grotesk';
    letter-spacing: -1.5px;
    overflow-wrap: anywhere;
    margin: 13px 0;
    color: var(--green);
}

.result-pair {
    color: var(--muted);
    font-size: 13px;
    margin-bottom: 24px;
}

.rate-box {
    padding: 15px;
    background: #ffffff08;
    border: 1px solid var(--border);
    border-radius: 12px;
    margin-top: 18px;
}

.rate-box span {
    display: block;
    font-size: 11px;
    color: var(--muted);
    margin-bottom: 7px;
}

.rate-box strong {
    font-size: 14px;
    overflow-wrap: anywhere;
}

.copy-btn {
    margin-top: 17px;
    padding: 10px 15px;
    border: 1px solid var(--border);
    border-radius: 9px;
    color: white;
    background: #ffffff0a;
    cursor: pointer;
    font-size: 12px;
}

.copy-btn:hover { border-color: var(--accent); }

.loader {
    width: 30px;
    height: 30px;
    border: 3px solid #ffffff20;
    border-top-color: var(--accent);
    border-radius: 50%;
    animation: spin .8s linear infinite;
    margin: 0 auto 18px;
}

@keyframes spin { to { transform: rotate(360deg); } }

.info-grid {
    display: grid;
    grid-template-columns: repeat(3,1fr);
    gap: 15px;
    margin: 26px 0 65px;
}

.info {
    padding: 18px;
    border: 1px solid var(--border);
    border-radius: 14px;
    background: #ffffff05;
}

.info strong {
    display: block;
    font-size: 13px;
    margin-bottom: 7px;
}

.info p {
    color: var(--muted);
    font-size: 11px;
    line-height: 1.6;
    margin: 0;
}

footer {
    border-top: 1px solid var(--border);
    padding: 24px 0;
    color: var(--muted);
    font-size: 11px;
    text-align: center;
}

.error { color: #ff8585; }

@media(max-width:760px) {
    .dashboard { grid-template-columns: 1fr; }
    .hero { padding: 48px 0 28px; }
    .card { padding: 21px; }
    .info-grid { grid-template-columns: 1fr; margin-bottom: 40px; }
    nav { height: 68px; }
    .nav-right { font-size: 10px; }
    h1 { letter-spacing: -1px; }
}
</style>
</head>

<body>
<div class="container">

<nav>
    <div class="logo">
        <div class="logo-icon">↗</div>
        Flux<span class="gradient">Exchange</span>
    </div>
    <div class="nav-right">
        <span class="status-dot"></span>
        AI POWERED · LIVE RATES
    </div>
</nav>

<section class="hero">
    <div class="tag">✦ SMART CURRENCY INTELLIGENCE</div>
    <h1>Currency conversion,<br><span class="gradient">made intelligent.</span></h1>
    <p class="subtitle">
        Just ask in natural language. Get currency conversions<br>
        powered by AI and live exchange-rate data.
    </p>
</section>

<section class="dashboard">

    <div class="card">
        <div class="card-heading">
            <h2>Make a conversion</h2>
            <span class="live">● READY</span>
        </div>

        <label for="question">YOUR CONVERSION REQUEST</label>

        <textarea id="question"
            placeholder="e.g. Convert 500 USD to INR at today's rate..."></textarea>

        <label>QUICK EXAMPLES</label>
        <div class="examples">
            <button class="example" onclick="setExample('Convert 100 USD to INR')">USD → INR</button>
            <button class="example" onclick="setExample('Convert 500 EUR to USD')">EUR → USD</button>
            <button class="example" onclick="setExample('Convert 1000 INR to GBP')">INR → GBP</button>
            <button class="example" onclick="setExample('Convert 2500 JPY to INR')">JPY → INR</button>
        </div>

        <button class="convert-btn" id="send" onclick="sendMessage()">
            Convert currency <span>→</span>
        </button>
    </div>

    <div class="card result-card">
        <div class="card-heading">
            <h2>Conversion result</h2>
            <span class="result-label">OUTPUT</span>
        </div>

        <div id="answer">
            <div class="result-placeholder">
                <div class="icon">💱</div>
                <strong>Your result awaits</strong>
                <p>Enter an amount and currencies to see your conversion details here.</p>
            </div>
        </div>
    </div>

</section>

<section class="info-grid">
    <div class="info">
        <strong>✦ AI-Powered Interface</strong>
        <p>Understand natural language conversion requests using an AI agent.</p>
    </div>
    <div class="info">
        <strong>↗ Live Exchange Rates</strong>
        <p>Fetch the latest available rates from an external exchange-rate API.</p>
    </div>
    <div class="info">
        <strong>◈ Smart & Simple</strong>
        <p>Get clear conversion results without manually calculating exchange rates.</p>
    </div>
</section>

<footer>
    FluxExchange · AI Currency Converter · Exchange rates are subject to API updates.
</footer>

</div>

<script>
function setExample(value) {
    document.getElementById("question").value = value;
    document.getElementById("question").focus();
}

function escapeHTML(value) {
    return String(value).replace(/[&<>"']/g, char => ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#39;"
    })[char]);
}

async function sendMessage() {
    const question = document.getElementById("question").value.trim();
    const answer = document.getElementById("answer");
    const button = document.getElementById("send");

    if (!question) {
        answer.innerHTML = '<div class="result-placeholder error">Please enter a conversion request.</div>';
        return;
    }

    button.disabled = true;
    button.textContent = "Processing your request...";

    answer.innerHTML = `
        <div class="result-placeholder">
            <div class="loader"></div>
            <strong>Calculating conversion...</strong>
            <p>AI agent is processing your request and retrieving exchange rates.</p>
        </div>`;

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({question})
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Request failed.");
        }

        const result = String(data.answer || "No result generated.");
        const safeResult = escapeHTML(result);

        answer.innerHTML = `
            <div class="result-content">
                <div class="result-label">AI CONVERSION SUMMARY</div>
                <div style="white-space:pre-wrap;line-height:1.8;font-size:14px;overflow-wrap:anywhere">${safeResult}</div>
                <button class="copy-btn" onclick="copyResult(this)">▣ Copy result</button>
            </div>`;

    } catch (error) {
        answer.innerHTML = `
            <div class="result-placeholder error">
                <div class="icon">⚠️</div>
                <strong>Conversion failed</strong>
                <p>${escapeHTML(error.message)}</p>
            </div>`;
    } finally {
        button.disabled = false;
        button.innerHTML = 'Convert currency <span>→</span>';
    }
}

async function copyResult(button) {
    const content = document.querySelector("#answer .result-content > div:nth-child(2)");
    try {
        await navigator.clipboard.writeText(content.innerText);
        button.textContent = "✓ Copied!";
    } catch {
        button.textContent = "Copy unavailable";
    }
}

document.getElementById("question").addEventListener("keydown", function(e) {
    if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) {
        sendMessage();
    }
});
</script>

</body>
</html>
"""
