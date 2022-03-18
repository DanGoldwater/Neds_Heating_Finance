#%%
from dataclasses import dataclass
import numpy_financial as npf

mortgage_1 = {
    'loan_years': 30,
    'rate': 6,
    'loan': 50000
}

@dataclass
class scenario:
    loan_years: int
    rate: int
    loan_amount: int
    electricity_price: float
    heating_need: int
    
    def monthly_loan_payment(self):
        int_per_month = self.rate / (100 * 12)
        return - npf.pmt(int_per_month, 12 * self.loan_years, self.loan_amount)

    def monthly_heat_source_bill(self):
        COP_air_source = 3.4
        return (self.heating_need / COP_air_source) * self.electricity_price

    def monthly_ordinary_heating_bill(self):
        return self.heating_need * self.electricity_price 

    def monthly_air_total(self):
        return self.monthly_loan_payment() + self.monthly_heat_source_bill()

    def give_summary(self):
        print(f'Monthly loan payments would be £{self.monthly_loan_payment() } ')
        print(f'Monthly heating bill would be £{self.monthly_heat_source_bill()} ')
        print(f'Monthly total bill would be {self.monthly_air_total()}')
        print(f'\n Or, with just electric heating:')
        print(f'Monthly heating bill would be £{self.monthly_ordinary_heating_bill() } ')
    



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
    

scen_1 = {
    'loan_years': 25,
    'rate': 6,
    'loan_amount': 40_000,
    'electricity_price': .3,
    'heating_need': 25000
}
    
scennn_1 = scenario(**scen_1) 
scennn_1.give_summary()
    

