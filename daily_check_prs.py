import os
import requests
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
REPO_URL = "biancassilva/smart-summary-app"

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json",
}

# Set time window: 18:00 UTC yesterday to 18:00 UTC today (24 hours)
TODAY = datetime.now(timezone.utc).date()
END_OF_DAY = datetime.combine(TODAY, datetime.min.time()).replace(tzinfo=timezone.utc, hour=18)
START_OF_DAY = END_OF_DAY - timedelta(hours=24)


def get_prs(state):
    """Fetch PRs by state (open, closed, all)"""
    url = f"https://api.github.com/repos/{REPO_URL}/pulls"
    params = {"state": state, "per_page": 100}
    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    return response.json()


def categorize_prs():
    """Return merged PRs between 00:00 UTC and 23:59 UTC today."""
    closed_prs = get_prs("closed")
    recent_merged = []

    # Check closed PRs for merged status
    for pr in closed_prs:
        # Fetch full PR details to check for merge
        details = requests.get(pr["url"], headers=HEADERS).json()
        merged_at = details.get("merged_at")

        if merged_at:
            merged_time = datetime.strptime(merged_at, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
            if START_OF_DAY <= merged_time <= END_OF_DAY:
                recent_merged.append(details)

    print(f"🔍 Found {len(recent_merged)} merged PRs in the last 24 hours (18:00 UTC)")
    return {
        "merged": recent_merged,
    }


def format_pr_section(title, prs, emoji):
    if not prs:
        return []
    blocks = [{"type": "header", "text": {"type": "plain_text", "text": f"{emoji} {title}"}}]
    for pr in prs:
        assignees = ", ".join([a["login"] for a in pr.get("assignees", [])]) or "None"
        reviewers = ", ".join([r["login"] for r in pr.get("requested_reviewers", [])]) or "None"
        description = pr.get("body") or "_No description_"
        status = "📝 Draft" if pr.get("draft") else "✅ Ready"

        text = (
            f"*<{pr['html_url']}|{pr['title']}>* by *{pr['user']['login']}*\n"
            f"Status: {status}\n"
            f"Assignees: {assignees}\n"
            f"Reviewers: {reviewers}\n\n"
            f"Summary: {description}"
        )
        blocks.append({"type": "section", "text": {"type": "mrkdwn", "text": text}})
        blocks.append({"type": "divider"})
    return blocks


def format_slack_message(summary):
    blocks = []
    for section, (emoji, title) in {
        "merged": ("🎉", "PRs Merged"),
    }.items():
        blocks += format_pr_section(title, summary[section], emoji)

    if not blocks:
        return {"text": "No PR activity in the last 24 hours 🚀"}
    return {"blocks": blocks}


def send_to_slack(message):
    response = requests.post(SLACK_WEBHOOK_URL, json=message)
    response.raise_for_status()


def main():
    try:
        summary = categorize_prs()
        slack_message = format_slack_message(summary)
        send_to_slack(slack_message)
        print("✅ Slack summary sent successfully.")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
