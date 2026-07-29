def welcome():
    print("=" * 35)
    print("      AI Career Copilot")
    print("=" * 35)


def get_user_name():
    name = input("Enter your name: ")
    print(f"Welcome, {name}!")

    print("\nChoose an option:")
    print("1. Resume Analysis")
    print("2. ATS Score")
    print("3. Interview Preparation")
    print("4. Career Roadmap")

    choice = input("Enter your choice: ")

    if choice == "1":
        print("Resume Analysis feature is coming soon.")

    elif choice == "2":
        print("ATS Score Checker is coming soon.")

    elif choice == "3":
        print("Interview Preparation feature is coming soon.")

    elif choice == "4":
        print("Career Roadmap feature is coming soon.")

    else:
        print("Invalid choice!")


welcome()
get_user_name()