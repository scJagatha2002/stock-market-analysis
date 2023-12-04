import requests
from collections import deque
import tkinter as tk
from tkinter import Entry, Button, Label, Text, Scrollbar

#GET THE JSON INFORMATION FROM THE GIVEN API
def process_data():
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=1min&apikey=MAOF2H7M93CZKWA2'
    response = requests.get(url)
    data = response.json()
    time_series = data.get('Time Series (1min)', {})
    
#ADD THE "high" DATA FROM JSON FILE TO LIST "input"
    Input = []
    for timestamp, values in time_series.items():
        High_Value = values['2. high']
        Input.append(High_Value)
    
#APPLY THE SLIDING WINDOW MAXIMUM ALGORITHM TO FIND THE GIGHEST STOCK MARKET PRICES FOR EVERY 5 MINS
    window = deque()
    Output = []
    
    k = 5
    
    for i in range(0, k):
        while len(window) != 0 and Input[i] >= Input[window[-1]]:
            window.pop()
        window.append(i)
    
    for i in range(k, len(Input)):
        Output.append(Input[window[0]])
        while len(window) != 0 and window[0] <= i - k:
            window.popleft()
        while len(window) != 0 and Input[i] >= Input[window[-1]]:
            window.pop()
        window.append(i)
    
    Output.append(Input[window[0]])
    
    output_text.delete(1.0, tk.END)  
    for i in Output:
        output_text.insert(tk.END, str(i) + "\n")

root = tk.Tk()
root.title("High Value Display")

label_interval = Label(root, text="Higest stock prices for every 5 mins is:")
label_interval.pack()

process_button = Button(root, text="Process Data", command=process_data)
process_button.pack()

# Smaller dimensions for the output_text widget
output_text = Text(root, height=10, width=50)  # Adjust the height and width as needed
output_text.pack()

scrollbar = Scrollbar(root, command=output_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
output_text.config(yscrollcommand=scrollbar.set)

root.mainloop()

