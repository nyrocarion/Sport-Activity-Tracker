import datetime
import json
import pandas

import matplotlib.pyplot as plt
import numpy as np

import matplotlib
import matplotlib as mpl
from matplotlib.colors import ListedColormap

class SportActivityManager(object):
    def __init__(self):
        '''
        Loads the existing json file or creates an initial empty file
        '''
        try:
            with open("sport_activity_data.json", "r") as file:
                self.activity_data = json.load(file)
        except:
            with open("sport_activity_data.json", "w") as file:
                file.close() 
                self.activity_data = dict()
        self.text_to_value_mapping = {
            "restday" : 
                {
                    "numeric_value" : 1,
                },
            "workout" : 
                {
                    "numeric_value" : 2,
                },
            "running" :
                {
                    "numeric_value" : 3,
                },
            "hiking" :
                {
                    "numeric_value" : 4,
                } 
        }
        self.num_to_display_mapping = {
            "1" : "RE",
            "2" : "WO",
            "3" : "RU",
            "4" : "HI"
        }
        

    def create_entry(self,default_date=""):
        '''
        Create a new entry over console input and safe it into the json file
        '''
        #print("Enter a date for the activity (leave empty if its for today)")
        #print("Enter activity type (workout (w), running (l) or restday (r))")
        #print("Enter any additional details (distance, workout name, etc.)\n")
        if default_date == "":
            date = input("Enter date (yyyy-mm-dd): ")
            if len(date) == 0:
                date = default_date
        else:
            date = default_date
            print(f"Date: {default_date}")
        type = input("Enter type: ")
        if len(type) == 1:
            type = {"w" : "workout", "l": "running", "r": "restday", "h": "hiking"}[type]
        details = input("Enter additional details: ")
        entry = {
            date: {
                "activity_type" : type,
                "activity_details" : details
            }
        }
        '''
        This is how one JSON entry should look like
        {
            "2025-10-24": {
                "activity_type" : "workout, running, restday",
                "activity_details" : "km / workout name"
            }
        }
        '''
        self.activity_data.update(entry)
        self.save_activity_date(entry)

    def save_activity_date(self,entry):
        with open("sport_activity_data.json", "w") as file:
            json.dump(self.activity_data,file,indent=4)

    def create_heatmap(self,start_date,end_date):
        date_range = pandas.date_range(start=start_date,end=end_date)

        calendar_weeks = list()
        weekdays = [1,2,3,4,5,6,7]
        data = []
        row_data = [0,0,0,0,0,0,0]

        for date in date_range:
            date = str(date)[:10]
            datetime_object = datetime.datetime.strptime(date, '%Y-%m-%d').date()
            calendar_week = datetime_object.isocalendar().week
            if calendar_week not in calendar_weeks:
                calendar_weeks.append(calendar_week)

            val = self.text_to_value_mapping[self.activity_data[date]["activity_type"]]["numeric_value"] 

            weekday = datetime_object.isocalendar().weekday # 7 is sunday!
            row_data[weekday-1] = val
            if weekday == 7 or date == end_date:
                data.append(row_data)
                row_data = [0,0,0,0,0,0,0]

        print(data)

        test = np.array(data)
    
        cmap = ListedColormap(["white", "gold", "lawngreen", "lightseagreen", "magenta"])

        fig, ax = plt.subplots()
        im = ax.imshow(test,cmap)

        # Set calendar week and weekday ticks
        ax.set_xticks(range(len(weekdays)), labels=weekdays)
        plt.xlabel("Weekdays")
        ax.set_yticks(range(len(calendar_weeks)), labels=calendar_weeks)
        plt.ylabel("Calendar week")

        for i in range(len(calendar_weeks)):
            for j in range(len(weekdays)):
                try:
                    text = self.num_to_display_mapping[str(test[i,j])]
                except:
                    text = ""
                text = ax.text(j, i, text, ha="center", va="center", color="w")

        ax.set_title(f"Sport Activity Data from {start_date} to {end_date}")
        plt.show()

        

if __name__ == "__main__":
    s = SportActivityManager()
    user_input = ""
    while user_input == "":
        user_input = input("Generate activiy map (M) or enter data (D)? ")
        if user_input == "D":
            s.create_entry()
        elif user_input == "M":
            print("Please specify the start and end date for the activity map!")
            start = input("Start date (yyyy-mm-dd): ")
            end = input("End date (yyyy-mm-dd): ")
            s.create_heatmap(start,end)
        elif user_input == "X":
            print("Special entry mode")
            start = input("Start date (yyyy-mm-dd): ")
            end = input("End date (yyyy-mm-dd): ")
            date_range = pandas.date_range(start=start,end=end)
            for date in date_range:
                date = str(date)[:10]
                s.create_entry(date)
        else:
            break

'''
{
    "2025-10-24": {
        "activity_type": "workout",
        "activity_details": "2"
    },
    "2025-10-25": {
        "activity_type": "workout",
        "activity_details": "3"
    },
    "2025-10-26": {
        "activity_type": "restday",
        "activity_details": "1"
    },
    "2025-10-27": {
        "activity_type": "running",
        "activity_details": "1"
    }
}
'''