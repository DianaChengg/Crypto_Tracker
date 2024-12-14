import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "token" not in st.session_state:
    st.session_state.token = None

if "crypto_prices" not in st.session_state:
    st.session_state.crypto_prices = None

st.sidebar.title("Navigation")
st.sidebar.button("Index", key="dashboard", on_click=lambda: st.experimental_set_query_params(page="dashboard"))
st.sidebar.button("Portfolio", key="portfolio", on_click=lambda: st.experimental_set_query_params(page="portfolio"))
st.sidebar.button("Wallet", key="wallet", on_click=lambda: st.experimental_set_query_params(page="wallet"))

st.sidebar.markdown("<div style='position: fixed; bottom: 0; width: 100%;'>", unsafe_allow_html=True)
if st.session_state.logged_in:
    st.sidebar.button("Profile", key="profile", on_click=lambda: st.experimental_set_query_params(page="profile"))
    st.sidebar.button("Logout", key="logout", on_click=lambda: logout())
else:
    st.sidebar.button("Login", key="login", on_click=lambda: st.experimental_set_query_params(page="login"))
    st.sidebar.button("Register", key="register", on_click=lambda: st.experimental_set_query_params(page="register"))
st.sidebar.markdown("</div>", unsafe_allow_html=True)

def logout():
    st.session_state.logged_in = False
    st.session_state.token = None
    st.experimental_set_query_params(page="welcome")
    st.experimental_rerun()

def expandable_button(row, col):
    expander_key = f"expander_{row['id']}"
    if expander_key not in st.session_state:
        st.session_state[expander_key] = False

    if col.button(f"{row['name']} ({row['symbol']}) - ${row['current_price']}", key=f"button_{row['id']}"):
        st.session_state[expander_key] = not st.session_state[expander_key]

    if st.session_state[expander_key]:
        col.write(f"Market Cap: ${row['market_cap']}")
        col.write(f"Total Volume: ${row['total_volume']}")
        col.button("Details", key=f"details_{row['id']}", on_click=lambda: st.experimental_set_query_params(page="chart", crypto=row["id"]))

def calculate_gains_losses(df):
    df['gains'] = df['price_change_percentage_24h'].apply(lambda x: x if x > 0 else 0)
    df['losses'] = df['price_change_percentage_24h'].apply(lambda x: x if x < 0 else 0)
    return df

def dashboard_page():
    st.title("Crypto Tracker")

    with st.expander("Advanced Search"):
        search_term = st.text_input("Search by name or symbol")
        min_price = st.number_input("Minimum Price", value=0.0)
        max_price = st.number_input("Maximum Price", value=100000.0)
        order_by = st.selectbox("Order by", ["current_price", "market_cap", "total_volume", "gains", "losses"])
        order_direction = st.selectbox("Order direction", ["Ascending", "Descending"])
        num_columns = st.selectbox("Number of columns", [1, 2, 3, 4, 5])

    def get_crypto_prices():
        response = requests.get("https://api.coingecko.com/api/v3/coins/markets", params={"vs_currency": "usd"})
        data = response.json()
        df = pd.DataFrame(data)
        return df

    if st.session_state.crypto_prices is None:
        st.session_state.crypto_prices = get_crypto_prices()

    crypto_prices = st.session_state.crypto_prices

    crypto_prices = calculate_gains_losses(crypto_prices)

    if search_term:
        crypto_prices = crypto_prices[
            crypto_prices['name'].str.contains(search_term, case=False) |
            crypto_prices['symbol'].str.contains(search_term, case=False)
        ]

    crypto_prices = crypto_prices[
        (crypto_prices['current_price'] >= min_price) &
        (crypto_prices['current_price'] <= max_price)
    ]

    required_columns = ["id", "name", "symbol", "current_price", "market_cap", "total_volume", "gains", "losses"]
    if all(column in crypto_prices.columns for column in required_columns):
        crypto_prices = crypto_prices[required_columns]
    else:
        st.error("The required columns are not present in the data.")
        st.write("Available columns:", crypto_prices.columns)
        return

    ascending = True if order_direction == "Ascending" else False
    crypto_prices = crypto_prices.sort_values(by=order_by, ascending=ascending)
    columns = st.columns(num_columns)

    for i, row in crypto_prices.iterrows():
        col = columns[i % num_columns]
        expandable_button(row, col)

    
def crypto_chart_page():
    st.markdown(
        """
        <style>
        .crypto-header {
            font-size: 32px;
            font-weight: bold;
            text-align: center;
            color: #2E86C1;
            margin-bottom: 20px;
        }
        .crypto-details {
            font-size: 16px;
            margin: 10px 0;
            line-height: 1.6;
        }
        .details-box {
            background-color: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Get the cryptocurrency ID from query params
    query_params = st.experimental_get_query_params()
    crypto_id = query_params.get("crypto", [""])[0]

    if not crypto_id:
        st.error("No cryptocurrency selected.")
        return

    st.markdown(f"<div class='crypto-header'>Historical Prices for {crypto_id.capitalize()}</div>", unsafe_allow_html=True)

    # Fetch current details of the cryptocurrency
    try:
        details_response = requests.get(
            f"https://api.coingecko.com/api/v3/coins/markets",
            params={"vs_currency": "usd", "ids": crypto_id}
        )
        if details_response.status_code == 200:
            details_data = details_response.json()[0]  # Extract the first element

            # Display current cryptocurrency details in a professional box layout
            st.markdown(
                f"""
                <div class="details-box">
                    <div class="crypto-details"><strong>Name:</strong> {details_data['name']}</div>
                    <div class="crypto-details"><strong>Symbol:</strong> {details_data['symbol'].upper()}</div>
                    <div class="crypto-details"><strong>Current Price (USD):</strong> ${details_data['current_price']:.2f}</div>
                    <div class="crypto-details"><strong>Market Cap (USD):</strong> ${details_data['market_cap']:,}</div>
                    <div class="crypto-details"><strong>Total Volume (USD):</strong> ${details_data['total_volume']:,}</div>
                    <div class="crypto-details"><strong>24h High (USD):</strong> ${details_data['high_24h']:.2f}</div>
                    <div class="crypto-details"><strong>24h Low (USD):</strong> ${details_data['low_24h']:.2f}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        else:
            st.error("Failed to fetch current details for the cryptocurrency.")

    except Exception as e:
        st.error(f"An error occurred while fetching cryptocurrency details: {str(e)}")

    # Fetch historical data for the chart
# 绘制图表部分
    try:
        history_response = requests.get(
            f"https://api.coingecko.com/api/v3/coins/{crypto_id}/market_chart",
            params={"vs_currency": "usd", "days": "14"}
        )
        if history_response.status_code == 200:
            data = history_response.json()
            prices = data.get("prices", [])

            # 数据处理
            df = pd.DataFrame(prices, columns=["timestamp", "price"])
            df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

            # 使用 Plotly 绘制图表
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df["timestamp"],
                y=df["price"],
                mode="lines+markers",
                name="Price (USD)",
                line=dict(color="blue", width=2),
                marker=dict(size=6),
                hovertemplate="<b>Date:</b> %{x}<br><b>Price:</b> $%{y:.2f}<extra></extra>"
            ))

            # 添加5日均线
            df["SMA"] = df["price"].rolling(window=5).mean()
            fig.add_trace(go.Scatter(
                x=df["timestamp"],
                y=df["SMA"],
                mode="lines",
                name="5-Day SMA",
                line=dict(color="orange", width=2, dash="dot"),
                hovertemplate="<b>Date:</b> %{x}<br><b>SMA:</b> $%{y:.2f}<extra></extra>"
            ))

            # 更新图表布局
            fig.update_layout(
                title=f"{crypto_id.capitalize()} Price Trend (Last 14 Days)",
                xaxis=dict(title="Date", showgrid=True, gridcolor="#eeeeee"),
                yaxis=dict(title="Price (USD)", showgrid=True, gridcolor="#eeeeee"),
                template="plotly_white",
                hovermode="x unified",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )

            # 只绘制一次图表
            st.plotly_chart(fig, use_container_width=True, key=f"chart_{crypto_id}")
        else:
            st.error("Failed to fetch historical data.")
    except Exception as e:
        st.error(f"An error occurred while fetching historical data: {str(e)}")

    # st.plotly_chart(fig, use_container_width=True, key=f"chart_{crypto_id}")
    
    symbol = details_data['symbol'].upper()
    wsj_link = f"https://www.wsj.com/search?query={symbol}"
    st.markdown("""
    <div style='background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 10px 0;'>
        <h3 style='color: #2E86C1; margin-bottom: 10px;'>Latest News</h3>
        <a href='{wsj_link}' target='_blank' style='text-decoration: none; color: #2874A6; font-weight: 500;'>
            Check {symbol} Market Updates on WSJ 📰
        </a>
    </div>
    """.format(wsj_link=wsj_link, symbol=symbol), unsafe_allow_html=True)



    if st.button("Back to Crypto Prices"):
        st.experimental_set_query_params(page="index")
        st.stop()

    

    # if st.button("Back to Crypto Prices"):
    #     st.experimental_set_query_params(page="index")
    #     st.stop()
def portfolio_page():
    # Title and introduction
    st.markdown("""
        <style>
        .main-title {
            font-size: 32px;
            font-weight: bold;
            color: #2b83ba;
            text-align: center;
            margin-bottom: 20px;
        }
        .sub-title {
            font-size: 24px;
            font-weight: bold;
            margin-top: 20px;
            color: #333333;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="main-title">Your Portfolio</div>', unsafe_allow_html=True)

    # Simulated user portfolio with updated column names
    if "user_portfolio" not in st.session_state:
        st.session_state.user_portfolio = pd.DataFrame({
            "Asset Name": ["Bitcoin", "Ethereum", "Cardano"],
            "Position (Units)": [0, 0, 0],
            "Current Price (USD)": [0, 0, 0],
        })
        st.session_state.user_portfolio["Total Value (USD)"] = (
            st.session_state.user_portfolio["Position (Units)"] * st.session_state.user_portfolio["Current Price (USD)"]
        )

    def get_crypto_price(asset_name):
        try:
            response = requests.get(
                "https://api.coingecko.com/api/v3/simple/price",
                params={"ids": asset_name.lower(), "vs_currencies": "usd"},
            )
            if response.status_code == 200:
                data = response.json()
                return data[asset_name.lower()]["usd"]
            else:
                st.error("Failed to fetch crypto price. Please check the name.")
                return 0
        except Exception as e:
            st.error(f"Error fetching price: {e}")
            return 0

    # Display user portfolio
    st.markdown('<div class="sub-title">Your Current Portfolio</div>', unsafe_allow_html=True)
    st.dataframe(st.session_state.user_portfolio.style.format({
        "Position (Units)": "{:.2f}",
        "Current Price (USD)": "${:,.2f}",
        "Total Value (USD)": "${:,.2f}"
    }))

    # Add cryptocurrency to portfolio
    st.markdown('<div class="sub-title">Add Cryptocurrency to Portfolio</div>', unsafe_allow_html=True)
    new_asset = st.text_input("Asset Name (e.g., Bitcoin, Ethereum)", key="asset_name")
    new_position = st.number_input("Units to Add", min_value=0.0, step=0.01, key="asset_position")

    if st.button("Add to Portfolio"):
        if new_asset.strip() and new_position > 0:
            # Fetch current price
            current_price = get_crypto_price(new_asset)
            if current_price > 0:
                portfolio = st.session_state.user_portfolio
                if new_asset.capitalize() in portfolio["Asset Name"].values:
                    # Update existing entry
                    index = portfolio[portfolio["Asset Name"] == new_asset.capitalize()].index[0]
                    portfolio.loc[index, "Position (Units)"] += new_position
                    portfolio.loc[index, "Current Price (USD)"] = current_price
                    portfolio.loc[index, "Total Value (USD)"] = (
                        portfolio.loc[index, "Position (Units)"] * portfolio.loc[index, "Current Price (USD)"]
                    )
                    st.success(f"Updated {new_asset.capitalize()} in your portfolio!")
                else:
                    # Add new entry
                    new_entry = {
                        "Asset Name": new_asset.capitalize(),
                        "Position (Units)": new_position,
                        "Current Price (USD)": current_price,
                        "Total Value (USD)": new_position * current_price,
                    }
                    st.session_state.user_portfolio = pd.concat(
                        [portfolio, pd.DataFrame([new_entry])], ignore_index=True
                    )
                    st.success(f"Added {new_asset.capitalize()} to your portfolio!")
            else:
                st.error(f"Could not fetch price for {new_asset}.")
        else:
            st.warning("Please provide valid asset name and position.")

    # Asset Allocation Chart
    st.markdown('<div class="sub-title">Portfolio Asset Allocation</div>', unsafe_allow_html=True)
    portfolio = st.session_state.user_portfolio
    if not portfolio.empty:
        fig = go.Figure(data=[go.Pie(
            labels=portfolio["Asset Name"],
            values=portfolio["Total Value (USD)"],
            hole=0.4,
            hoverinfo="label+percent+value",
            textinfo="label+percent",
            textfont_size=14,
            marker=dict(colors=px.colors.sequential.Viridis, line=dict(color="#000000", width=2)),
        )])

        fig.update_layout(
            
            margin=dict(t=50, b=50, l=25, r=25),
            showlegend=True,
            legend=dict(font=dict(size=12), orientation="h", x=0.5, xanchor="center", y=-0.2),
        )

        st.plotly_chart(fig, use_container_width=True)


def wallet_page():
    # 设置页面标题和介绍文字
    st.markdown("""
    <style>
    .title {
        font-size: 36px;
        font-weight: bold;
        color: #2E8B57;
        text-align: center;
        margin-bottom: 20px;
    }
    .subtitle {
        font-size: 20px;
        color: #4B0082;
        text-align: center;
        margin-bottom: 30px;
    }
    .wallet-card {
        background: #f5f5f5;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    .add-wallet {
        background: linear-gradient(90deg, #ff7e5f, #feb47b);
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        color: white;
        font-size: 18px;
        font-weight: bold;
        cursor: pointer;
    }
    .delete-wallet {
        background: linear-gradient(90deg, #ff6a95, #fd3a69);
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        color: white;
        font-size: 18px;
        font-weight: bold;
        cursor: pointer;
    }
    </style>
    <div class="title">🚀 Wallet Management</div>
    <div class="subtitle">Easily view, add, or delete your cryptocurrency wallets.</div>
    """, unsafe_allow_html=True)

    # 获取钱包数据
    try:
        headers = {"Authorization": f"Bearer {st.session_state.token}"}
        uid = 1  # Replace with dynamic UID if available
        response = requests.get(f"http://localhost:8000/wallet/{uid}", headers=headers)

        if response.status_code == 200:
            wallet_data = response.json()

            if wallet_data:
                st.markdown("<h3>💼 Your Wallets</h3>", unsafe_allow_html=True)

                for wallet in wallet_data:
                    st.markdown(f"""
                    <div class="wallet-card">
                        <strong>Name:</strong> {wallet['wname']}<br>
                        <strong>Address:</strong> {wallet['address']}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No wallet data available.")
        else:
            st.error("Failed to fetch wallet data.")
    except Exception as e:
        st.error(f"Error fetching wallet data: {e}")

    # 添加新钱包
    st.markdown("<h3>➕ Add a New Wallet</h3>", unsafe_allow_html=True)
    new_wallet_name = st.text_input("Wallet Name", placeholder="e.g., My Crypto Wallet")
    new_wallet_address = st.text_input("Wallet Address", placeholder="e.g., 0x123abc...")
    if st.button("Add Wallet"):
        try:
            payload = {
                "uid": uid,
                "wname": new_wallet_name,
                "address": new_wallet_address,
            }
            add_response = requests.post(
                "http://localhost:8000/wallet/",
                headers=headers,
                json=payload
            )

            if add_response.status_code == 200:
                st.success("🎉 Wallet added successfully!")
                st.experimental_rerun()
            else:
                st.error(f"Failed to add wallet: {add_response.json().get('detail', 'Unknown error')}")
        except Exception as e:
            st.error(f"Error adding wallet: {e}")

    # 删除钱包
    st.markdown("<h3>🗑️ Delete a Wallet</h3>", unsafe_allow_html=True)
    delete_wallet_name = st.text_input("Enter Wallet Name to Delete", placeholder="e.g., My Crypto Wallet")
    if st.button("Delete Wallet"):
        try:
            delete_response = requests.delete(
                f"http://localhost:8000/wallet/{uid}/{delete_wallet_name}",
                headers=headers
            )
            if delete_response.status_code == 200:
                st.success("✅ Wallet deleted successfully!")
                st.experimental_rerun()
            else:
                st.error(f"Failed to delete wallet: {delete_response.json().get('detail', 'Unknown error')}")
        except Exception as e:
            st.error(f"Error deleting wallet: {e}")

    # 返回主页面
    st.button("Back to Dashboard", lambda: st.experimental_set_query_params(page="dashboard"))
    
def profile_page():
    st.header("Profile")

    try:
        headers = {"Authorization": f"Bearer {st.session_state.token}"}
        response = requests.get("http://localhost:8000/users/me", headers=headers)
        if response.status_code == 200:
            user_info = response.json()
        else:
            st.error("Failed to fetch user info.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

    st.text(f"Username: {user_info.get('username', 'Placeholder')}")
    st.text(f"Email: {user_info.get('email', 'placeholder@example.com')}")

def login(email, password):
    try:
        response = requests.post(
            "http://localhost:8000/token",
            data={"username": email, "password": password},
        )
        if response.status_code == 200:
            st.success("Login successful!")
            st.session_state.logged_in = True
            st.session_state.token = response.json()["access_token"]
            st.experimental_set_query_params(page="dashboard")
        else:
            st.error("Login failed. Please check your email and password.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

def login_page():
    st.header("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    st.button("Login", on_click=lambda: login(email, password))

def register(email, username, password):
    try:
        response = requests.post(
            "http://localhost:8000/users/",
            json={"username": username, "email": email, "password": password},
        )
        if response.status_code == 201:
            st.success("Registration successful! Please log in.")
            st.experimental_set_query_params(page="login")
            st.experimental_rerun()
        else:
            st.error("Registration failed. Please try again.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

def register_page():
    st.header("Register")
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    st.button("Register", on_click=lambda: register(email, username, password))

query_params = st.experimental_get_query_params()
page = query_params.get("page", ["dashboard"])[0]

if page == "dashboard":
    dashboard_page()
elif page == "portfolio":
    portfolio_page()
elif page == "wallet":
    wallet_page()
elif page == "login":
    login_page()
elif page == "register":
    register_page()
elif page == "chart":
    crypto_chart_page()
elif page == "profile":
    profile_page()
else:
    dashboard_page()