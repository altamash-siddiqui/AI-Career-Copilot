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
    print("5. Career History")
    print("6. Exit")

    return input("Enter your choice: ")


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

    elif interest == "web" or interest == "web development":
        print("\nSuggested Career Roadmap:")
        print("- Learn HTML")
        print("- Learn CSS")
        print("- Learn JavaScript")

    elif interest == "python" or interest == "python programming":
        print("\nSuggested Career Roadmap:")
        print("- Learn Python Basics")
        print("- Learn Object-Oriented Programming")
        print("- Build Python Projects")

    elif interest == "data science" or interest == "datascience":
        print("\nSuggested Career Roadmap:")
        print("- Learn Python")
        print("- Learn Pandas")
        print("- Learn SQL")


def resume_analysis():

    skills = input("Enter your skills (comma separated): ")

    skills_list = skills.split(",")

    print("\n========== Resume Analysis ==========")

    print("\nYour Skills:")
    for skill in skills_list:
        print("-", skill.strip())

    print("\nTotal Skills:", len(skills_list))

    if len(skills_list) >= 5:
        print("✅ Good! Your resume has a decent number of skills.")
    else:
        print("⚠ Add more skills to strengthen your resume.")

    required_skills = ["python", "git", "sql"]

    print("\nSkill Check:")

    user_skills = [skill.strip().lower() for skill in skills_list]

    for skill in required_skills:
        if skill in user_skills:
            print(f"✅ {skill.capitalize()} - Available")
        else:
            print(f"❌ {skill.capitalize()} - Missing")


def ats_score():

    score = 0

    skills = input("Enter your skills (comma separated): ").lower()

    if "python" in skills:
        score += 25

    if "git" in skills:
        score += 25

    if "sql" in skills:
        score += 25

    if "html" in skills or "css" in skills:
        score += 25

    print("\n========== ATS SCORE ==========")
    print(f"Your ATS Score: {score}/100")

    if score >= 75:
        print("✅ Excellent Resume")
    elif score >= 50:
        print("👍 Good Resume")
    else:
        print("⚠ Improve your Resume")


def interview_preparation():

    print("\n========== Interview Preparation ==========")

    questions = [
        "What is Python?",
        "What is a List in Python?",
        "What is a Function?"
    ]

    answers = [
        "Python is a high-level, interpreted programming language.",
        "A List is a collection used to store multiple items.",
        "A Function is a reusable block of code that performs a specific task."
    ]

    score = 0

    for i in range(len(questions)):

        print(f"\nQuestion {i + 1}")
        print(questions[i])

        user_answer = input("Your Answer: ")

        if len(user_answer.strip()) > 10:
            score += 1

        print("\nSample Answer:")
        print(answers[i])

    print(f"\n🏆 Your Practice Score: {score}/{len(questions)}")
    print("🎉 Interview Practice Completed!")

def career_history():

    print("\n========== Career History ==========")

    try:
        file = open("career_data.txt", "r")

        data = file.read()

        if data.strip() == "":
            print("No career history found.")
        else:
            print(data)

        file.close()

    except FileNotFoundError:
        print("No career history found.")


def process_choice(choice):

    if choice == "1":

        interest = get_career_interest()

        file = open("career_data.txt", "a")
        file.write(f"Name: {name}, Career: {interest}\n")
        file.close()

        print("\n✅ Career saved successfully!")

        show_career_roadmap(interest)

    elif choice == "2":
        resume_analysis()

    elif choice == "3":
        ats_score()

    elif choice == "4":
        interview_preparation()

    elif choice == "5":
        career_history()

    elif choice == "6":
        print("\nThank you for using AI Career Copilot!")

    else:
        print("\n❌ Invalid choice! Please select 1 to 6.")


welcome()

name = get_user_name()

print(f"\nWelcome, {name}")

while True:

    choice = show_menu()

    if choice == "6":
        print("\nThank you for using AI Career Copilot!")
        break

    process_choice(choice)