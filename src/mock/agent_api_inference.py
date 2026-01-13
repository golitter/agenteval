import requests

def agent_api_health_check() -> dict:
    url = "http://127.0.0.1:8001/health/"

    resp = requests.get(url, timeout=500)
    if resp.status_code == 200:
        return {"status":200, "message":"智能体正常"}
    else:
        return {"status":resp.status_code, "message":"智能体异常", "details": resp.text}

def agent_api_inference(query: str, session_id: str) -> str:
    url = "http://127.0.0.1:8001/chat"
    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "query": query,
        "session_id": session_id
    }

    response = requests.post(
        url=url,
        json=payload,
        headers=headers,
        timeout=30000
    )

    response.raise_for_status()
    result = response.json()
    # print(result)
    return result.get("response", "")