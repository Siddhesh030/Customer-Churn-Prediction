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
<html lang="en" data-theme="obsidian">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ChurnPulse AI™ | Enterprise Retention Cockpit</title>
    
    <!-- Typography & Icons -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cabinet+Grotesk:wght@700;800;900&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    
    <!-- Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

    <style>
        /* ================= Multi-Color Theme Variables ================= */
        
        /* 1. Default: Midnight Obsidian (Indigo / Violet Glow) */
        :root, [data-theme="obsidian"] {
            --bg-canvas: #060810;
            --surface-panel: #0E1322;
            --surface-card: rgba(16, 22, 38, 0.75);
            --surface-field: rgba(10, 15, 28, 0.9);
            --border-subtle: rgba(255, 255, 255, 0.08);
            --border-glow: rgba(99, 102, 241, 0.4);
            
            --text-heading: #F8FAFC;
            --text-body: #94A3B8;
            --text-dim: #64748B;
            
            --brand-primary: #6366F1;
            --brand-secondary: #06B6D4;
            --brand-gradient: linear-gradient(135deg, #6366F1, #8B5CF6);
            --brand-glow-radial: radial-gradient(circle at 15% 10%, rgba(99, 102, 241, 0.16) 0%, transparent 40%),
                                 radial-gradient(circle at 85% 85%, rgba(6, 182, 212, 0.1) 0%, transparent 45%);
            
            --status-safe: #10B981;
            --status-danger: #F43F5E;
            --status-warn: #F59E0B;
            --chart-fill: rgba(99, 102, 241, 0.4);
            --chart-stroke: #6366F1;
        }

        /* 2. Cyber Aurora (Cyan / Neon Pink / Future Dark) */
        [data-theme="aurora"] {
            --bg-canvas: #050A14;
            --surface-panel: #091224;
            --surface-card: rgba(11, 22, 44, 0.78);
            --surface-field: rgba(6, 14, 30, 0.95);
            --border-subtle: rgba(0, 240, 255, 0.15);
            --border-glow: rgba(0, 240, 255, 0.5);
            
            --text-heading: #FFFFFF;
            --text-body: #A5F3FC;
            --text-dim: #4B7A94;
            
            --brand-primary: #00F0FF;
            --brand-secondary: #FF007F;
            --brand-gradient: linear-gradient(135deg, #00F0FF, #FF007F);
            --brand-glow-radial: radial-gradient(circle at 10% 10%, rgba(0, 240, 255, 0.18) 0%, transparent 40%),
                                 radial-gradient(circle at 90% 90%, rgba(255, 0, 127, 0.14) 0%, transparent 45%);
            
            --status-safe: #00F5A0;
            --status-danger: #FF1744;
            --status-warn: #FFD600;
            --chart-fill: rgba(0, 240, 255, 0.35);
            --chart-stroke: #00F0FF;
        }

        /* 3. Emerald Matrix (Biotech / Fintech Green / Jade) */
        [data-theme="emerald"] {
            --bg-canvas: #050E0B;
            --surface-panel: #0A1C16;
            --surface-card: rgba(12, 33, 26, 0.78);
            --surface-field: rgba(7, 22, 17, 0.92);
            --border-subtle: rgba(16, 185, 129, 0.16);
            --border-glow: rgba(16, 185, 129, 0.45);
            
            --text-heading: #ECFDF5;
            --text-body: #A7F3D0;
            --text-dim: #4D8B72;
            
            --brand-primary: #10B981;
            --brand-secondary: #34D399;
            --brand-gradient: linear-gradient(135deg, #059669, #10B981);
            --brand-glow-radial: radial-gradient(circle at 15% 15%, rgba(16, 185, 129, 0.18) 0%, transparent 40%),
                                 radial-gradient(circle at 85% 85%, rgba(52, 211, 153, 0.1) 0%, transparent 45%);
            
            --status-safe: #34D399;
            --status-danger: #FB7185;
            --status-warn: #FBBF24;
            --chart-fill: rgba(16, 185, 129, 0.35);
            --chart-stroke: #10B981;
        }

        /* 4. Sunset Ember (Crimson / Warm Amber / Orange Fire) */
        [data-theme="sunset"] {
            --bg-canvas: #120908;
            --surface-panel: #20110F;
            --surface-card: rgba(38, 20, 18, 0.8);
            --surface-field: rgba(26, 12, 10, 0.95);
            --border-subtle: rgba(249, 115, 22, 0.16);
            --border-glow: rgba(249, 115, 22, 0.45);
            
            --text-heading: #FFF7ED;
            --text-body: #FED7AA;
            --text-dim: #9A6855;
            
            --brand-primary: #F97316;
            --brand-secondary: #EF4444;
            --brand-gradient: linear-gradient(135deg, #F97316, #DC2626);
            --brand-glow-radial: radial-gradient(circle at 10% 10%, rgba(249, 115, 22, 0.2) 0%, transparent 40%),
                                 radial-gradient(circle at 90% 90%, rgba(239, 68, 68, 0.14) 0%, transparent 45%);
            
            --status-safe: #22C55E;
            --status-danger: #EF4444;
            --status-warn: #F59E0B;
            --chart-fill: rgba(249, 115, 22, 0.4);
            --chart-stroke: #F97316;
        }

        /* 5. Enterprise Light (Clean Crisp Corporate Slate) */
        [data-theme="light"] {
            --bg-canvas: #F8FAFC;
            --surface-panel: #FFFFFF;
            --surface-card: rgba(255, 255, 255, 0.95);
            --surface-field: #F1F5F9;
            --border-subtle: rgba(15, 23, 42, 0.1);
            --border-glow: rgba(79, 70, 229, 0.3);
            
            --text-heading: #0F172A;
            --text-body: #334155;
            --text-dim: #64748B;
            
            --brand-primary: #4F46E5;
            --brand-secondary: #0284C7;
            --brand-gradient: linear-gradient(135deg, #4F46E5, #6366F1);
            --brand-glow-radial: radial-gradient(circle at 15% 15%, rgba(79, 70, 229, 0.08) 0%, transparent 40%),
                                 radial-gradient(circle at 85% 85%, rgba(2, 132, 199, 0.06) 0%, transparent 45%);
            
            --status-safe: #059669;
            --status-danger: #DC2626;
            --status-warn: #D97706;
            --chart-fill: rgba(79, 70, 229, 0.25);
            --chart-stroke: #4F46E5;
        }

        /* ================= Base Styles ================= */
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Inter', sans-serif;
            transition: background-color 0.3s ease, border-color 0.3s ease, color 0.3s ease;
        }

        body {
            background-color: var(--bg-canvas);
            color: var(--text-body);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            overflow-x: hidden;
            background-image: var(--brand-glow-radial);
            background-attachment: fixed;
        }

        /* Top Bar */
        header {
            background: var(--surface-panel);
            backdrop-filter: blur(20px);
            border-bottom: 1px solid var(--border-subtle);
            padding: 0.9rem 2.2rem;
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
            gap: 12px;
        }

        .logo-icon {
            width: 42px;
            height: 42px;
            border-radius: 10px;
            background: var(--brand-gradient);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 1.25rem;
            box-shadow: 0 4px 15px var(--border-glow);
        }

        .brand-title {
            font-family: 'Cabinet Grotesk', sans-serif;
            font-size: 1.35rem;
            font-weight: 800;
            color: var(--text-heading);
            letter-spacing: -0.5px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .brand-badge {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.65rem;
            padding: 3px 8px;
            border-radius: 6px;
            background: rgba(255, 255, 255, 0.08);
            color: var(--brand-primary);
            border: 1px solid var(--border-subtle);
            letter-spacing: 0.5px;
        }

        .header-controls {
            display: flex;
            align-items: center;
            gap: 1.2rem;
        }

        /* Theme Picker Pills */
        .theme-pill-selector {
            display: flex;
            align-items: center;
            gap: 6px;
            background: rgba(0, 0, 0, 0.2);
            padding: 4px 8px;
            border-radius: 30px;
            border: 1px solid var(--border-subtle);
        }

        .theme-swatch {
            width: 22px;
            height: 22px;
            border-radius: 50%;
            cursor: pointer;
            border: 2px solid transparent;
            transition: transform 0.2s, border-color 0.2s;
            position: relative;
        }

        .theme-swatch:hover {
            transform: scale(1.18);
        }

        .theme-swatch.active {
            border-color: var(--text-heading);
            transform: scale(1.15);
        }

        .swatch-obsidian { background: linear-gradient(135deg, #6366F1, #8B5CF6); }
        .swatch-aurora { background: linear-gradient(135deg, #00F0FF, #FF007F); }
        .swatch-emerald { background: linear-gradient(135deg, #10B981, #059669); }
        .swatch-sunset { background: linear-gradient(135deg, #F97316, #DC2626); }
        .swatch-light { background: linear-gradient(135deg, #E2E8F0, #4F46E5); }

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

        /* App Grid */
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

        /* Surface Panel Box */
        .surface-box {
            background: var(--surface-card);
            border: 1px solid var(--border-subtle);
            border-radius: 20px;
            padding: 1.75rem;
            backdrop-filter: blur(16px);
            box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.5);
            display: flex;
            flex-direction: column;
            gap: 1.4rem;
        }

        .section-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .section-header h2 {
            font-family: 'Cabinet Grotesk', sans-serif;
            font-size: 1.25rem;
            font-weight: 800;
            color: var(--text-heading);
            display: flex;
            align-items: center;
            gap: 10px;
        }

        /* Preset Controls */
        .preset-bar {
            display: flex;
            gap: 8px;
            background: rgba(0, 0, 0, 0.15);
            padding: 5px;
            border-radius: 10px;
            border: 1px solid var(--border-subtle);
        }

        .btn-preset {
            flex: 1;
            padding: 7px 10px;
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

        /* Input Form Groupings */
        .fieldset-block {
            border: 1px solid var(--border-subtle);
            border-radius: 12px;
            padding: 1.15rem;
            background: rgba(0, 0, 0, 0.1);
            display: flex;
            flex-direction: column;
            gap: 0.9rem;
        }

        .fieldset-legend {
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.75px;
            color: var(--brand-primary);
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .input-row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 0.9rem;
        }

        .input-group {
            display: flex;
            flex-direction: column;
            gap: 5px;
        }

        .input-group label {
            font-size: 0.775rem;
            color: var(--text-body);
            font-weight: 600;
        }

        .input-control {
            background: var(--surface-field);
            border: 1px solid var(--border-subtle);
            color: var(--text-heading);
            padding: 0.75rem 0.85rem;
            border-radius: 8px;
            font-size: 0.9rem;
            outline: none;
            transition: border-color 0.2s, box-shadow 0.2s;
        }

        .input-control:focus {
            border-color: var(--brand-primary);
            box-shadow: 0 0 0 3px var(--border-glow);
        }

        /* Submit Button */
        .btn-run {
            background: var(--brand-gradient);
            border: none;
            color: white;
            font-family: 'Cabinet Grotesk', sans-serif;
            font-size: 1.05rem;
            font-weight: 800;
            padding: 1.05rem;
            border-radius: 12px;
            cursor: pointer;
            box-shadow: 0 10px 25px -5px var(--border-glow);
            transition: transform 0.2s, box-shadow 0.2s;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
        }

        .btn-run:hover {
            transform: translateY(-2px);
            box-shadow: 0 14px 30px -5px var(--border-glow);
        }

        /* Cockpit Side Elements */
        .cockpit-view {
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
        }

        .overview-hero {
            display: grid;
            grid-template-columns: 220px 1fr;
            gap: 1.5rem;
            background: rgba(0, 0, 0, 0.15);
            border: 1px solid var(--border-subtle);
            border-radius: 16px;
            padding: 1.5rem;
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
            stroke: var(--border-subtle);
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
            font-family: 'Cabinet Grotesk', sans-serif;
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
            font-family: 'Cabinet Grotesk', sans-serif;
            font-size: 1.55rem;
            font-weight: 800;
            color: var(--text-heading);
        }

        .verdict-summary {
            font-size: 0.9rem;
            color: var(--text-body);
            line-height: 1.5;
        }

        /* KPI Quick Stats */
        .kpi-row {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1rem;
        }

        .kpi-stat-card {
            background: rgba(0, 0, 0, 0.15);
            border: 1px solid var(--border-subtle);
            border-radius: 12px;
            padding: 1.15rem;
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
            background: rgba(255, 255, 255, 0.05);
            color: var(--brand-primary);
        }

        .kpi-data-val {
            font-family: 'Cabinet Grotesk', sans-serif;
            font-size: 1.35rem;
            font-weight: 800;
            color: var(--text-heading);
        }

        .kpi-data-lbl {
            font-size: 0.725rem;
            color: var(--text-dim);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        /* Split Insights */
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
            background: rgba(0, 0, 0, 0.12);
            border: 1px solid var(--border-subtle);
            border-radius: 12px;
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
                    <span class="brand-badge">ENTERPRISE v3.0</span>
                </div>
            </div>
        </div>

        <div class="header-controls">
            <!-- Dynamic 5-Color Theme Switcher -->
            <div class="theme-pill-selector" title="Select Multi-Color Theme">
                <div class="theme-swatch swatch-obsidian active" onclick="setAppTheme('obsidian')" title="Midnight Obsidian"></div>
                <div class="theme-swatch swatch-aurora" onclick="setAppTheme('aurora')" title="Cyber Aurora"></div>
                <div class="theme-swatch swatch-emerald" onclick="setAppTheme('emerald')" title="Emerald Matrix"></div>
                <div class="theme-swatch swatch-sunset" onclick="setAppTheme('sunset')" title="Sunset Ember"></div>
                <div class="theme-swatch swatch-light" onclick="setAppTheme('light')" title="Enterprise Light"></div>
            </div>

            <div class="status-pill">
                <div class="status-dot"></div>
                <span>AdaBoost Core Active</span>
            </div>
        </div>
    </header>

    <!-- Main Workspace -->
    <div class="app-grid">
        
        <!-- Left: Configurator Panel -->
        <div class="surface-box">
            <div class="section-header">
                <h2><i class="fa-solid fa-sliders" style="color: var(--brand-primary);"></i> Customer Parameters</h2>
            </div>

            <!-- Fast Scenario Presets -->
            <div class="preset-bar">
                <button type="button" class="btn-preset active" onclick="loadPreset('loyal')">Loyal Member</button>
                <button type="button" class="btn-preset" onclick="loadPreset('atrisk')">High Attrition</button>
                <button type="button" class="btn-preset" onclick="loadPreset('newbie')">Early Stage</button>
            </div>

            <form id="churnForm">
                <div style="display: flex; flex-direction: column; gap: 1rem;">
                    
                    <!-- Domain 1: Demographics & Tenure -->
                    <div class="fieldset-block">
                        <div class="fieldset-legend">
                            <i class="fa-solid fa-id-badge"></i> Account Demographics
                        </div>
                        <div class="input-row">
                            <div class="input-group">
                                <label>Age</label>
                                <input type="number" id="Age" name="Age" class="input-control" value="41" min="18" max="100" required>
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
                            <label>Tenure (Months)</label>
                            <input type="number" id="Tenure" name="Tenure" class="input-control" value="28" min="0" max="120" required>
                        </div>
                    </div>

                    <!-- Domain 2: Product & Support Velocity -->
                    <div class="fieldset-block">
                        <div class="fieldset-legend">
                            <i class="fa-solid fa-bolt"></i> Behavioral Engagement
                        </div>
                        <div class="input-row">
                            <div class="input-group">
                                <label>Usage Frequency / Mo</label>
                                <input type="number" id="Usage Frequency" name="Usage Frequency" class="input-control" value="16" min="0" max="100" required>
                            </div>
                            <div class="input-group">
                                <label>Support Tickets</label>
                                <input type="number" id="Support Calls" name="Support Calls" class="input-control" value="1" min="0" max="25" required>
                            </div>
                        </div>
                        <div class="input-group">
                            <label>Days Since Last Interaction</label>
                            <input type="number" id="Last Interaction" name="Last Interaction" class="input-control" value="4" min="0" max="365" required>
                        </div>
                    </div>

                    <!-- Domain 3: Billing & Contract Terms -->
                    <div class="fieldset-block">
                        <div class="fieldset-legend">
                            <i class="fa-solid fa-credit-card"></i> Contract & Billing
                        </div>
                        <div class="input-row">
                            <div class="input-group">
                                <label>Subscription Tier</label>
                                <select id="Subscription Type" name="Subscription Type" class="input-control">
                                    <option value="Basic">Basic Plan</option>
                                    <option value="Standard">Standard</option>
                                    <option value="Premium" selected>Premium Plan</option>
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
                        <span id="btnLabel"><i class="fa-solid fa-satellite-dish"></i> Execute Risk Inference</span>
                        <div class="spinner" id="btnLoader"></div>
                    </button>
                </div>
            </form>
        </div>

        <!-- Right: Diagnostic Cockpit -->
        <div class="surface-box cockpit-view">
            
            <div class="section-header">
                <h2><i class="fa-solid fa-microchip" style="color: var(--brand-secondary);"></i> Executive Cockpit</h2>
                <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: var(--text-dim);" id="timestamp">REALTIME READY</span>
            </div>

            <!-- Risk Gauge & Headline -->
            <div class="overview-hero">
                <div class="gauge-wrapper">
                    <svg class="gauge-svg" width="170" height="170" viewBox="0 0 170 170">
                        <circle class="gauge-bg" cx="85" cy="85" r="70" />
                        <circle class="gauge-fill" id="gaugeCircle" cx="85" cy="85" r="70" />
                    </svg>
                    <div class="gauge-center-text">
                        <div class="gauge-val" id="churnRiskPercent">--%</div>
                        <div class="gauge-sub">Churn Risk</div>
                    </div>
                </div>

                <div class="verdict-info">
                    <div id="riskBadge" class="verdict-badge badge-safe">
                        <i class="fa-solid fa-shield-check"></i> <span id="riskBadgeText">Awaiting Assessment</span>
                    </div>
                    <div class="verdict-heading" id="verdictHeadline">Run Inference to Evaluate</div>
                    <div class="verdict-summary" id="verdictSummary">
                        Adjust parameters on the customer DNA panel or select a scenario to evaluate retention probability via the AdaBoost ensemble.
                    </div>
                </div>
            </div>

            <!-- KPI Row -->
            <div class="kpi-row">
                <div class="kpi-stat-card">
                    <div class="kpi-stat-icon"><i class="fa-solid fa-gauge-high"></i></div>
                    <div>
                        <div class="kpi-data-val" id="kpiModelConfidence">--%</div>
                        <div class="kpi-data-lbl">Ensemble Confidence</div>
                    </div>
                </div>
                <div class="kpi-stat-card">
                    <div class="kpi-stat-icon"><i class="fa-solid fa-hand-holding-dollar"></i></div>
                    <div>
                        <div class="kpi-data-val" id="kpiLTV">$840</div>
                        <div class="kpi-data-lbl">Account Value</div>
                    </div>
                </div>
                <div class="kpi-stat-card">
                    <div class="kpi-stat-icon"><i class="fa-solid fa-heart-pulse"></i></div>
                    <div>
                        <div class="kpi-data-val" id="kpiHealthRating">Healthy</div>
                        <div class="kpi-data-lbl">Lifecycle Status</div>
                    </div>
                </div>
            </div>

            <!-- Playbook and Signal Chart Split -->
            <div class="insights-grid">
                <div class="playbook-card">
                    <div class="playbook-title">
                        <i class="fa-solid fa-lightbulb" style="color: var(--status-warn);"></i> Prescribed Action Plan
                    </div>
                    <div id="playbookItems">
                        <div class="action-item">
                            <strong>System Idle</strong>
                            Execute prediction to trigger automated AI retention interventions.
                        </div>
                    </div>
                </div>

                <div class="playbook-card">
                    <div class="playbook-title">
                        <i class="fa-solid fa-chart-column" style="color: var(--brand-primary);"></i> Risk Distribution Vectors
                    </div>
                    <div style="height: 180px; position: relative;">
                        <canvas id="featureChart"></canvas>
                    </div>
                </div>
            </div>

        </div>

    </div>

    <!-- Scripts -->
    <script>
        let featureChartInstance = null;
        let lastFeatureMetrics = null;

        // Theme Switcher Logic with LocalStorage Persist
        function setAppTheme(themeName) {
            document.documentElement.setAttribute('data-theme', themeName);
            localStorage.setItem('churnpulse_theme', themeName);
            
            document.querySelectorAll('.theme-swatch').forEach(sw => {
                sw.classList.remove('active');
                if (sw.classList.contains(`swatch-${themeName}`)) {
                    sw.classList.add('active');
                }
            });

            // Re-render chart if already populated to synchronize colors
            if (lastFeatureMetrics) {
                renderChart(lastFeatureMetrics);
            }
        }

        // Restore Theme on Mount
        window.addEventListener('DOMContentLoaded', () => {
            const savedTheme = localStorage.getItem('churnpulse_theme') || 'obsidian';
            setAppTheme(savedTheme);
        });

        // Scenario Presets
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

        // Form Submit Execution
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
            document.getElementById('timestamp').innerText = new Date().toLocaleTimeString();

            // Gauge animation
            const risk = res.risk_score;
            document.getElementById('churnRiskPercent').innerText = `${risk}%`;
            
            const circle = document.getElementById('gaugeCircle');
            const circumference = 440;
            const offset = circumference - (risk / 100) * circumference;
            circle.style.strokeDashoffset = offset;

            // Verdict Badges & Status
            const badge = document.getElementById('riskBadge');
            const badgeText = document.getElementById('riskBadgeText');
            const headline = document.getElementById('verdictHeadline');
            const summary = document.getElementById('verdictSummary');
            const healthRating = document.getElementById('kpiHealthRating');

            const style = getComputedStyle(document.documentElement);
            const statusDanger = style.getPropertyValue('--status-danger').trim();
            const statusSafe = style.getPropertyValue('--status-safe').trim();

            if (res.prediction === 1) {
                circle.style.stroke = statusDanger;
                badge.className = 'verdict-badge badge-danger';
                badgeText.innerHTML = '<i class="fa-solid fa-triangle-exclamation"></i> High Churn Threat';
                headline.innerText = 'Immediate Churn Risk';
                summary.innerText = 'The model flags high friction points: elevated support velocity, overdue payments, or decaying login frequency.';
                healthRating.innerText = 'Critical';
                healthRating.style.color = statusDanger;
            } else {
                circle.style.stroke = statusSafe;
                badge.className = 'verdict-badge badge-safe';
                badgeText.innerHTML = '<i class="fa-solid fa-shield-check"></i> Retained & Stable';
                headline.innerText = 'Customer Retained';
                summary.innerText = 'Healthy retention telemetry. Customer displays solid tenure stability, on-time billings, and regular platform activity.';
                healthRating.innerText = 'Optimal';
                healthRating.style.color = statusSafe;
            }

            document.getElementById('kpiModelConfidence').innerText = `${res.confidence}%`;
            document.getElementById('kpiLTV').innerText = `$${parseFloat(document.getElementById('Total Spend').value).toFixed(2)}`;

            buildPlaybook(res);

            lastFeatureMetrics = res.features_impact;
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
                        title: 'Assign Dedicated CSM Agent',
                        desc: `Account logged ${supportCalls} tickets. Trigger automated priority escalation.`
                    });
                }
                if (delay > 5) {
                    actions.push({
                        title: 'Billing Grace Period & Payment Setup',
                        desc: `Payment latency is ${delay} days. Send personalized invoice reconciliation.`
                    });
                }
                if (daysSinceTouch > 15) {
                    actions.push({
                        title: 'Automated Lifecycle Nudge Campaign',
                        desc: 'Customer inactive for >15 days. Deploy retention feature highlight digest.'
                    });
                }
                if (actions.length === 0) {
                    actions.push({
                        title: 'Executive Renewal Incentive',
                        desc: 'Offer complimentary 15% discount or feature add-on prior to billing cycle.'
                    });
                }
            } else {
                actions.push({
                    title: 'Account Expansion / Tier Upgrade',
                    desc: 'Healthy metrics detected. Target for annual contract conversion or enterprise tier.'
                });
                actions.push({
                    title: 'Customer Advisory Invitation',
                    desc: 'Invite to product beta testing group and collect quarterly CSAT feedback.'
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

            const style = getComputedStyle(document.documentElement);
            const chartFill = style.getPropertyValue('--chart-fill').trim() || 'rgba(99, 102, 241, 0.4)';
            const chartStroke = style.getPropertyValue('--chart-stroke').trim() || '#6366F1';
            const textDim = style.getPropertyValue('--text-dim').trim() || '#64748B';

            if (featureChartInstance) {
                featureChartInstance.destroy();
            }

            featureChartInstance = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Feature Intensity',
                        data: values,
                        backgroundColor: chartFill,
                        borderColor: chartStroke,
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
                            ticks: { color: textDim, font: { size: 10 } },
                            grid: { display: false }
                        },
                        y: {
                            ticks: { color: textDim, font: { size: 10 } },
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
        # Extract features from form submission
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

        # Encodings aligned with dataset
        gender = 1 if gender_str == 'Male' else 0
        sub_map = {'Basic': 0, 'Standard': 1, 'Premium': 2}
        subscription_type = sub_map.get(sub_type_str, 0)
        contract_map = {'Monthly': 0, 'Quarterly': 1, 'Annual': 2}
        contract_length = contract_map.get(contract_str, 0)

        # 10-feature matrix in exact trained order
        features = np.array([[
            age, gender, tenure, usage_freq, support_calls,
            payment_delay, subscription_type, contract_length,
            total_spend, last_interaction
        ]])

        prediction = model.predict(features)[0]

        # Calculate confidence & probability
        confidence = 91.5
        risk_score = 12
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

# Export WSGI application for Vercel
app = app

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
