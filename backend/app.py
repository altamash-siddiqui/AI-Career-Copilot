def welcome():
    print("=" * 35)
    print("      AI Career Copilot")
    print("=" * 35)


def get_user_name():

    while True:
        name = input("Enter your name: ")

        if name.replace(" ", "").isalpha():
            return name
        else:
            print("❌ Invalid name! Please enter only alphabets.")


def show_menu():
    print("\nChoose an option:")
    print("1. Career Roadmap")
    print("2. Resume Analysis")
    print("3. ATS Score")
    print("4. Interview Preparation")
    print("5. Exit")

    choice = input("Enter your choice: ")
    return choice


def get_career_interest():

    while True:
        interest = input("Enter your career interest: ").lower()

        if interest in [
            "ai",
            "artificial intelligence",
            "web",
            "web development",
            "python",
            "python programming",
            "data science",
            "datascience",
        ]:
            return interest

        else:
            print("❌ Invalid career! Please choose a valid career.")


def show_career_roadmap(interest):

    if interest == "ai" or interest == "artificial intelligence":
        print("\nSuggested Career Roadmap:")
        print("- Learn Python")
        print("- Learn Machine Learning")
        print("- Build AI Projects")

    elif interest == "web development" or interest == "web":
        print("\nSuggested Career Roadmap:")
        print("- Learn HTML")
        print("- Learn CSS")
        print("- Learn JavaScript")

    elif interest == "data science" or interest == "datascience":
        print("\nSuggested Career Roadmap:")
        print("- Learn Python")
        print("- Learn Pandas")
        print("- Learn SQL")

    elif interest == "python" or interest == "python programming":
        print("\nSuggested Career Roadmap:")
        print("- Learn Python Basics")
        print("- Learn Object-Oriented Programming")
        print("- Build Python Projects")


def process_choice(choice):

    if choice == "1":
        interest = get_career_interest()
        show_career_roadmap(interest)

    elif choice == "2":
        print("\nResume Analysis feature is coming soon.")

    elif choice == "3":
        print("\nATS Score Checker feature is coming soon.")

    elif choice == "4":
        print("\nInterview Preparation feature is coming soon.")

    elif choice == "5":
        print("\nThank you for using AI Career Copilot!")

    else:
        print("\n❌ Invalid choice! Please select 1 to 5.")


welcome()

name = get_user_name()

print(f"\nWelcome, {name}")

while True:

    choice = show_menu()

    if choice == "5":
        print("\nThank you for using AI Career Copilot!")
        break

    process_choice(choice)