import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze from the CITY DATA variable.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    cities = ['chicago', 'new york city', 'washington']
    city = input('Please enter a valid city from chicago, new york city, washington: ').lower()
    while city not in cities:
        print('Sorry, invalid input')
        city = input('Please enter a valid city from chicago, new york city, washington: ').lower()
    # TO DO: get user input for month (all, january, february, ... , june)
    months =['january', 'february', 'march', 'april', 'may', 'june', 'all']
    month = input('Please enter a valid month from: january to june or type "all" for no filter: ').lower()
    while month not in months:
        print('Sorry, invalid input')
        month = input('Please enter a valid month from january to june or type "all" for no filter: ').lower()
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    day = input('Please enter a valid day from monday to sunday or type "all" for no filter: ').lower()
    while day not in days:
        print('Sorry, invalid input')
        day = input('Please enter a valid day from monday to sunday or type "all" for no filter: ').lower()
    print('-'*40)
    return city, month, day


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
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    if month != 'all':
        months =['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1
        df = df[df['month'] == month]
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    return df

def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    if month != 'all':
        popular_month = month
        print('Most popular month: You filtered on', month.title(), 'so this is the only month!')
    else:
        popular_month = df['month'].mode()[0]
        print('Most popular month:', popular_month)
        
    # TO DO: display the most common day of week
    if day != 'all':
        popular_day_of_week = day
        print('Most popular day of the week: You filtered on', day.title(), 'so this is the only day!')
    else:
        popular_day_of_week = df['day_of_week'].mode()[0]
        print('Most popular day of the week:', popular_day_of_week)
    
    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_start_hour = df['hour'].mode()[0]
    print('Most popular start hour:', popular_start_hour)
    
    print("\nThis took {0:.3f} seconds.".format(time.time() - start_time))
    print('-'*40)
    return popular_month, popular_day_of_week, popular_start_hour
    
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most popular start station:', popular_start_station)

    # TO DO: display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most popular end station:', popular_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    Start_End_Station_Combination = df.groupby(['Start Station', 'End Station']).size().nlargest(1)
    print('\nMost popular Start End Station combination:')
    print(Start_End_Station_Combination)

    print("\nThis took {0:.3f} seconds.".format(time.time() - start_time))
    print('-'*40)
    return popular_start_station, popular_end_station, Start_End_Station_Combination

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    
    # TO DO: display total travel time
    Total_travel_time_days = df['Trip Duration'].sum()/60/60/24
    print('Total travel time is {0:.0f} days.'.format(Total_travel_time_days))

    # TO DO: display mean travel time
    Mean_travel_time_mins = df['Trip Duration'].mean()/60
    print('Mean travel time is {0:.0f} minutes'.format(Mean_travel_time_mins))

    print("\nThis took {0:.3f} seconds.".format(time.time() - start_time))
    print('-'*40)
    return Total_travel_time_days, Mean_travel_time_mins

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    Counts_of_user_types = df['User Type'].value_counts()
    print('The number of user types is:')
    print(Counts_of_user_types)

    # TO DO: Display counts of gender
    if 'Gender' not in df.columns:
        print("\nThere is no gender column in this dataset")
    else:
        Counts_of_gender = df['Gender'].value_counts()
        print('\nThe number of gender types is:')
        print(Counts_of_gender)

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' not in df.columns:
        print("\nThere is no birth year column in this dataset")
        print('-'*40)
    else:
        Earliest_birth_year = df['Birth Year'].min()
        print('\nThe earliest birth year is {0:.0f}'.format(Earliest_birth_year))
        Mostrecent_birth_year = df['Birth Year'].max()
        print('The most recent birth year is {0:.0f}'.format(Mostrecent_birth_year))
        Most_common_birth_year = df['Birth Year'].mode()[0]
        print('The common birth year is {0:.0f}'.format(Most_common_birth_year))
        print("\nThis took {0:.3f} seconds.".format(time.time() - start_time))
        print('-'*40)

def display_data(df):
    view_data = input("Would you like to view 5 rows of individual trip data? Enter yes or no?")
    start_loc = 0
    while True:
        print(df.iloc[start_loc:start_loc+5])
        start_loc += 5
        view_display = input("Do you wish to continue?: ").lower()
        if view_display.lower() != 'yes':
            break
        
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
