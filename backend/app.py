def welcome():
    print("=" * 35)
    print("      AI Career Copilot")
    print("=" * 35)


def get_user_name():
    name = input("Enter your name: ")
    return name


def get_career_interest():
    interest = input("Enter your career interest: ")
    return interest


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

    else:
        print("\nSorry, this career is not available yet.")


welcome()

name = get_user_name()
interest = get_career_interest()

interest = interest.lower()

print(f"\nWelcome, {name}")
print(f"Career Interest: {interest}")

show_career_roadmap(interest)