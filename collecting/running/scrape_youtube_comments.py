import argparse

from collecting.scraper.youtube_scraper import YoutubeScraper


parser = argparse.ArgumentParser(description="Crawl Youtube comments.")
parser.add_argument("--file-path", type=str, required=True)
parser.add_argument("--target-category", type=str, required=True)
parser.add_argument("--output-folder", type=str, required=True)


if __name__ == "__main__":
    args = parser.parse_args()

    youtube_scraper = YoutubeScraper(args.file_path, args.target_category, args.output_folder)
    youtube_scraper.main()