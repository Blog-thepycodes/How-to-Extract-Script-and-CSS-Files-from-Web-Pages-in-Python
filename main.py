import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import logging
import tkinter as tk
from tkinter import ttk, messagebox
 
 
# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
 
 
 
 
def fetch_url_content(url):
   """Fetches the content of the given URL."""
   try:
       session = requests.Session()
       session.headers.update({
           "User-Agent": "CustomUserAgent/1.0 (UniqueUser; Python Script)"
       })
       response = session.get(url)
       response.raise_for_status()
       logging.info(f"Successfully fetched content from {url}")
       return response.content
   except requests.RequestException as e:
       logging.error(f"Error fetching content from {url}: {e}")
       return None
 
 
 
 
def extract_file_urls(soup, tag, attribute):
   """Extracts URLs of files from the given BeautifulSoup object based on the specified tag and attribute."""
   file_urls = []
   for element in soup.find_all(tag):
       if element.attrs.get(attribute):
           file_url = urljoin(target_url, element.attrs[attribute])
           file_urls.append(file_url)
   return file_urls
 
 
 
 
def on_extract():
   """Handles the extract button click event."""
   global target_url
   target_url = url_entry.get().strip()
 
 
   if not target_url:
       messagebox.showerror("Input Error", "Please enter a URL.")
       return
 
 
   html_content = fetch_url_content(target_url)
   if html_content is None:
       messagebox.showerror("Fetch Error", "Failed to retrieve HTML content.")
       return
 
 
   soup = BeautifulSoup(html_content, "html.parser")
   js_files = extract_file_urls(soup, "script", "src")
   css_files = extract_file_urls(soup, "link", "href")
 
 
   # Display results in the text widget
   result_text.config(state=tk.NORMAL)
   result_text.delete(1.0, tk.END)  # Clear previous results
   result_text.insert(tk.END, f"JavaScript files ({len(js_files)}):\n")
   result_text.insert(tk.END, "\n".join(js_files) + "\n\n")
   result_text.insert(tk.END, f"CSS files ({len(css_files)}):\n")
   result_text.insert(tk.END, "\n".join(css_files))
   result_text.config(state=tk.DISABLED)
 
 
 
 
# Create the main Tkinter window
root = tk.Tk()
root.title("Web Resource Extractor - The Pycodes")
root.geometry("600x400")
 
 
# URL input
url_label = ttk.Label(root, text="Enter URL:")
url_label.pack(pady=10)
 
 
url_entry = ttk.Entry(root, width=50)
url_entry.pack(pady=5)
 
 
# Extract button
extract_button = ttk.Button(root, text="Extract", command=on_extract)
extract_button.pack(pady=20)
 
 
# Frame for Text widget and Scrollbar
frame = ttk.Frame(root)
frame.pack(pady=10, fill=tk.BOTH, expand=True)
 
 
# Text widget to display results
result_text = tk.Text(frame, wrap=tk.WORD, state=tk.DISABLED, width=70, height=15)
result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
 
 
# Scrollbar
scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=result_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
result_text.config(yscrollcommand=scrollbar.set)
 
 
# Run the Tkinter event loop
root.mainloop()
