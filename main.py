#%%
import numpy_financial as npf

mortgage_1 = {
    'loan_years': 30,
    'rate': 6,
    'loan': 50000
}




def monthly_loan_payment(loan_years, loan_amount, rate, **_):
    int_per_month = rate / (100 * 12)
    return - npf.pmt(int_per_month, 12 * loan_years, loan_amount)

def monthly_heat_source_bill(heating_need, electricity_price, **_):
    COP_air_source = 3.4
    return (heating_need / COP_air_source) * electricity_price

def monthly_ordinary_heating_bill(heating_need, electricity_price, **_):
    return heating_need * electricity_price 

def give_summary(scenario):
    monthly_loan = monthly_loan_payment(**scenario)
    monthly_air_bill = monthly_heat_source_bill(**scenario)
    ordinary_bill = monthly_ordinary_heating_bill(**scenario)
    print(f'Monthly loan payments would be £{monthly_loan} ')
    print(f'Monthly heating bill would be £{monthly_air_bill} ')
    print(f'Monthly total bill would be {monthly_loan + monthly_air_bill}')
    print(f'\n Or, with just electric heating:')
    print(f'Monthly heating bill would be £{ordinary_bill} ')
    

    
  

    

