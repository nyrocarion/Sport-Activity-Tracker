import datetime
import json
import pandas

import matplotlib.pyplot as plt
import numpy as np

import matplotlib
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
            "restday" : 1,
            "workout" : 2,
            "running" : 3,
            "hiking" : 4
        }
        self.num_to_display_mapping = {
            "1" : "\U0001F4A4",
            "2" : "\U0001F4AA",
            "3" : "\U0001F3C3",
            "4" : "\U0001F97E"
        }

    def create_entry(self,default_date:str=""):
        '''
        Create a new entry over console input and save it into the json file.
        Parameters:
            - default_date: str (used when generating multiple entries)
        '''
        if default_date == "":
            date = input("Enter date (yyyy-mm-dd, leave empty for todays date): ")
            if len(date) == 0:
                date = default_date
        else:
            date = default_date
            print(f"Date: {default_date}")
        type = input("Enter type (workout w, running r, hiking h or restday ENTER): ")
        if len(type) == 1:
            type = {"w" : "workout", "r": "running", "h": "hiking"}[type]
            details = input("Enter additional details (distance, workout name, etc.)")
        else:
            type = "restday"
            details = ""
        entry = {
            date: {
                "activity_type" : type,
                "activity_details" : details
            }
        }
        self.activity_data.update(entry)
        with open("sport_activity_data.json", "w") as file:
            json.dump(self.activity_data,file,indent=4)

    def create_activity_map(self,start_date:str,end_date:str):
        '''
        Creates an activity map for all the activity from start to end date.
        '''
        # Default dates (min or max date)
        if start_date == "":
            start_date = list(self.activity_data.items())[0][0]
        if end_date == "":
            end_date = list(self.activity_data.items())[-1][0]

        # Create Date Range and initial data structures
        date_range = pandas.date_range(start=start_date,end=end_date)
        calendar_weeks = list()
        weekdays = [1,2,3,4,5,6,7]
        data = list()
        row_data = [0,0,0,0,0,0,0]

        # Generating the data for the map as a list of row based lists
        for date in date_range:
            date = str(date)[:10]
            datetime_object = datetime.datetime.strptime(date, '%Y-%m-%d').date()
            calendar_week = datetime_object.isocalendar().week
            if calendar_week not in calendar_weeks:
                calendar_weeks.append(calendar_week)
            try: 
                val = self.text_to_value_mapping[self.activity_data[date]["activity_type"]] 
            except:
                val = 0
            weekday = datetime_object.isocalendar().weekday
            row_data[weekday-1] = val
            if weekday == 7 or date == end_date:
                data.append(row_data)
                row_data = [0,0,0,0,0,0,0]
                
        structured_data = np.array(data)

        # Basic plot config
        background_color = "#F1BB7E"
        colors = ["#F9DBBD", background_color, "#FF858D", "#DA627D", "#A53860"]
        color_map = ListedColormap(colors)
        fig, ax = plt.subplots()
        plt.rc('font', family='Consolas', size=12)
        im = ax.imshow(structured_data,cmap=color_map)
        fig.patch.set_facecolor(background_color)
        ax.set_xticks(range(len(weekdays)), labels=weekdays)
        plt.xlabel("Weekdays")
        ax.set_yticks(range(len(calendar_weeks)), labels=calendar_weeks)
        plt.ylabel("Calendar week")

        # Adding text on top of the heatmap squares
        for i in range(len(calendar_weeks)):
            for j in range(len(weekdays)):
                try:
                    text = self.num_to_display_mapping[str(structured_data[i,j])]
                except:
                    text = ""
                text = ax.text(j, i, text, ha="center", va="center", color="w", fontfamily="Segoe UI Emoji", fontsize=20)

        ax.set_title(f"Sport Activity Data from {start_date} to {end_date}")

        # Legend for the plot
        legend_labels = {
            0: "No data",
            1: "Restday",
            2: "Workout",
            3: "Running",
            4: "Hiking"
        }
        patches = [matplotlib.patches.Patch(color=colors[i], label=legend_labels[i]) for i in range(len(colors))]
        ax.legend(handles=patches, bbox_to_anchor=(1.05, 1), loc='upper left', title="Activity Type")

        plt.show()

# Idea: A mode which allows a user to add all entries since the last entry
# Idea: A mode that creates the activity map for the last full month

if __name__ == "__main__":
    s = SportActivityManager()
    while True:
        user_input = input("Generate activiy map (M)\n" \
        "Enter new entry (D)\n" \
        "Enter multiple entries (X)")
        if user_input == "D":
            print("Now adding an entry for today!")
            s.create_entry()
        elif user_input == "M":
            print("Please specify the start and end date for the activity map!")
            start = input("Start date (yyyy-mm-dd): ")
            end = input("End date (yyyy-mm-dd): ")
            s.create_activity_map(start,end)
        elif user_input == "X":
            print("Please specify the start and end date for the timespan you want to add entries in!")
            start = input("Start date (yyyy-mm-dd): ")
            end = input("End date (yyyy-mm-dd): ")
            date_range = pandas.date_range(start=start,end=end)
            for date in date_range:
                date = str(date)[:10]
                s.create_entry(date)
        else:
            print("Not a known option!")