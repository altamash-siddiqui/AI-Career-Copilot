import json
import logging
import csv
import shutil

from person import Person
from career_features import CareerFeatures
from utils import get_user_name, get_career_interest
from datetime import datetime

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
        print("7. Search Career Record")
        print("8. Update Career Record")
        print("9. Delete Career Record")
        print("10. Dashboard")
        print("11. Export Career Report (TXT)")
        print("12. Mark Favorite Career")
        print("13. View Favorite Careers")
        print("14. Backup Career Data")
        print("15. Restore Backup")
        print("16. Exit")
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
                "career": interest,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "favorite": False
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
            self.search_career()
            
        elif choice == "8":
            self.update_career()

        elif choice == "9":
            self.delete_career()

        elif choice == "10":
            self.dashboard()

        elif choice == "11":
            self.export_to_txt()
            
        elif choice == "12":
            self.mark_favorite()
            
        elif choice == "13":
            self.view_favorites()
            
        elif choice == "14":
            self.backup_data()

        elif choice == "15":
            self.restore_data()

        elif choice == "16":
            print("\nThank you for using AI Career Copilot!")
            return False

        else:
            print("\n❌ Invalid choice! Please select 1 to 16.")

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
            
            
    def search_career(self):

        search_name = input("Enter name to search: ").strip().lower()

        try:

            with open("career_data.json", "r") as file:
                careers = json.load(file)

            found = False

            for record in careers:

                if search_name in record["name"].lower():

                    print("\n========== Record Found ==========")
                    print(f"Name       : {record['name']}")
                    print(f"Career     : {record['career']}")

                    if "timestamp" in record:
                        print(f"Created On : {record['timestamp']}")

                    print("=" * 32)

                    found = True

                    logging.info(f"Search successful for {search_name}")

                    break

            if not found:

                print("❌ No record found.")

                logging.warning(f"Search failed for {search_name}")

        except Exception as e:

            logging.error(str(e))

            print(f"❌ {e}")
            
    def update_career(self):

        update_name = input("Enter name to update: ").strip().lower()

        try:

            with open("career_data.json", "r") as file:
                careers = json.load(file)

            updated = False

            for record in careers:

                if record["name"].lower() == update_name:

                    print(f"\nCurrent Career: {record['career']}")

                    new_career = get_career_interest()

                    record["career"] = new_career

                    updated = True

                    break

            if updated:

                with open("career_data.json", "w") as file:
                    json.dump(careers, file, indent=4)

                print("✅ Career updated successfully!")

                logging.info(f"Career updated for {update_name}")

            else:

                print("❌ Record not found.")

        except Exception as e:

            logging.error(str(e))

            print(f"❌ {e}")
            
    def delete_career(self):

        delete_name = input("Enter name to delete: ").strip().lower()

        try:

            with open("career_data.json", "r") as file:
                careers = json.load(file)

            updated_list = []

            deleted = False

            for record in careers:

                if record["name"].lower() == delete_name:

                    deleted = True

                    continue

                updated_list.append(record)

            if deleted:

                with open("career_data.json", "w") as file:
                    json.dump(updated_list, file, indent=4)

                print("✅ Career record deleted successfully!")

                logging.info(f"Career deleted for {delete_name}")

            else:

                print("❌ Record not found.")

        except Exception as e:

            logging.error(str(e))

            print(f"❌ {e}")
            
    def dashboard(self):

        try:

            with open("career_data.json", "r") as file:
                careers = json.load(file)

            total_users = len(careers)

            career_count = {}

            for record in careers:

                career = record["career"]

                if career in career_count:
                    career_count[career] += 1
                else:
                    career_count[career] = 1

            print("\n========== DASHBOARD ==========")
            print(f"Total Users : {total_users}")
            print(f"Total Career Records : {total_users}")

            print("\nCareer Statistics:")

            for career, count in career_count.items():
                print(f"{career.title()} : {count}")

            if career_count:

                popular_career = max(
                    career_count,
                    key=career_count.get
                )

                print(f"\n🏆 Most Popular Career : {popular_career.title()}")

            print("\nCareer Percentage:")

            for career, count in career_count.items():

                percentage = (count / total_users) * 100

                print(f"{career.title()} : {percentage:.2f}%")

        except Exception as e:

            logging.error(str(e))

            print(f"❌ {e}")
            
    def mark_favorite(self):

        favorite_name = input("Enter name to mark as favorite: ").strip().lower()

        try:

            with open("career_data.json", "r") as file:
                careers = json.load(file)

            found = False

            for record in careers:

                if record["name"].lower() == favorite_name:

                    record["favorite"] = True

                    found = True

                    break

            if found:

                with open("career_data.json", "w") as file:
                    json.dump(careers, file, indent=4)

                print("⭐ Career marked as Favorite!")

                logging.info(f"{favorite_name} marked as favorite.")

            else:

                print("❌ Record not found.")

        except Exception as e:

            logging.error(str(e))

            print(f"❌ {e}")
            
    def view_favorites(self):

        try:

            with open("career_data.json", "r") as file:
                careers = json.load(file)

            found = False

            print("\n========== Favorite Careers ==========")

            for record in careers:

                if record.get("favorite", False):

                    print(f"\nName       : {record['name']}")
                    print(f"Career     : {record['career']}")

                    if "timestamp" in record:
                        print(f"Created On : {record['timestamp']}")

                    print("⭐ Favorite")

                    found = True

            if not found:
                print("No favorite careers found.")

        except Exception as e:

            logging.error(str(e))

            print(f"❌ {e}")
            
    def backup_data(self):

        try:

            shutil.copy(
                "career_data.json",
                "career_data_backup.json"
            )

            print("✅ Backup created successfully!")

            logging.info("Career data backup created.")

        except Exception as e:

            logging.error(str(e))

            print(f"❌ {e}")
            
    def export_to_txt(self):

        try:

            with open("career_data.json", "r") as file:
                careers = json.load(file)

            with open("career_report.txt", "w") as report:

                report.write("========== AI Career Copilot Report ==========\n\n")

                for record in careers:

                    report.write(f"Name       : {record['name']}\n")
                    report.write(f"Career     : {record['career']}\n")

                    if "timestamp" in record:
                        report.write(f"Created On : {record['timestamp']}\n")

                    report.write("-" * 40 + "\n")

            print("✅ Career report exported successfully!")

            logging.info("Career report exported to TXT.")

        except Exception as e:

            logging.error(str(e))

            print(f"❌ {e}")
            
    def restore_data(self):

        try:

            shutil.copy(
                "career_data_backup.json",
                "career_data.json"
            )

            print("✅ Data restored successfully!")

            logging.info("Career data restored from backup.")

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