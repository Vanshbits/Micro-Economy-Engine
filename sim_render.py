from simulator import run_sim
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from IPython.display import HTML
import numpy as np

df = run_sim()
df.to_csv("simulation_data.csv", index=False)

# 1. Setup the Dark Slate Canvas
fig, ax = plt.subplots(figsize=(10, 10))

# Modern dark slate background
fig.patch.set_facecolor('#1E293B')
ax.set_facecolor('#1E293B')

# Subtle gridlines
ax.grid(True, color='#334155', linestyle='-', linewidth=0.7)

# Hide borders
for spine in ax.spines.values():
    spine.set_visible(False)

# Muted tick labels
ax.tick_params(colors='#94A3B8')

# 2. Apply Custom Typography to Title (Curvy, italic, white)
ax.set_xlim(-1, 12)
ax.set_ylim(-1, 12)
ax.set_title("Micro Economy: Real-Time Engine", 
             color='white', 
             fontsize=22, 
             pad=20,
             style='italic',
             family='cursive')

# 3. Draw static infrastructure with white borders for contrast
ax.add_patch(plt.Rectangle((4.5, 4.5), 1, 1, facecolor='#5F6A72', edgecolor='white', linewidth=1.5, zorder=1))
ax.text(5, 5.8, "Factory", ha='center', color='white', fontsize=14, style='italic', family='cursive')

ax.add_patch(plt.Rectangle((1.5, 7.5), 1, 1, facecolor='#4CAF50', edgecolor='white', linewidth=1.5, zorder=1))
ax.text(2, 8.8, "Store", ha='center', color='white', fontsize=14, style='italic', family='cursive')

# 4. Custom State Color Dictionary
color_map = {
    "working": "#FBBF24",
    "sleep": "#4338CA",
    "shopping": "#FB7185",
    "travelling": "#00C2FF"
}

# 5. Initialize the dynamic agents (Added white edge colors to make them pop)
scatter = ax.scatter([], [], s=450, alpha=0.9, zorder=2, edgecolors='white', linewidths=1.5)
time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes, color='white', fontsize=14, style='italic', family='cursive')

# Create empty text objects with the curvy italic font for the agent IDs
unique_agents = df["NAME"].unique()
agent_labels = [ax.text(0, 0, '', fontsize=10, fontweight='bold', ha='center', va='center', color='white', style='italic', family='cursive', zorder=3) for _ in range(len(unique_agents))]

# 6. Build the Dark Mode Legend
for state, color in color_map.items():
    ax.scatter([], [], c=color, label=state, s=150, edgecolors='white', linewidths=1)
ax.legend(loc="upper right", framealpha=0.2, facecolor='#121212', edgecolor='white', labelcolor='white')

# 7. The Frame-by-Frame Execution Loop
def update(hour):
    # Filter and physically sort the data so label [0] always attaches to Agent_1
    current_data = df[df["HOUR"] == hour].sort_values(by="NAME").reset_index(drop=True)
    
    # Extract coordinates and push them to the map
    coords = np.c_[current_data["X_CORD"], current_data["Y_CORD"]]
    scatter.set_offsets(coords)
    
    # Force the color to match the text state perfectly
    colors = current_data["STATE"].map(color_map).fillna("#808080").tolist()
    scatter.set_color(colors)
    
    # Update the clock
    time_text.set_text(f'Simulation Hour: {hour}')
    
    # Paint the agent numbers directly inside their dots
    for i, row in current_data.iterrows():
        agent_labels[i].set_position((row["X_CORD"], row["Y_CORD"]))
        # Strip the word "agent_" and just print the number (e.g., "49")
        num = str(row["NAME"]).split('_')[-1] 
        agent_labels[i].set_text(num)
    
    return [scatter, time_text] + agent_labels

# 8. Compile the animation
anim = animation.FuncAnimation(
    fig, 
    update, 
    frames=df["HOUR"].unique(), 
    interval=400,
    blit=True
)

# Render as an interactive HTML5 video player in Jupyter (Uncomment if you are using interactive window)
# plt.close()
# HTML(anim.to_jshtml())

print("Rendering MP4 video... Please wait.")
writer = animation.FFMpegWriter(fps=2, bitrate=1800)
anim.save('economy_engine_render.mp4', writer=writer)
print("Success: Video saved as 'economy_engine_render.mp4'")
