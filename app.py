import os
import pickle
import numpy as np
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# Model loading logic with serverless fallback
MODEL_FILENAMES = ["Adaboost_model.pkl", "model.pkl"]
model = None

for fname in MODEL_FILENAMES:
    candidate_path = os.path.join(os.path.dirname(__file__), fname)
    if os.path.exists(candidate_path):
        try:
            with open(candidate_path, "rb") as f:
                model = pickle.load(f)
            break
        except Exception as e:
            print(f"Error loading {fname}: {e}")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en" data-theme="dark" data-palette="indigo">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RetainIQ Pro - Enterprise Customer Retention & Churn Analytics</title>
    
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <style>
        :root {
            --bg-base: #090D16;
            --bg-surface: #0F172A;
            --bg-card: rgba(17, 24, 39, 0.7);
            --border: rgba(255, 255, 255, 0.08);
            --text-main: #F8FAFC;
            --text-muted: #94A3B8;
            
            --brand-primary: #6366F1;
            --brand-secondary: #EC4899;
            --brand-gradient: linear-gradient(135deg, #6366F1 0%, #A855F7 50%, #EC4899 100%);
            
            --success: #10B981;
            --danger: #F43F5E;
            --warning: #F59E0B;
            --info: #06B6D4;
            
            --radius-xl: 20px;
            --radius-md: 12px;
            --shadow-glass: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
            --transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        }

        [data-theme="light"] {
            --bg-base: #F8FAFC;
            --bg-surface: #FFFFFF;
            --bg-card: rgba(255, 255, 255, 0.85);
            --border: rgba(0, 0, 0, 0.08);
            --text-main: #0F172A;
            --text-muted: #64748B;
            --shadow-glass: 0 10px 25px -5px rgba(0, 0, 0, 0.08);
        }

        [data-palette="emerald"] {
            --brand-primary: #059669;
            --brand-secondary: #10B981;
            --brand-gradient: linear-gradient(135deg, #059669 0%, #10B981 50%, #06B6D4 100%);
        }

        [data-palette="sunset"] {
            --brand-primary: #FF512F;
            --brand-secondary: #DD2476;
            --brand-gradient: linear-gradient(135deg, #FF512F 0%, #F09819 50%, #DD2476 100%);
        }

        [data-palette="cyberpunk"] {
            --brand-primary: #FF007F;
            --brand-secondary: #00F0FF;
            --brand-gradient: linear-gradient(135deg, #FF007F 0%, #7928CA 50%, #00F0FF 100%);
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Plus Jakarta Sans', sans-serif;
            transition: background 0.3s, border 0.3s, color 0.3s;
        }

        body {
            background: var(--bg-base);
            color: var(--text-main);
            min-height: 100vh;
            background-image: 
                radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.12) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(236, 72, 153, 0.1) 0px, transparent 50%);
            background-attachment: fixed;
        }

        .navbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1.1rem 2rem;
            background: var(--bg-surface);
            border-bottom: 1px solid var(--border);
            position: sticky;
            top: 0;
            z-index: 50;
            backdrop-filter: blur(14px);
        }

        .brand-container {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .brand-icon {
            width: 42px;
            height: 42px;
            border-radius: 10px;
            background: var(--brand-gradient);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.25rem;
            color: #fff;
            box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
        }

        .brand-text h1 {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 1.25rem;
            font-weight: 700;
            letter-spacing: -0.5px;
        }

        .brand-text span {
            font-size: 0.725rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .nav-controls {
            display: flex;
            align-items: center;
            gap: 16px;
        }

        .palette-dock {
            display: flex;
            gap: 8px;
            background: rgba(0,0,0,0.2);
            padding: 5px 8px;
            border-radius: 30px;
            border: 1px solid var(--border);
        }

        .palette-opt {
            width: 18px;
            height: 18px;
            border-radius: 50%;
            cursor: pointer;
            border: 2px solid transparent;
            transition: transform 0.2s;
        }

        .palette-opt:hover { transform: scale(1.2); }
        .palette-opt.active { border-color: #fff; transform: scale(1.15); }
        .p-indigo { background: linear-gradient(135deg, #6366F1, #EC4899); }
        .p-emerald { background: linear-gradient(135deg, #059669, #10B981); }
        .p-sunset { background: linear-gradient(135deg, #FF512F, #DD2476); }
        .p-cyberpunk { background: linear-gradient(135deg, #FF007F, #00F0FF); }

        .btn-theme {
            background: var(--bg-card);
            border: 1px solid var(--border);
            color: var(--text-main);
            width: 38px;
            height: 38px;
            border-radius: 10px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: var(--transition);
        }

        .container {
            max-width: 1400px;
            margin: 2rem auto;
            padding: 0 1.5rem;
            display: grid;
            grid-template-columns: 1.1fr 1.25fr;
            gap: 2rem;
        }

        @media (max-width: 1024px) {
            .container { grid-template-columns: 1fr; }
        }

        .glass-card {
            background: var(--bg-card);
            backdrop-filter: blur(20px);
            border: 1px solid var(--border);
            border-radius: var(--radius-xl);
            padding: 2rem;
            box-shadow: var(--shadow-glass);
            position: relative;
            overflow: hidden;
        }

        .glass-card::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 4px;
            background: var(--brand-gradient);
        }

        .section-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.8rem;
        }

        .section-header h2 {
            font-size: 1.2rem;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .section-header h2 i { color: var(--brand-primary); }

        .badge-pill {
            font-size: 0.75rem;
            font-weight: 600;
            padding: 4px 10px;
            border-radius: 20px;
            background: rgba(99, 102, 241, 0.12);
            color: var(--brand-primary);
            border: 1px solid rgba(99, 102, 241, 0.3);
        }

        .form-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1.2rem;
        }

        @media (max-width: 600px) {
            .form-grid { grid-template-columns: 1fr; }
        }

        .input-group {
            display: flex;
            flex-direction: column;
            gap: 6px;
        }

        .input-group label {
            font-size: 0.775rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.6px;
            color: var(--text-muted);
        }

        .input-group input, .input-group select {
            width: 100%;
            padding: 0.8rem 1rem;
            background: rgba(0, 0, 0, 0.2);
            border: 1px solid var(--border);
            border-radius: var(--radius-md);
            color: var(--text-main);
            font-size: 0.95rem;
            outline: none;
            transition: var(--transition);
        }

        .input-group input:focus, .input-group select:focus {
            border-color: var(--brand-primary);
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2);
            background: rgba(0, 0, 0, 0.3);
        }

        .btn-predict {
            grid-column: span 2;
            margin-top: 1rem;
            padding: 1.1rem;
            background: var(--brand-gradient);
            border: none;
            border-radius: var(--radius-md);
            color: #fff;
            font-size: 1rem;
            font-weight: 700;
            cursor: pointer;
            box-shadow: 0 4px 20px rgba(99, 102, 241, 0.4);
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            transition: var(--transition);
        }

        .btn-predict:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(236, 72, 153, 0.45);
        }

        .analytics-flow {
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
        }

        .result-billboard {
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid var(--border);
            border-radius: var(--radius-md);
            padding: 1.5rem 2rem;
            position: relative;
        }

        .billboard-status {
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: var(--text-muted);
        }

        .billboard-verdict {
            font-size: 1.8rem;
            font-weight: 800;
            font-family: 'Space Grotesk', sans-serif;
            margin: 4px 0;
        }

        .status-chip {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            font-size: 0.85rem;
            font-weight: 700;
            padding: 6px 14px;
            border-radius: 30px;
        }

        .chip-safe { background: rgba(16, 185, 129, 0.15); color: var(--success); border: 1px solid var(--success); }
        .chip-danger { background: rgba(244, 63, 94, 0.15); color: var(--danger); border: 1px solid var(--danger); }

        .kpi-row {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1rem;
        }

        .kpi-tile {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid var(--border);
            border-radius: var(--radius-md);
            padding: 1.2rem;
            text-align: center;
        }

        .kpi-tile .kpi-num {
            font-size: 1.7rem;
            font-weight: 800;
            font-family: 'Space Grotesk', sans-serif;
            margin: 4px 0;
        }

        .kpi-tile .kpi-sub {
            font-size: 0.75rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .breakdown-box {
            background: rgba(0, 0, 0, 0.2);
            border-radius: var(--radius-md);
            border: 1px solid var(--border);
            padding: 1.5rem;
        }

        .breakdown-title {
            font-size: 0.9rem;
            font-weight: 700;
            margin-bottom: 1.2rem;
            display: flex;
            justify-content: space-between;
        }

        .feature-bar-list {
            display: flex;
            flex-direction: column;
            gap: 12px;
        }

        .feature-bar-unit {
            display: grid;
            grid-template-columns: 130px 1fr 60px;
            align-items: center;
            gap: 12px;
            font-size: 0.825rem;
        }

        .bar-outer {
            height: 8px;
            background: rgba(255, 255, 255, 0.06);
            border-radius: 10px;
            overflow: hidden;
        }

        .bar-inner {
            height: 100%;
            background: var(--brand-gradient);
            width: 0%;
            border-radius: 10px;
            transition: width 0.8s cubic-bezier(0.16, 1, 0.3, 1);
        }

        .spinner-loader {
            display: none;
            width: 22px;
            height: 22px;
            border: 3px solid rgba(255,255,255,0.3);
            border-radius: 50%;
            border-top-color: #fff;
            animation: spin 0.8s linear infinite;
        }

        @keyframes spin { to { transform: rotate(360deg); } }
    </style>
</head>
<body>

    <header class="navbar">
        <div class="brand-container">
            <div class="brand-icon"><i class="fa-solid fa-chart-pie"></i></div>
            <div class="brand-text">
                <h1>RetainIQ Pro</h1>
                <span>Enterprise Churn Intelligence</span>
            </div>
        </div>
        <div class="nav-controls">
            <div class="palette-dock">
                <div class="palette-opt p-indigo active" onclick="switchPalette('indigo')"></div>
                <div class="palette-opt p-emerald" onclick="switchPalette('emerald')"></div>
                <div class="palette-opt p-sunset" onclick="switchPalette('sunset')"></div>
                <div class="palette-opt p-cyberpunk" onclick="switchPalette('cyberpunk')"></div>
            </div>
            <button class="btn-theme" onclick="toggleMode()"><i class="fa-solid fa-moon" id="modeIcon"></i></button>
        </div>
    </header>

    <main class="container">
        
        <div class="glass-card">
            <div class="section-header">
                <h2><i class="fa-solid fa-sliders"></i> Behavioral Profile</h2>
                <span class="badge-pill">AdaBoost Model V1.6</span>
            </div>

            <form id="churnForm">
                <div class="form-grid">
                    
                    <div class="input-group">
                        <label>Age</label>
                        <input type="number" name="Age" value="38" min="18" max="100" required>
                    </div>

                    <div class="input-group">
                        <label>Gender</label>
                        <select name="Gender">
                            <option value="Male">Male</option>
                            <option value="Female">Female</option>
                        </select>
                    </div>

                    <div class="input-group">
                        <label>Tenure (Months)</label>
                        <input type="number" name="Tenure" value="24" min="0" max="120" required>
                    </div>

                    <div class="input-group">
                        <label>Usage Frequency</label>
                        <input type="number" name="Usage Frequency" value="12" min="1" max="100" required>
                    </div>

                    <div class="input-group">
                        <label>Support Calls</label>
                        <input type="number" name="Support Calls" value="3" min="0" max="25" required>
                    </div>

                    <div class="input-group">
                        <label>Payment Delay (Days)</label>
                        <input type="number" name="Payment Delay" value="8" min="0" max="90" required>
                    </div>

                    <div class="input-group">
                        <label>Subscription Tier</label>
                        <select name="Subscription Type">
                            <option value="Basic">Basic</option>
                            <option value="Standard">Standard</option>
                            <option value="Premium" selected>Premium</option>
                        </select>
                    </div>

                    <div class="input-group">
                        <label>Contract Length</label>
                        <select name="Contract Length">
                            <option value="Monthly">Monthly</option>
                            <option value="Quarterly">Quarterly</option>
                            <option value="Annual" selected>Annual</option>
                        </select>
                    </div>

                    <div class="input-group">
                        <label>Total Spend ($)</label>
                        <input type="number" step="0.01" name="Total Spend" value="540.00" min="0" required>
                    </div>

                    <div class="input-group">
                        <label>Last Interaction (Days)</label>
                        <input type="number" name="Last Interaction" value="14" min="0" max="365" required>
                    </div>

                    <button type="submit" class="btn-predict" id="submitBtn">
                        <span id="btnText">Execute Risk Inference</span>
                        <div class="spinner-loader" id="spinner"></div>
                        <i class="fa-solid fa-arrow-trend-up"></i>
                    </button>

                </div>
            </form>
        </div>

        <div class="analytics-flow">
            
            <div class="result-billboard">
                <div>
                    <div class="billboard-status">Prediction Assessment</div>
                    <div class="billboard-verdict" id="resultStatus">Awaiting Execution</div>
                    <div id="statusBadge" class="status-chip chip-safe" style="display: none;">
                        <i class="fa-solid fa-shield-check"></i> <span id="badgeContent">Retained</span>
                    </div>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase;">Engine Model</div>
                    <div style="font-family: 'Space Grotesk'; font-weight: 700; color: var(--brand-primary);">AdaBoost 50x</div>
                </div>
            </div>

            <div class="kpi-row">
                <div class="kpi-tile">
                    <div class="kpi-sub">Confidence</div>
                    <div class="kpi-num" style="color: var(--success);" id="kpiConf">--%</div>
                </div>
                <div class="kpi-tile">
                    <div class="kpi-sub">Churn Risk Index</div>
                    <div class="kpi-num" style="color: var(--danger);" id="kpiRisk">--</div>
                </div>
                <div class="kpi-tile">
                    <div class="kpi-sub">Customer LTV</div>
                    <div class="kpi-num" style="color: var(--info);" id="kpiLtv">$0.00</div>
                </div>
            </div>

            <div class="glass-card breakdown-box">
                <div class="breakdown-title">
                    <span>Feature Normalization Index</span>
                    <i class="fa-solid fa-chart-simple" style="color: var(--brand-secondary);"></i>
                </div>
                <div class="feature-bar-list" id="featureList">
                    <div style="color: var(--text-muted); font-size: 0.85rem; text-align: center; padding: 1.5rem 0;">
                        Submit profile values to render relative impact scale.
                    </div>
                </div>
            </div>

        </div>

    </main>

    <script>
        function switchPalette(pal) {
            document.documentElement.setAttribute('data-palette', pal);
            document.querySelectorAll('.palette-opt').forEach(el => el.classList.remove('active'));
            event.target.classList.add('active');
        }

        function toggleMode() {
            const doc = document.documentElement;
            const isDark = doc.getAttribute('data-theme') === 'dark';
            doc.setAttribute('data-theme', isDark ? 'light' : 'dark');
            document.getElementById('modeIcon').className = isDark ? 'fa-solid fa-sun' : 'fa-solid fa-moon';
        }

        document.getElementById('churnForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const btnText = document.getElementById('btnText');
            const spinner = document.getElementById('spinner');
            btnText.style.display = 'none';
            spinner.style.display = 'block';

            const formData = new FormData(this);

            try {
                const res = await fetch('/predict', { method: 'POST', body: formData });
                const data = await res.json();
                
                if (data.status === 'success') {
                    renderResults(data, formData);
                } else {
                    alert('Server error: ' + data.message);
                }
            } catch(err) {
                alert('Connection failure to inference endpoint');
            } finally {
                btnText.style.display = 'inline';
                spinner.style.display = 'none';
            }
        });

        function renderResults(data, formData) {
            document.getElementById('resultStatus').textContent = data.prediction_text;
            const badge = document.getElementById('statusBadge');
            const badgeContent = document.getElementById('badgeContent');
            badge.style.display = 'inline-flex';

            if(data.prediction === 1) {
                badge.className = 'status-chip chip-danger';
                badgeContent.textContent = 'High Attrition Danger';
            } else {
                badge.className = 'status-chip chip-safe';
                badgeContent.textContent = 'Customer Safe';
            }

            document.getElementById('kpiConf').textContent = data.confidence + '%';
            document.getElementById('kpiRisk').textContent = data.risk_score + '/100';
            document.getElementById('kpiLtv').textContent = '$' + parseFloat(formData.get('Total Spend')).toFixed(2);

            const container = document.getElementById('featureList');
            container.innerHTML = '';

            const feats = data.features_impact;
            const maxVal = Math.max(...Object.values(feats));

            for (const [k, v] of Object.entries(feats)) {
                const ratio = maxVal > 0 ? (v / maxVal) * 100 : 0;
                const unit = document.createElement('div');
                unit.className = 'feature-bar-unit';
                unit.innerHTML = `
                    <div style="color: var(--text-muted); text-overflow: ellipsis; overflow: hidden;">${k}</div>
                    <div class="bar-outer">
                        <div class="bar-inner" style="width: 0%"></div>
                    </div>
                    <div style="text-align: right; font-weight: 700;">${v}</div>
                `;
                container.appendChild(unit);
                setTimeout(() => {
                    unit.querySelector('.bar-inner').style.width = ratio.toFixed(0) + '%';
                }, 80);
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({
            'status': 'error',
            'message': 'Model file (Adaboost_model.pkl) was not found in directory.'
        })

    try:
        age = float(request.form.get('Age', 0))
        gender_raw = request.form.get('Gender', 'Male')
        tenure = float(request.form.get('Tenure', 0))
        usage_freq = float(request.form.get('Usage Frequency', 0))
        support_calls = float(request.form.get('Support Calls', 0))
        payment_delay = float(request.form.get('Payment Delay', 0))
        sub_type_raw = request.form.get('Subscription Type', 'Basic')
        contract_raw = request.form.get('Contract Length', 'Monthly')
        total_spend = float(request.form.get('Total Spend', 0))
        last_interaction = float(request.form.get('Last Interaction', 0))

        # Encodings matching dataset pipeline
        gender = 1 if gender_raw == 'Male' else 0
        sub_type = {'Basic': 0, 'Standard': 1, 'Premium': 2}.get(sub_type_raw, 0)
        contract = {'Monthly': 0, 'Quarterly': 1, 'Annual': 2}.get(contract_raw, 0)

        # Features order matching the AdaBoost estimator
        features = np.array([[
            age, gender, tenure, usage_freq, support_calls,
            payment_delay, sub_type, contract,
            total_spend, last_interaction
        ]])

        prediction = int(model.predict(features)[0])
        
        confidence = 85.0
        risk_score = 30
        if hasattr(model, "predict_proba"):
            probs = model.predict_proba(features)[0]
            confidence = round(float(np.max(probs)) * 100, 1)
            risk_score = round(float(probs[1]) * 100, 1) if len(probs) > 1 else int(prediction * 100)

        verdict = "Customer Churn Likely" if prediction == 1 else "Customer Retained"

        return jsonify({
            'status': 'success',
            'prediction': prediction,
            'prediction_text': verdict,
            'confidence': confidence,
            'risk_score': risk_score,
            'features_impact': {
                'Age': age,
                'Tenure (mo)': tenure,
                'Usage Freq': usage_freq,
                'Support Calls': support_calls,
                'Payment Delay': payment_delay,
                'Total Spend ($)': total_spend,
                'Last Interaction': last_interaction
            }
        })

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
