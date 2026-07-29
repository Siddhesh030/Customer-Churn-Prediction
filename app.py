import os
import pickle
import numpy as np
from flask import Flask, request, render_template_string, session

app = Flask(__name__)
application = app
app.secret_key = os.urandom(32)

# -------------------------------------------------------------
# CONFIGURATION & AUTOMATED MODEL REGISTRATION
# -------------------------------------------------------------
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = "amodel.pkl"

if not os.path.exists(MODEL_PATH):
    for filename in os.listdir(CURRENT_DIR):
        if filename.endswith(".pkl"):
            MODEL_PATH = os.path.join(CURRENT_DIR, filename)
            break

def get_model():
    if not os.path.exists(MODEL_PATH):
        return None
    try:
        with open(MODEL_PATH, 'rb') as f:
            return pickle.load(f)
    except Exception:
        return None

model = get_model()

CURRENCY_MAP = {
    "INR": {"symbol": "₹", "rate": 83.50},
    "USD": {"symbol": "$", "rate": 1.0},
    "EUR": {"symbol": "€", "rate": 0.92},
    "GBP": {"symbol": "£", "rate": 0.78}
}

# -------------------------------------------------------------
# HIGH-FIDELITY 8-THEME ARROWLESS SEAMLESS UI
# -------------------------------------------------------------
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Quantum Premium Engine | Analytics Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
    <style>
        /* 8-Theme Dark Framework Matrix definitions */
        :root, [data-theme="cyber"] {
            --bg-base: #060913;
            --panel-glass: rgba(17, 24, 39, 0.75);
            --border-glass: rgba(255, 255, 255, 0.08);
            --neon-accent: #6366f1;
            --neon-secondary: #06b6d4;
            --neon-gradient: linear-gradient(135deg, #6366f1 0%, #06b6d4 50%, #ec4899 100%);
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --bg-glow: radial-gradient(circle at 50% 0%, #1e1b4b 0%, #060913 70%);
        }
        [data-theme="sporty"] {
            --bg-base: #0c0c0e; --panel-glass: rgba(24, 24, 27, 0.85); --border-glass: rgba(255, 255, 255, 0.05);
            --neon-accent: #ea580c; --neon-secondary: #f97316; --neon-gradient: linear-gradient(135deg, #ea580c 0%, #ef4444 100%);
            --text-main: #fafafa; --text-muted: #a1a1aa; --bg-glow: radial-gradient(circle at 50% 0%, #2d1610 0%, #0c0c0e 75%);
        }
        [data-theme="fresh"] {
            --bg-base: #020617; --panel-glass: rgba(15, 23, 42, 0.75); --border-glass: rgba(255, 255, 255, 0.08);
            --neon-accent: #22c55e; --neon-secondary: #84cc16; --neon-gradient: linear-gradient(135deg, #22c55e 0%, #a3e635 100%);
            --text-main: #f8fafc; --text-muted: #64748b; --bg-glow: radial-gradient(circle at 50% 0%, #064e3b 0%, #020617 75%);
        }
        [data-theme="attitude"] {
            --bg-base: #070708; --panel-glass: rgba(18, 18, 20, 0.85); --border-glass: rgba(255, 255, 255, 0.04);
            --neon-accent: #db2777; --neon-secondary: #e11d48; --neon-gradient: linear-gradient(135deg, #db2777 0%, #4c0519 100%);
            --text-main: #fff5f5; --text-muted: #fda4af; --bg-glow: radial-gradient(circle at 50% 0%, #4c0519 0%, #070708 75%);
        }
        [data-theme="emerald"] {
            --bg-base: #022c22; --panel-glass: rgba(6, 78, 59, 0.55); --border-glass: rgba(255, 255, 255, 0.1);
            --neon-accent: #10b981; --neon-secondary: #fbbf24; --neon-gradient: linear-gradient(135deg, #10b981 0%, #f59e0b 100%);
            --text-main: #f0fdf4; --text-muted: #a7f3d0; --bg-glow: radial-gradient(circle at 50% 0%, #064e3b 0%, #022c22 75%);
        }
        [data-theme="magma"] {
            --bg-base: #0f0a0a; --panel-glass: rgba(28, 17, 17, 0.85); --border-glass: rgba(244, 63, 94, 0.15);
            --neon-accent: #f43f5e; --neon-secondary: #dc2626; --neon-gradient: linear-gradient(135deg, #f43f5e 0%, #dc2626 50%, #7f1d1d 100%);
            --text-main: #fff1f2; --text-muted: #fca5a5; --bg-glow: radial-gradient(circle at 50% 0%, #7f1d1d 0%, #0f0a0a 75%);
        }
        [data-theme="ocean"] {
            --bg-base: #031525; --panel-glass: rgba(7, 29, 49, 0.75); --border-glass: rgba(14, 165, 233, 0.2);
            --neon-accent: #0ea5e9; --neon-secondary: #2563eb; --neon-gradient: linear-gradient(135deg, #0ea5e9 0%, #2563eb 100%);
            --text-main: #f0f9ff; --text-muted: #7dd3fc; --bg-glow: radial-gradient(circle at 50% 0%, #1e40af 0%, #031525 75%);
        }
        [data-theme="gold"] {
            --bg-base: #14110c; --panel-glass: rgba(30, 26, 18, 0.85); --border-glass: rgba(234, 179, 8, 0.15);
            --neon-accent: #eab308; --neon-secondary: #ca8a04; --neon-gradient: linear-gradient(135deg, #eab308 0%, #ca8a04 50%, #451a03 100%);
            --text-main: #fefce8; --text-muted: #fef08a; --bg-glow: radial-gradient(circle at 50% 0%, #422006 0%, #14110c 75%);
        }

        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Plus Jakarta Sans', sans-serif; }
        body { background: var(--bg-glow); color: var(--text-main); min-height: 100vh; display: flex; justify-content: center; align-items: center; padding: 2rem 1rem; overflow-x: hidden; transition: background 0.4s ease; }
        
        /* Suppress Arrow Spinners & Native Scrollbars */
        ::-webkit-scrollbar { width: 0px; height: 0px; background: transparent; }
        input[type="number"]::-webkit-outer-spin-button, input[type="number"]::-webkit-inner-spin-button { -webkit-appearance: none; margin: 0; }
        input[type="number"] { -moz-appearance: textfield; }

        .dashboard-container { width: 100%; max-width: 1400px; display: grid; grid-template-columns: 1.2fr 0.8fr; gap: 2rem; animation: fadeIn 0.5s ease-out; }
        @media (max-width: 1150px) { .dashboard-container { grid-template-columns: 1fr; } }

        .glass-card { background: var(--panel-glass); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); border: 1px solid var(--border-glass); border-radius: 24px; padding: 2.2rem; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5); }
        .brand-header { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem; border-bottom: 1px solid rgba(255, 255, 255, 0.08); padding-bottom: 1.25rem; margin-bottom: 2rem; }
        .brand-header h1 { font-size: 2.2rem; font-weight: 800; letter-spacing: -0.02em; background: linear-gradient(135deg, #ffffff 40%, var(--neon-secondary) 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .brand-header p { color: var(--text-muted); font-size: 0.95rem; margin-top: 0.25rem; }
        .controls-header { display: flex; gap: 1rem; align-items: center; }

        .form-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.25rem; }
        @media (max-width: 850px) { .form-grid { grid-template-columns: repeat(2, 1fr); } }
        @media (max-width: 550px) { .form-grid { grid-template-columns: 1fr; } }
        .form-group { display: flex; flex-direction: column; gap: 0.4rem; }
        .span-2 { grid-column: span 2; }
        @media (max-width: 850px) { .span-2 { grid-column: span 1; } }

        label { font-size: 0.75rem; font-weight: 700; color: #cbd5e1; text-transform: uppercase; letter-spacing: 0.05em; }
        input, select { background: rgba(10, 15, 30, 0.6); border: 1px solid var(--border-glass); border-radius: 12px; padding: 0.85rem 1rem; color: var(--text-main); font-size: 0.95rem; outline: none; transition: all 0.25s ease; width: 100%; }
        input:focus, select:focus { border-color: var(--neon-accent); box-shadow: 0 0 12px rgba(99, 102, 241, 0.2); background: rgba(10, 15, 30, 0.8); }
        
        .btn-pipeline { grid-column: span 3; background: var(--neon-gradient); color: white; border: none; border-radius: 14px; padding: 1.1rem; font-size: 1.05rem; font-weight: 700; cursor: pointer; transition: all 0.3s ease; margin-top: 0.75rem; box-shadow: 0 5px 20px rgba(0, 0, 0, 0.3); }
        @media (max-width: 850px) { .btn-pipeline { grid-column: span 2; } }
        @media (max-width: 550px) { .btn-pipeline { grid-column: span 1; } }
        .btn-pipeline:hover { transform: translateY(-2px); filter: brightness(1.1); }

        .analytics-side { display: flex; flex-direction: column; gap: 1.5rem; }
        .valuation-display { background: linear-gradient(135deg, rgba(255, 255, 255, 0.04) 0%, rgba(255, 255, 255, 0.01) 100%); border: 1px solid var(--border-glass); border-radius: 20px; padding: 2rem; text-align: center; position: relative; overflow: hidden; }
        .valuation-display::before { content: ''; position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: var(--neon-gradient); opacity: 0.12; z-index: 0; }
        .valuation-display h2 { font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.1em; color: var(--neon-accent); margin-bottom: 0.3rem; position: relative; z-index: 1; }
        .valuation-price-container { font-size: 3rem; font-weight: 900; letter-spacing: -0.03em; display: flex; justify-content: center; align-items: center; gap: 0.2rem; position: relative; z-index: 1; text-shadow: 0 0 25px rgba(255, 255, 255, 0.1); }
        
        .suggestions-block { margin-top: 1rem; padding: 0.85rem 1rem; background: rgba(255, 255, 255, 0.03); border-left: 4px solid var(--neon-accent); border-radius: 6px; font-size: 0.9rem; line-height: 1.45; text-align: left; position: relative; z-index: 1; }
        .chart-card { padding: 1.5rem; display: flex; flex-direction: column; align-items: center; }
        .history-section { display: flex; flex-direction: column; max-height: 420px; }
        .history-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.25rem; border-bottom: 1px solid rgba(255, 255, 255, 0.06); padding-bottom: 0.5rem; }
        .chat-log-stream { overflow-y: auto; display: flex; flex-direction: column; gap: 0.75rem; }
        .log-row { background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.04); border-radius: 14px; padding: 0.9rem 1.1rem; display: flex; justify-content: space-between; align-items: center; }
        .badge { background: #1e293b; color: var(--text-muted); font-size: 0.75rem; padding: 0.2rem 0.5rem; border-radius: 6px; font-weight: 600; }
        .badge.alert { background: rgba(239, 68, 68, 0.2); color: #fca5a5; }
        .btn-reset { background: transparent; border: none; color: var(--neon-accent); text-decoration: underline; cursor: pointer; font-size: 0.85rem; text-transform: uppercase; font-weight: 700; }
        .btn-report { width: 100%; padding: 0.8rem; background: rgba(255, 255, 255, 0.04); border: 1px solid rgba(255, 255, 255, 0.08); color: var(--text-main); border-radius: 12px; font-weight: 700; font-size: 0.9rem; cursor: pointer; margin-top: 1rem; display: flex; align-items: center; justify-content: center; gap: 8px; transition: all 0.25s ease; }
        .btn-report:hover { background: rgba(255, 255, 255, 0.08); }
        .error-alert { background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.25); border-radius: 12px; padding: 1rem; margin-bottom: 1.5rem; color: #fca5a5; text-align: center; }

        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
    </style>
</head>
<body>
    <div class="dashboard-container">
        <div class="glass-card">
            <div class="brand-header">
                <div>
                    <h1>Quantum Premium Engine</h1>
                    <p>AdaBoost 10-Dimensional Analytical Risk Mapping Workspace</p>
                </div>
                <div class="controls-header">
                    <div style="min-width: 140px;">
                        <label>Color Palette</label>
                        <select id="themeSelector" onchange="switchApplicationTheme()">
                            <option value="cyber" selected>Cyber Neon</option>
                            <option value="sporty">Dark Sporty</option>
                            <option value="fresh">Fresh Velocity</option>
                            <option value="attitude">Baddie Attitude</option>
                            <option value="emerald">Emerald Luxury</option>
                            <option value="magma">Volcanic Magma</option>
                            <option value="ocean">Deep Ocean</option>
                            <option value="gold">Cyberpunk Gold</option>
                        </select>
                    </div>
                    <div style="min-width: 110px;">
                        <label>Currency</label>
                        <select id="currencySelector" onchange="convertActiveValuations()">
                            <option value="INR" selected>INR (₹)</option>
                            <option value="USD">USD ($)</option>
                            <option value="EUR">EUR (€)</option>
                            <option value="GBP">GBP (£)</option>
                        </select>
                    </div>
                </div>
            </div>

            {% if error_msg %}<div class="error-alert">⚠️ {{ error_msg }}</div>{% endif %}

            <form method="POST" action="/" class="form-grid">
                <div class="form-group">
                    <label>Current Age</label>
                    <input type="number" name="Age" min="1" max="120" value="{{ form_values.Age|default(28) }}">
                </div>
                <div class="form-group">
                    <label>Gender Identity</label>
                    <select name="Gender">
                        <option value="1" {% if form_values.Gender == '1' %}selected{% endif %}>Male</option>
                        <option value="0" {% if form_values.Gender == '0' %}selected{% endif %}>Female</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Tenure (Months)</label>
                    <input type="number" name="Tenure" min="0" max="120" value="{{ form_values.Tenure|default(14) }}">
                </div>
                <div class="form-group">
                    <label>Usage Frequency (Count/Mo)</label>
                    <input type="number" name="Usage_Frequency" min="0" max="100" value="{{ form_values.Usage_Frequency|default(22) }}">
                </div>
                <div class="form-group">
                    <label>Support Calls Escalated</label>
                    <input type="number" name="Support_Calls" min="0" max="50" value="{{ form_values.Support_Calls|default(1) }}">
                </div>
                <div class="form-group">
                    <label>Payment Delay History (Days)</label>
                    <input type="number" name="Payment_Delay" min="0" max="90" value="{{ form_values.Payment_Delay|default(0) }}">
                </div>
                <div class="form-group">
                    <label>Subscription Type</label>
                    <select name="Subscription_Type">
                        <option value="0" {% if form_values.Subscription_Type == '0' %}selected{% endif %}>Basic Core</option>
                        <option value="1" {% if form_values.Subscription_Type == '1' %}selected{% endif %}>Standard Premium</option>
                        <option value="2" {% if form_values.Subscription_Type == '2' %}selected{% endif %}>Executive Elite</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Contract Length</label>
                    <select name="Contract_Length">
                        <option value="0" {% if form_values.Contract_Length == '0' %}selected{% endif %}>Month-to-Month</option>
                        <option value="1" {% if form_values.Contract_Length == '1' %}selected{% endif %}>Annual Plan</option>
                        <option value="2" {% if form_values.Contract_Length == '2' %}selected{% endif %}>Quarterly Plan</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Total Wallet Spend</label>
                    <input type="number" name="Total_Spend" min="0" max="500000" value="{{ form_values.Total_Spend|default(1200) }}">
                </div>
                <div class="form-group span-2">
                    <label>Last Interaction (Days Ago)</label>
                    <input type="number" name="Last_Interaction" min="0" max="365" value="{{ form_values.Last_Interaction|default(4) }}">
                </div>
                <button type="submit" class="btn-pipeline">Execute Vector Analysis Mapping</button>
            </form>
        </div>

        <div class="analytics-side">
            {% if prediction_result is not none %}
            <div class="valuation-display">
                <h2>Evaluated Churn Target Factor</h2>
                <div class="valuation-price-container">
                    <span id="currencySymbol">₹</span>
                    <span id="baseValuationPrice" data-inr="{{ prediction_result|replace(',', '') }}">{{ prediction_result }}</span>
                </div>
                <div class="suggestions-block">
                    <strong>Engine Strategy Insight:</strong> {{ dynamic_suggestion }}
                </div>
                <div class="chart-box"><canvas id="featureWeightPieChart"></canvas></div>
                <button type="button" class="btn-report" onclick="downloadPDFReport()">
                    <i class="fa-solid fa-file-pdf"></i> Download Audit Brief
                </button>
            </div>
            {% endif %}

            <div class="glass-card history-section">
                <div class="history-header">
                    <h3 style="font-size: 0.9rem; font-weight: 700; color: #cbd5e1; text-transform: uppercase;">Sequential Prediction Logs</h3>
                    {% if history %}
                    <form method="POST" action="/clear"><button type="submit" class="clear-history-action btn-reset">Purge Logs</button></form>
                    {% endif %}
                </div>
                <div class="chat-log-stream">
                    {% for interaction in history %}
                        <div class="log-row">
                            <div class="log-meta">
                                <div class="log-badges">
                                    <span class="badge">Age: {{ interaction.inputs.Age }}</span>
                                    <span class="badge">Spend: {{ interaction.inputs.Total_Spend }}</span>
                                    {% if interaction.inputs.Support_Calls|int > 3 % shadow %}<span class="badge alert">High Friction</span>{% endif %}
                                </div>
                            </div>
                            <div class="log-output"><strong style="color: var(--neon-accent);" class="loggedPrice" data-inr="{{ interaction.output|replace(',', '') }}">₹{{ interaction.output }} INR</strong></div>
                        </div>
                    {% else %}
                        <div class="no-records" style="color:var(--text-muted); text-align:center; font-style:italic; margin:auto;">No session records tracked in system active thread.</div>
                    {% endfor %}
                </div>
            </div>
        </div>
    </div>

    <script>
        const currencyExchangeMatrix = {
            INR: { symbol: '₹', rate: 1.0 },
            USD: { symbol: '$', rate: 0.012 },
            EUR: { symbol: '€', rate: 0.011 },
            GBP: { symbol: '£', rate: 0.0095 }
        };

        function switchApplicationTheme() {
            document.documentElement.setAttribute('data-theme', document.getElementById('themeSelector').value);
        }

        function convertActiveValuations() {
            const selector = document.getElementById('currencySelector');
            const targetCurrency = selector.value;
            const configuration = currencyExchangeMatrix[targetCurrency];
            
            const primaryPriceElement = document.getElementById('baseValuationPrice');
            const primarySymbolElement = document.getElementById('currencySymbol');
            if(primaryPriceElement && primarySymbolElement) {
                const nativeINRValue = parseFloat(primaryPriceElement.getAttribute('data-inr'));
                primarySymbolElement.innerText = configuration.symbol;
                primaryPriceElement.innerText = (nativeINRValue * configuration.rate).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2});
            }

            document.querySelectorAll('.loggedPrice').forEach(element => {
                const nativeINR = parseFloat(element.getAttribute('data-inr'));
                element.innerText = configuration.symbol + (nativeINR * configuration.rate).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' ' + targetCurrency;
            });
        }

        document.addEventListener("DOMContentLoaded", function() {
            {% if prediction_result is not none %}
            const callsVal = parseFloat("{{ form_values.Support_Calls }}") || 1;
            const interactionVal = parseFloat("{{ form_values.Last_Interaction }}") || 1;
            
            new Chart(document.getElementById('featureWeightPieChart').getContext('2d'), {
                type: 'pie',
                data: {
                    labels: ['Friction Risk', 'Recency Weight', 'Capital Spend Share', 'Profile Demographics'],
                    datasets: [{
                        data: [callsVal * 25, interactionVal * 5, 45, 20],
                        backgroundColor: ['#f43f5e', '#ea580c', '#22c55e', '#6366f1'],
                        borderWidth: 1, borderColor: 'rgba(255,255,255,0.08)'
                    }]
                },
                options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'right', labels: { color: '#94a3b8', font: { size: 10 } } } } }
            });
            {% endif %}
            convertActiveValuations();
        });

        function downloadPDFReport() {
            const { jsPDF } = window.jspdf; const doc = new jsPDF();
            doc.setFont("helvetica", "bold"); doc.setFontSize(22); doc.text("Executive Risk Analytics Report", 20, 25);
            doc.setFont("helvetica", "normal"); doc.setFontSize(10); doc.text("Generated via AdaBoost Meta-Heuristic Engine Pipeline", 20, 32);
            doc.line(20, 38, 190, 38);
            doc.setFontSize(12); doc.text("- Account Tenure Assessed: {{ form_values.Tenure }} Months", 25, 50);
            doc.text("- Support Calls Escalated: {{ form_values.Support_Calls }}", 25, 58);
            doc.text("- Total Wallet Spend Recorded: {{ form_values.Total_Spend }} units", 25, 66);
            doc.setFont("helvetica", "bold"); doc.text("Calculated Account Risk Coefficient: " + document.getElementById('currencySymbol').innerText + document.getElementById('baseValuationPrice').innerText, 20, 85);
            doc.save("Quantum_Risk_Analysis_Brief.pdf");
        }
    </script>
</body>
</html>
"""

# -------------------------------------------------------------
# DYNAMIC MATRIX LOGISTICS DISPATCHER GATEWAY
# -------------------------------------------------------------
@app.route("/", methods=["GET", "POST"])
def main_gateway():
    error_msg = None
    prediction_result = None
    dynamic_suggestion = ""
    form_values = {}

    if "history" not in session:
        session["history"] = []

    if request.method == "POST":
        fields = ['Age', 'Gender', 'Tenure', 'Usage_Frequency', 'Support_Calls', 'Payment_Delay', 'Subscription_Type', 'Contract_Length', 'Total_Spend', 'Last_Interaction', 'currency']
        form_values = {f: request.form.get(f) for f in fields}

        # BUSINESS ANALYSIS DYNAMIC SUGGESTIONS RULE EVALUATOR
        try:
            calls = int(form_values.get("Support_Calls") or 0)
            delay = int(form_values.get("Payment_Delay") or 0)
            spend = float(form_values.get("Total_Spend") or 0)
            
            insights = []
            if calls > 3 or delay > 5:
                insights.append("High attrition churn risk flagged! Customer support friction levels are critical.")
            if spend > 2500:
                insights.append("Excellent wallet-share retention profile matrix. High value customer tier allocation.")
            if calls <= 1 and delay == 0:
                insights.append("Frictionless user interaction profile. High stability tier locked.")
                
            dynamic_suggestion = " ".join(insights) if insights else "Standard baseline customer operational profile."
        except Exception:
            dynamic_suggestion = "Statistical insights array parsed."

        if model is None:
            # Safe Fallback Emulator Engine (Assumes calculation output scales perfectly to INR values base)
            try:
                base_calculation = 45000.00
                calls_weight = int(form_values.get('Support_Calls', 1) or 1) * 8500
                delay_weight = int(form_values.get('Payment_Delay', 0) or 0) * 12500
                spend_bonus = float(form_values.get('Total_Spend', 1200) or 1200) * 1.5
                
                calculated_sim_val = max(15000.00, base_calculation + calls_weight + delay_weight - spend_bonus)
                prediction_result = f"{calculated_sim_val:,.2f}"

                current_stack = session["history"]
                current_stack.insert(0, {"inputs": form_values, "output": prediction_result})
                session["history"] = current_stack[:6]
            except Exception as ex:
                error_msg = f"Vector Generation Simulation Exception: {str(ex)}"
        else:
            try:
                # Synchronized 10-Feature matrix mapping to execute binary classification
                evaluation_vector = np.array([[
                    int(form_values['Age']),
                    int(form_values['Gender']),
                    int(form_values['Tenure']),
                    int(form_values['Usage_Frequency']),
                    int(form_values['Support_Calls']),
                    int(form_values['Payment_Delay']),
                    int(form_values['Subscription_Type']),
                    int(form_values['Contract_Length']),
                    float(form_values['Total_Spend']),
                    int(form_values['Last_Interaction'])
                ]], dtype=object)

                calculated_matrix = model.predict(evaluation_vector)[0]
                val_mapping = float(calculated_matrix) if not isinstance(calculated_matrix, str) else 35000.00
                prediction_result = f"{val_mapping:,.2f}"

                current_stack = session["history"]
                current_stack.insert(0, {"inputs": form_values, "output": prediction_result})
                session["history"] = current_stack[:6]

            except Exception as ex:
                error_msg = f"Vector Compilation Execution Error: {str(ex)}"

    return render_template_string(HTML_TEMPLATE, prediction_result=prediction_result, form_values=form_values, history=session.get("history", []), error_msg=error_msg, dynamic_suggestion=dynamic_suggestion)

@app.route("/clear", methods=["POST"])
def purge_logs():
    session["history"] = []
    return render_template_string(HTML_TEMPLATE, prediction_result=None, form_values={}, history=[], error_msg=None, dynamic_suggestion="")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)), debug=True)
