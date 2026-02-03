import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# --- CONFIGURATION: Add your settings here ---
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"

# --- HELPER FUNCTION: Downloads and parses a page ---
def get_soup(url):
    try:
        headers = {"User-Agent": USER_AGENT}
        print(f"🌍 Connecting to {url}...")
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        print(f"❌ Error fetching {url}: {e}")
        return None

# --- SOURCE 1: DTU Main Website (Jobs Tab) ---
def scrape_dtu_jobs():
    url = "http://www.dtu.ac.in/"
    soup = get_soup(url)
    notices = []
    
    if not soup: return []

    # Strategy: Look for the specific 'tab2' div we saw earlier
    content_box = soup.find("div", id="tab2")
    if content_box:
        links = content_box.find_all("a")
        for link in links:
            text = link.get_text(strip=True)
            href = link.get("href")
            if text and href:
                # Fix relative links (e.g., "upload/file.pdf" -> "http://dtu.ac.in/upload/...")
                href = urljoin(url, href)
                
                notices.append({"source": "DTU Jobs", "title": text, "link": href})
    
    return notices

# --- SOURCE 2: DTU Exam Portal ---
def scrape_dtu_exams():
    url = "https://exam.dtu.ac.in/Notices-n-Circulars.htm"
    soup = get_soup(url)
    notices = []
    
    if not soup: return []

    # Strategy: Exam sites usually list links in a main content area.
    # Since we haven't inspected this one, let's grab ALL links that look like notices first.
    # (We can refine this Selector later if it grabs too much junk)
    
    # Try to find the main table or list. 
    # Usually inside a div with class "content" or similar. 
    # For now, we grab all 'a' tags that link to PDF or standard pages
    links = soup.find_all("a")
    
    for link in links:
        text = link.get_text(strip=True)
        href = link.get("href")
        
        # Simple filter: Ignore empty links or generic "Home" buttons
        if text and href and len(text) > 10: 
            href = urljoin(url, href)
            
            notices.append({"source": "DTU Exams", "title": text, "link": href})
            
    return notices

# --- THE REGISTRY: Register your functions here ---
# To add a new site, write a function above and add it to this list.
SCRAPER_FUNCTIONS = [
    scrape_dtu_jobs,
    scrape_dtu_exams
]

def run_all_scrapers():
    all_data = []
    for scraper_func in SCRAPER_FUNCTIONS:
        data = scraper_func()
        print(f"   ↳ Found {len(data)} items from {scraper_func.__name__}")
        all_data.extend(data)
    return all_data

# --- TEST BLOCK ---
if __name__ == "__main__":
    print("🚀 Starting modular scrape...")
    results = run_all_scrapers()
    
    print(f"\n✅ Total Notifications Found: {len(results)}")
    print("Here are the top 5 recent ones:")
    for n in results[:5]:
        print(f"[{n['source']}] {n['title']} \n   🔗 {n['link']}")