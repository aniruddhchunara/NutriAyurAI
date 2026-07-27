import pandas as pd
from analytics.data_loader import load_data
from sklearn.model_selection import train_test_split





def prepare_dataset():

    df = load_data()

    print(df.head())

    df["bmi"] = df["weight"] / ((df["height"] / 100) ** 2)
    X = df[
        ["age","weight" , "height"]
    ]

    y = df["bmi"]
    
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,test_size=0.2,
        random_state=42
    )



    print("\n========== FEATURES (X) ==========")
    print(X)

    print("\n========== TARGET (y) ==========")
    print(y)
    
    print("\n========== DATA SPLIT ==========")
    
    print("Training Samples : ", len(X_train))
    print("Testing Samples :", len(X_test))















if __name__ == "__main__":
    prepare_dataset()