import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Please run sim_render.py once before running this file

df = pd.read_csv("simulation_data.csv")
print(df.to_string())

class_colors = {
    "Poverty_class": "#FB7185",
    "Middle_class": "#4338CA",
    "Upper_class": "#FBBF24"
}

plt.style.use("dark_background")
plt.figure(figsize=(10, 6))

y_axis = "SUPPLIES" # OR "MONEY"

sns.lineplot(data= df, x= "HOUR", y= y_axis , hue="CLASS", palette= class_colors, linewidth= 2.5)
plt.title("SIMCITY_STATS")
plt.xlabel("hour")
plt.ylabel(y_axis)
plt.xticks(range(0,49,2))
plt.show()