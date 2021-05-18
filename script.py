import time

import requests

backlog_space = ""
url = f"https://{backlog_space}.backlog.jp/api/v2/notifications"
api_key = ""
batch_count = 20
payload = {"apiKey": api_key, "count": batch_count}
max_id = None

res = requests.get(url, params=payload)

while True:
    if max_id is None:
        res = requests.get(url, params=payload)
    else:
        payload["maxId"] = max_id
        res = requests.get(url, params=payload)

    issues = res.json()
    for issue in issues:
        if issue["resourceAlreadyRead"] is False:
            requests.post(url=f"{url}/{issue['id']}/markAsRead", params=payload)
            print(f"既読化(id={issue['id']})")
            time.sleep(1)

        max_id = issue["id"]

    if len(issues) < batch_count:
        print("下限に到達したので終了")
        break

    time.sleep(1)

    print(f"次のリストを検索(maxId={max_id})...")
