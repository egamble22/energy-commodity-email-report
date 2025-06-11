from tabulate import tabulate
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()

def send_email(rows, headers, news_articles):
    """
    Sends an HTML-formatted email containing a styled table of market data and top news articles.
    """
    # Format the table as HTML
    html_table = tabulate(rows, headers=headers, tablefmt="html")

    # Format news articles into an HTML list
    news_html = "<h3>📰 Suggested Daily Reads</h3><ul>"
    for article in news_articles:
        news_html += f'<li><a href="{article["url"]}" target="_blank">{article["title"]}</a> — <em>{article["source"]}</em></li>'
    news_html += "</ul>"

    # Full HTML content
    html_content = f"""
    <html>
      <head>
        <style>
          body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
          }}
          table {{
            border-collapse: collapse;
            width: 100%;
          }}
          th, td {{
            border: 1px solid #dddddd;
            text-align: left;
            padding: 8px;
          }}
          tr:nth-child(even) {{
            background-color: #f9f9f9;
          }}
          th {{
            background-color: #4CAF50;
            color: white;
          }}
        </style>
      </head>
      <body>
        <h2>⚡ Morning Energy Market Update</h2>
        {html_table}
        <br>
        {news_html}
        <p>Have a great trading day! 🚀</p>
      </body>
    </html>
    """

    # Email parameters loaded from environment variables
    sender_email = os.getenv("EMAIL_ADDRESS")
    receiver_email = os.getenv("EMAIL_ADDRESS")  # or put another env var if receiver differs
    password = os.getenv("EMAIL_PASSWORD")

    if not sender_email or not password:
        print("❌ Missing email credentials in environment variables.")
        return

    # Compose and send the email
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Daily Energy Market Report"
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg.attach(MIMEText(html_content, "html"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print("✅ Email sent successfully!")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")