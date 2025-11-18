import pandas as pd
from tqdm import tqdm
import os
import csv

from collecting.scraper.reddit_scraper.yars.src.yars.yars import YARS


class RedditScraper():
    def __init__(
        self,
        file_path: str,
        target_category: str,
        output_folder: str
    ):
        data = pd.read_excel(file_path, sheet_name=target_category)
        self.reddit_links = data[(data["Platform"] == "Reddit") & (data["Ghi chú"].isna())]

        self.output_folder = output_folder

        self.reddit = YARS()

    def main(self):
        """Scrape all of links in file"""
        for index, link in tqdm(self.reddit_links[["No.", "Link"]].values):
            comments = self.get_comments(link)
            comments = self.flatten_comments(comments)

            for comment in comments:
                comment["link"] = link
            
            output_path = os.path.join(self.output_folder, f"reddit_comments_{index}.csv")
            with open(output_path, "a", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=["author", "body", "score", "link"])
                writer.writeheader()
                writer.writerows(comments)
        
    def get_comments(self, permalink: str):
        """Scrape a link"""
        post_details = self.reddit.scrape_post_details(permalink.split("reddit.com")[1])

        if post_details:
            comments = self.flatten_comments(post_details.get("comments"))

        return comments

    def flatten_comments(self, comments):
        new_comments = []
        for comment in comments:
            body = comment.get("body", "")
            
            new_comments.append({
                "author": comment.get("author"),
                "body": body,
                "score": comment.get("score"),
            })

            new_comments.extend(self.flatten_comments(comment.get("replies", [])))

        return new_comments
    