import os
import pickle
import numpy as np
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# Model loading logic
MODEL_PATH = os.path.join(os.path.dirname(__file__), "Adaboost_model.pkl")
model = None

try:
    if os.path.exists(MODEL_PATH):
        with open(MODEL_PATH, "rb") as f:
            model = pickle.load(f)
        print("ChurnPulse Engine: Model loaded successfully.")
    else:
        print(f"Warning: Model file not found at {MODEL_PATH}")
except Exception as e:
    print(f"Model initialization error: {e}")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ChurnPulse AI™ | Enterprise Retention Intelligence</title>
    
    <!-- Typography & Icons -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cabinet+Grotesk:wght@700;800;900&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <!-- Chart.js for visualization -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

    <style>
        :root {
            --bg-canvas: #06080F;
            --surface-panel: #0E131F;
            --surface-card: rgba(18, 24, 38, 0.7);
            --surface-card-hover: rgba(26, 34, 52, 0.85);
            --border-subtle: rgba(255, 255, 255, 0.08);
            --border-glow: rgba(99, 102, 241, 0.35);
            
            --text-heading: #F8FAFC;
            --text-body: #94A3B8;
            --text-dim: #64748B;
            
            --brand-primary: #6366F1;
            --brand-secondary: #06B6D4;
            --brand-accent: #8B5CF6;
            
            --status-safe: #10B981;
            --status-danger: #F43F5E;
            --status-warn: #F59E0B;
            
            --mono-font: 'JetBrains Mono', monospace;
            --heading-font: 'Cabinet Grotesk', sans-serif;
            --body-font: 'Inter', sans-serif;
            
            --shadow-elevation: 0 20px 40px -15px rgba(0, 0, 0, 0.6);
            --radius-md: 12px;
            --radius-lg: 20px;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: var(--body-font);
        }

        body {
            background-color: var(--bg-canvas);
            color: var(--text-body);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            overflow-x: hidden;
            background-image: 
                radial-gradient(circle at 15% 10%, rgba(99, 102, 241, 0.12) 0%, transparent 40%),
                radial-gradient(circle at 85% 85%, rgba(6, 182, 212, 0.08) 0%, transparent 45%);
            background-attachment: fixed;
        }

        /* Top Bar */
        header {
            background: rgba(14, 19, 31, 0.8);
            backdrop-filter: blur(20px);
            border-bottom: 1px solid var(--border-subtle);
            padding: 1rem 2.5rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: sticky;
            top: 0;
            z-index: 50;
        }

        .brand-wrap {
            display: flex;
            align-items: center;
            gap: 14px;
        }

        .logo-icon {
            width: 42px;
            height: 42px;
            border-radius: 10px;
            background: linear-gradient(135deg, var(--brand-primary), var(--brand-secondary));
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 1.3rem;
            box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);
        }

        .brand-title {
            font-family: var(--heading-font);
            font-size: 1.35rem;
            color: var(--text-heading);
            letter-spacing: -0.5px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .brand-badge {
            font-family: var(--mono-font);
            font-size: 0.65rem;
            padding: 3px 8px;
            border-radius: 6px;
            background: rgba(99, 102, 241, 0.15);
            color: #818CF8;
            border: 1px solid rgba(99, 102, 241, 0.3);
            letter-spacing: 0.5px;
        }

        .status-pill {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 0.8rem;
            color: var(--text-heading);
            background: rgba(16, 185, 129, 0.08);
            border: 1px solid rgba(16, 185, 129, 0.25);
            padding: 6px 14px;
            border-radius: 50px;
        }

        .status-dot {
            width: 8px;
            height: 8px;
            background-color: var(--status-safe);
            border-radius: 50%;
            box-shadow: 0 0 10px var(--status-safe);
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.4; transform: scale(0.9); }
        }

        /* App Wrapper */
        .app-grid {
            max-width: 1540px;
            width: 100%;
            margin: 2rem auto;
            padding: 0 2rem;
            display: grid;
            grid-template-columns: 480px 1fr;
            gap: 2rem;
            flex: 1;
        }

        @media (max-width: 1180px) {
            .app-grid {
                grid-template-columns: 1fr;
            }
        }

        /* Card Styles */
        .surface-box {
            background: var(--surface-card);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-lg);
            padding: 1.75rem;
            backdrop-filter: blur(16px);
            box-shadow: var(--shadow-elevation);
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
        }

        .section-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .section-header h2 {
            font-family: var(--heading-font);
            font-size: 1.25rem;
            color: var(--text-heading);
            display: flex;
            align-items: center;
            gap: 10px;
        }

        /* Preset Selectors */
        .preset-bar {
            display: flex;
            gap: 8px;
            background: rgba(0, 0, 0, 0.25);
            padding: 6px;
            border-radius: 10px;
            border: 1px solid var(--border-subtle);
        }

        .btn-preset {
            flex: 1;
            padding: 6px 10px;
            font-size: 0.75rem;
            font-weight: 600;
            background: transparent;
            color: var(--text-body);
            border: none;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.2s ease;
        }

        .btn-preset:hover, .btn-preset.active {
            background: var(--brand-primary);
            color: white;
        }

        /* Inputs Grouping */
        .fieldset-block {
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-md);
            padding: 1.25rem;
            background: rgba(0, 0, 0, 0.15);
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }

        .fieldset-legend {
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.75px;
            color: #818CF8;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .input-row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1rem;
        }

        .input-group {
            display: flex;
            flex-direction: column;
            gap: 6px;
        }

        .input-group label {
            font-size: 0.775rem;
            color: var(--text-body);
            font-weight: 500;
        }

        .input-control {
            background: rgba(14, 19, 31, 0.9);
            border: 1px solid var(--border-subtle);
            color: var(--text-heading);
            padding: 0.75rem 0.9rem;
            border-radius: 8px;
            font-size: 0.9rem;
            outline: none;
            transition: all 0.2s;
        }

        .input-control:focus {
            border-color: var(--brand-primary);
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2);
        }

        /* Submit Button */
        .btn-run {
            background: linear-gradient(135deg, #6366F1, #8B5CF6);
            border: none;
            color: white;
            font-family: var(--heading-font);
            font-size: 1.05rem;
            padding: 1.1rem;
            border-radius: var(--radius-md);
            cursor: pointer;
            box-shadow: 0 10px 25px -5px rgba(99, 102, 241, 0.4);
            transition: all 0.25s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
        }

        .btn-run:hover {
            transform: translateY(-2px);
            box-shadow: 0 15px 30px -5px rgba(99, 102, 241, 0.6);
        }

        /* Cockpit Visuals */
        .cockpit-view {
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
        }

        .overview-hero {
            display: grid;
            grid-template-columns: 240px 1fr;
            gap: 1.5rem;
            background: rgba(0, 0, 0, 0.3);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-lg);
            padding: 1.75rem;
            align-items: center;
        }

        @media (max-width: 768px) {
            .overview-hero {
                grid-template-columns: 1fr;
                text-align: center;
            }
        }

        /* Radial Gauge */
        .gauge-wrapper {
            position: relative;
            width: 170px;
            height: 170px;
            margin: 0 auto;
        }

        .gauge-svg {
            transform: rotate(-90deg);
        }

        .gauge-bg {
            stroke: rgba(255, 255, 255, 0.08);
            fill: none;
            stroke-width: 14;
        }

        .gauge-fill {
            stroke: var(--status-safe);
            fill: none;
            stroke-width: 14;
            stroke-linecap: round;
            stroke-dasharray: 440;
            stroke-dashoffset: 440;
            transition: stroke-dashoffset 1.2s cubic-bezier(0.16, 1, 0.3, 1), stroke 0.4s ease;
        }

        .gauge-center-text {
            position: absolute;
            inset: 0;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }

        .gauge-val {
            font-family: var(--heading-font);
            font-size: 2.2rem;
            font-weight: 800;
            color: var(--text-heading);
        }

        .gauge-sub {
            font-size: 0.65rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: var(--text-dim);
        }

        .verdict-info {
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        .verdict-badge {
            align-self: flex-start;
            padding: 6px 14px;
            border-radius: 30px;
            font-size: 0.8rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }

        .badge-safe {
            background: rgba(16, 185, 129, 0.15);
            color: var(--status-safe);
            border: 1px solid rgba(16, 185, 129, 0.3);
        }

        .badge-danger {
            background: rgba(244, 63, 94, 0.15);
            color: var(--status-danger);
            border: 1px solid rgba(244, 63, 94, 0.3);
        }

        .verdict-heading {
            font-family: var(--heading-font);
            font-size: 1.6rem;
            color: var(--text-heading);
        }

        .verdict-summary {
            font-size: 0.9rem;
            color: var(--text-body);
            line-height: 1.5;
        }

        /* KPI Cards Grid */
        .kpi-row {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1rem;
        }

        .kpi-stat-card {
            background: rgba(14, 19, 31, 0.6);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-md);
            padding: 1.2rem;
            display: flex;
            align-items: center;
            gap: 14px;
        }

        .kpi-stat-icon {
            width: 44px;
            height: 44px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.15rem;
            background: rgba(255, 255, 255, 0.04);
            color: var(--brand-secondary);
        }

        .kpi-data-val {
            font-family: var(--heading-font);
            font-size: 1.35rem;
            color: var(--text-heading);
        }

        .kpi-data-lbl {
            font-size: 0.75rem;
            color: var(--text-dim);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        /* Action Playbook & Chart Side by Side */
        .insights-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1.5rem;
        }

        @media (max-width: 900px) {
            .insights-grid {
                grid-template-columns: 1fr;
            }
        }

        .playbook-card {
            background: rgba(0, 0, 0, 0.2);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-md);
            padding: 1.25rem;
        }

        .playbook-title {
            font-size: 0.85rem;
            font-weight: 700;
            color: var(--text-heading);
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .action-item {
            background: rgba(255, 255, 255, 0.02);
            border-left: 3px solid var(--brand-primary);
            padding: 10px 12px;
            border-radius: 0 6px 6px 0;
            margin-bottom: 8px;
            font-size: 0.8rem;
            color: var(--text-body);
        }

        .action-item strong {
            color: var(--text-heading);
            display: block;
            margin-bottom: 2px;
        }

        /* Spinner */
        .spinner {
            display: none;
            width: 20px;
            height: 20px;
            border: 3px solid rgba(255,255,255,0.3);
            border-radius: 50%;
            border-top-color: white;
            animation: spin 0.7s linear infinite;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }
    </style>
</head>
<body>

    <!-- Header Bar -->
    <header>
        <div class="brand-wrap">
            <div class="logo-icon">
                <i class="fa-solid fa-chart-line-up"></i>
            </div>
            <div>
                <div class="brand-title">
                    ChurnPulse AI™
                    <span class="brand-badge">PRO v2.4</span>
                </div>
            </div>
        </div>
        <div class="status-pill">
            <div class="status-dot"></div>
            <span>AdaBoost Ensemble Core Active</span>
        </div>
    </header>

    <!-- Main Workspace -->
    <div class="app-grid">
        
        <!-- Left Column: Inputs & Scenarios -->
        <div class="surface-box">
            <div class="section-header">
                <h2><i class="fa-solid fa-sliders text-indigo-400"></i> Customer Profile</h2>
            </div>

            <!-- Quick Scenario Tester -->
            <div class="preset-bar">
                <button type="button" class="btn-preset active" onclick="loadPreset('loyal')">Loyal Member</button>
                <button type="button" class="btn-preset" onclick="loadPreset('atrisk')">High Churn Risk</button>
                <button type="button" class="btn-preset" onclick="loadPreset('newbie')">Early Lifecycle</button>
            </div>

            <form id="churnForm">
                <div style="display: flex; flex-direction: column; gap: 1rem;">
                    
                    <!-- Domain 1: Demographic & Tenancy -->
                    <div class="fieldset-block">
                        <div class="fieldset-legend">
                            <i class="fa-solid fa-id-badge"></i> Account & Demographics
                        </div>
                        <div class="input-row">
                            <div class="input-group">
                                <label>Customer Age</label>
                                <input type="number" id="Age" name="Age" class="input-control" value="42" min="18" max="100" required>
                            </div>
                            <div class="input-group">
                                <label>Gender</label>
                                <select id="Gender" name="Gender" class="input-control">
                                    <option value="Female">Female</option>
                                    <option value="Male">Male</option>
                                </select>
                            </div>
                        </div>
                        <div class="input-group">
                            <label>Account Tenure (Months)</label>
                            <input type="number" id="Tenure" name="Tenure" class="input-control" value="28" min="0" max="120" required>
                        </div>
                    </div>

                    <!-- Domain 2: Product Engagement & Support Velocity -->
                    <div class="fieldset-block">
                        <div class="fieldset-legend">
                            <i class="fa-solid fa-bolt"></i> Behavioral & Support Activity
                        </div>
                        <div class="input-row">
                            <div class="input-group">
                                <label>Usage Frequency / Mo</label>
                                <input type="number" id="Usage Frequency" name="Usage Frequency" class="input-control" value="18" min="0" max="100" required>
                            </div>
                            <div class="input-group">
                                <label>Support Tickets</label>
                                <input type="number" id="Support Calls" name="Support Calls" class="input-control" value="1" min="0" max="25" required>
                            </div>
                        </div>
                        <div class="input-group">
                            <label>Last Touchpoint (Days Ago)</label>
                            <input type="number" id="Last Interaction" name="Last Interaction" class="input-control" value="4" min="0" max="365" required>
                        </div>
                    </div>

                    <!-- Domain 3: Billing & Financials -->
                    <div class="fieldset-block">
                        <div class="fieldset-legend">
                            <i class="fa-solid fa-credit-card"></i> Contract & Billing Health
                        </div>
                        <div class="input-row">
                            <div class="input-group">
                                <label>Subscription Tier</label>
                                <select id="Subscription Type" name="Subscription Type" class="input-control">
                                    <option value="Basic">Basic Tier</option>
                                    <option value="Standard">Standard Tier</option>
                                    <option value="Premium" selected>Premium Enterprise</option>
                                </select>
                            </div>
                            <div class="input-group">
                                <label>Contract Type</label>
                                <select id="Contract Length" name="Contract Length" class="input-control">
                                    <option value="Monthly">Monthly Flex</option>
                                    <option value="Quarterly">Quarterly</option>
                                    <option value="Annual" selected>Annual Committed</option>
                                </select>
                            </div>
                        </div>
                        <div class="input-row">
                            <div class="input-group">
                                <label>Total Spend ($)</label>
                                <input type="number" step="0.01" id="Total Spend" name="Total Spend" class="input-control" value="840.00" required>
                            </div>
                            <div class="input-group">
                                <label>Payment Delay (Days)</label>
                                <input type="number" id="Payment Delay" name="Payment Delay" class="input-control" value="2" min="0" max="90" required>
                            </div>
                        </div>
                    </div>

                    <button type="submit" class="btn-run" id="btnSubmit">
                        <span id="btnLabel"><i class="fa-solid fa-radar mr-2"></i> Compute Predictive Risk</span>
                        <div class="spinner" id="btnLoader"></div>
                    </button>
                </div>
            </form>
        </div>

        <!-- Right Column: Operations Diagnostic Cockpit -->
        <div class="surface-box cockpit-view">
            
            <div class="section-header">
                <h2><i class="fa-solid fa-microchip-ai text-cyan-400"></i> Executive Diagnostics</h2>
                <span style="font-family: var(--mono-font); font-size: 0.75rem; color: var(--text-dim);" id="timestamp">REALTIME READY</span>
            </div>

            <!-- Hero Risk Summary -->
            <div class="overview-hero">
                <div class="gauge-wrapper">
                    <svg class="gauge-svg" width="170" height="170" viewBox="0 0 170 170">
                        <circle class="gauge-bg" cx="85" cy="85" r="70" />
                        <circle class="gauge-fill" id="gaugeCircle" cx="85" cy="85" r="70" />
                    </svg>
                    <div class="gauge-center-text">
                        <div class="gauge-val" id="churnRiskPercent">--%</div>
                        <div class="gauge-sub">Probability</div>
                    </div>
                </div>

                <div class="verdict-info">
                    <div id="riskBadge" class="verdict-badge badge-safe">
                        <i class="fa-solid fa-shield-check"></i> <span id="riskBadgeText">Awaiting Assessment</span>
                    </div>
                    <div class="verdict-heading" id="verdictHeadline">Run Model to Generate Score</div>
                    <div class="verdict-summary" id="verdictSummary">
                        Adjust customer indicators on the configurator panel or apply a preset scenario to evaluate probability through the ensemble classifier.
                    </div>
                </div>
            </div>

            <!-- KPI Metric Bar -->
            <div class="kpi-row">
                <div class="kpi-stat-card">
                    <div class="kpi-stat-icon"><i class="fa-solid fa-gauge-high"></i></div>
                    <div>
                        <div class="kpi-data-val" id="kpiModelConfidence">--%</div>
                        <div class="kpi-data-lbl">Ensemble Confidence</div>
                    </div>
                </div>
                <div class="kpi-stat-card">
                    <div class="kpi-stat-icon"><i class="fa-solid fa-sack-dollar"></i></div>
                    <div>
                        <div class="kpi-data-val" id="kpiLTV">$840</div>
                        <div class="kpi-data-lbl">Recorded Spend</div>
                    </div>
                </div>
                <div class="kpi-stat-card">
                    <div class="kpi-stat-icon"><i class="fa-solid fa-triangle-exclamation"></i></div>
                    <div>
                        <div class="kpi-data-val" id="kpiHealthRating">Healthy</div>
                        <div class="kpi-data-lbl">Account Health</div>
                    </div>
                </div>
            </div>

            <!-- Dual Insight Split: Playbook & Chart -->
            <div class="insights-grid">
                <!-- Action Recommendations -->
                <div class="playbook-card">
                    <div class="playbook-title">
                        <i class="fa-solid fa-lightbulb text-amber-400"></i> Prescribed Interventions
                    </div>
                    <div id="playbookItems">
                        <div class="action-item">
                            <strong>No Action Required</strong>
                            Run risk computation to generate contextual intervention strategies.
                        </div>
                    </div>
                </div>

                <!-- Feature Distribution Radar / Bar -->
                <div class="playbook-card">
                    <div class="playbook-title">
                        <i class="fa-solid fa-chart-radar text-indigo-400"></i> Signal Vector Analysis
                    </div>
                    <div style="height: 180px; position: relative;">
                        <canvas id="featureChart"></canvas>
                    </div>
                </div>
            </div>

        </div>

    </div>

    <script>
        let radarChart = null;

        // Preset Data
        const presets = {
            loyal: {
                Age: 44, Gender: 'Female', Tenure: 36,
                'Usage Frequency': 24, 'Support Calls': 1, 'Payment Delay': 0,
                'Subscription Type': 'Premium', 'Contract Length': 'Annual',
                'Total Spend': 960.00, 'Last Interaction': 2
            },
            atrisk: {
                Age: 31, Gender: 'Male', Tenure: 5,
                'Usage Frequency': 3, 'Support Calls': 7, 'Payment Delay': 19,
                'Subscription Type': 'Basic', 'Contract Length': 'Monthly',
                'Total Spend': 110.00, 'Last Interaction': 29
            },
            newbie: {
                Age: 25, Gender: 'Female', Tenure: 2,
                'Usage Frequency': 12, 'Support Calls': 2, 'Payment Delay': 1,
                'Subscription Type': 'Standard', 'Contract Length': 'Monthly',
                'Total Spend': 180.00, 'Last Interaction': 6
            }
        };

        function loadPreset(key) {
            document.querySelectorAll('.btn-preset').forEach(b => b.classList.remove('active'));
            event.target.classList.add('active');
            const data = presets[key];
            for (const field in data) {
                const el = document.getElementById(field);
                if (el) el.value = data[field];
            }
        }

        // Form Submit
        document.getElementById('churnForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            const btnLabel = document.getElementById('btnLabel');
            const btnLoader = document.getElementById('btnLoader');
            btnLabel.style.display = 'none';
            btnLoader.style.display = 'block';

            const formData = new FormData(this);

            try {
                const res = await fetch('/predict', {
                    method: 'POST',
                    body: formData
                });
                const result = await res.json();
                
                if (result.status === 'success') {
                    updateDashboard(result);
                } else {
                    alert('Prediction Engine Error: ' + result.message);
                }
            } catch (err) {
                console.error(err);
                alert('Connection failure to prediction API.');
            } finally {
                btnLabel.style.display = 'flex';
                btnLoader.style.display = 'none';
            }
        });

        function updateDashboard(res) {
            // Update timestamp
            document.getElementById('timestamp').innerText = new Date().toLocaleTimeString();

            // Gauge calculations
            const risk = res.risk_score;
            document.getElementById('churnRiskPercent').innerText = `${risk}%`;
            
            const circle = document.getElementById('gaugeCircle');
            const circumference = 440;
            const offset = circumference - (risk / 100) * circumference;
            circle.style.strokeDashoffset = offset;

            // Verdict and styling
            const badge = document.getElementById('riskBadge');
            const badgeText = document.getElementById('riskBadgeText');
            const headline = document.getElementById('verdictHeadline');
            const summary = document.getElementById('verdictSummary');
            const healthRating = document.getElementById('kpiHealthRating');

            if (res.prediction === 1) {
                circle.style.stroke = 'var(--status-danger)';
                badge.className = 'verdict-badge badge-danger';
                badgeText.innerHTML = '<i class="fa-solid fa-triangle-exclamation"></i> High Churn Probability';
                headline.innerText = 'High Retention Risk Detected';
                summary.innerText = 'Model diagnostics detect severe disengagement patterns, high ticket density, or overdue payment intervals requiring proactive retention.';
                healthRating.innerText = 'Critical';
                healthRating.style.color = 'var(--status-danger)';
            } else {
                circle.style.stroke = 'var(--status-safe)';
                badge.className = 'verdict-badge badge-safe';
                badgeText.innerHTML = '<i class="fa-solid fa-shield-check"></i> Account Healthy';
                headline.innerText = 'Low Retention Risk Expected';
                summary.innerText = 'Customer manifests steady product adoption, regular billing compliance, and adequate interaction velocity.';
                healthRating.innerText = 'Optimal';
                healthRating.style.color = 'var(--status-safe)';
            }

            document.getElementById('kpiModelConfidence').innerText = `${res.confidence}%`;
            document.getElementById('kpiLTV').innerText = `$${parseFloat(document.getElementById('Total Spend').value).toFixed(2)}`;

            // Build dynamic playbook
            buildPlaybook(res);

            // Update Chart.js Radar
            renderChart(res.features_impact);
        }

        function buildPlaybook(res) {
            const container = document.getElementById('playbookItems');
            container.innerHTML = '';
            const actions = [];

            const supportCalls = parseFloat(document.getElementById('Support Calls').value);
            const delay = parseFloat(document.getElementById('Payment Delay').value);
            const daysSinceTouch = parseFloat(document.getElementById('Last Interaction').value);

            if (res.prediction === 1) {
                if (supportCalls >= 3) {
                    actions.push({
                        title: 'Technical Account Manager Escalation',
                        desc: `Account has ${supportCalls} tickets recorded. Assign Tier-3 specialist for prompt issue resolution.`
                    });
                }
                if (delay > 7) {
                    actions.push({
                        title: 'Dunning & Flexible Billing Outreach',
                        desc: `Payment latency is ${delay} days overdue. Offer split invoices or grace periods before service disruption.`
                    });
                }
                if (daysSinceTouch > 15) {
                    actions.push({
                        title: 'Re-engagement Workflow Trigger',
                        desc: 'Customer has been dormant for over 2 weeks. Initiate product training webinar invitation.'
                    });
                }
                if (actions.length === 0) {
                    actions.push({
                        title: 'Executive Retention Discount',
                        desc: 'Offer 15% discount upon renewal to protect annual contract.'
                    });
                }
            } else {
                actions.push({
                    title: 'Upsell & Expansion Opportunity',
                    desc: 'Account exhibits high health. Target for annual contract conversion or higher plan tier.'
                });
                actions.push({
                    title: 'Advocate Program Enrollment',
                    desc: 'Nominate user for quarterly case-study & enterprise reference board.'
                });
            }

            actions.forEach(a => {
                const el = document.createElement('div');
                el.className = 'action-item';
                el.innerHTML = `<strong>${a.title}</strong>${a.desc}`;
                container.appendChild(el);
            });
        }

        function renderChart(metrics) {
            const ctx = document.getElementById('featureChart').getContext('2d');
            
            const labels = Object.keys(metrics);
            const values = Object.values(metrics);

            if (radarChart) {
                radarChart.destroy();
            }

            radarChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Signal Values',
                        data: values,
                        backgroundColor: 'rgba(99, 102, 241, 0.4)',
                        borderColor: '#6366F1',
                        borderWidth: 1.5,
                        borderRadius: 6
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false }
                    },
                    scales: {
                        x: {
                            ticks: { color: '#64748B', font: { size: 10 } },
                            grid: { display: false }
                        },
                        y: {
                            ticks: { color: '#64748B', font: { size: 10 } },
                            grid: { color: 'rgba(255,255,255,0.05)' }
                        }
                    }
                }
            });
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
            'message': 'Model file (Adaboost_model.pkl) is not available.'
        })

    try:
        # Extract features
        age = float(request.form.get('Age', 0))
        gender_str = request.form.get('Gender', 'Male')
        tenure = float(request.form.get('Tenure', 0))
        usage_freq = float(request.form.get('Usage Frequency', 0))
        support_calls = float(request.form.get('Support Calls', 0))
        payment_delay = float(request.form.get('Payment Delay', 0))
        sub_type_str = request.form.get('Subscription Type', 'Basic')
        contract_str = request.form.get('Contract Length', 'Annual')
        total_spend = float(request.form.get('Total Spend', 0))
        last_interaction = float(request.form.get('Last Interaction', 0))

        # Encodings matching dataset
        gender = 1 if gender_str == 'Male' else 0
        sub_map = {'Basic': 0, 'Standard': 1, 'Premium': 2}
        subscription_type = sub_map.get(sub_type_str, 0)
        contract_map = {'Monthly': 0, 'Quarterly': 1, 'Annual': 2}
        contract_length = contract_map.get(contract_str, 0)

        # Feature matrix in model feature sequence
        features = np.array([[
            age, gender, tenure, usage_freq, support_calls,
            payment_delay, subscription_type, contract_length,
            total_spend, last_interaction
        ]])

        prediction = model.predict(features)[0]

        # Probabilities & confidence score
        confidence = 90.0
        risk_score = 15
        if hasattr(model, "predict_proba"):
            probs = model.predict_proba(features)[0]
            confidence = round(float(np.max(probs)) * 100, 1)
            risk_score = round(float(probs[1]) * 100, 1) if len(probs) > 1 else int(prediction * 100)

        pred_text = "Churn Imminent" if prediction == 1 else "Customer Retained"

        features_dict = {
            'Age': age,
            'Tenure (mo)': tenure,
            'Usage/mo': usage_freq,
            'Tickets': support_calls,
            'Delay (d)': payment_delay,
            'Last Int (d)': last_interaction
        }

        return jsonify({
            'status': 'success',
            'prediction': int(prediction),
            'prediction_text': pred_text,
            'confidence': confidence,
            'risk_score': risk_score,
            'features_impact': features_dict
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        })

# Vercel WSGI entry point
app = app

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
