# split-urls
Analyze GET URLS vs ZXTM redirects and splits ZXTM redirects, GETs redirects and pages that can be deleted

# How to use it
- pip install requests
- clone the repo locally
- run python split.py [PROJECT_FOLDRER] [RULES_FILE]
- will produce 3 files. redirect_in_zxtm.txt, redirect_in_cms.txt, delete_from_project.txt

# Dependency
- Python 3+
- Requests
