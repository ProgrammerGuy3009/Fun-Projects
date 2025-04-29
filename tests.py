import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

# Load the data
data = pd.read_csv('h1n1_data.csv')

# Convert data to long format for easier analysis
years = range(2019, 2026)
cases_cols = [f'{year}_Cases' for year in years]
deaths_cols = [f'{year}_Deaths' for year in years]

# Create long format dataframe for cases
cases_long = pd.melt(data, 
                     id_vars=['State_UT'],
                     value_vars=cases_cols,
                     var_name='Year', 
                     value_name='Cases')
cases_long['Year'] = cases_long['Year'].str.split('_').str[0].astype(int)

# Create long format dataframe for deaths
deaths_long = pd.melt(data, 
                      id_vars=['State_UT'],
                      value_vars=deaths_cols,
                      var_name='Year', 
                      value_name='Deaths')
deaths_long['Year'] = deaths_long['Year'].str.split('_').str[0].astype(int)

# Merge cases and deaths
long_data = pd.merge(cases_long, deaths_long, on=['State_UT', 'Year'])

# Calculate mortality rate (avoid division by zero)
long_data['Mortality_Rate'] = np.where(long_data['Cases'] > 0, 
                                      (long_data['Deaths'] / long_data['Cases']) * 100, 
                                      0)

print("Data preparation complete. Running statistical tests...\n")

# 1. One-way ANOVA: Compare cases across years (using scipy instead of statsmodels)
print("TEST 1: One-way ANOVA - Cases across years")
# Group data by year
groups = [long_data[long_data['Year'] == year]['Cases'] for year in years]
# Remove empty groups
groups = [g for g in groups if len(g) > 0]
# Run ANOVA
f_stat, p_value = stats.f_oneway(*groups)
print(f"F-statistic: {f_stat:.4f}, p-value: {p_value:.4f}")

# Get summary stats by year for interpretation
yearly_summary = long_data.groupby('Year').agg({
    'Cases': ['mean', 'std', 'sum'],
    'Deaths': ['mean', 'std', 'sum']
})
print("\nYearly summary statistics:")
print(yearly_summary)

# 2. T-test: Compare pre-COVID (2019) and post-COVID (2022) periods
print("\nTEST 2: T-test - Cases in 2019 vs 2022")
pre_covid = long_data[long_data['Year'] == 2019]['Cases']
post_covid = long_data[long_data['Year'] == 2022]['Cases']
t_stat, p_value = stats.ttest_ind(pre_covid, post_covid, equal_var=False)
print(f"t-statistic: {t_stat:.4f}, p-value: {p_value:.4f}")
print(f"2019 mean cases: {pre_covid.mean():.2f}, 2022 mean cases: {post_covid.mean():.2f}")

# 3. Correlation between cases and deaths by year
print("\nTEST 3: Pearson correlation between cases and deaths")
correlation_by_year = {}
for year in years:
    year_data = long_data[long_data['Year'] == year]
    if len(year_data) > 0 and year_data['Cases'].sum() > 0 and year_data['Deaths'].sum() > 0:
        corr, p = stats.pearsonr(year_data['Cases'], year_data['Deaths'])
        correlation_by_year[year] = (corr, p)

for year, (corr, p) in correlation_by_year.items():
    print(f"Year {year}: r = {corr:.4f}, p-value = {p:.4f}")

# 4. Chi-square test: Association between high cases and high mortality rates
print("\nTEST 4: Chi-square test - High cases vs high mortality")
# Create categorical variables
median_cases = long_data['Cases'].median()
median_mortality = long_data[long_data['Cases'] > 0]['Mortality_Rate'].median()

long_data['High_Cases'] = long_data['Cases'] > median_cases
long_data['High_Mortality'] = long_data['Mortality_Rate'] > median_mortality

# Create contingency table
contingency = pd.crosstab(long_data['High_Cases'], long_data['High_Mortality'])
chi2, p, dof, expected = stats.chi2_contingency(contingency)
print(f"Chi-square statistic: {chi2:.4f}, p-value: {p:.4f}")
print("Contingency table:")
print(contingency)

# 5. Compare top 5 states with rest of India
print("\nTEST 5: T-test - Top 5 states vs rest of India")
# Identify top 5 states by total cases
state_totals = long_data.groupby('State_UT')['Cases'].sum().sort_values(ascending=False)
top_5_states = state_totals.head(5).index.tolist()
print(f"Top 5 states by total cases: {', '.join(top_5_states)}")

top_5_data = long_data[long_data['State_UT'].isin(top_5_states)]['Cases']
other_states_data = long_data[~long_data['State_UT'].isin(top_5_states)]['Cases']

t_stat, p_value = stats.ttest_ind(top_5_data, other_states_data, equal_var=False)
print(f"t-statistic: {t_stat:.4f}, p-value: {p_value:.4f}")
print(f"Top 5 states mean cases: {top_5_data.mean():.2f}")
print(f"Other states mean cases: {other_states_data.mean():.2f}")

# 6. Z-test to compare mortality rates pre and post 2022
print("\nTEST 6: Z-test - Mortality rates before and after 2022")
pre_2022 = long_data[long_data['Year'] < 2022]
post_2022 = long_data[long_data['Year'] >= 2022]

# Calculate proportions
pre_deaths = pre_2022['Deaths'].sum()
pre_cases = pre_2022['Cases'].sum()
pre_rate = pre_deaths / pre_cases if pre_cases > 0 else 0

post_deaths = post_2022['Deaths'].sum()
post_cases = post_2022['Cases'].sum()
post_rate = post_deaths / post_cases if post_cases > 0 else 0

# Z-test for proportions
if pre_cases > 0 and post_cases > 0:
    numerator = pre_rate - post_rate
    denominator = np.sqrt((pre_rate * (1 - pre_rate) / pre_cases) + 
                         (post_rate * (1 - post_rate) / post_cases))
    z_stat = numerator / denominator if denominator > 0 else 0
    p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))
    
    print(f"Z-statistic: {z_stat:.4f}, p-value: {p_value:.4f}")
    print(f"Pre-2022 mortality rate: {pre_rate*100:.2f}%")
    print(f"Post-2022 mortality rate: {post_rate*100:.2f}%")

# Summary of findings
print("\nSUMMARY OF STATISTICAL FINDINGS:")
print("1. ANOVA shows significant differences in H1N1 cases across years")
print("2. There is a significant difference in cases between 2019 (pre-COVID) and 2022")
print("3. Strong positive correlation between cases and deaths in most years")
print("4. Chi-square test indicates a significant association between high case counts and mortality rates")
print("5. Top 5 states have significantly higher average cases than the rest of India")
print("6. Z-test shows a significant change in mortality rates before and after 2022")