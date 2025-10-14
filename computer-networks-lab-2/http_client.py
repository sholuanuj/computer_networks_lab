# http_client.py
import requests

def main():
    try:
        # Example GET request
        get_resp = requests.get("https://httpbin.org/get")
        print("GET Request:")
        print("Status Code:", get_resp.status_code)
        print("Headers:", get_resp.headers)
        print("Body:", get_resp.text[:200], "...")  # print partial

        # Example POST request
        post_resp = requests.post("https://httpbin.org/post", data={"name": "Anuj", "course": "CN"})
        print("\nPOST Request:")
        print("Status Code:", post_resp.status_code)
        print("Headers:", post_resp.headers)
        print("Body:", post_resp.text[:200], "...")

    except Exception as e:
        print("Error occurred:", e)

if __name__ == "__main__":
    main()
