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

        self.current_user = None


    def welcome(self):

        print("=" * 35)
        print("      AI Career Copilot")
        print("=" * 35)


    def welcome_user(self):

        print("\n" + "=" * 35)

        super().welcome_user()

        print("Let's build your career together! 🚀")

        print("=" * 35)


    def register_user(self):

        username = input(
            "Create Username: "
        ).strip()

        password = input(
            "Create Password: "
        ).strip()

        if not username or not password:

            print(
                "❌ Username and password "
                "cannot be empty!"
            )

            return False

        try:

            with open("users.json", "r") as file:

                users = json.load(file)

        except:

            users = []

        for user in users:

            if user["name"].lower() == username.lower():

                print(
                    "❌ Username already exists!"
                )

                return False

        users.append({

            "name": username,

            "password": password

        })

        with open("users.json", "w") as file:

            json.dump(
                users,
                file,
                indent=4
            )

        print(
            "✅ Registration Successful!"
        )

        logging.info(
            f"New user registered: {username}"
        )

        return True


    def login_user(self):

        username = input(
            "Username: "
        ).strip()

        password = input(
            "Password: "
        ).strip()

        try:

            with open("users.json", "r") as file:

                users = json.load(file)

        except:

            print(
                "❌ No users found!"
            )

            return False

        for user in users:

            if (
                user["name"].lower() == username.lower()
                and
                user["password"] == password
            ):

                self.set_name(
                    user["name"]
                )

                self.current_user = user["name"]

                print(
                    f"\n✅ Welcome back, "
                    f"{user['name']}!"
                )

                logging.info(
                    f"{user['name']} logged in."
                )

                return True

        print(
            "❌ Invalid Username or Password!"
        )

        logging.warning(
            f"Failed login attempt: {username}"
        )

        return False


    def authentication_menu(self):

        while True:

            print(
                "\n========== Authentication =========="
            )

            print("1. Register")
            print("2. Login")
            print("3. Exit")

            choice = input(
                "Enter your choice: "
            ).strip()

            if choice == "1":

                self.register_user()

            elif choice == "2":

                if self.login_user():

                    return True

            elif choice == "3":

                print(
                    "\nThank you for using "
                    "AI Career Copilot!"
                )

                return False

            else:

                print(
                    "\n❌ Invalid choice! "
                    "Please select 1 to 3."
                )


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

        return input(
            "Enter your choice: "
        ).strip()


    def process_choice(self, choice):

        if choice == "1":

            interest = get_career_interest()

            try:

                with open(
                    "career_data.json",
                    "r"
                ) as file:

                    careers = json.load(file)

            except:

                careers = []

            careers.append({

                "name": self.get_name(),

                "career": interest,

                "timestamp": datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),

                "favorite": False,

                "user": self.current_user

            })

            with open(
                "career_data.json",
                "w"
            ) as file:

                json.dump(
                    careers,
                    file,
                    indent=4
                )

            print(
                "\n✅ Career saved successfully!"
            )

            logging.info(
                f"Career selected: {interest}"
            )

            self.show_career_roadmap(
                interest
            )


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

            print(
                "\nThank you for using "
                "AI Career Copilot!"
            )

            return False


        else:

            print(
                "\n❌ Invalid choice! "
                "Please select 1 to 16."
            )

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

        print(
            "\n========== Career Roadmap =========="
        )

        if interest not in roadmaps:

            print(
                "❌ Roadmap not available."
            )

            return

        for index, step in enumerate(
            roadmaps[interest],
            start=1
        ):

            print(
                f"{index}. {step}"
            )

        print("=" * 35)


    def export_to_csv(self):

        try:

            with open(
                "career_data.json",
                "r"
            ) as file:

                data = json.load(file)

            user_data = []

            for record in data:

                if record.get("user") == self.current_user:

                    user_data.append(record)

            with open(
                "career_history.csv",
                "w",
                newline=""
            ) as file:

                writer = csv.writer(file)

                writer.writerow([
                    "Name",
                    "Career",
                    "Created On",
                    "Favorite"
                ])

                for record in user_data:

                    writer.writerow([

                        record["name"],

                        record["career"],

                        record.get(
                            "timestamp",
                            ""
                        ),

                        record.get(
                            "favorite",
                            False
                        )

                    ])

            print(
                "✅ Your career history "
                "exported to career_history.csv"
            )

            logging.info(
                "Current user's career history "
                "exported to CSV."
            )

        except Exception as e:

            logging.error(str(e))

            print(
                f"❌ {e}"
            )


    def search_career(self):

        search_name = input(
            "Enter name to search: "
        ).strip().lower()

        try:

            with open(
                "career_data.json",
                "r"
            ) as file:

                careers = json.load(file)

            found = False

            for record in careers:

                if record.get(
                    "user"
                ) != self.current_user:

                    continue

                if (
                    search_name
                    in record["name"].lower()
                ):

                    print(
                        "\n========== Record Found =========="
                    )

                    print(
                        f"Name       : "
                        f"{record['name']}"
                    )

                    print(
                        f"Career     : "
                        f"{record['career']}"
                    )

                    if "timestamp" in record:

                        print(
                            f"Created On : "
                            f"{record['timestamp']}"
                        )

                    if record.get(
                        "favorite",
                        False
                    ):

                        print(
                            "⭐ Favorite"
                        )

                    print("=" * 32)

                    found = True

                    break

            if not found:

                print(
                    "❌ No record found for "
                    "the current user."
                )

        except Exception as e:

            logging.error(str(e))

            print(
                f"❌ {e}"
            )


    def update_career(self):

        update_name = input(
            "Enter name to update: "
        ).strip().lower()

        try:

            with open(
                "career_data.json",
                "r"
            ) as file:

                careers = json.load(file)

            updated = False

            for record in careers:

                if record.get(
                    "user"
                ) != self.current_user:

                    continue

                if (
                    record["name"].lower()
                    == update_name
                ):

                    print(
                        f"\nCurrent Career: "
                        f"{record['career']}"
                    )

                    new_career = (
                        get_career_interest()
                    )

                    record["career"] = (
                        new_career
                    )

                    record["user"] = (
                        self.current_user
                    )

                    updated = True

                    break

            if updated:

                with open(
                    "career_data.json",
                    "w"
                ) as file:

                    json.dump(
                        careers,
                        file,
                        indent=4
                    )

                print(
                    "✅ Career updated successfully!"
                )

            else:

                print(
                    "❌ Record not found for "
                    "the current user."
                )

        except Exception as e:

            logging.error(str(e))

            print(
                f"❌ {e}"
            )


    def delete_career(self):

        delete_name = input(
            "Enter name to delete: "
        ).strip().lower()

        try:

            with open(
                "career_data.json",
                "r"
            ) as file:

                careers = json.load(file)

            updated_list = []

            deleted = False

            for record in careers:

                if record.get(
                    "user"
                ) != self.current_user:

                    updated_list.append(record)

                    continue

                if (
                    record["name"].lower()
                    == delete_name
                ):

                    deleted = True

                    continue

                updated_list.append(record)

            if deleted:

                with open(
                    "career_data.json",
                    "w"
                ) as file:

                    json.dump(
                        updated_list,
                        file,
                        indent=4
                    )

                print(
                    "✅ Career record deleted successfully!"
                )

            else:

                print(
                    "❌ Record not found for "
                    "the current user."
                )

        except Exception as e:

            logging.error(str(e))

            print(
                f"❌ {e}"
            )


    def dashboard(self):

        try:

            # ==============================
            # LOAD CAREER DATA
            # ==============================

            with open(
                "career_data.json",
                "r"
            ) as file:

                careers = json.load(file)


            # ==============================
            # LOAD REGISTERED USERS
            # ==============================

            try:

                with open(
                    "users.json",
                    "r"
                ) as file:

                    users = json.load(file)

                total_registered_users = len(users)

            except:

                total_registered_users = 0


            # ==============================
            # CURRENT USER DATA
            # ==============================

            user_records = []

            for record in careers:

                if record.get(
                    "user"
                ) == self.current_user:

                    user_records.append(record)


            print(
                "\n========== MY DASHBOARD =========="
            )

            print(
                f"User : {self.current_user}"
            )

            total_records = len(
                user_records
            )

            print(
                f"Your Career Records : "
                f"{total_records}"
            )


            # ==============================
            # MY CAREER STATISTICS
            # ==============================

            if total_records == 0:

                print(
                    "\nNo career records found."
                )

            else:

                user_career_count = {}

                for record in user_records:

                    career = record["career"]

                    if career in user_career_count:

                        user_career_count[career] += 1

                    else:

                        user_career_count[career] = 1


                print(
                    "\nYour Career Statistics:"
                )

                for career, count in user_career_count.items():

                    print(
                        f"{career.title()} : "
                        f"{count}"
                    )


                print(
                    "\nYour Career Percentage:"
                )

                for career, count in user_career_count.items():

                    percentage = (
                        count
                        / total_records
                    ) * 100

                    print(
                        f"{career.title()} : "
                        f"{percentage:.2f}%"
                    )


                # ==============================
                # MY MOST SELECTED CAREER
                # ==============================

                max_count = max(
                    user_career_count.values()
                )

                popular_careers = []

                for career, count in user_career_count.items():

                    if count == max_count:

                        popular_careers.append(
                            career
                        )


                if len(
                    popular_careers
                ) == 1:

                    print(
                        f"\n🏆 Your Most Selected Career : "
                        f"{popular_careers[0].title()}"
                    )

                else:

                    print(
                        "\n🏆 Your Most Selected Careers : "
                        + ", ".join(
                            career.title()
                            for career in popular_careers
                        )
                    )


            # ==============================
            # GLOBAL CAREER STATISTICS
            # ==============================

            print(
                "\n========== GLOBAL CAREER STATISTICS =========="
            )

            print(
                f"Total Registered Users : "
                f"{total_registered_users}"
            )

            total_global_records = len(
                careers
            )

            print(
                f"Total Career Records : "
                f"{total_global_records}"
            )


            if total_global_records == 0:

                print(
                    "\nNo global career records available."
                )

                return


            # ==============================
            # GLOBAL CAREER COUNT
            # ==============================

            global_career_count = {}

            for record in careers:

                career = record["career"]

                if career in global_career_count:

                    global_career_count[career] += 1

                else:

                    global_career_count[career] = 1


            print(
                "\nCareer Popularity:"
            )


            for career, count in global_career_count.items():

                percentage = (
                    count
                    / total_global_records
                ) * 100

                print(
                    f"{career.title()} : "
                    f"{count} users "
                    f"({percentage:.2f}%)"
                )


            # ==============================
            # GLOBAL MOST POPULAR CAREER
            # ==============================

            max_global_count = max(
                global_career_count.values()
            )

            popular_global_careers = []

            for career, count in global_career_count.items():

                if count == max_global_count:

                    popular_global_careers.append(
                        career
                    )


            if len(
                popular_global_careers
            ) == 1:

                print(
                    f"\n🏆 Most Popular Career : "
                    f"{popular_global_careers[0].title()}"
                )

            else:

                print(
                    "\n🏆 Most Popular Careers : "
                    + ", ".join(
                        career.title()
                        for career in popular_global_careers
                    )
                )


        except FileNotFoundError:

            print(
                "❌ Career data file not found."
            )


        except Exception as e:

            logging.error(
                str(e)
            )

            print(
                f"❌ {e}"
            )


    def mark_favorite(self):

        favorite_name = input(
            "Enter name to mark as favorite: "
        ).strip().lower()

        try:

            with open(
                "career_data.json",
                "r"
            ) as file:

                careers = json.load(file)

            found = False

            for record in careers:

                if record.get(
                    "user"
                ) != self.current_user:

                    continue

                if (
                    record["name"].lower()
                    == favorite_name
                ):

                    record["favorite"] = True

                    found = True

                    break

            if found:

                with open(
                    "career_data.json",
                    "w"
                ) as file:

                    json.dump(
                        careers,
                        file,
                        indent=4
                    )

                print(
                    "⭐ Career marked as Favorite!"
                )

            else:

                print(
                    "❌ Record not found for "
                    "the current user."
                )

        except Exception as e:

            logging.error(str(e))

            print(
                f"❌ {e}"
            )


    def view_favorites(self):

        try:

            with open(
                "career_data.json",
                "r"
            ) as file:

                careers = json.load(file)

            found = False

            print(
                "\n========== Favorite Careers =========="
            )

            for record in careers:

                if record.get(
                    "user"
                ) != self.current_user:

                    continue

                if record.get(
                    "favorite",
                    False
                ):

                    print(
                        f"\nName       : "
                        f"{record['name']}"
                    )

                    print(
                        f"Career     : "
                        f"{record['career']}"
                    )

                    if "timestamp" in record:

                        print(
                            f"Created On : "
                            f"{record['timestamp']}"
                        )

                    print(
                        "⭐ Favorite"
                    )

                    found = True

            if not found:

                print(
                    "No favorite careers found."
                )

        except Exception as e:

            logging.error(str(e))

            print(
                f"❌ {e}"
            )


    def backup_data(self):

        try:

            shutil.copy(
                "career_data.json",
                "career_data_backup.json"
            )

            print(
                "✅ Backup created successfully!"
            )

            logging.info(
                "Career data backup created."
            )

        except Exception as e:

            logging.error(str(e))

            print(
                f"❌ {e}"
            )


    def restore_data(self):

        try:

            shutil.copy(
                "career_data_backup.json",
                "career_data.json"
            )

            print(
                "✅ Data restored successfully!"
            )

            logging.info(
                "Career data restored from backup."
            )

        except Exception as e:

            logging.error(str(e))

            print(
                f"❌ {e}"
            )


    def export_to_txt(self):

        try:

            with open(
                "career_data.json",
                "r"
            ) as file:

                careers = json.load(file)

            user_records = []

            for record in careers:

                if record.get(
                    "user"
                ) == self.current_user:

                    user_records.append(record)

            with open(
                "career_report.txt",
                "w"
            ) as report:

                report.write(
                    "========== "
                    "AI Career Copilot Report "
                    "==========\n\n"
                )

                report.write(
                    f"User: "
                    f"{self.current_user}\n\n"
                )

                for record in user_records:

                    report.write(
                        f"Name       : "
                        f"{record['name']}\n"
                    )

                    report.write(
                        f"Career     : "
                        f"{record['career']}\n"
                    )

                    if "timestamp" in record:

                        report.write(
                            f"Created On : "
                            f"{record['timestamp']}\n"
                        )

                    if record.get(
                        "favorite",
                        False
                    ):

                        report.write(
                            "Favorite   : Yes\n"
                        )

                    report.write(
                        "-" * 40
                        + "\n"
                    )

            print(
                "✅ Your career report "
                "exported successfully!"
            )

            logging.info(
                "Current user's career report "
                "exported to TXT."
            )

        except Exception as e:

            logging.error(str(e))

            print(
                f"❌ {e}"
            )


copilot = CareerCopilot()

copilot.welcome()

if copilot.authentication_menu():

    copilot.welcome_user()

    while True:

        choice = copilot.show_menu()

        if not copilot.process_choice(choice):

            break