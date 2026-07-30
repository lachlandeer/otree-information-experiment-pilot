# Information and Social Norms Experiment - Pilot

This repository contains the oTree implementation for the pilot phase of the Information and Social Norms Experiment.

## Key Design Parameters
* **Base Currency:** GBP (£)
* **Exchange Rate:** 200 Points = £1.00
* **Participation Fee:** £1.00

---

## Experiment Flow (App Sequence)

Participants move through the following sequence of apps:

1. **`Introduction`**: General introduction to the study, payment rates, and instruction guidelines.
2. **`asset_indiv_no_game` (Task 1)**: Asset valuation and individual belief elicitation task. One round is randomly drawn for payment.
3. **`GroupPreferenceElicitation` / `BonusStage01` (Task 2)**: Group preference/social task. Payment is resolved post-experiment.
4. **`CollectivismSurvey`**: Survey measuring collectivism.
5. **`CognitiveReflectionTask`**: A 7-item Cognitive Reflection Test (Frederick 2005 + Toplak et al. 2014) with a 2-minute soft timer nudge per page.
6. **`DemographicsSurvey`**: Demographic background survey.
7. **`conformity_main` (Task 3)**: Color prediction task. Participants choose between Peer Predictions (Advisor A) and varying Computer Prediction accuracies (Advisor B) before guessing a ball color.
8. **`RandomPaymentResults`**: Final earnings summary screen displaying itemized payments and total payouts.

---

## Local Setup & Development

### 1. Prerequisites
* Python 3.10
* Virtual environment tool (`venv` or `uv`)

### 2. Installation
Clone the repository and install the dependencies inside a virtual environment:

```bash
# Clone the repository
git clone <repo-url>
cd otree-information-experiment-pilot

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### 3. Database Initialization
Before running the server for the first time (or after making model changes), reset the local SQLite database:
```bash
otree resetdb
```

### 4. Running the Server
Start the local oTree development server:
```bash
otree devserver
```
Once running, open your browser and navigate to:
* **Admin Interface & Demos:** [http://localhost:8000](http://localhost:8000)
