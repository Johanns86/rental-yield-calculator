import streamlit as st

# Streamlit UI for the advanced rental yield calculator
def main():
    st.title("Advanced Rental Yield Calculator")

    st.header("Property & Income Details")
    purchase_price = st.number_input("Purchase Price ($)", min_value=0.0, step=1000.0)
    annual_rent = st.number_input("Annual Rental Income ($)", min_value=0.0, step=100.0)

    st.header("Optional Upfront Costs")
    stamp_duty = st.number_input("Stamp Duty ($)", min_value=0.0, step=100.0)
    legal_fees = st.number_input("Legal Fees ($)", min_value=0.0, step=100.0)

    st.header("Annual Running Costs")
    maintenance_costs = st.number_input("Maintenance Costs ($)", min_value=0.0, step=100.0)
    management_fees = st.number_input("Management Fees ($)", min_value=0.0, step=100.0)
    insurance_costs = st.number_input("Insurance Costs ($)", min_value=0.0, step=100.0)
    council_rates = st.number_input("Council Rates ($)", min_value=0.0, step=100.0)
    vacancy_rate = st.slider("Vacancy Rate (%)", 0.0, 100.0, 5.0)

    st.header("Mortgage Details (Optional)")
    include_mortgage = st.checkbox("Include Mortgage")
    mortgage_interest_rate = mortgage_term_years = loan_to_value_ratio = None

    if include_mortgage:
        mortgage_interest_rate = st.number_input("Mortgage Interest Rate (%)", min_value=0.0, max_value=100.0, step=0.1)
        mortgage_term_years = st.number_input("Mortgage Term (Years)", min_value=1, max_value=40, step=1)
        loan_to_value_ratio = st.number_input("Loan to Value Ratio (%)", min_value=0.0, max_value=100.0, step=1.0)

    if st.button("Calculate Yield"):
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

        st.subheader("Results")
        st.write(f"**Gross Rental Yield:** {results['Gross Yield (%)']}%")
        st.write(f"**Net Rental Yield:** {results['Net Yield (%)']}%")
        st.write(f"**Effective Annual Rent:** ${results['Annual Rent (after vacancy)']}")

        st.subheader("Annual Expenses Breakdown")
        for key, val in results['Annual Expenses'].items():
            st.write(f"{key}: ${val}")

        st.subheader("Upfront Costs")
        for key, val in results['Upfront Costs'].items():
            st.write(f"{key}: ${val}")

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

    total_annual_expenses = (
        maintenance_costs +
        management_fees +
        insurance_costs +
        council_rates
    )

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
