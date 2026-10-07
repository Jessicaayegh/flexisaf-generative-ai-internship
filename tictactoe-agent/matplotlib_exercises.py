import pandas as pd
import matplotlib.pyplot as plt

url = "https://pynative.com/wp-content/uploads/2019/01/company_sales_data.csv"
df = pd.read_csv("company_sales_data.csv")

# Exercise 1: total profit of all months as a line plot
plt.figure()
plt.plot(df["month_number"], df["total_profit"], marker="o")
plt.xlabel("Month number")
plt.ylabel("Total profit")
plt.title("Total profit of all months")
plt.savefig("exercise1_total_profit.png")
plt.show()

# Exercise 2: bathing soap and facewash sales using subplots
fig, axs = plt.subplots(2, 1, sharex=True)
axs[0].plot(df["month_number"], df["bathingsoap"], marker="o")
axs[0].set_title("Bathing soap sales")
axs[1].plot(df["month_number"], df["facewash"], marker="o", color="green")
axs[1].set_title("Facewash sales")
axs[1].set_xlabel("Month number")
fig.tight_layout()
plt.savefig("exercise2_subplots.png")
plt.show()
