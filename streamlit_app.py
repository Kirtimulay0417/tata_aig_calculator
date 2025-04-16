import streamlit as st
import pandas as pd
import requests
import io

# Load Excel data from GitHub using raw link
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/Kirtimulay0417/tata_aig_calculator/main/Tata%20Aig%20Premium_Data.xlsx"
    response = requests.get(url)
    data = pd.read_excel(io.BytesIO(response.content), sheet_name='Premium_TATA')
    return data

def calculate_premium(age, deductible, sum_insured, term, global_cover):
    data = load_data()

    # Filter by user inputs
    filtered = data[
        (data['Age Band'] == age) &
        (data['Deductible'] == deductible) &
        (data['Sum Insured'] == sum_insured)
    ]

    if filtered.empty:
        return "No matching data found. Please check your inputs.", None

    base_premium = filtered['Premium'].values[0]

    # Apply discounts/add-ons
    discount = 0.1 if term == 2 else 0.15 if term == 3 else 0
    premium_after_term = base_premium * (1 - discount)

    global_cover_addon = 0.15 * base_premium if global_cover else 0
    final_premium = premium_after_term + global_cover_addon

    gst = final_premium * 0.18
    total = final_premium + gst

    breakdown = {
        "Base Premium": base_premium,
        f"Term Discount ({term} year)": -base_premium * discount,
        "Global Cover Add-On": global_cover_addon,
        "Premium Before GST": final_premium,
        "GST (18%)": gst,
        "Total Premium": total
    }

    return None, breakdown

def run_calculator():
    st.title("TATA AIG Super Top-Up Premium Calculator")

    age = st.selectbox("Select Age Band", options=[
        '18-35', '36-45', '46-50', '51-55', '56-60', '61-65', '66-70', '71-75'
    ])
    deductible = st.selectbox("Select Deductible", options=[
        300000, 500000, 1000000
    ])
    sum_insured = st.selectbox("Select Sum Insured", options=[
        500000, 1000000, 2000000
    ])
    term = st.selectbox("Policy Term (Years)", options=[1, 2, 3])
    global_cover = st.checkbox("Add Global Cover?")

    if st.button("Calculate Premium"):
        error, result = calculate_premium(age, deductible, sum_insured, term, global_cover)

        if error:
            st.error(error)
        else:
            st.success("Premium Breakdown")
            for label, amount in result.items():
                st.write(f"**{label}:** ₹{amount:,.2f}")

if __name__ == "__main__":
    run_calculator()
