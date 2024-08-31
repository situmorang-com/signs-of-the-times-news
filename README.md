
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
   ```

2. **Create a Virtual Environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**:

   Create a `.env` file in the root directory and add your News API key:

   ```plaintext
   MY_API_KEY=your_news_api_key_here
   ```

5. **Initialize the Database**:

   Run the Flask application to create and initialize the SQLite database:

   ```bash
   python app.py
   ```

## Usage

### Running the Application

1. **Start the Flask Server**:

   ```bash
   python app.py
   ```

   The application will start and run on `http://127.0.0.1:5000/`.

2. **Open Your Browser**:

   Go to `http://127.0.0.1:5000/` to access the web interface.

### Data Collection

- Enter a keyword related to "signs of the times" (e.g., "Sunday law") in the "Collect New Data" form and click "Collect New Data".
- The system will fetch relevant news articles from the News API and save them to the SQLite database.
- A success message will be displayed on the webpage upon successful data collection.

### Advanced Search and Filtering

- Use the **Advanced Search** form to filter news articles based on:
  - **Keyword**: Search for specific words or phrases in the articles.
  - **Date Range**: Filter articles published within a certain period.
  - **Sentiment**: Filter articles based on sentiment (positive, negative, neutral).
- Click "Search" to display the filtered results.

## File Structure

```plaintext
.
├── app.py                  # Main Flask application file
├── data_collection.py      # Script for collecting news data from the News API
├── nlp_filtering.py        # Script for NLP filtering and sentiment analysis
├── alert_system.py         # Script for alerting system (if any)
├── templates/
│   └── index.html          # HTML template for the web interface
├── requirements.txt        # List of Python dependencies
├── .env                    # Environment variables file
└── README.md               # Documentation for the project
```

## Contributing

To contribute to this project:

1. **Fork the Repository**.
2. **Create a New Branch** (`git checkout -b feature-branch`).
3. **Commit Your Changes** (`git commit -m 'Add some feature'`).
4. **Push to the Branch** (`git push origin feature-branch`).
5. **Create a Pull Request**.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
