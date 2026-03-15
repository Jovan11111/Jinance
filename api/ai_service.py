import json
import logging
import os
import re
import time
from datetime import datetime

import requests
from dotenv import load_dotenv

from models.news_article import NewsArticle
from utils.singleton_meta import SingletonMeta

load_dotenv()

logger = logging.getLogger(__name__)


class AiService(metaclass=SingletonMeta):
    """Class responsible for communicating with external AI API.

    Chosen AI API is: GROQ, free model llama-3.1-8b-instant.
    """

    GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
    MODEL = "llama-3.1-8b-instant"

    BATCH_SIZE = 50
    MAX_RETRIES = 3

    def __init__(self):
        logger.debug("AI Service initialized.")
        self.__api_key = os.getenv("GROQ_API_KEY")

        if not self.__api_key:
            logger.error("GROQ_API_KEY not found in environment")
            raise RuntimeError("GROQ_API_KEY not found in environment")

    def filter_news(
        self, news: list[NewsArticle], top_k: int = 10
    ) -> list[NewsArticle]:
        """Filter a list of news, and return only those that could affect the market the most.

        Args:
            news (list[NewsArticle]): List of all news articles to filter.
            top_k (int): Number of news that are left after filtering. Defaults to 10.

        Returns:
            list[NewsArticle]: List of articles most likely to affect the market.
        """
        logger.debug("Filtering news with AI.")

        if len(news) <= top_k:
            return news

        summary_map = {n.url: n.summary for n in news}
        try:
            if len(news) <= self.BATCH_SIZE:
                prompt = self.__build_prompt(news, top_k)
                response = self.__call_groq(prompt)
                return self.__parse_response(response, summary_map)

            logger.debug("Entering batch processing mode for AI filtering.")
            finalists = []
            for i in range(0, len(news), self.BATCH_SIZE):
                batch = news[i : i + self.BATCH_SIZE]
                prompt = self.__build_prompt(batch, top_k)
                response = self.__call_groq(prompt)
                parsed = self.__parse_response(response, summary_map)
                finalists.extend(parsed)
                time.sleep(20)

            time.sleep(20)
            prompt = self.__build_prompt(finalists, top_k)
            response = self.__call_groq(prompt)

            return self.__parse_response(response, summary_map)

        except Exception as e:
            logger.warning(f"AI filtering failed: {e}")
            return self.__fallback(news, top_k)

    def __build_prompt(self, news: list[NewsArticle], top_k: int) -> str:
        """Builds the prompt sent to the AI model.

        Args:
            news (list[NewsArticle]): List of news articles to filter.
            top_k (int): Number of news that are left after filtering.

        Returns:
            str: Prompt string.
        """
        logger.debug("Building prompt for AI model.")
        news_dicts = []

        for article in news:
            news_dicts.append(
                {
                    "pubTime": article.pub_time.isoformat(),
                    "title": article.title,
                    "url": article.url,
                    "ticker": article.ticker,
                }
            )

        prompt = f"""
You are a financial markets AI.

Select the {top_k} news articles MOST likely to impact stock prices.
Return ONLY valid JSON array in the same format that is given to you.

Each object must contain exactly:
- pubTime
- title
- url
- ticker

Return exactly {top_k} articles if {top_k} are available.
If fewer than {top_k} articles are provided, return all of them.

Articles:
{json.dumps(news_dicts)}
""".strip()

        return prompt

    def __call_groq(self, prompt: str) -> str:
        """Send a request to an AI model.

        Args:
            prompt (str): Prompt to be sent.

        Returns:
            str: Response from the AI model.
        """
        logger.debug("Calling GROQ API.")
        payload = {
            "model": self.MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a financial news ranking AI. Output only valid JSON.",
                },
                {"role": "user", "content": prompt},
            ],
            "temperature": 0,
        }

        headers = {
            "Authorization": f"Bearer {self.__api_key}",
            "Content-Type": "application/json",
        }

        for attempt in range(self.MAX_RETRIES):
            try:
                response = requests.post(
                    self.GROQ_API_URL,
                    json=payload,
                    headers=headers,
                    timeout=(5, 20),
                )

                response.raise_for_status()
                content = response.json()["choices"][0]["message"]["content"]
                return content

            except requests.RequestException as e:
                logger.warning(f"GROQ call failed attempt {attempt+1}: {e}")
                if attempt == self.MAX_RETRIES - 1:
                    raise

                time.sleep(2 ** (attempt + 1))

    def __extract_json(self, text: str):
        """Extract JSON from the response from AI.

        If non valid json is returned, find a substring from 1st [ to last ]

        Args:
            text (str): Response from AI model.

        Returns:
            JSON formatted response or None if no valid JSON found.
        """
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass

        match = re.search(r"\[.*\]", text, re.DOTALL)

        if match:
            try:
                return json.loads(match.group(0))
            except json.JSONDecodeError:
                pass

        return None

    def __parse_response(self, response: str, summary_map: dict) -> list[NewsArticle]:
        """Parse the response to a list of NewsArticles, since AI doesn't know about internal data classes.

        Args:
            response (str): Response string from the AI model.
            summary_map (dict): Mapping of url -> summary to restore original summaries.

        Returns:
            list[NewsArticle]: List of NewsArticle objects parsed from the response.
        """
        data = self.__extract_json(response)
        if data is None:
            raise RuntimeError("AI returned invalid JSON")

        articles: list[NewsArticle] = []
        for item in data:
            if not isinstance(item, dict):
                continue

            url = item.get("url")

            if url not in summary_map:
                continue

            pub_time = item.get("pubTime")

            if isinstance(pub_time, str):
                try:
                    pub_time = datetime.fromisoformat(pub_time.replace("Z", "+00:00"))
                except Exception:
                    pub_time = None

            articles.append(
                NewsArticle(
                    title=item.get("title", ""),
                    summary=summary_map.get(url, ""),
                    pub_time=pub_time,
                    url=url,
                    ticker=item.get("ticker", ""),
                )
            )

        return articles

    def __fallback(self, news: list[NewsArticle], top_k: int) -> list[NewsArticle]:
        """Return latest top_k articles if groq is not responding.

        This exists so the whole app doesn't crash when groq doesn't work.

        Args:
            news (list[NewsArticle]): list of all news articles to filter
            top_k (int, optional): Number of news that are left after filtering. Defaults to 10.

        Returns:
            list[NewsArticle]: First {top_k} articles from the input list, sorted by publish time descending.
        """
        logger.warning("Using fallback news selection")
        return sorted(news, key=lambda x: x.pub_time, reverse=True)[:top_k]
