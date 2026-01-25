import json
import logging
import os
from datetime import datetime

import requests
from dotenv import load_dotenv

from models.news_article import NewsArticle
from utils.singleton_meta import SingletonMeta

load_dotenv()

logger = logging.getLogger(__name__)


class AiService(metaclass=SingletonMeta):
    """Class responsible for communicating with external AI API.

    Chosen AI API is: GROQ, free model llama-3.1-8b-instant
    """

    GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
    MODEL = "llama-3.1-8b-instant"

    def __init__(self):
        logger.debug("AI Service initialized.")
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            logger.error("GROQ_API_KEY not found in environment")
            raise RuntimeError("GROQ_API_KEY not found in environment")

    def filter_news(
        self, news: list[NewsArticle], top_k: int = 10
    ) -> list[NewsArticle]:
        """Filteres a list of news, and returns only those that could affect the market the most.

        Args:
            news (list[NewsArticle]): list of all news articles to filter
            top_k (int, optional): Number of news that are left after filtering. Defaults to 10.

        Returns:
            list[NewsArticle]: list of articles most likely to affect the market
        """
        logger.debug("Filtering news articles using AI service.")
        prompt = self._build_prompt(news, top_k)
        response = self._call_groq(prompt)

        return self._parse_response(response)

    def _build_prompt(self, news: list[NewsArticle], top_k: int) -> str:
        """Builds the prompt sent to the AI model.

        Args:
            news (list[NewsArticle]): list of news articles to filter
            top_k (int): Number of news that are left after filtering

        Returns:
            str: Promt string that is to be sent to the AI model
        """
        logger.debug("Building prompt for AI model.")
        news_dicts = [article.to_dict() for article in news]
        return f"""
You are a financial markets AI.

You will receive a list of recent financial news articles.
Each article has:
- pubTime
- title
- summary
- url
- ticker

Your task:
Select the {top_k} articles that are MOST LIKELY to significantly impact stock prices in the upcoming days/weeks.

Return ONLY a JSON array of article objects.
Each object MUST contain exactly:
pubTime, title, summary, url, ticker

DO NOT add explanations.
DO NOT add extra fields.
DO NOT return text outside JSON.

Articles:
{json.dumps(news_dicts, indent=2, default=str)}
""".strip()

    def _call_groq(self, prompt: str) -> str:
        """Sends a request to an AI model

        Args:
            prompt (str): Promt to be sent

        Returns:
            str: Response from the AI model
        """
        logger.debug("Calling GROQ AI model.")
        payload = {
            "model": self.MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0,
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        response = requests.post(
            self.GROQ_API_URL,
            json=payload,
            headers=headers,
            timeout=30,
        )
        response.raise_for_status()

        return response.json()["choices"][0]["message"]["content"]

    def _parse_response(self, response: str) -> list[NewsArticle]:
        """Since AI doesn't know about internal data classes, parses the response to a list of NewsArticles

        Args:
            response (str): Response string from the AI model

        Raises:
            ValueError: Raised when the response is not valid JSON or doesn't match expected format
            RuntimeError: Raised if any type error occurs during parsing

        Returns:
            list[NewsArticle]: List of NewsArticle objects parsed from the response
        """
        try:
            logger.debug("Parsing response from AI model.")
            data = json.loads(response)
            if not isinstance(data, list):
                logger.error("AI response is not a list")
                raise ValueError("AI response is not a list")

            articles: list[NewsArticle] = []

            for item in data:
                if not isinstance(item, dict):
                    logger.error("Article item is not a dict")
                    raise ValueError("Article item is not a dict")

                pub_time = item.get("pubTime")
                if isinstance(pub_time, str):
                    pub_time = datetime.fromisoformat(pub_time.replace("Z", "+00:00"))

                articles.append(
                    NewsArticle(
                        title=item.get("title", ""),
                        summary=item.get("summary", ""),
                        pub_time=pub_time,
                        url=item.get("url"),
                        ticker=item.get("ticker", ""),
                    )
                )

            return articles

        except Exception as e:
            logger.error(f"Error parsing AI response: {e}")
            raise RuntimeError(f"Invalid AI response: {response}") from e
