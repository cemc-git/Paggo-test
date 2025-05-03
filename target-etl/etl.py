from typing import Any, Dict, List
import httpx

class SourceApiClient:
    SOURCE_URL = "http://source_db_api:8000/data"

    @staticmethod
    async def get_wind_speed_info_from_date(date: str) -> List[Dict[str, Any]]:
        payload = {
            "date": date,
            "wind_speed": True,
            "power": False,
            "ambient_temperature": False
        }
        async with httpx.AsyncClient() as client:
            response = await client.get(SourceApiClient.SOURCE_URL, params=payload)
            response.raise_for_status()
            return response.json()

    @staticmethod
    async def get_power_info_from_date(date: str) -> List[Dict[str, Any]]:
        payload = {
            "date": date,
            "wind_speed": False,
            "power": True,
            "ambient_temperature": False
        }
        async with httpx.AsyncClient() as client:
            response = await client.get(SourceApiClient.SOURCE_URL, params=payload)
            response.raise_for_status()
            return response.json()

    @staticmethod
    async def get_ambient_temperature_from_date(date: str) -> List[Dict[str, Any]]:
        payload = {
            "date": date,
            "wind_speed": False,
            "power": False,
            "ambient_temperature": True
        }
        async with httpx.AsyncClient() as client:
            response = await client.get(SourceApiClient.SOURCE_URL, params=payload)
            response.raise_for_status()
            return response.json()

    @staticmethod
    async def get_full_data_from_date(date: str) -> List[Dict[str, Any]]:
        payload = {
            "date": date,
            "wind_speed": True,
            "power": True,
            "ambient_temperature": True
        }
        async with httpx.AsyncClient() as client:
            response = await client.get(SourceApiClient.SOURCE_URL, params=payload)
            response.raise_for_status()
            return response.json()
