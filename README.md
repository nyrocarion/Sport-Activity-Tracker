# Overview

This small python projects transform a set of user given sport activities from a json-file into an activity map using matplotlib.

## How to use

1. Start the programm
2. Choose a mode and follow instructions

## Modes

- M: Create an activity map with the current data
- D: Add a singular entry to the json file
- X: Add a range of entries to the json file

## Format

```python
entry = {
            date: {
                "activity_type" : type,
                "activity_details" : details
            }
        }
```

- date: YYYY-MM-DD
- type: workout, running, hiking, restday
- details: additional information

# Example Result

![ExampleResult](https://github.com/nyrocarion/Sport-Activity-Tracker/blob/main/Example.png)
