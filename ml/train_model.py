import os
import pickle
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)
from analytics.data_loader import load_data


def train_model():
    df = load_data()
    
    df["bmi"] = df["weight"] / ((df["height"] / 100) ** 2)
    
    X =df[
        ["age", "weight","height"]
    ]
    
    y = df["bmi"]
    
    X_train, X_test ,y_train ,y_test = train_test_split(
        X,
        y,
        test_size=.02,
        random_state=42
    )
    
    model = LinearRegression()
    
    model.fit(
        X_train,
        y_train
    )
    
    os.makedirs("models", exist_ok=True)

    with open("models/bmi_model.pkl", "wb") as file:
       pickle.dump(model, file)
       

    print("Model Saved successfully!")


    new_patient =[[23,72,175]]
    predictied_bmi = model.predict(new_patient)
    
    print("\nPredicted BMI ;", round(predictied_bmi[0],2))
    
    
    y_pred = model.predict(X_test)
    
    mae = mean_absolute_error(y_test, y_pred)
    
    mse = mean_squared_error(y_test, y_pred)
    
    r2 = r2_score(y_test ,y_pred)
    
    print("\n========== MODEL EVALUTION ==========")
    
    print(f"MAE : {mae:4f}")
    print(f"MSE : {mse:4f}")
    print(f"R² : {r2:4f}")
    
    
    print("\nModel trained successfully!")
    
    
   
    
if __name__== "__main__":
    train_model()