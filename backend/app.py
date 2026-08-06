import json
import logging
import csv

from person import Person
from career_features import CareerFeatures
from utils import get_user_name, get_career_interest

class CareerCopilot(Person, CareerFeatures):

    def __init__(self):
        super().__init__()

    def welcome(self):
        print("=" * 35)
        print("      AI Career Copilot")
        print("=" * 35)

    def welcome_user(self):
        print("\n" + "=" * 35)
        super().welcome_user()
        print("Let's build your career together! 🚀")
        print("=" * 35)

    def show_menu(self):
        print("\nChoose an option:")
        print("1. Career Roadmap")
        print("2. Resume Analysis")
        print("3. ATS Score")
        print("4. Interview Preparation")
        print("5. Career History")
        print("6. Export Career History to CSV")
        print("7. Exit")

        return input("Enter your choice: ")
    
    
    def process_choice(self, choice):

        if choice == "1":

            interest = get_career_interest()

            try:
                with open("career_data.json", "r") as file:
                    careers = json.load(file)
            except:
                careers = []

            careers.append({
                "name": self.get_name(),
                "career": interest
            })

            with open("career_data.json", "w") as file:
                json.dump(careers, file, indent=4)

            print("\n✅ Career saved successfully!")

            logging.info(f"Career selected: {interest}")

            self.show_career_roadmap(interest)

        elif choice == "2":
            self.resume_analysis()

        elif choice == "3":
            self.ats_score()

        elif choice == "4":
            self.interview_preparation()

        elif choice == "5":
            self.career_history()

        elif choice == "6":
            self.export_to_csv()

        elif choice == "7":
            print("\nThank you for using AI Career Copilot!")
            return False

        else:
            print("\n❌ Invalid choice! Please select 1 to 7.")

        return True
            
            
    def show_career_roadmap(self, interest):

        roadmaps = {
            "ai": [
                "Learn Python",
                "Learn Machine Learning",
                "Build AI Projects"
            ],
            "web": [
                "Learn HTML",
                "Learn CSS",
                "Learn JavaScript"
            ],
            "python": [
                "Learn Python Basics",
                "Learn Object-Oriented Programming",
                "Build Python Projects"
            ],
            "data science": [
                "Learn Python",
                "Learn Pandas",
                "Learn SQL"
            ]
        }

        print("\n========== Career Roadmap ==========")

        for index, step in enumerate(roadmaps[interest], start=1):
            print(f"{index}. {step}")

        print("=" * 35)
        
    def export_to_csv(self):

        try:

            with open("career_data.json", "r") as file:
                data = json.load(file)

            with open("career_history.csv", "w", newline="") as file:

                writer = csv.writer(file)

                writer.writerow(["Name", "Career"])

                for record in data:
                    writer.writerow(
                        [record["name"], record["career"]]
                    )

            print("✅ Career history exported to career_history.csv")

            logging.info("Career history exported to CSV.")

        except Exception as e:

            logging.error(str(e))

            print(f"❌ {e}")


copilot = CareerCopilot()

copilot.welcome()

name = get_user_name()

copilot.set_name(name)

copilot.welcome_user()

while True:

    choice = copilot.show_menu()

    if not copilot.process_choice(choice):
        break