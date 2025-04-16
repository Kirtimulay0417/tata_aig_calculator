import streamlit as st
import pandas as pd

# Load data from Excel
@st.cache
def load_data():
    data = pd.read_excel(r'Tata Aig Premium_Data.xlsx', sheet_name='Premium_TATA')
    return data

# Function to get the age band based on the provided age
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

# Function to get premium from the data table
def get_premium(age_band, deductible, sum_insured, data):
    premium_data = data[(data['Age Band'] == age_band) & (data['Deductible'] == deductible) & (data['Sum Insured'] == sum_insured)]
    if not premium_data.empty:
        return premium_data['Premium'].values[0]
    return 0

# Main function to run the calculator
def run_calculator():
    # Load data
    data = load_data()

    st.title("TATA AIG Premium Calculator")

    # Input fields
    family_size = st.number_input("Family Size (Number of members)", min_value=1, max_value=10, step=1)
    age_input = st.text_input("Enter ages of family members (comma separated)", "25,30")
    deductible = st.number_input("Enter Deductible Amount", min_value=0, step=1000)
    sum_insured = st.number_input("Enter Sum Insured", min_value=0, step=10000)
    policy_term = st.selectbox("Select Policy Term", [1, 2, 3])
    global_cover = st.selectbox("Global Cover (Yes/No)", ["Yes", "No"])

    # Convert age input to list
    age_arr = [int(age.strip()) for age in age_input.split(",")]

    if st.button("Calculate Premium"):
        total_base_premium = 0
        family_discount_pct = 0
        total_members = len(age_arr)

        # Calculate Family Discount
        if total_members == 2:
            family_discount_pct = 0.2
        elif total_members == 3:
            family_discount_pct = 0.28
        elif total_members >= 4:
            family_discount_pct = 0.32

        # Calculate Term Discount
        term_discount_pct = 0
        if policy_term == 2:
            term_discount_pct = 0.05
        elif policy_term == 3:
            term_discount_pct = 0.1

        # Calculate Global Cover Add-on
        global_add_pct = 0.1 if global_cover == "Yes" else 0

        premium_breakdown = []

        # Loop through each family member
        for age in age_arr:
            age_band = get_age_band(age)
            base_premium = get_premium(age_band, deductible, sum_insured, data)

            if base_premium == 0:
                st.warning(f"Premium not found for Age Band {age_band} with Deductible {deductible} and Sum Insured {sum_insured}")
                continue

            # Calculate discounted premium
            discounted_premium = base_premium * (1 - family_discount_pct) * (1 - term_discount_pct) * (1 + global_add_pct)
            gst_amount = discounted_premium * 0.18
            final_premium = discounted_premium + gst_amount

            # Add to total base premium
            total_base_premium += discounted_premium

            # Save breakdown for display
            premium_breakdown.append({
                "Age": age,
                "Age Band": age_band,
                "Deductible": deductible,
                "Sum Insured": sum_insured,
                "Base Premium": base_premium,
                "Family Discount %": family_discount_pct * 100,
                "GST": gst_amount,
                "Final Premium": final_premium
            })

        # Display premium breakdown
        st.write("Premium Breakdown:")
        st.write(pd.DataFrame(premium_breakdown))

        # Final Premium calculation
        final_premium = total_base_premium * 1.18
        st.write(f"Total Base Premium (Excl. GST): {total_base_premium:.2f}")
        st.write(f"Final Premium (Incl. GST): {final_premium:.2f}")

# Run the calculator
if __name__ == "__main__":
    run_calculator()
