import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor, RadioButtons
import numpy as np

infraLevel = list(range(6))
costOfEachInfraLevel = [6000, 5000, 4285.714, 3750, 3333.333]
slotsLeft = list(range(26))

X = []  
Y = []  
C = []  
savings_values = []  

def calculate_savings(saving_per_slot):
    global X, Y, C, savings_values
    X = []
    Y = []
    C = []
    savings_values = []
    for i in infraLevel:
        costOfInfra = sum(costOfEachInfraLevel[i:5])
        for x in slotsLeft:
            savings = (x * saving_per_slot) / 2 - costOfInfra
            X.append(x)
            Y.append(i)
            C.append('green' if savings > 0 else 'red')
            savings_values.append(savings)
            
calculate_savings(10800)

fig, ax = plt.subplots(figsize=(10, 6))
sc = ax.scatter(X, Y, c=C, alpha=0.7, edgecolor='k')

plt.subplots_adjust(bottom=0.25)
plt.title("How much IC do you save by maxxing out inf on tiles with different building slots?")
plt.suptitle("Green indicates positive savings; Red indicates negative savings", fontsize=10, color="gray")
plt.xlabel("Slots Left")
plt.ylabel("Infrastructure Originally")
plt.yticks(ticks=infraLevel, labels=[str(i) for i in (infraLevel)])
plt.grid(alpha=0.3)

annot = ax.annotate("", xy=(0, 0), xytext=(10, 10), textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="w"), arrowprops=dict(arrowstyle="->"))
annot.set_visible(False)

def update_annot(ind):
    pos = sc.get_offsets()[ind[0]]
    annot.xy = pos
    text = f"Savings: {savings_values[ind[0]]:.2f}"
    annot.set_text(text)
    annot.get_bbox_patch().set_facecolor(C[ind[0]])
    annot.get_bbox_patch().set_alpha(0.6)

def hover(event):
    vis = annot.get_visible()
    if event.inaxes == ax:
        cont, ind = sc.contains(event)
        if cont:
            update_annot(ind["ind"])
            annot.set_visible(True)
            fig.canvas.draw_idle()
        else:
            if vis:
                annot.set_visible(False)
                fig.canvas.draw_idle()

def update_plot(label):
    saving_per_slot = 10800 if label == 'Civs' else 7200
    calculate_savings(saving_per_slot)
    sc.set_offsets(np.c_[X, Y])
    sc.set_facecolors(C)
    fig.canvas.draw_idle()

ax_radio = plt.axes([0.15, 0.05, 0.2, 0.15], facecolor="lightgray")
radio = RadioButtons(ax_radio, ("Civs", "Mils"))
radio.on_clicked(update_plot)

fig.canvas.mpl_connect("motion_notify_event", hover)

plt.show()
