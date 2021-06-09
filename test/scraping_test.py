import requests


def scraping_test(url_key):
    r = requests.get(f"http://localhost:5000/api/gameUrl/{url_key}")

    result = r.json()

    if result["result"] == "success":
        return True
    else:
        return False


if __name__ == "__main__":
    test_result = scraping_test("1372810")
    if test_result:
        print("test Success")
    else:
        print("test Fail")