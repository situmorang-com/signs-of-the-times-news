# Signs of the Times News Filtering System

This system is designed to filter news articles related to "signs of the times" that align with the Adventist view of the Sunday law. It allows users to search and filter news articles based on different criteria, such as keywords, date range, sentiment, and relevance score.

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
  - [Running the Application](#running-the-application)
  - [Data Collection](#data-collection)
  - [Advanced Search and Filtering](#advanced-search-and-filtering)
- [File Structure](#file-structure)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Data Collection**: Collects news articles from an API based on user-provided keywords.
- **NLP Filtering**: Uses Natural Language Processing (NLP) to filter articles based on relevance to "signs of the times" and Sunday law.
- **Sentiment Analysis**: Analyzes sentiment (positive, negative, neutral) of articles to provide more insightful filtering.
- **Advanced Search and Filtering**: Allows users to filter articles based on keywords, date range, sentiment, and relevance score.
- **User Feedback**: Provides visual feedback on the web interface for data collection and filtering actions.

## Getting Started

### Prerequisites

Before you begin, ensure you have met the following requirements:

- **Python 3.6+** installed on your system.
- **Flask** for running the web application.
- **SQLite** for storing and managing the news articles.
- **Dotenv** to manage environment variables securely.
- **Required Python Libraries**: Install dependencies listed in `requirements.txt`.

### Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/yourusername/signs-of-the-times-news-filtering.git
   cd signs-of-the-times-news-filtering
