\# GOAT Data Analyst - User Guide



\*\*Version\*\*: 1.5.0  

\*\*Last Updated\*\*: December 5, 2025



---



\## Table of Contents



1\. \[Getting Started](#getting-started)

2\. \[Uploading a CSV](#uploading-a-csv)

3\. \[Understanding Your Report](#understanding-your-report)

4\. \[Using Auto-Fix Features](#using-auto-fix-features)

5\. \[Batch Analysis](#batch-analysis)

6\. \[Troubleshooting](#troubleshooting)



---



\## Getting Started



\### Sign Up



1\. Go to \[GOAT Data Analyst](https://goat-data-analyst-fctfqjst9eaphnfstsn4sb.streamlit.app)

2\. Click \*\*"Sign Up"\*\*

3\. Enter your email and password

4\. Click \*\*"Create Account"\*\*

5\. You're ready to analyze!



\### Log In



1\. Enter your email and password

2\. Click \*\*"Login"\*\*

3\. You'll see the main dashboard



---



\## Uploading a CSV



\### Step 1: Click "Upload CSV"



\- Supported formats: `.csv` only

\- Max file size: \*\*100 MB\*\*

\- Encoding: UTF-8 (recommended)



\### Step 2: Select Your File



\- Choose a CSV file from your computer

\- File must have headers in the first row



\### Step 3: Wait for Analysis



\- Small files (<1 MB): ~10 seconds

\- Medium files (1-10 MB): ~30 seconds

\- Large files (10-100 MB): ~1-2 minutes



---



\## Understanding Your Report



Your report contains \*\*4 main sections\*\*:



\### 📊 1. Data Profile

\- \*\*Rows \& Columns\*\*: Total count

\- \*\*File Size\*\*: In MB

\- \*\*Quality Score\*\*: 0-100 (higher is better)



\### 🏢 2. Business Domain

\- Auto-detected industry (e.g., E-commerce, Finance, HR)

\- Key business metrics identified



\### ⚠️ 3. Data Quality Issues

\- Missing values

\- Duplicates

\- Outliers

\- Data type mismatches



\### 💡 4. AI-Powered Insights

\- Pain points identified

\- Action plan with priorities

\- Business recommendations



---



\## Using Auto-Fix Features



\### Fix Missing Values



1\. Scroll to \*\*"Data Quality Issues"\*\*

2\. Click \*\*"Fix Missing Values"\*\*

3\. Choose method:

&nbsp;  - \*\*Mean/Median\*\* (for numbers)

&nbsp;  - \*\*Mode\*\* (for categories)

&nbsp;  - \*\*Remove rows\*\* (if too many missing)

4\. Click \*\*"Apply Fix"\*\*

5\. Download cleaned CSV



\### Remove Duplicates



1\. Click \*\*"Remove Duplicates"\*\*

2\. Select columns to check

3\. Click \*\*"Apply"\*\*

4\. Download cleaned CSV



\### Remove Outliers



1\. Click \*\*"Remove Outliers"\*\*

2\. Choose method:

&nbsp;  - \*\*IQR\*\* (recommended)

&nbsp;  - \*\*Z-score\*\*

3\. Click \*\*"Apply"\*\*

4\. Download cleaned CSV



---



\## Batch Analysis



\### Analyze Multiple Files



1\. Click \*\*"Batch Analysis"\*\*

2\. Upload folder or select multiple CSVs

3\. Wait for all files to process

4\. View dashboard with:

&nbsp;  - Quality scores comparison

&nbsp;  - Common issues across files

&nbsp;  - Combined action plan



\### Download All Reports



1\. Click \*\*"Download All Reports (ZIP)"\*\*

2\. Extract ZIP file

3\. Open individual HTML reports



---



\## Troubleshooting



\### "File too large" Error



\*\*Solution\*\*: Split your CSV into smaller chunks (<100 MB each)

Python script to split large CSV

import pandas as pd



df = pd.read\_csv('large\_file.csv')

chunk\_size = 100000 # rows per file



for i, chunk in enumerate(df.groupby(df.index // chunk\_size)):

chunk.to\_csv(f'chunk\_{i}.csv', index=False




---



\### "Invalid file format" Error



\*\*Solution\*\*: 

1\. Open file in Excel/Google Sheets

2\. File → Save As → CSV (UTF-8)

3\. Try uploading again



---



\### "Encoding issue" Error



\*\*Solution\*\*:

1\. Open CSV in Notepad++

2\. Encoding → Convert to UTF-8

3\. Save and re-upload



---



\### Analysis Stuck/Frozen



\*\*Solution\*\*:

1\. Refresh the page

2\. Log in again

3\. If issue persists, contact support



---



\### "Rate limit exceeded" Error



\*\*Solution\*\*:

\- Free tier: Wait 1 minute between analyses

\- Pro tier: Unlimited analyses (\[Upgrade here](https://goat-data-analyst-fctfqjst9eaphnfstsn4sb.streamlit.app))



---



\## Best Practices



\### ✅ DO:

\- Use UTF-8 encoded CSV files

\- Include clear column headers

\- Keep files under 50 MB for faster results

\- Review AI suggestions before applying fixes



\### ❌ DON'T:

\- Upload files with passwords/sensitive data

\- Expect 100% accuracy on AI insights (always verify)

\- Apply all fixes blindly (review first)



---



\## Support



\*\*Need help?\*\*

\- Email: support@goat-analyst.com

\- Discord: \[Join our community](#)

\- GitHub Issues: \[Report bugs](https://github.com/ojayWillow/goat-data-analyst/issues)



---



\*\*Status Page\*\*: \[Check service uptime](https://status.goat-analyst.com)



---



\*Happy Analyzing! 🐐\*







