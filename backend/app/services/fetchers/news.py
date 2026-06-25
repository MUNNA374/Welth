import logging
import xml.etree.ElementTree as ET
import re
from typing import List, Dict, Any
from backend.app.services.fetchers.base import BaseFetcher

logger = logging.getLogger("welth.fetchers.news")

class FinancialNewsFetcher(BaseFetcher):
    def __init__(self):
        super().__init__(name="financial_news", cache_ttl_seconds=900)

    def _fallback(self) -> List[Dict[str, Any]]:
        return [
            {
                "title": "Fed hints at interest rate cuts in coming quarters",
                "source": "Financial Times",
                "url": "https://ft.com/fed-rates",
                "summary": "The Federal Reserve suggests policy shifts as inflation metrics ease towards targets."
            },
            {
                "title": "Crypto markets rebound as institutional inflow increases",
                "source": "Bloomberg",
                "url": "https://bloomberg.com/crypto",
                "summary": "Bitcoin and Ether lead broad recoveries driven by ETF assets accumulation."
            }
        ]

    async def get_latest_news(self) -> List[Dict[str, Any]]:
        """Fetch latest financial news from Yahoo Finance RSS Feed."""
        try:
            url = "https://finance.yahoo.com/news/rssindex"
            
            # Since fetch standardly decodes json, we perform raw http request for XML
            import httpx
            async with httpx.AsyncClient(timeout=10.0) as client:
                headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                xml_data = response.text
                
            root = ET.fromstring(xml_data)
            channel = root.find("channel")
            items = channel.findall("item") if channel is not None else []
            
            news_list = []
            for item in items[:6]:
                title_el = item.find("title")
                link_el = item.find("link")
                desc_el = item.find("description")
                
                title = title_el.text if title_el is not None else ""
                link = link_el.text if link_el is not None else ""
                desc = desc_el.text if desc_el is not None else ""
                
                if desc:
                    desc = re.sub('<[^<]+?>', '', desc)
                    
                news_list.append({
                    "title": title,
                    "source": "Yahoo Finance",
                    "url": link,
                    "summary": desc[:150] + "..." if len(desc) > 150 else desc
                })
            
            if news_list:
                return news_list
            return self._fallback()
        except Exception as e:
            logger.warning(f"Failed to fetch live RSS news, using fallback: {e}")
            return self._fallback()
