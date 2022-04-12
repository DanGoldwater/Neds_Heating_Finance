#%%
import seaborn
from dataclasses import dataclass
import numpy_financial as npf
import numpy as np
import pandas as pd

seaborn.set(rc = {'figure.figsize':(15,8)})
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
    hot_water_need: int
    
    def __post_init__(self) -> None:
        self.total_need = self.hot_water_need + self.heating_need
        pass
    
    def monthly_loan_payment(self):
        int_per_month = self.rate / (100 * 12)
        return - npf.pmt(int_per_month, 12 * self.loan_years, self.loan_amount)

    def monthly_heat_source_bill(self):
        COP_air_source = 3.4
        return (self.total_need / (12 *  COP_air_source)) * self.electricity_price

    def monthly_ordinary_heating_bill(self):
        night_to_day_use_ratio = 2
        night_to_day_price_ratio = 2/3
        night_price = night_to_day_price_ratio * self.electricity_price
        night_use = (night_to_day_use_ratio / (night_to_day_use_ratio + 1)) * self.heating_need
        day_use = self.heating_need - night_use
        day_cost = (day_use + self.hot_water_need) * self.electricity_price
        night_cost = night_use * night_price
        return (day_cost + night_cost) / 12

    def monthly_air_total(self):
        return self.monthly_loan_payment() + self.monthly_heat_source_bill()

    def give_summary(self):
        print(f'Monthly loan payments would be £{self.monthly_loan_payment():.2f} ')
        print(f'Monthly heating bill would be £{self.monthly_heat_source_bill():.2f} ')
        print(f'Monthly total bill would be {self.monthly_air_total():.2f}')
        print(f'\n Or, with just electric heating:')
        print(f'Monthly heating bill would be £{self.monthly_ordinary_heating_bill():.2f} ')
    
def make_changing_electric_price_data(scenario, e_min = .1, e_max = .7):
    e_range = np.arange(e_min, e_max, .01)
    air_source_payments = []
    ordinary_payments = []
    for e in e_range:
        scenario.electricity_price = e
        air_source_payments += [scenario.monthly_air_total()]
        ordinary_payments += [scenario.monthly_ordinary_heating_bill()]
    df = pd.DataFrame({
        'electricity': e_range,
        'Ordinary Price': ordinary_payments,
        'Air Source': air_source_payments
    }) 
    return df


def make_scenario_electricity_plot(scenario):
    df = make_changing_electric_price_data(scenario)
    dfm = df.melt('electricity', var_name='Energy Type', value_name='Price')
    plot_here = seaborn.lineplot(data=dfm, x='electricity', y='Price', hue='Energy Type')
    plot_here.set_xlabel('Price per kWh (£)')
    plot_here.set_ylabel('Price per month')
    return plot_here

def find_crossing_price(scenario):
    df = make_changing_electric_price_data(scenario)
    df2 = df.loc[df['Ordinary Price'] > df['Air Source']]
    return df2['electricity'].min()


def estimate_load():
    Nc = 15_000
    Lc = 27_000
    Lp = 17_000
    Nw = 3_500
    K = 1.4
    return (Nc * K * (Lp / Lc)) + Nw


# print(estimate_load())


# Neds_current_low_heat = scenario(**{
#     'loan_years': 20,
#     'rate': 5,
#     'loan_amount': 40_000,
#     'heating_need': 15_000,
#     'hot_water_need': 3500,
#     'electricity_price': .2,
#  })

    

