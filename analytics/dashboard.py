import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

def load_data():

    conn = sqlite3.connect("patients.db")

    df = pd.read_sql_query(
        "SELECT * FROM patients",
        conn
    )

    conn.close()

    return df


def basic_statistics():

    df = load_data()

    print("\n========== Health Statistics ==========\n")

    print(df.describe())

    print("\n=======================================\n")


def bmi_category(bmi):

    if bmi < 18.5:
        return "underweight"

    elif bmi < 25:
        return "Normal"

    elif bmi < 30:
        return "Overweight"

    else:
        return "obese"


def bmi_distribution():

    df = load_data()

    df["bmi"] = df["weight"] / ((df["height"] / 100) ** 2)

    df["BMI Category"] = df["bmi"].apply(bmi_category)

    counts = df["BMI Category"].value_counts()

    plt.figure(figsize=(8, 5))

    counts.plot(kind="bar")

    plt.title("BMI Category Distribution")

    plt.xlabel("BMI Category")

    plt.ylabel("Number of Patients")

    plt.tight_layout()

    plt.show()


def age_distribution():

    df = load_data()

    plt.figure(figsize=(8, 5))

    plt.hist(df["age"], bins=10)

    plt.title("Age Distribution of Patients")

    plt.xlabel("Age")

    plt.ylabel("Number of Patients")

    plt.tight_layout()

    plt.show()



def bmi_pie_chart():

    df = load_data()

    # Calculate BMI
    df["bmi"] = df["weight"] / ((df["height"] / 100) ** 2)

    # Create BMI Category
    df["BMI Category"] = df["bmi"].apply(bmi_category)

    counts = df["BMI Category"].value_counts()

    plt.figure(figsize=(7, 7))

    plt.pie(
        counts,
        labels=counts.index,
        autopct="%1.1f%%",
        startangle=90
    )

    plt.title("BMI Category Distribution")

    plt.axis("equal")

    plt.show()

def health_dashboard():

    df = load_data()

    # Calculate BMI
    df["bmi"] = df["weight"] / ((df["height"] / 100) ** 2)

    # Create BMI Category
    df["BMI Category"] = df["bmi"].apply(bmi_category)

    bmi_counts = df["BMI Category"].value_counts()

    plt.figure(figsize=(14, 10))

    # ---------------- Bar Chart ----------------
    ax1 = plt.subplot(2, 2, 1)

    bmi_counts.plot(kind="bar", ax=ax1)

    ax1.set_title("BMI Category Distribution")
    ax1.set_xlabel("Category")
    ax1.set_ylabel("Patients")

    # ---------------- Histogram ----------------
    ax2 = plt.subplot(2, 2, 2)

    ax2.hist(df["age"], bins=10)

    ax2.set_title("Age Distribution")
    ax2.set_xlabel("Age")
    ax2.set_ylabel("Patients")

    # ---------------- Pie Chart ----------------
    ax3 = plt.subplot(2, 2, 3)

    ax3.pie(
        bmi_counts,
        labels=bmi_counts.index,
        autopct="%1.1f%%",
        startangle=90
    )

    ax3.set_title("BMI Percentage")

    # ---------------- Summary ----------------
    ax4 = plt.subplot(2, 2, 4)

    ax4.axis("off")

    summary = f"""
Total Patients : {len(df)}

Average Age : {df['age'].mean():.1f}

Average Weight : {df['weight'].mean():.1f} kg

Average Height : {df['height'].mean():.1f} cm

Average BMI : {df['bmi'].mean():.2f}
"""

    ax4.text(
        0.05,
        0.95,
        summary,
        fontsize=12,
        va="top"
    )

    plt.suptitle("NutriAyurAI Health Analytics Dashboard", fontsize=18)

    plt.tight_layout()

    folder = create_reports_folder()

    plt.savefig(
        os.path.join(folder, "health_dashboard.png"),
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()

    # ---------------- Summary ----------------
    ax4 = plt.subplot(2, 2, 4)

    ax4.axis("off")

    summary = f"""
Total Patients : {len(df)}

Average Age : {df['age'].mean():.1f}

Average Weight : {df['weight'].mean():.1f} kg

Average Height : {df['height'].mean():.1f} cm

Average BMI : {df['bmi'].mean():.2f}
"""

    ax4.text(
        0.05,
        0.95,
        summary,
        fontsize=12,
        va="top"
    )

    plt.suptitle("NutriAyurAI Health Analytics Dashboard", fontsize=18)

    plt.tight_layout()

    folder = create_reports_folder()

    plt.savefig(
        os.path.join(folder, "health_dashboard.png"),
        dpi=300,
        bbox_inches="tight"
)

plt.show()

def create_reports_folder():

    folder = "reports/graphs"

    os.makedirs(folder, exist_ok=True)

    return folder




if __name__== "__main__":
    health_dashboard()

