import argparse

from collecting.scraper.reddit_scraper.reddit_scraper import RedditScraper

parser = argparse.ArgumentParser(description="Crawl Reddit comments.")
parser.add_argument("--file-path", type=str, required=True)
parser.add_argument("--target-category", type=str, required=True)
parser.add_argument("--output-folder", type=str, required=True)

if __name__ == "__main__":
    args = parser.parse_args()

    reddit_scraper = RedditScraper(args.file_path, args.target_category, args.output_folder)
    reddit_scraper.main()
