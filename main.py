import time
import os
import requests
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
from dotenv import load_dotenv

# Import our modules
from database import SessionLocal, Notification, init_db
from scraper import run_all_scrapers

# Load secrets
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_alert(title, link, source):
    """Sends a message to your Telegram"""
    print(f"   📲 Sending Alert: {title[:30]}...")
    
    # Format the message nicely
    message = (
        f"🚨 <b>New {source} Update!</b>\n\n"
        f"📝 {title}\n\n"
        f"🔗 <a href='{link}'>Click to View</a>"
    )
    
    # Try sending as a document if it's a PDF
    if link.lower().endswith(".pdf"):
        doc_url = f"https://api.telegram.org/bot{TOKEN}/sendDocument"
        doc_payload = {
            "chat_id": CHAT_ID,
            "document": link,
            "caption": message,
            "parse_mode": "HTML"
        }
        try:
            print("   📄 Detected PDF. Attempting to send as document...")
            resp = requests.post(doc_url, json=doc_payload)
            if resp.status_code == 200:
                print("   ✅ PDF sent successfully!")
                return
            else:
                print(f"   ⚠️ PDF send failed (Status {resp.status_code}). Falling back to text link.")
        except Exception as e:
             print(f"   ⚠️ PDF send error: {e}. Falling back to text link.")

    # Fallback / Standard Message
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"   ❌ Failed to send Telegram: {e}")

def check_for_updates():
    """The main job function that runs every 15 minutes"""
    print(f"\n🔄 [{datetime.now().strftime('%H:%M:%S')}] Checking for updates...")
    
    # 1. Open the database
    db = SessionLocal()
    
    # 2. Scrape the websites
    latest_data = run_all_scrapers()
    
    # --- FIX START: Remove duplicates from the scraped list ---
    # Sometimes the website lists the same link twice. We must deduplicate BEFORE DB.
    unique_data = []
    seen_urls = set()
    
    for item in latest_data:
        if item['link'] not in seen_urls:
            unique_data.append(item)
            seen_urls.add(item['link'])
    
    print(f"   🔍 Filtered {len(latest_data)} items down to {len(unique_data)} unique links.")
    # --- FIX END ---

    # 3. Check if this is the FIRST run ever (is DB empty?)
    first_run = db.query(Notification).first() is None
    
    new_count = 0
    
    for item in unique_data:
        # Check if link already exists in DB
        exists = db.query(Notification).filter(Notification.link == item['link']).first()
        
        if not exists:
            # Create new record
            new_note = Notification(
                title=item['title'],
                link=item['link'],
                date_posted=datetime.now().strftime("%Y-%m-%d"),
                is_sent=False 
            )
            
            if first_run:
                # First run? Mark as sent so we don't spam.
                new_note.is_sent = True
                # Optional: Print just one line every 50 items to keep terminal clean
                if new_count % 50 == 0:
                    print(f"   💾 Saving initial history... ({new_count} done)")
            else:
                # Real new update! Send alert.
                send_telegram_alert(item['title'], item['link'], item['source'])
                new_note.is_sent = True
            
            db.add(new_note)
            new_count += 1
    
    # Commit all changes
    try:
        db.commit()
        if first_run:
            print(f"✅ First run complete. Saved {new_count} notifications. Waiting for NEW updates...")
        elif new_count == 0:
            print("💤 No new updates found.")
        else:
            print(f"🚀 Sent {new_count} new alerts!")
            
    except Exception as e:
        print(f"❌ Database Error: {e}")
        db.rollback() # Undo changes if error
    finally:
        db.close()

if __name__ == "__main__":
    # 1. Initialize the database
    init_db()
    
    # 2. Start the scheduler
    scheduler = BlockingScheduler()
    
    # Run immediately once to fill the DB
    check_for_updates()
    
    # Then run every 15 minutes
    print("⏳ Scheduler started. Running every 15 minutes...")
    scheduler.add_job(check_for_updates, 'interval', minutes=15)
    scheduler.start()