# Contoso Retail FY2025 Dashboard

An interactive Streamlit dashboard for exploring Contoso Retail's FY2025
financial results, customer trends, sales channels, store performance, product
rankings, and customer retention.

The interface supports desktop and mobile layouts, including compact charts,
responsive tables, and expandable analysis text on smaller screens.

## Features

- Revenue, customer, and order KPIs
- Monthly revenue and customer trends
- Customer distribution by age group and region
- Online versus in-store order analysis
- Store, brand, category, and product performance
- Customer cohort, retention, and churn analysis
- Responsive desktop and mobile presentation

## Run locally

1. Create and activate a Python virtual environment.
2. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Start the dashboard:

   ```bash
   streamlit run app.py
   ```

## Project structure

```text
.
|-- app.py             # Streamlit application
|-- data/              # CSV files consumed by the dashboard
|-- images/            # Dashboard image assets
|-- sql/               # SQL queries used to prepare the analysis
|-- LICENSE            # MIT license for the repository
|-- requirements.txt   # Runtime dependencies
|-- .gitignore         # Files excluded from Git
`-- README.md          # Project documentation
```

## Deployment

Push the repository to GitHub, then select `app.py` as the application entry
point in your Streamlit hosting provider. The committed `requirements.txt`
installs all direct runtime dependencies. Keep secrets outside the repository;
`.streamlit/secrets.toml` and `.env` files are ignored by Git.

## Data source

Microsoft Contoso Retail dataset.
