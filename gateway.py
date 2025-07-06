from flask import Flask, request, redirect, abort
from urllib.parse import quote_plus
import requests

app = Flask(__name__)

GOOGLE_CHECK_URL = "https://www.google.com/generate_204"
GOOGLE_SEARCH_URL = "https://www.google.com/search?q={query}"
BING_SEARCH_URL   = "https://www.bing.com/search?q={query}"
TIMEOUT_SECONDS   = 1        # 探测超时
HEADERS           = {"User-Agent": "Mozilla/5.0"}

def google_reachable() -> bool:
    """快速探测 Google 是否可用"""
    try:
        r = requests.get(GOOGLE_CHECK_URL, timeout=TIMEOUT_SECONDS, headers=HEADERS)
        return r.status_code == 204
    except requests.RequestException:
        return False

@app.route("/", methods=["GET"])
def index():
    q = request.args.get("q", default="", type=str).strip()
    if not q:
        abort(400, description="用法：/?q=python+flask")
    encoded = quote_plus(q)
    target = GOOGLE_SEARCH_URL.format(query=encoded) if google_reachable() \
             else BING_SEARCH_URL.format(query=encoded)
    return redirect(target, code=302)

if __name__ == "__main__":
    # 开发模式直接运行： python smart_search_gateway.py
    app.run(host="0.0.0.0", port=6626, debug=False)
