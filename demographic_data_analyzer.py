import pandas as pd

def calculate_demographic_data(print_data=True):
    # Read data from file
    df = pd.read_csv('adult.data.csv')
    
    # How many of each race are represented in this dataset?
    race_count = df['race'].value_counts()

    # What is the average age of men?
    average_age_men = round(df[df['sex'] == 'Male']['age'].mean(), 1)  # Round to the nearest tenth

    # What is the percentage of people who have a Bachelor's degree?
    ed_count = df['education'].value_counts()
    percentage_bachelors = round((ed_count.get('Bachelors', 0) / df['education'].shape[0]) * 100, 1)  # Round to the nearest tenth

    # What percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
    advanced_education = ['Bachelors', 'Masters', 'Doctorate']
    hi_count = df[(df['education'].isin(advanced_education)) & (df['salary'] == '>50K')].shape[0]  
    
    # What percentage of people without advanced education make more than 50K?
    lo_count = df[(~df['education'].isin(advanced_education)) & (df['salary'] == '>50K')].shape[0]

    # with and without `Bachelors`, `Masters`, or `Doctorate`
    higher_education = df[(df['education'].isin(advanced_education))].shape[0]
    lower_education = df[(~df['education'].isin(advanced_education))].shape[0]

    # percentage with salary >50K
    higher_education_rich = round((hi_count / higher_education) * 100, 1)  # Round to the nearest tenth
    lower_education_rich = round((lo_count / lower_education) * 100, 1)  # Round to the nearest tenth

    # What is the minimum number of hours a person works per week?
    min_work_hours = df['hours-per-week'].min()

    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    num_min_workers = df[(df['hours-per-week'] == min_work_hours) & (df['salary'] == '>50K')].shape[0]
    rich_percentage = round((num_min_workers / df[(df['hours-per-week'] == min_work_hours)].shape[0]) * 100, 1)  # Round to the nearest tenth

    # What country has the highest percentage of people that earn >50K?
    country_salary_count = df.groupby('native-country')['salary'].value_counts(normalize=True).unstack(fill_value=0)
    highest_earning_country_percentage = country_salary_count['>50K'] * 100
    highest_earning_country = highest_earning_country_percentage.idxmax()  # Get country with highest percentage
    highest_earning_country_percentage = round(highest_earning_country_percentage.max(), 1)  # Round to the nearest tenth

    # Identify the most popular occupation for those who earn >50K in India.
    top_IN_occupation = df[(df['native-country'] == 'India') & (df['salary'] == '>50K')]['occupation'].mode()

    # DO NOT MODIFY BELOW THIS LINE

    if print_data:
        print("Number of each race:\n", race_count) 
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations in India:", top_IN_occupation.values)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage': highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation.values[0] if not top_IN_occupation.empty else None  # Get the most common occupation
    }

# Call the function to test it
calculate_demographic_data()
