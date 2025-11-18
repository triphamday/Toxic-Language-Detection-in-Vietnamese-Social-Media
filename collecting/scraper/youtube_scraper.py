import pandas as pd
from tqdm import tqdm
import os
import csv
from dotenv import load_dotenv
from googleapiclient.discovery import build


load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")


class YoutubeScraper():
    def __init__(
        self,
        file_path: str,
        target_category: str,
        output_folder: str
    ):
        data = pd.read_excel(file_path, sheet_name=target_category)
        self.youtube_links = data[(data["Platform"] == "Youtube") & (data["Ghi chú"].isna())]

        self.output_folder = output_folder

        self.youtube = build("youtube", "v3", developerKey=API_KEY)

    def main(self):
        """Scrape all of links in file"""
        for index, link in tqdm(self.youtube_links[["No.", "Link"]].values):
            if "shorts" in link.split("/"):
                video_id = link.split("/")[-1]
            else:
                video_id = link.split("=")[1]
            
            comments = self.get_comments(video_id)
            
            for comment in comments:
                comment["video_id"] = video_id
            
            output_path = os.path.join(self.output_folder, f"youtube_comments_{index}.csv")
            with open(output_path, "a", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=["author", "text", "likeCount", "publishedAt", "video_id"])
                writer.writeheader()
                writer.writerows(comments)

    def get_comments(self, video_id: str):
        """Scrape a link with video id"""
        comments = []
        next_page_token = None
        page = 0

        while True:
            response = self.youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=100,
                pageToken=next_page_token,
                textFormat="plainText"
            ).execute()

            for item in response["items"]:
                top_comment_snippet = item["snippet"]["topLevelComment"]["snippet"]

                comments.append({
                    "author": top_comment_snippet["authorDisplayName"],
                    "text": top_comment_snippet["textDisplay"],
                    "likeCount": top_comment_snippet["likeCount"],
                    "publishedAt": top_comment_snippet["publishedAt"]
                })

                if item["snippet"]["totalReplyCount"] > 0:
                    replies_response = self.youtube.comments().list(
                        part="snippet",
                        parentId=item["snippet"]["topLevelComment"]["id"],
                        maxResults=100
                    ).execute()

                    for reply in replies_response["items"]:
                        reply_snippet = reply["snippet"]
                        comments.append({
                            "author": reply_snippet["authorDisplayName"],
                            "text": reply_snippet["textDisplay"],
                            "likeCount": reply_snippet["likeCount"],
                            "publishedAt": reply_snippet["publishedAt"]
                        })

            next_page_token = response.get("nextPageToken")
            page += 1
            if not next_page_token:
                break

        return comments
