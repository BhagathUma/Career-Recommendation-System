import json

with open("data/career_skills.json", "r") as f:
    career_skills = json.load(f)


def recommend_careers(user_skills, top_n=5):

    scores = {}

    for career, skills in career_skills.items():

        matched = set(user_skills).intersection(set(skills))

        score = len(matched) / len(skills)

        scores[career] = score

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    return ranked[:top_n]

    return ranked

if __name__ == "__main__":

    user_skills = [
        "Programming",
        "Statistics"
    ]

    recommendations = recommend_careers(user_skills)

    for career, score in recommendations[:10]:
        print(career, score)