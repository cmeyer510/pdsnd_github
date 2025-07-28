#to execute, type ipython bikeshare.py in the terminal

#import packages
import time
import pandas as pd
import numpy as np


#establish data paths
CITY_DATA = { 
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv' 
}

#Add print divider function
def print_divider():
    print('-' * 40)

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: Get user input for city
    while True:
        city = input("Please enter a city to explore (Chicago, New York City, or Washington): ").strip().lower()
        if city in CITY_DATA:
            break
        else:
            print("Invalid input. Please choose from Chicago, New York City, or Washington.")

    # TO DO: Get user input for month
    while True:
        month = input("Please enter a month to explore (January to June) or 'all' for no filter: ").strip().lower()
        if month in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
            break
        else:
            print("Invalid input. Please choose a valid month (January to June) or 'all'.")

    # TO DO: Get user input for day of week
    while True:
        day = input("Please enter a day of the week to explore or 'all' for no filter: ").strip().lower()
        if day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday','sunday', 'all']:
            break
        else:
            print("Invalid input. Please choose a valid day of the week or 'all'.")

    print_divider()
    return city, month, day

# Show raw data if requested 
def display_raw_data(df):
    """Displays 5 rows of raw data at a time upon user request."""
    row_start = 0
    while True:
        show_data = input("Would you like to see 5 lines of raw data? (yes/no): ").strip().lower()
        if show_data != 'yes':
            break
        print(df.iloc[row_start:row_start + 5])
        row_start += 5
        if row_start >= len(df):
            print("No more data to display.")
            break

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable. 
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    
    df = pd.read_csv(CITY_DATA[city]) 
    df['Start Time'] = pd.to_datetime(df['Start Time'], errors='coerce')
    df['month'] = df['Start Time'].dt.month_name().str.lower()
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()

    # TO DO: Filter by month if applicable
    if month != 'all':
        df = df[df['month'] == month]

    # TO DO: Filter by day of week if applicable
    if day != 'all':
        df = df[df['day_of_week'] == day]
    return df

def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""
    
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

# TO DO: Display month
    if month == 'all':
        popular_month = df['month'].mode()[0]
        print("Most common month:", popular_month.title())
    else:
        print("Month selected:", month.title())

    # TO DO: Display day of week
    if day == 'all':
        popular_dow = df['day_of_week'].mode()[0]
        print("Most common day of week:", popular_dow.title())
    else:
        print("Day selected:", day.title())


    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print("Most common hour:", popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print_divider()
    
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print("Most common start station:", popular_start_station)
    # TO DO: display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print("Most common end station:", popular_end_station)

    # TO DO: display most frequent combination of start station and end station trip 
    df['trip'] = df['Start Station'] + " to " + df['End Station']
    popular_trip = df['trip'].mode()[0]
    print("Most frequent trip:", popular_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print_divider()
    
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_duration = df['Trip Duration'].sum()
    total_hours = int(total_duration // 3600)
    total_minutes = int((total_duration % 3600) // 60)
    total_seconds = int(total_duration % 60)
    print(f"Total trip duration for all users was: {total_hours:,}h {total_minutes}m {total_seconds}s")

    # TO DO: display mean travel time
    avg_duration = df['Trip Duration'].mean()
    avg_hours = int(avg_duration // 3600)
    avg_minutes = int((avg_duration % 3600) // 60)
    avg_seconds = int(avg_duration % 60)
    print(f"Average trip duration for all users was: {avg_hours}h {avg_minutes}m {avg_seconds}s")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print_divider()

def user_stats(df):
    """Displays user type and gender statistics on bikeshare users."""
    
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].fillna('Not Specified').value_counts()
    print('Count of Each User Type:')
    for user_type, count in user_types.items():
        print(f"{user_type}: {count:,}")       
    print()
    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].fillna('Not Specified').value_counts()
        print('Count of Each Gender:')
        for gender, count in gender_counts.items():
            print(f"{gender}: {count:,}")
    else:
        print("Gender data is not available in this dataset.")

    print()    
    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        birth_years = df['Birth Year'].dropna()

        if not birth_years.empty:
            min_year = int(birth_years.min())
            print('Earliest birth year:', min_year)

            max_year = int(birth_years.max())
            print('Most recent birth year:', max_year)

            common_year = int(birth_years.mode()[0])
            print('Most common birth year:', common_year)
        else:
            print("Birth year column exists but contains only missing values.")
    else:
        print("Birth year data is not available in this dataset.")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print_divider()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)    
        display_raw_data(df)
        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
