from datetime import datetime, timezone

import pytest
import requests

from api.ai_service import AiService
from models.news_article import NewsArticle


class TestAiService:
    """Test class for AiService."""

    @staticmethod
    def _create_service(mocker) -> AiService:
        AiService.clear()
        mocker.patch("api.ai_service.os.getenv", return_value="test-api-key")
        return AiService()

    def test__init__without_api_key__raises_runtime_error(self, mocker):
        """Check that service initialization fails when GROQ_API_KEY is missing."""
        AiService.clear()
        mocker.patch("api.ai_service.os.getenv", return_value=None)

        with pytest.raises(RuntimeError, match="GROQ_API_KEY"):
            AiService()

    def test__filter_news__small_input_returns_same_list(self, mocker):
        """Check that filter_news returns input unchanged when news count is <= top_k."""
        service = self._create_service(mocker)
        news = [
            NewsArticle(
                "Title 1",
                "Summary 1",
                datetime(2026, 4, 1, 10, 0, tzinfo=timezone.utc),
                "https://news1.com",
                "TCK1",
            ),
            NewsArticle(
                "Title 2",
                "Summary 2",
                datetime(2026, 4, 1, 9, 0, tzinfo=timezone.utc),
                "https://news2.com",
                "TCK2",
            ),
        ]

        result = service.filter_news(news, top_k=2)

        assert result == news

    def test__filter_news__single_batch_uses_groq_and_parse(self, mocker):
        """Check that filter_news calls GROQ and parse methods in single-batch mode."""
        service = self._create_service(mocker)
        news = [
            NewsArticle(
                f"Title {i}",
                f"Summary {i}",
                datetime(2026, 4, 1, 10, 0, tzinfo=timezone.utc),
                f"https://news{i}.com",
                f"TCK{i}",
            )
            for i in range(3)
        ]

        expected = [news[0], news[2]]
        call_mock = mocker.patch.object(
            service,
            "_AiService__call_groq",
            return_value='[{"url":"https://news0.com"}]',
        )
        parse_mock = mocker.patch.object(
            service, "_AiService__parse_response", return_value=expected
        )

        result = service.filter_news(news, top_k=2)

        assert result == expected
        call_mock.assert_called_once()
        parse_mock.assert_called_once()

    def test__filter_news__call_failure_uses_fallback(self, mocker):
        """Check that filter_news falls back to latest articles when AI call fails."""
        service = self._create_service(mocker)
        news = [
            NewsArticle(
                "Older",
                "Summary 1",
                datetime(2026, 4, 1, 9, 0, tzinfo=timezone.utc),
                "https://old.com",
                "TCK1",
            ),
            NewsArticle(
                "Newer",
                "Summary 2",
                datetime(2026, 4, 1, 11, 0, tzinfo=timezone.utc),
                "https://new.com",
                "TCK2",
            ),
        ]

        mocker.patch.object(
            service, "_AiService__call_groq", side_effect=Exception("GROQ unavailable")
        )

        result = service.filter_news(news, top_k=1)

        assert len(result) == 1
        assert result[0].url == "https://new.com"

    def test__call_groq__request_fails_once_then_succeeds(self, mocker):
        """Check that call_groq retries after request error and returns content on next success."""
        service = self._create_service(mocker)

        successful_response = mocker.MagicMock()
        successful_response.raise_for_status.return_value = None
        successful_response.json.return_value = {
            "choices": [{"message": {"content": "[]"}}]
        }

        post_mock = mocker.patch(
            "api.ai_service.requests.post",
            side_effect=[requests.RequestException("timeout"), successful_response],
        )
        sleep_mock = mocker.patch("api.ai_service.time.sleep")

        result = service._AiService__call_groq("prompt")

        assert result == "[]"
        assert post_mock.call_count == 2
        sleep_mock.assert_called_once_with(2)

    def test__call_groq__all_retries_fail_raises(self, mocker):
        """Check that call_groq raises after all retry attempts fail."""
        service = self._create_service(mocker)

        mocker.patch(
            "api.ai_service.requests.post",
            side_effect=requests.RequestException("still failing"),
        )
        sleep_mock = mocker.patch("api.ai_service.time.sleep")

        with pytest.raises(requests.RequestException):
            service._AiService__call_groq("prompt")

        assert sleep_mock.call_count == 2

    def test__parse_response__skips_invalid_items_and_restores_summary(self, mocker):
        """Check that parse_response keeps valid known URLs and restores summary from map."""
        service = self._create_service(mocker)
        response = """
[
  {"pubTime":"2026-04-01T10:00:00Z","title":"Valid","url":"https://ok.com","ticker":"TCK1"},
  {"pubTime":"2026-04-01T11:00:00Z","title":"Unknown","url":"https://missing.com","ticker":"TCK2"},
  "not-a-dict"
]
"""
        summary_map = {"https://ok.com": "Restored summary"}

        result = service._AiService__parse_response(response, summary_map)

        assert len(result) == 1
        assert result[0].url == "https://ok.com"
        assert result[0].summary == "Restored summary"
        assert result[0].title == "Valid"
        assert result[0].ticker == "TCK1"

    def test__extract_json__extracts_array_from_wrapped_text(self, mocker):
        """Check that extract_json can recover JSON array from non-JSON wrapper text."""
        service = self._create_service(mocker)
        text = 'AI said: [{"url":"https://ok.com","title":"t","pubTime":"2026-04-01T10:00:00Z","ticker":"TCK"}] End.'

        result = service._AiService__extract_json(text)

        assert isinstance(result, list)
        assert result[0]["url"] == "https://ok.com"
