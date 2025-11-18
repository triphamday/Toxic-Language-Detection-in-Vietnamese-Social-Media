import json
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


from utils import load_json


def plot_ratio_of_similarity_to_difference(file_path: str, label: str):
    data = load_json(file_path)

    similarity_count = 0
    difference_count = 0
    
    for item in data:
        if item.get(f"{label}_deepseek") == None:
            similarity_count += 1
        else:
            difference_count += 1

    plt.figure(figsize=(8, 6))
    plt.pie(
        [similarity_count, difference_count],
        labels=["Similar", "Different"],
        autopct="%1.1f%%",
        colors=sns.color_palette("pastel"),
        startangle=140
    )
    plt.title("Ratio of Similarity to Difference") 
    plt.axis("equal")
    plt.show()


def plot_number_of_similar_comments_with_checker_each_annotator(file_path: str, label: str):
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    deepseek_count = 0
    _count = 0
    _count = 0
    
    for item in data:
        if item.get(f"{label}_deepseek") != None:
            if item.get(f"{label}_deepseek") == item.get(f"{label}"):
                deepseek_count += 1
            if item.get(f"{label}_") == item.get(f"{label}"):
                _count += 1
            if item.get(f"{label}_") == item.get(f"{label}_"):
                _count += 1

    plt.figure(figsize=(8, 6))
    sns.barplot(
        x=["Deepseek", "_", "_"],
        y=[deepseek_count, _count, _count],
        palette=sns.color_palette("pastel")
    )
    plt.title("Number of comments that are similar to the checker")
    plt.ylabel("Number of Comments")
    plt.show()

def plot_number_of_different_comments_each_category(file_path: str, label: str):
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    categories = {}
    for item in data:
        if item.get(f"{label}_deepseek") != None:
            try:
                categories[item["category"]] += 1
            except KeyError:
                categories[item["category"]] = 1

    df = pd.DataFrame(list(categories.items()), columns=["Category", "Count"])
    df = df.sort_values(by="Count", ascending=False)
    plt.figure(figsize=(10, 6))
    sns.barplot(
        x="Category",
        y="Count",
        data=df,
        palette=sns.color_palette("pastel")
    )
    plt.title("Number of Different Comments in Each Category")
    plt.ylabel("Number of Comments")
    plt.xticks(rotation=45)
    plt.show()

def print_different_comments(file_path: str):
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    return pd.DataFrame(data)