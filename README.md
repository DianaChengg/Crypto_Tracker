# Crypto Tracker

## Overview
**Crypto Tracker** is a web application designed to help users track cryptocurrency prices, market trends, and news in real-time. The application leverages the **CoinGecko API** to provide up-to-date market data and insights. Users can search for specific cryptocurrencies, monitor historical price trends, and manage their investment portfolios efficiently.

---

## Features

### 1. Cryptocurrency Price Search
- Users can search for specific cryptocurrencies by name or symbol.
- Provides real-time market data, including price, market capitalization, and trading volume.
- Utilizes CoinGecko API to fetch accurate and up-to-date information.

### 2. Market Trends
- Displays key market metrics such as:
  - Price changes (24-hour, 7-day, 30-day)
  - Market capitalization
  - Trading volume
- Presents data in a user-friendly format with sorting and filtering options.

### 3. Historical Data
- Users can analyze cryptocurrency performance over time using interactive charts.
- Historical price data is visualized using Plotly for better insights.
- Options to view trends over different time frames (e.g., 7 days, 30 days, 1 year).

### 4. News Feed
- Aggregates the latest cryptocurrency-related news from trusted sources.
- Provides real-time updates on market events and trends.
- Users can stay informed about regulatory changes and major market movements.

### 5. User Accounts
- Enables users to create and manage accounts using **Firebase Authentication**.
- Allows users to save favorite cryptocurrencies for quick access.
- Supports setting up price alerts for specific cryptocurrencies.

### 6. Portfolio Tracker
- Users can add cryptocurrency holdings and track their portfolio value in real-time.
- Calculates total portfolio value based on current market prices.
- Visual representation of asset allocation using a pie chart.

---

## Tech Stack

### **Frontend**
- [Streamlit](https://streamlit.io/) – For building an interactive web interface.
- [Plotly](https://plotly.com/python/) – For creating interactive data visualizations.
- [Firebase](https://firebase.google.com/) – For user authentication and data storage.

### **Backend**
- [CoinGecko API](https://www.coingecko.com/en/api/documentation) – For fetching cryptocurrency market data.
- Python (Flask/FastAPI) – For backend processing and handling API calls (optional for authentication and storage).

---

## Installation

### Prerequisites
Ensure you have the following installed on your system:
- Python 3.8+
- Streamlit
- Requests
- Plotly
- Firebase Admin SDK 

### Setup Instructions

1. **Clone the repository:**
    ```sh
    git clone https://github.com/DianaChengg/Crypto_Tracker.git
    cd crypto-tracker
    ```

2. **Create a virtual environment:**
    ```sh
    python -m venv venv
    source venv/bin/activate   # On macOS/Linux
    venv\Scripts\activate      # On Windows
    ```

3. **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4. **Run the application:**
    ```sh
    streamlit run web_main.py
    ```

---

## Usage

1. **Search for Cryptocurrencies:**  
   Use the search bar to find cryptocurrencies by name or symbol.

2. **View Market Trends:**  
   Navigate through the dashboard to explore real-time market data.

3. **Analyze Historical Data:**  
   Select a cryptocurrency to view price trends over different time periods.

4. **Manage Portfolio:**  
   Add cryptocurrencies to your portfolio and track their performance.

5. **User Authentication (optional):**  
   Log in to save favorites and set up alerts.

---

## API Integration

The application relies on the **CoinGecko API** to fetch real-time and historical market data. Some key endpoints used include:

- **Get current price of cryptocurrencies:**
  ```http
  GET https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd

