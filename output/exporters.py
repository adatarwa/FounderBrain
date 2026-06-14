"""
output/exporters.py
Export FounderBrain reports to Notion and Google Docs.
Also exports clean markdown and JSON for any other use.
"""

import os
import json
import requests
from pathlib import Path
from datetime import datetime
from memory.shared_memory import SharedMemory


class NotionExporter:
    """Export FounderBrain report to a Notion page."""

    def __init__(self):
        self.token = os.getenv("NOTION_TOKEN")
        self.database_id = os.getenv("NOTION_DATABASE_ID")
        self.base_url = "https://api.notion.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        }

    def export(self, memory: SharedMemory) -> str:
        """Export to Notion. Returns URL of created page."""
        if not self.token:
            raise ValueError(
                "NOTION_TOKEN not set.\n"
                "1. Go to notion.so/my-integrations\n"
                "2. Create a new integration\n"
                "3. Copy the token to .env as NOTION_TOKEN\n"
                "4. Share your database with the integration"
            )

        # Build page content
        children = []

        # Callout block with startup name
        children.append({
            "object": "block", "type": "callout",
            "callout": {
                "rich_text": [{"type": "text", "text": {"content": f"FounderBrain report for {memory.startup_name}"}}],
                "icon": {"type": "emoji", "emoji": "🧠"},
                "color": "purple_background"
            }
        })

        # Add each agent section
        agents = [
            ("market_output",      "📊 Market Analysis"),
            ("customer_output",    "🎯 Customer & ICP"),
            ("gtm_output",         "🚀 Go-To-Market"),
            ("hiring_output",      "👥 Hiring Plan"),
            ("fundraising_output", "💰 Fundraising"),
            ("ops_output",         "📅 90-Day Ops Plan"),
            ("legal_output",       "⚖️ Legal"),
        ]

        for attr, title in agents:
            output = getattr(memory, attr, None)
            if not output or output.status != "complete":
                continue

            # Section heading
            children.append({
                "object": "block", "type": "heading_2",
                "heading_2": {"rich_text": [{"type": "text", "text": {"content": title}}]}
            })

            # Summary quote
            children.append({
                "object": "block", "type": "quote",
                "quote": {"rich_text": [{"type": "text", "text": {"content": output.summary}}]}
            })

            # Key facts as bullets
            for fact in (output.key_facts or [])[:5]:
                children.append({
                    "object": "block", "type": "bulleted_list_item",
                    "bulleted_list_item": {
                        "rich_text": [{"type": "text", "text": {"content": fact}}]
                    }
                })

            # Full output as paragraph chunks (Notion has 2000 char limit per block)
            text = output.full_output or ""
            for i in range(0, len(text), 1900):
                children.append({
                    "object": "block", "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": text[i:i+1900]}}]
                    }
                })

            children.append({"object": "block", "type": "divider", "divider": {}})

        # Create the page
        page_data = {
            "parent": {"database_id": self.database_id} if self.database_id
                      else {"type": "workspace", "workspace": True},
            "icon": {"type": "emoji", "emoji": "🧠"},
            "properties": {
                "title": {"title": [{"text": {"content": f"FounderBrain — {memory.startup_name}"}}]}
            },
            "children": children[:100],  # Notion limit: 100 blocks per request
        }

        r = requests.post(f"{self.base_url}/pages", headers=self.headers, json=page_data)
        r.raise_for_status()
        page = r.json()
        url = page.get("url", "")
        print(f"  ✓ Exported to Notion: {url}")
        return url


class GoogleDocsExporter:
    """Export FounderBrain report to Google Docs."""

    def export(self, memory: SharedMemory, report_markdown: str) -> str:
        """
        Export to Google Docs.
        Requires Google Docs API credentials — guides the user to set up.
        Returns instructions URL.
        """
        # Check for credentials
        creds_path = Path("credentials.json")
        if not creds_path.exists():
            print("\n  To export to Google Docs:")
            print("  1. Go to console.cloud.google.com")
            print("  2. Enable Google Docs API + Google Drive API")
            print("  3. Create OAuth 2.0 credentials")
            print("  4. Download as credentials.json to this folder")
            print("  5. Run: pip install google-auth google-auth-oauthlib google-api-python-client")
            print("  6. Re-run the export\n")
            return None

        try:
            from google.oauth2.credentials import Credentials
            from google_auth_oauthlib.flow import InstalledAppFlow
            from googleapiclient.discovery import build

            SCOPES = ["https://www.googleapis.com/auth/documents",
                      "https://www.googleapis.com/auth/drive"]

            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

            docs_service = build("docs", "v1", credentials=creds)
            drive_service = build("drive", "v3", credentials=creds)

            # Create document
            doc = docs_service.documents().create(body={
                "title": f"FounderBrain — {memory.startup_name}"
            }).execute()

            doc_id = doc.get("documentId")

            # Insert content
            requests_body = [{
                "insertText": {
                    "location": {"index": 1},
                    "text": report_markdown
                }
            }]

            docs_service.documents().batchUpdate(
                documentId=doc_id,
                body={"requests": requests_body}
            ).execute()

            url = f"https://docs.google.com/document/d/{doc_id}/edit"
            print(f"  ✓ Exported to Google Docs: {url}")
            return url

        except ImportError:
            print("  Run: pip install google-auth google-auth-oauthlib google-api-python-client")
            return None
        except Exception as e:
            print(f"  Google Docs export failed: {e}")
            return None


class JSONExporter:
    """Export raw structured data as JSON for custom integrations."""

    def export(self, memory: SharedMemory, output_dir: str = None) -> str:
        output_dir = Path(output_dir or Path.home() / "FounderBrain" / "exports")
        output_dir.mkdir(parents=True, exist_ok=True)

        filename = f"{memory.startup_name.replace(' ', '_')}_{memory.run_id}.json"
        path = output_dir / filename

        data = {
            "startup_name": memory.startup_name,
            "run_id": memory.run_id,
            "founder_input": memory.founder_input,
            "generated_at": datetime.now().isoformat(),
            "agents": {}
        }

        for attr in ["market_output", "customer_output", "gtm_output",
                     "hiring_output", "fundraising_output", "ops_output", "legal_output"]:
            output = getattr(memory, attr, None)
            if output and output.status == "complete":
                data["agents"][attr] = {
                    "summary": output.summary,
                    "key_facts": output.key_facts,
                    "full_output": output.full_output,
                }

        path.write_text(json.dumps(data, indent=2))
        print(f"  ✓ JSON exported → {path}")
        return str(path)
