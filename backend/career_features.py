import json


class CareerFeatures:

    def resume_analysis(self):

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

        user_skills = [
            skill.strip().lower()
            for skill in skills_list
        ]

        for skill in required_skills:

            if skill in user_skills:
                print(f"✅ {skill.capitalize()} - Available")
            else:
                print(f"❌ {skill.capitalize()} - Missing")


    def ats_score(self):

        score = 0

        skills = input(
            "Enter your skills (comma separated): "
        ).lower()

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


    def interview_preparation(self):

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

        print(
            f"\n🏆 Your Practice Score: "
            f"{score}/{len(questions)}"
        )

        print("🎉 Interview Practice Completed!")


    def career_history(self):

        print("\n========== Career History ==========")

        try:

            with open("career_data.json", "r") as file:
                careers = json.load(file)

            found = False

            for career in careers:

                # Show only current user's records
                if career.get("user") != self.current_user:
                    continue

                print("\n------------------------------")

                print(
                    f"Name       : {career['name']}"
                )

                print(
                    f"Career     : {career['career']}"
                )

                if "timestamp" in career:

                    print(
                        f"Created On : {career['timestamp']}"
                    )

                if career.get("favorite", False):

                    print("⭐ Favorite")

                print("------------------------------")

                found = True

            if not found:

                print(
                    "No career history found for "
                    "the current user."
                )

        except FileNotFoundError:

            print("No career history found.")

        except Exception as e:

            print(f"❌ Error: {e}")