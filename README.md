# 🚀 ChurnPulse AI™ — Customer Churn Prediction

### An Intelligent Customer Retention & Churn Risk Assessment System

ChurnPulse AI™ is a machine learning-powered web application designed to predict customer churn risk and help businesses identify customers who may be likely to discontinue their services.

The application uses an **AdaBoost classification model** to analyze customer demographics, engagement behavior, subscription details, billing patterns, and interaction history. It transforms customer information into a churn prediction, risk score, model confidence estimate, and actionable retention recommendations through an interactive dashboard.

The project combines machine learning with a modern enterprise-style interface to make customer risk assessment more accessible, intuitive, and useful for data-driven decision-making.

## 🌐 Live Demo

**Try the application online:**

🔗 **Live Project:** https://customer-churn-prediction-nine-chi.vercel.app/

📂 **GitHub Repository:** https://github.com/Siddhesh030/Customer-Churn-Prediction

Explore the dashboard, enter customer details, select predefined customer scenarios, and execute a churn risk assessment directly in your browser.

## 📌 Table of Contents

- [Project Overview](#-project-overview)
- [Problem Statement](#-problem-statement)
- [Project Objectives](#-project-objectives)
- [Key Features](#-key-features)
- [Customer Information Used](#-customer-information-used)
- [Machine Learning Model](#-machine-learning-model)
- [How the Application Works](#-how-the-application-works)
- [Technology Stack](#️-technology-stack)
- [Project Structure](#-project-structure)
- [Installation and Setup](#️-installation-and-setup)
- [Running the Application](#-running-the-application)
- [Using the Application](#-using-the-application)
- [Prediction Results](#-prediction-results)
- [Deployment](#-deployment)
- [Applications and Use Cases](#-applications-and-use-cases)
- [Limitations and Future Improvements](#-limitations-and-future-improvements)
- [Author](#-author)

## 📖 Project Overview

Customer churn is a major challenge for businesses that depend on recurring customers, subscriptions, or long-term customer relationships. When customers discontinue their services, businesses may experience revenue loss, reduced customer lifetime value, and increased customer acquisition costs.

ChurnPulse AI™ addresses this challenge by providing an interactive platform that estimates whether a customer is likely to churn based on selected customer attributes and behavioral indicators.

The application uses a pretrained AdaBoost model stored as a serialized machine learning artifact. A Flask application loads the model, processes customer inputs, and returns a prediction through its prediction endpoint. The interface then presents the result using a visual risk indicator, status information, and retention-oriented recommendations.

### What makes this project useful?

- **Predictive analytics:** Estimates customer churn using machine learning.
- **Risk assessment:** Displays a churn risk score for an individual customer.
- **Customer insights:** Summarizes selected customer characteristics in a dashboard.
- **Retention support:** Generates rule-based recommendations for customers flagged as at risk.
- **Interactive experience:** Provides scenario presets, visual indicators, charts, and theme customization.
- **Web deployment:** Makes the application accessible through a live Vercel deployment.

## 🎯 Problem Statement

Businesses often identify customer churn only after a customer has already discontinued a service. A reactive approach limits the time available to understand customer concerns and take preventive action.

The objective of this project is to build a machine learning application that can:

1. Analyze customer information and behavioral patterns.
2. Classify customers into churn or retention outcomes.
3. Estimate churn risk using the model's predicted probabilities when available.
4. Present prediction results through an intuitive dashboard.
5. Suggest potential retention actions based on the customer's risk status and selected behavioral indicators.

The ultimate goal is to demonstrate how machine learning can support proactive customer retention and business decision-making.

## 🎯 Project Objectives

- Develop a customer churn prediction application using an AdaBoost classifier.
- Integrate a pretrained machine learning model into a Flask web application.
- Process numerical and categorical customer attributes before inference.
- Provide an easy-to-use customer information form.
- Display churn risk, prediction status, and model confidence.
- Present customer indicators through interactive data visualizations.
- Generate rule-based retention recommendations for at-risk customers.
- Deploy the application online using Vercel.

## ✨ Key Features

### 1. 🤖 Machine Learning-Based Churn Prediction

The application uses a pretrained AdaBoost classification model to evaluate customer information and predict a churn-related outcome.

The model accepts ten features in the order expected by the saved model, ensuring that customer inputs are assembled consistently for inference.

### 2. 📊 Customer Churn Risk Score

The dashboard displays a percentage-based churn risk score when the model supports probability prediction.

This helps users quickly interpret the estimated risk associated with a customer.

**Note:** A risk score is a model-generated estimate, not a guarantee that a customer will churn.

### 3. 🎛️ Interactive Customer Input Form

Users can provide customer information through grouped input sections.

The form covers:

- Account demographics
- Customer tenure
- Behavioral engagement
- Support interactions
- Subscription information
- Contract length
- Payment delays
- Total customer spending
- Recent interaction history

### 4. ⚡ Predefined Customer Scenarios

The application includes three preset scenarios to make testing easier:

- **Loyal Member:** Represents a customer profile with longer tenure, frequent usage, and an annual subscription.
- **High Attrition:** Represents a customer profile with shorter tenure, reduced usage, more support calls, and payment delays.
- **Early Stage:** Represents a newer customer profile with moderate usage and a shorter customer relationship.

These presets populate the form with example values. They are intended for demonstration and do not guarantee a particular model prediction.

### 5. 🎨 Modern Enterprise Dashboard

The interface, branded as ChurnPulse AI™, features a dark, dashboard-oriented design with responsive layout elements and a customer risk assessment panel.

The dashboard includes:

- Churn risk indicator
- Prediction status
- Model confidence display
- Account value display
- Customer lifecycle status
- Retention action plan
- Customer feature visualization

### 6. 🌈 Multiple Interface Themes

Users can switch between five visual themes:

- Midnight Obsidian
- Cyber Aurora
- Emerald Matrix
- Sunset Ember
- Enterprise Light

The selected theme is stored in the browser's local storage so the interface can restore the user's preference.

### 7. 💡 Retention Recommendation Playbook

When a customer is classified as at risk, the application generates suggested actions based on selected customer indicators.

Examples include:

- Escalating accounts with frequent support interactions.
- Reviewing payment difficulties and payment setup.
- Considering personalized customer engagement.
- Prioritizing follow-up for customers with reduced interaction.

These recommendations are rule-based suggestions generated by the application, rather than actions automatically executed against real customer accounts.

### 8. 📈 Interactive Feature Visualization

The application uses Chart.js to display selected customer attributes as a bar chart.

This provides a visual summary of indicators such as tenure, usage frequency, support calls, payment delays, and recent interactions.

The visualization is descriptive; it should not be interpreted as a formal model explainability technique or a verified measurement of each feature's causal impact.

### 9. 🌍 Live Web Application

The application is deployed on Vercel, allowing users to access the interface without installing Python or machine learning dependencies locally.

## 👥 Customer Information Used

The application accepts ten input features.

| Feature | Description |
|---|---|
| Age | Customer age |
| Gender | Customer gender category |
| Tenure | Duration of the customer relationship, in months |
| Usage Frequency | Frequency of customer usage per month |
| Support Calls | Number of support interactions |
| Payment Delay | Number of days associated with payment delays |
| Subscription Type | Basic, Standard, or Premium |
| Contract Length | Monthly, Quarterly, or Annual |
| Total Spend | Total customer spending |
| Last Interaction | Days since the last customer interaction |

Categorical fields are converted into numeric values before being passed to the trained model. The encoding follows the mappings implemented in the application.

The quality of a prediction depends on providing sensible input values and using feature definitions consistent with those used when the model was trained.

## 🧠 Machine Learning Model

### AdaBoost Classifier

The project uses an **AdaBoost classification model**, loaded from the serialized file `Adaboost_model.pkl`.

AdaBoost, short for Adaptive Boosting, is an ensemble learning technique that combines multiple weak learners to produce a stronger predictive model.

During training, AdaBoost adjusts the importance of training examples so that subsequent learners can focus more on examples that were previously misclassified.

For a classification problem such as customer churn, this approach can learn patterns associated with customers who discontinue their services and customers who remain active.

### Model inference workflow

1. Load the serialized AdaBoost model.
2. Collect customer information from the web form.
3. Convert the submitted values into the expected numerical representation.
4. Construct the ten-feature input array in the trained feature order.
5. Generate the predicted class using the model.
6. Obtain class probabilities when the model supports `predict_proba`.
7. Return the prediction, estimated churn risk, and confidence information.
8. Update the dashboard with the results.

### Prediction interpretation

The application uses the following outcome labels:

- **Churn Imminent:** The model predicts the churn class.
- **Customer Retained:** The model predicts the non-churn class.

The probability-based churn score and the confidence estimate represent different quantities. The confidence estimate is based on the largest predicted class probability when probabilities are available, while the churn score uses the probability associated with the churn class.

The displayed score should be interpreted in the context of the model's training data and validation performance.

### Model performance

This repository contains the serialized model used for inference. The repository documentation does not currently establish verified test-set accuracy, precision, recall, F1-score, or ROC-AUC.

For that reason, this README does not claim a specific model accuracy. Such metrics should be added only after evaluating the model against a held-out test dataset.

## ⚙️ How the Application Works

The application follows a simple web-based machine learning inference workflow.

```text
User opens the web application
            |
            v
Enters customer information
            |
            v
Flask receives form submission
            |
            v
Categorical values are encoded
            |
            v
Ten-feature input array is created
            |
            v
Pretrained AdaBoost model
            |
            v
Customer churn prediction
            |
            v
Risk score and confidence estimate
            |
            v
Dashboard and retention recommendations
```

### Application components

**Frontend:** HTML, CSS, and JavaScript provide the user interface, input form, theme selection, charts, and interactive dashboard updates.

**Backend:** Flask serves the web interface and handles prediction requests.

**Machine learning:** NumPy constructs the feature array, and the serialized AdaBoost model performs inference.

**Visualization:** Chart.js renders the interactive feature chart.

**Deployment:** Vercel hosts the deployed application using the repository's deployment configuration.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Flask | Web application and prediction endpoint |
| NumPy | Numerical feature preparation |
| Scikit-learn | Machine learning model compatibility |
| AdaBoost | Customer churn classification |
| HTML5 | Application structure |
| CSS3 | Styling, themes, and responsive layout |
| JavaScript | Form submission and dynamic dashboard updates |
| Chart.js | Interactive bar chart |
| Font Awesome | Interface icons |
| Google Fonts | Interface typography |
| Pickle | Loading the serialized model |
| Vercel | Cloud deployment |
| Git and GitHub | Version control and source code hosting |

## 📁 Project Structure

The repository contains the following primary files:

```text
Customer-Churn-Prediction/
│
├── app.py                 # Flask application, interface, and prediction logic
├── Adaboost_model.pkl     # Serialized AdaBoost model
├── requirements.txt       # Python dependencies
├── vercel.json            # Vercel deployment configuration
└── README.md              # Project documentation
```

### File descriptions

- **`app.py`** — Contains the Flask routes, embedded HTML interface, styling, JavaScript functionality, customer input processing, prediction logic, and dashboard response handling.
- **`Adaboost_model.pkl`** — Stores the pretrained machine learning model loaded by the application.
- **`requirements.txt`** — Defines the pinned Python dependencies needed by the application.
- **`vercel.json`** — Contains deployment configuration for hosting the Flask application on Vercel.
- **`README.md`** — Documents the project, technologies, features, setup instructions, and usage.

## 🖥️ Installation and Setup

Follow these steps to run the project locally.

### Prerequisites

Install the following:

- Python 3.10 or a compatible Python version supported by the pinned dependencies.
- Git
- pip, the Python package installer

The project requirements pin Flask 3.0.3, NumPy 1.26.4, scikit-learn 1.6.1, and Gunicorn 22.0.0.

### Step 1: Clone the repository

```bash
git clone https://github.com/Siddhesh030/Customer-Churn-Prediction.git
```

### Step 2: Navigate to the project directory

```bash
cd Customer-Churn-Prediction
```

### Step 3: Create a virtual environment

```bash
python -m venv venv
```

Activate it using the command for your operating system.

**Windows — Command Prompt**

```bash
venv\Scripts\activate
```

**Windows — PowerShell**

```powershell
.\venv\Scripts\Activate.ps1
```

**macOS or Linux**

```bash
source venv/bin/activate
```

### Step 4: Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Step 5: Verify the project files

Make sure the following files are present in the project directory:

```text
app.py
Adaboost_model.pkl
requirements.txt
vercel.json
```

The model file is required for prediction. If it is missing or cannot be loaded, the application cannot perform normal inference.

## ▶️ Running the Application

Start the Flask development server with:

```bash
python app.py
```

Open your browser and navigate to:

**http://127.0.0.1:5000**

The application should display the ChurnPulse AI™ dashboard.

Enter customer information and submit the form to test the prediction workflow.

**Important:** Use the development server for local testing only. The production deployment uses the repository's Vercel configuration.

## 🧪 Using the Application

### Step 1: Open the application

Visit the [live ChurnPulse AI™ application](https://customer-churn-prediction-nine-chi.vercel.app/).

### Step 2: Select a customer scenario

Choose one of the available presets:

- Loyal Member
- High Attrition
- Early Stage

Alternatively, enter your own example customer information.

### Step 3: Enter customer details

Complete the form with demographic, engagement, support, subscription, contract, and billing information.

### Step 4: Execute risk inference

Click the **Execute Risk Inference** button to submit the form to the Flask prediction endpoint.

### Step 5: Review the prediction

Review the displayed prediction outcome, churn risk score, confidence estimate, lifecycle status, and feature chart.

### Step 6: Review suggested actions

If the customer is classified as at risk, review the suggested retention actions and consider which interventions may be appropriate for that customer.

## 📊 Prediction Results

After a successful prediction, the application returns a structured response containing fields such as:

| Field | Meaning |
|---|---|
| `status` | Indicates whether the prediction request succeeded |
| `prediction` | Predicted class encoded as an integer |
| `prediction_text` | Human-readable prediction outcome |
| `confidence` | Maximum class probability, when available |
| `risk_score` | Estimated probability of the churn class, when available |
| `features_impact` | Selected customer inputs presented for dashboard visualization |

The dashboard uses this response to update the risk indicator, customer status, account value display, retention playbook, and feature chart.

### Example interpretation

A customer with shorter tenure, low usage frequency, frequent support calls, or substantial payment delays may warrant closer review.

However, the application should not be assumed to classify every such customer as high risk. The actual prediction depends on the trained model and the complete set of input features.

## ☁️ Deployment

The project is deployed using Vercel.

🔗 **Production URL:** https://customer-churn-prediction-nine-chi.vercel.app/

The repository includes a `vercel.json` configuration file and exports the Flask application for deployment.

### Deployment workflow

1. Push the project files to GitHub.
2. Import the repository into Vercel.
3. Verify the Python runtime and deployment configuration.
4. Ensure the model artifact is included and accessible during deployment.
5. Deploy the application.
6. Open the production URL and test the prediction workflow.

### Deployment considerations

- The serialized model must be available at the path expected by `app.py`.
- The deployment environment must use compatible Python and scikit-learn versions.
- The model must load successfully in the serverless runtime.
- Prediction requests should be tested after deployment, not just the landing page.
- The model artifact should come from a trusted source because loading pickle files can execute arbitrary code.

## 💼 Applications and Use Cases

### Customer retention

Identify customers who may require proactive engagement and prioritize follow-up efforts.

### Subscription businesses

Evaluate customer profiles based on tenure, subscription plan, contract length, usage, and payment behavior.

### Customer success teams

Use prediction results as one additional input when reviewing customer accounts and planning retention activities.

### Business analytics

Demonstrate how machine learning predictions can be incorporated into an interactive dashboard for customer-risk assessment.

### Machine learning education

Explore the integration of a classification model with a Flask application and a browser-based interface.

## ⚠️ Limitations

- **Prediction uncertainty:** A model prediction is an estimate and does not guarantee future customer behavior.
- **Model validation:** Verified evaluation metrics should be documented before using the model for business-critical decisions.
- **Feature compatibility:** Input features and categorical encodings must match the model's training configuration.
- **Recommendation scope:** Retention recommendations are rule-based suggestions and do not represent an automated CRM integration.
- **Explainability:** The dashboard's feature chart visualizes customer inputs; it does not establish causal relationships or formal feature importance.
- **Data privacy:** Use synthetic or appropriately authorized customer data when testing the application.
- **Serialized model security:** Only load model files from trusted sources.

## 🔮 Future Improvements

Potential improvements for future versions include:

- Add a dedicated model training and evaluation script.
- Document accuracy, precision, recall, F1-score, and ROC-AUC on a held-out test set.
- Add confusion matrix and ROC curve visualizations.
- Implement explainability techniques such as SHAP, where compatible with the trained model.
- Improve input validation and error handling.
- Add bulk customer scoring through CSV uploads.
- Provide downloadable prediction reports.
- Introduce customer segmentation and churn-risk summaries.
- Integrate with a CRM or customer management platform.
- Add model versioning, monitoring, and periodic retraining.
- Expand automated testing for prediction logic and deployment reliability.

## 🤝 Contributing

Contributions, suggestions, and improvements are welcome.

To contribute:

1. Fork this repository.
2. Create a feature branch.
3. Implement and test your changes.
4. Commit your updates.
5. Push the branch to GitHub.
6. Open a pull request describing the proposed improvement.

## 📜 License

No license has been specified in this README. Before distributing the project for reuse, add an appropriate `LICENSE` file to the repository and document the selected license here.

## 👨‍💻 Author

**Siddhesh**

GitHub: [@Siddhesh030](https://github.com/Siddhesh030)

Project Repository: [Customer-Churn-Prediction](https://github.com/Siddhesh030/Customer-Churn-Prediction)

Live Application: [ChurnPulse AI™](https://customer-churn-prediction-nine-chi.vercel.app/)

---

⭐ If you find this project interesting, consider starring the repository and exploring the live application.

**ChurnPulse AI™ — Turning Customer Data into Actionable Churn Insights.**
