import streamlit as st
import pandas as pd

# Load Excel data (adjust the path accordingly)
@st.cache_data
def load_data():
    data = pd.read_excel(r'Tata Aig Premium_Data.xlsx', sheet_name='Premium_TATA')
    return data

# Function to calculate premium for each family member
def calculate_premium(age, deductible, sum_insured, term, pincode):
    data = load_data()
    
    # Get the base premium for the given age
    premium_row = data[data['Age Band'] == age]
    
    if premium_row.empty:
        return "Age not found in the data."
    
    base_premium = premium_row['Premium'].values[0]
    
    # Apply discounts and add-ons
    discount = 0.1  # Example discount logic (10% for this term)
    family_discount = 0.05  # Example family discount (5%)
    term_discount = base_premium * discount
    
    # Family size discount (add logic for family members)
    family_discount_value = base_premium * family_discount
    
    # Sum insured adjustments (example logic)
    sum_adjustment = (sum_insured - 500000) * 0.02  # Example adjustment logic for sum insured

    gst = 0.18  # 18% GST
    premium_with_gst = base_premium + term_discount + family_discount_value + sum_adjustment
    total_premium = premium_with_gst * (1 + gst)
    
    # Return the premium breakdown for this member
    breakdown = {
        "Base Premium": base_premium,
        "Term Discount": term_discount,
        "Family Discount": family_discount_value,
        "Sum Insured Adjustment": sum_adjustment,
        "GST": total_premium - premium_with_gst,
        "Total Premium": total_premium,
        "Pincode": pincode  # Just showing pincode in the breakdown for reference
    }

    return breakdown

# Function to run the calculator
def run_calculator():
    # Input Fields
    st.title("Tata AIG Premium Calculator")
    
    # Family Size input (1 to 6 members)
    family_size = st.slider("Select Family Size (Number of Members)", 1, 6, 1)
    
    pincode = st.text_input("Enter Pincode (for reference only):")
    
    # Loop to input age, deductible, sum insured for each family member
    family_premiums = []
    for i in range(family_size):
        st.subheader(f"Member {i+1}")
        
        age = st.number_input(f"Enter Age for Member {i+1}", min_value=0, max_value=100, step=1)
        deductible = st.number_input(f"Enter Deductible Amount for Member {i+1}", min_value=0, step=5000)
        sum_insured = st.number_input(f"Enter Sum Insured for Member {i+1}", min_value=100000, step=50000)
        term = st.selectbox(f"Select Policy Term (in years) for Member {i+1}", [1, 2, 3, 5])
        
        # Calculate premium for this member
        premium_breakdown = calculate_premium(age, deductible, sum_insured, term, pincode)
        
        # Store family member's premium breakdown
        family_premiums.append(premium_breakdown)

    # Display family premiums breakdown
    st.write("### Premium Breakdown for Family")
    for i, breakdown in enumerate(family_premiums):
        st.write(f"#### Member {i+1} Premium Breakdown")
        st.write(f"Base Premium: ₹{breakdown['Base Premium']}")
        st.write(f"Term Discount: ₹{breakdown['Term Discount']}")
        st.write(f"Family Discount: ₹{breakdown['Family Discount']}")
        st.write(f"Sum Insured Adjustment: ₹{breakdown['Sum Insured Adjustment']}")
        st.write(f"GST: ₹{breakdown['GST']}")
        st.write(f"Total Premium: ₹{breakdown['Total Premium']}")
        st.write(f"Pincode: {breakdown['Pincode']}")  # Display pincode for reference

if __name__ == "__main__":
    run_calculator()
