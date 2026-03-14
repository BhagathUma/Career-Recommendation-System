import boto3
import pandas as pd
from io import StringIO

s3 = boto3.client("s3")

bucket_name = "career-recommendation-system-data"

occupation_obj = s3.get_object(
    Bucket=bucket_name,
    Key="raw_data/Occupation Data.txt"
)

occupation_df = pd.read_csv(
    StringIO(occupation_obj["Body"].read().decode("utf-8")),
    sep="\t"
)

skills_obj = s3.get_object(
    Bucket=bucket_name,
    Key="raw_data/Skills.txt"
)

skills_df = pd.read_csv(
    StringIO(skills_obj["Body"].read().decode("utf-8")),
    sep="\t"
)

# print("Occupations Data:")
# print(occupation_df.head())

# print("Skills Data:")
# print(skills_df.head())

occupations = occupation_df[["O*NET-SOC Code", "Title"]]

skills = skills_df[
    (skills_df["Scale ID"] == "IM")
][["O*NET-SOC Code", "Element Name", "Data Value"]]

merged = pd.merge(
    skills,
    occupations,
    on="O*NET-SOC Code"
)

print(merged.head())
merged.to_csv("data/merged_skills.csv", index=False)









filtered = merged[merged["Data Value"] >= 3]
career_groups = filtered.groupby("Title")["Element Name"].apply(list)
career_skills = career_groups.to_dict()


career_skills = {
    career: list(set(skills))
    for career, skills in career_skills.items()
}

import json

with open("data/career_skills.json", "w") as f:
    json.dump(career_skills, f, indent=4)


s3.upload_file(
    "data/career_skills.json",
    bucket_name,
    "processed_data/career_skills.json"
)


for career, skills in list(career_skills.items())[:5]:
    print(career)
    print(skills)
    print()