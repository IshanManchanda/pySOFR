# pySOFR

pySOFR is a web scraper that fetches the results of SOF Olympiads.  
It takes the school code as an input from the user (or from the env)
and performs an optimized brute force search.
The output is tabulated in a Microsoft Excel sheet. 

### Major Technologies Used
- Python 3.7
- Requests (HTTP for Humans - the Python module)
- BeautifulSoup4
- OpenPyXL

### Things I've Learnt
- Building web scrapers with the Requests module.
- Parsing HTML using BS4.
- Creating Microsoft Excel sheets with OpenPyXL.
- Modifying a brute-force search to hit every candidate while minimizing excess
 requests.
- Breaking a simple math-based captcha, finding and returning form ids and
 tokens, and using session objects to bypass textbook-level security features.
