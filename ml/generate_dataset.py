import random
from models.patient import Patient
from database.database import add_patient

names = [

    "Aarav",
    "Vivaan",
    "Krish",
    "Anil",
    "Sagar",
    "Rahul",
    "Neha",
    "Priya",
    "Riya",
    "Ananya",
    "Arjun",
    "Karan",
    "Nisha",
    "Meera",
    "Yash"

]


def generate_patients():
    
    for  _ in range(500):
        
        patient = Patient(
            name=random.choice(names),
            
            age = random.randint(18,65),
            
            weight = round(random.uniform(45, 95),1),
            
            height = round(random.uniform(150,190),1),
            
            activity_factor=random.choice(
                [1.2, 1.375, 1.55, 1.725, 1.9]
            )
        )
        
        add_patient(patient)
        
    print("\n500 Patients Generated Successfully!")
    
    
if __name__== "__main__":
    generate_patients()
        