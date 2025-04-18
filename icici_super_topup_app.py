import streamlit as st
import pandas as pd

# Load data from Excel
@st.cache_data
def load_data():
    df = pd.read_excel("Premium_ICICI.xlsx", sheet_name="Premium_ICICI")
    return df

# Get Age Band
def get_age_band(age):
    if 0 <= age <= 18:
        return "0-18"
    elif 19 <= age <= 35:
        return "19-35"
    elif 36 <= age <= 45:
        return "36-45"
    elif 46 <= age <= 50:
        return "46-50"
    elif 51 <= age <= 55:
        return "51-55"
    elif 56 <= age <= 60:
        return "56-60"
    elif 61 <= age <= 65:
        return "61-65"
    elif 66 <= age <= 70:
        return "66-70"
    else:
        return "71-99"

# Get Premium from table
def get_premium(df, age_band, plan, deductible, sum_insured):
    filtered = df[
        (df['Age Band'] == age_band) &
        (df['Plan'].str.upper() == plan.upper()) &
        (df['Deductible'] == deductible) &
        (df['Sum Insured'] == sum_insured)
    ]
    if not filtered.empty:
        return filtered['Premium'].values[0]
    return 0

# Main Streamlit App
def run_icici_calculator():
    st.title("ICICI Super Top-Up Premium Calculator")

    df = load_data()

    # User Inputs
   family_size = st.number_input("Family Size (Number of members)", min_value=1, max_value=10, step=1)
    age_input = st.text_input("Enter Ages (comma-separated)", "25,30")
    deductible = st.number_input("Enter Deductible Amount", min_value=0, step=10000)
    sum_insured = st.number_input("Enter Sum Insured", min_value=0, step=100000)
    plan = st.selectbox("Select Plan", ["A", "B"])

    age_list = [int(a.strip()) for a in age_input.split(",") if a.strip().isdigit()]

    if st.button("Calculate Premium"):
        total_base = 0
        breakdown = []

        for age in age_list:
            if age <= 0 or age > 120:
                continue

            age_band = get_age_band(age)
            base_premium = get_premium(df, age_band, plan, deductible, sum_insured)
            gst = base_premium * 0.18
            final = base_premium + gst
            total_base += base_premium

            breakdown.append({
                "Age": age,
                "Age Band": age_band,
                "Plan": plan.upper(),
                "Deductible": deductible,
                "Sum Insured": sum_insured,
                "Base Premium": round(base_premium, 2),
                "GST": round(gst, 2),
                "Final Premium": round(final, 2)
            })

        st.subheader("Premium Breakdown")
        st.dataframe(pd.DataFrame(breakdown))

        st.subheader("Total")
        st.write(f"**Base Premium (Excl. GST): ₹{round(total_base, 2)}**")
        st.write(f"**Final Premium (Incl. GST): ₹{round(total_base * 1.18, 2)}**")

# Run
if __name__ == "__main__":
    run_icici_calculator()
