# LinkedIn-Profiles-scraping

This is a Python script for scraping LinkedIn profiles to extract information about a user's work experience, education, and skills. It uses the Selenium and BeautifulSoup libraries to automate the process of logging into LinkedIn and navigating to each user's profile page, and then extracts relevant information using web scraping techniques.
![Alt Text](LinkedIn.jpg)

## Getting Started

1. Install Python 3.x on your machine
2. Clone this repository to your local machine using `git clone https://github.com/T81oub/LinkedIn-Profiles-scraping`
3. Install the required Python packages by running `pip install -r requirements.txt`
4. Download the latest version of ChromeDriver from https://sites.google.com/a/chromium.org/chromedriver/downloads and extract the executable to a directory on your machine
5. Update the `path` variable in the `main.py` file to point to the location of your ChromeDriver executable
6. Create a `login.txt` file in the same directory as `main.py` with your LinkedIn account login credentials in the format `email\npassword`
7. Run `python main.py` to start the scraper and follow the prompts to input the LinkedIn profile URLs you want to scrape

## Usage

This script can be used to extract information from LinkedIn profiles for research or analysis purposes. However, please use this tool responsibly and within the terms of service of LinkedIn. This tool should not be used for spamming or other unethical purposes.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.
