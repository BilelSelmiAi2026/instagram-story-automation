# 🤖 Instagram Story Automation Bot

A production-ready Python application that automatically collects news articles, summarizes them using Natural Language Processing (NLP), generates professional Instagram Story slides, uploads them to Cloudinary, and publishes them to Instagram.

The project demonstrates modern Python software engineering, object-oriented design, NLP, image processing, cloud integration, Docker, and automation.

---

## 🚀 Features

### 📰 Content Collection

- Collect articles from RSS feeds
- Extract the full article content
- Extract high-resolution featured images
- Automatically process the latest news article

### 🧠 NLP Summarization

Supports multiple extractive summarization algorithms:

- TextRank
- SumBasic
- KL-Sum

The summarization engine is built using the Factory Pattern, making it easy to add additional algorithms such as GPT or other LLMs.

### 🖼 Image Processing

- Download article images
- Resize images to Instagram Story format (1080 × 1920)
- Apply a dark overlay for improved readability
- Render article title and summary onto the image
- Generate polished Story slides

### 📱 Story Generation

- Automatically split long summaries into multiple Story slides
- Create Story carousels
- Display article title
- Display article source
- Display slide numbering

### ☁ Cloud Integration

- Upload Story slides to Cloudinary
- Receive public HTTPS URLs
- Ready for Instagram Graph API publishing

### 📤 Instagram Publishing

- Instagram publishing service
- Dry-run mode for safe testing
- Ready for Meta Graph API integration

### ⚙ Reliability

- Duplicate article detection
- Environment-based configuration
- Docker support
- Modular architecture
- Easily extensible

---

# 🏗 Architecture

```text
                    RSS Feed
                        │
                        ▼
                RSS Collector
                        │
                        ▼
            Article Text Extractor
                        │
                        ▼
           High Resolution Image Extractor
                        │
                        ▼
               Summarizer Factory
        ┌────────────┬────────────┬────────────┐
        ▼            ▼            ▼
     TextRank     SumBasic      KL-Sum
                        │
                        ▼
               Image Downloader
                        │
                        ▼
            Story Image Processor
                        │
                        ▼
           Story Slide Generator
                        │
                        ▼
        Story Carousel Generator
                        │
                        ▼
            Cloudinary Uploader
                        │
                        ▼
           Instagram Publisher
```

---

# 🛠 Technologies

## Programming Language

- Python 3.12

## NLP

- Sumy
- NLTK

## Article Extraction

- Newspaper3k
- BeautifulSoup4
- Feedparser

## Image Processing

- Wand
- ImageMagick

## Cloud

- Cloudinary

## Deployment

- Docker

## Networking

- Requests

---

# 🎯 Software Engineering Concepts

This project demonstrates:

- Object-Oriented Programming (OOP)
- Encapsulation
- Inheritance
- Abstract Base Classes
- Factory Pattern
- Strategy Pattern
- Dependency Injection
- SOLID Principles
- Modular Design
- Docker Containerization

---

# 📂 Project Structure

```text
instagram-story-bot/
│
├── Dockerfile
├── .dockerignore
├── .gitignore
├── .env.example
├── README.md
├── requirements.txt
├── config.py
├── main.py
│
├── src/
│   ├── collectors/
│   ├── summarizers/
│   ├── images/
│   ├── publishing/
│   └── storage/
│
├── data/
│   ├── input/
│   ├── output/
│   └── history/
│
├── test_rss.py
├── test_article_extractor.py
├── test_article_image_extractor.py
├── test_cloudinary_uploader.py
└── test_instagram_publisher.py
```

---

# ⚙ Installation

Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/instagram-story-bot.git

cd instagram-story-bot
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate it

### macOS / Linux

```bash
source .venv/bin/activate
```

### Windows

```bash
.venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Configuration

Create your environment file

```bash
cp .env.example .env
```

Fill in the required values

```env
INSTAGRAM_ACCOUNT_ID=your_instagram_account_id

INSTAGRAM_ACCESS_TOKEN=your_instagram_access_token

INSTAGRAM_API_VERSION=v24.0

INSTAGRAM_DRY_RUN=true

CLOUDINARY_CLOUD_NAME=your_cloud_name

CLOUDINARY_API_KEY=your_cloudinary_api_key

CLOUDINARY_API_SECRET=your_cloudinary_api_secret
```

---

# ▶ Running Locally

Run the complete pipeline

```bash
python main.py
```

---

# 🐳 Docker

Build the Docker image

```bash
docker build -t instagram-story-bot .
```

Run the container

```bash
docker run --rm --env-file .env instagram-story-bot
```

---

# 🔄 Pipeline

```text
Collect RSS Article
        │
        ▼
Extract Full Article
        │
        ▼
Summarize Article
        │
        ▼
Extract High Resolution Image
        │
        ▼
Download Image
        │
        ▼
Resize Image
        │
        ▼
Generate Story Slides
        │
        ▼
Generate Story Carousel
        │
        ▼
Upload to Cloudinary
        │
        ▼
Publish to Instagram
```

---

# 📸 Example Output

The application automatically generates:

- Instagram Story slides
- Story carousels
- Cloudinary-hosted images
- Instagram-ready Stories

*(Screenshots coming soon.)*

---

# 🚀 Future Improvements

- GPT / OpenAI Summarizer
- LangChain Integration
- Multiple RSS Feeds
- AI-generated Images
- PostgreSQL Database
- Render Cron Deployment
- Telegram Notifications
- Analytics Dashboard
- Multi-language Support
- AI-generated Story Titles
- Automatic Hashtag Generation

---

# 📈 Skills Demonstrated

This project demonstrates experience with:

- Python
- Object-Oriented Programming
- Software Architecture
- Design Patterns
- NLP
- Automation
- Docker
- REST APIs
- Cloud Services
- Image Processing
- Environment Configuration
- Production Deployment

---

# 👨‍💻 Author

**Bilel Selmi**

Senior iOS Engineer transitioning into AI Engineering.

### Technologies

- Python
- AI Engineering
- Swift
- SwiftUI
- FastAPI
- Docker
- NLP
- REST APIs
- Computer Vision
- Mobile Development

---

# 📄 License

MIT License

---

## ⭐ Project Roadmap

- ✅ RSS Collector
- ✅ Full Article Extraction
- ✅ Multiple Summarization Algorithms
- ✅ Image Downloader
- ✅ Story Image Processor
- ✅ Story Slide Generator
- ✅ Story Carousel Generator
- ✅ Cloudinary Upload
- ✅ Docker Support
- ⏳ Instagram Graph API Publishing (awaiting Meta developer account verification)
- ⏳ Render Deployment
- ⏳ Automatic Scheduling
- ⏳ GPT Summarizer