Ycseek - For scrapping forum websites, Hackernews here (https://news.ycombinator.com/),
A lightweight web crawling search engine built with Python and Flask

Live Demo: https://ycseek.onrender.com

⚠️ Hosted on Render's free tier— the site may take 30–60 seconds to wake up on first visit due to inactivity sleep. Just wait, it will load!,
The inactivity issue can be resolved by use of "Uptimerbot".

What it does

Ycseek crawls websites, stores the data in MongoDB, and lets you search through it via a clean web interface. Currently crawling Hacker News(news.ycombinator.com).

How it works
Crawler (Python crawls pages)  ->  MongoDB Atlas (stores data)  ->  Flask App (queries DB)   ->  User Search (shows results)


CMFR flow,

Crawler visits pages, extracts title, URL, and description,

MongoDB Atlas stores all crawled data in the cloud,

Flask app takes your search query and runs a full-text search on the database,

Results are displayed back to you instantly.

## Project Structure

| File/Folder | Purpose |
|---|---|
| `app.py` | Flask app entry point |
| `requirements.txt` | Dependencies |
| `crawler/testcrawler3.py` | Web crawler |
| `routes/search.py` | Search route and MongoDB query |
| `templates/search.html` | Home search page |
| `templates/search_results.html` | Results page |
| `templates/layout.html` | Base layout |
| `templates/includes/` | Navbar and messages |


Tech Stack
LayerTechnologyBackendPython, FlaskCrawlerRequests, BeautifulSoup4DatabaseMongoDB AtlasDeploymentRenderEnvironmentpython-dotenv

Run locally-


1. Clone the repo -> bashgit clone https://github.com/MayankTiwari005/Ycseek.git

    cd Ycseek
3. Install dependencies -> bashpip install -r requirements.txt

4. Create a .env file

    MONGODB_URI=your_mongodb_connection_string

    SECRET_KEY=your_secret_key

5. Run the crawler to populate data (Create a MongoDB Atlas account if not have) 

    bashpython crawler/testcrawler3.py

7. Start the Flask app
    bashpython app.py
    Visit http://localhost:5000 in your device loacally

Add more data

Just run the crawler anytime, or increase the depth:

bashpython crawler/testcrawler3.py

No duplicates — the crawler uses upsert so running it multiple times is safe.

Made by

Mayank Tiwari

https://github.com/MayankTiwari005
