import datetime
import pandas as pd
import numpy as np

CITY_DATA = { 'Chicago': 'chicago.csv',
              'NewYork': 'new_york_city.csv',
              'Washington': 'washington.csv' }
print('Hello! Let\'s explore some US bikeshare data!')

#Defining a function below to get input for City, Month and Day from the User

def get_filters():
    cities=["Chicago","NewYork","Washington"]
    while True:
        try:    #using try block to tackle excptions and errors
            names=int(input('Please select city.\n Type 0 for Chicago, 1 for NewYork and 2 for Washington\n\n'))
            city=cities[names]
        except:
            print("Invalid Entry, Please try again")
            continue

        print("Looks like you selected {}".format(city))

        decision=input('Are you sure?  Y/N: ')  #Confirming uer input
        if decision=="Y":
            print("Great, lets move on")
            break
        elif decision=="N":
            continue
        else:
            print("Invalid Entry. Please use capital letters only")
            continue

#After City, now asking user input for desired month

    list_month=["All","January","February","March","April","May","June"]
    while True:
        try:    #using try block to tackle excptions and errors
            mons=int(input('Please choose the month or all from the options\n0 -All, 1 -January, 2 -February,3 -March, 4 -April, 5 -May and 6 -June\n'))
            month=list_month[mons]
        except:
            print("Invalid Entry, Please try again")
            continue

        print("Great! you have selected {} and {}".format(city,month))

        decision1=input('Are you sure?  Y/N: ')
        if decision1=="Y":  #Confirming uer input
            print("Great, lets move on")
            break
        elif decision1=="N":
            continue
        else:
            print("Invalid Entry. Please use capital letters only")
            continue

#Finally asking user for day of the week

    list_week=["All","Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
    while True:
        try:    #using try block to tackle excptions and errors
            week=int(input('Choose your day to view info\n 0 for all, 1 for Sunday, 2 for Monday, ... and 7 for Saturday\n'))
            day=list_week[week]
        except:
            print("Invalid Entry, Please try again")
            continue
        print("Great! you have selected {} to be viewed for the month of {}\n and all its {}s".format(city,month,day))
        break
    print('-'*40)
    return city, month, day


#Defining a function below to load the data acquired from user in the above function


def load_data(city, month, day):
    df=pd.read_csv(CITY_DATA[city]) #Using the dictionary defined in the begining of the code in line 5

    df['Start Time']=pd.to_datetime(df['Start Time'])   #Convert dtype of the column

    df['End Time'] =pd.to_datetime(df['End Time'])

    df['month']=df['Start Time'].dt.month   #Adding month column from Start Time

    df['Day_of_Week']=df['Start Time'].dt.weekday_name  #Adding Day_of_Week column

    if month!="All":    #filtering month data
        months = ["January","February","March","April","May","June"]
        month = months.index(month) + 1     #adding plus 1 since in pd library January =1 and December =12
        df=df[df['month']==month]

    if day!="All":
        df=df[df['Day_of_Week']==day.title()]
    return df

#Calculation Station statistics in below function


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')

    start=df['Start Station'].mode()[0]     #Calculating most frequ used Start Station and End Station in these two lines of code

    end=df['End Station'].mode()[0]

    df['new']=df['Start Station'] + ";" + df['End Station']

    value=df['new'].mode()[0]

    print("{} is the most frequenty used Start Station, where as {} is the most frequently used End Station \n furthermore, {} are the most frequently used start-end combination".format(start,end,value))

    print('-'*40)


#Calculation of Trip Duration in below function

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')

    df['End Time'] =pd.to_datetime(df['End Time'])

    df['Min2']=df['Start Time'].dt.minute   #Creating minutes column from Start Time

    df['Min1']=df['End Time'].dt.minute     #Creating minutes column from End Time

    df['travel']=df['Min1']-df['Min2']

    df['travel']=pd.to_datetime(df['travel'])   #Converting dtype of Travel column

    df['mins']=df['travel'].dt.minute

    max=df['mins'].max()
    avg=df['mins'].mean()
    mean1=round(avg,2)


    print('-'*40)
    print("Maximum time taken is {} minutes, and average is {} minutes.".format(max,mean1))
    print('-'*40)

#Calculating user Stats in below function

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')

    series=df['User Type'].value_counts()
    print("The distribution of user types is given below\n{}".format(series))   #Distribution of users


    try:    #Gender info not available for Washington city therefore adding try and exceot bloack
        series1=df.groupby(['Gender'])['Gender'].count()
    except KeyError:
        print("Gender data was not availabe for the city of Washington")


    try:    #Birth year info not available for Washington city therefore adding try and exceot bloack
        freq=df['Birth Year'].mode()[0]
        old=df['Birth Year'].min()
        new=df['Birth Year'].max()
        year=datetime.datetime.now().year
        oldest=year-old     #Age of oldest user
        youngest=year-new   #Age of youngest user
        common=year-freq

        print("Below is the distribution of gender\n{}.".format(series1))
        print("Oldest user is {} years of age.\n".format(oldest))
        print("Youngest user is {} years of age.\n".format(youngest))
        print("Most uers are {} years old.".format(common))
    except:
            print("Birth Year information was not available for the city of Washington")

    print('-'*40)
def data_view(df): #Used to show a part of data  to the user
    view_data=input('\n Would you like to view 5 rows of individual trip data? (Y/N)')
    start_loc=0
    while view_data=='Y': #So long as the uer says yes, this loop will not terminate
        print(df.iloc[start_loc:start_loc+5])   #This will keep incrementing the values by 5
        start_loc+=5
        view_display=input('Do you wish to continue? (Y/N):  ')
        if view_display=='Y':
            continue
        else:
            break
    print('-'*40)

#Defining main funcion below to call all other functions

def main():

    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        data_view(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')


        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
