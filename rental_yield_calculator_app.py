import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Streamlit UI for the enhanced rental yield calculator
def main():
    st.set_page_config(page_title="Rental Yield Calculator", layout="centered")
    st.title("📊 Advanced Rental Yield Calculator")
    st.markdown("Use this tool to evaluate property returns, loan impacts, and overall investment performance.")

    with st.form("rental_form"):
        st.header("🏠 Property Details")
        purchase_price = st.number_input("Purchase Price ($)", min_value=0.0, step=1000.0, value=500000.0)
        annual_rent = st.number_input("Annual Rental Income ($)", min_value=0.0, step=100.0, value=26000.0)

        st.header("💰 Upfront & Annual Costs")
        stamp_duty = st.number_input("Stamp Duty ($)", min_value=0.0, step=100.0, value=18000.0)
        legal_fees = st.number_input("Legal Fees ($)", min_value=0.0, step=100.0, value=1500.0)
        maintenance_costs = st.number_input("Annual Maintenance ($)", min_value=0.0, step=100.0, value=1000.0)
        management_fees = st.number_input("Annual Management Fees ($)", min_value=0.0, step=100.0, value=2000.0)
        insurance_costs = st.number_input("Annual Insurance ($)", min_value=0.0, step=100.0, value=1200.0)
        council_rates = st.number_input("Council Rates ($)", min_value=0.0, step=100.0, value=1800.0)
        vacancy_rate = st.slider("Expected Vacancy Rate (%)", 0.0, 20.0, 5.0)

        st.header("🏦 Mortgage Details (Optional)")
        include_mortgage = st.checkbox("Include Mortgage")
        mortgage_interest_rate = mortgage_term_years = loan_to_value_ratio = None
        if include_mortgage:
            mortgage_interest_rate = st.number_input("Interest Rate (%)", min_value=0.0, max_value=100.0, step=0.1, value=6.0)
            mortgage_term_years = st.number_input("Term (Years)", min_value=1, max_value=40, step=1, value=30)
            loan_to_value_ratio = st.number_input("Loan to Value Ratio (%)", min_value=0.0, max_value=100.0, step=1.0, value=80.0)

        submitted = st.form_submit_button("Calculate")

    if submitted:
        results = calculate_rental_yield(
            purchase_price,
            annual_rent,
            include_mortgage=include_mortgage,
            mortgage_interest_rate=mortgage_interest_rate,
            mortgage_term_years=mortgage_term_years,
            loan_to_value_ratio=loan_to_value_ratio,
            stamp_duty=stamp_duty,
            legal_fees=legal_fees,
            maintenance_costs=maintenance_costs,
            management_fees=management_fees,
            insurance_costs=insurance_costs,
            council_rates=council_rates,
            vacancy_rate=vacancy_rate
        )

        st.header("📈 Results")
        st.metric("Gross Yield", f"{results['Gross Yield (%)']}%")
        st.metric("Net Yield", f"{results['Net Yield (%)']}%")
        st.metric("Annual Rent (After Vacancy)", f"${results['Annual Rent (after vacancy)']:,}")

        st.subheader("💸 Expense Breakdown")
        exp_data = results['Annual Expenses']
        exp_labels = list(exp_data.keys())[:-1]
        exp_values = [exp_data[k] for k in exp_labels]
        fig1, ax1 = plt.subplots()
        ax1.pie(exp_values, labels=exp_labels, autopct='%1.1f%%', startangle=90)
        ax1.axis('equal')
        st.pyplot(fig1)

        st.subheader("📊 10-Year Cash Flow Projection")
        df = pd.DataFrame({"Year": list(range(1, 11))})
        df["Rent"] = results['Annual Rent (after vacancy)'] * (1.03 ** df["Year"])  # assume 3% growth
        df["Expenses"] = exp_data['Total'] * (1.02 ** df["Year"])  # assume 2% cost inflation
        df["Cash Flow"] = df["Rent"] - df["Expenses"]

        st.line_chart(df.set_index("Year")[["Rent", "Expenses", "Cash Flow"]])

        st.subheader("📤 Download Report")
        st.download_button("Download CSV", df.to_csv(index=False).encode(), "cashflow_projection.csv")

def calculate_rental_yield(
    purchase_price,
    annual_rent,
    costs=None,
    include_mortgage=False,
    mortgage_interest_rate=None,
    mortgage_term_years=None,
    loan_to_value_ratio=None,
    stamp_duty=0,
    legal_fees=0,
    maintenance_costs=0,
    management_fees=0,
    insurance_costs=0,
    council_rates=0,
    vacancy_rate=0
):
    gross_yield = (annual_rent / purchase_price) * 100 if purchase_price else 0
    vacancy_loss = (vacancy_rate / 100) * annual_rent
    effective_rent = annual_rent - vacancy_loss

    total_annual_expenses = maintenance_costs + management_fees + insurance_costs + council_rates

    annual_mortgage_payment = 0
    if include_mortgage and mortgage_interest_rate and loan_to_value_ratio:
        loan_amount = (loan_to_value_ratio / 100) * purchase_price
        r = (mortgage_interest_rate / 100) / 12
        n = mortgage_term_years * 12
        monthly_payment = loan_amount * r * (1 + r)**n / ((1 + r)**n - 1)
        annual_mortgage_payment = monthly_payment * 12
        total_annual_expenses += annual_mortgage_payment

    upfront_costs = stamp_duty + legal_fees

    net_yield = ((effective_rent - total_annual_expenses) / (purchase_price + upfront_costs)) * 100 if purchase_price + upfront_costs else 0

    return {
        "Gross Yield (%)": round(gross_yield, 2),
        "Net Yield (%)": round(net_yield, 2),
        "Annual Rent (after vacancy)": round(effective_rent, 2),
        "Annual Expenses": {
            "Maintenance": maintenance_costs,
            "Management Fees": management_fees,
            "Insurance": insurance_costs,
            "Council Rates": council_rates,
            "Mortgage (if any)": round(annual_mortgage_payment, 2),
            "Total": round(total_annual_expenses, 2)
        },
        "Upfront Costs": {
            "Stamp Duty": stamp_duty,
            "Legal Fees": legal_fees,
            "Total": stamp_duty + legal_fees
        }
    }

if __name__ == "__main__":
    main()
