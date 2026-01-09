# AFW Thread to PDF/HTML Exporter

You can use this to convert AFWRPG threads into PDFs and/or HTML files.

The code here is a slightly modified version of the code for an identical tool for LAW-RP.  That code can be found [here](https://github.com/IchiTK0/LAW-Thread-Exporter).

Note that both text color and formatting appear to be slightly bugged when exporting as a PDF.  As a workaround, you may want to export as an HTML file first and then convert it to a PDF yourself.

## Prerequisites
1. **Python 3.x**
2. **wkhtmltopdf**: If you don't install this binary on your system, you're gonna have a bad time (it's needed for PDF conversion to work).
   - [Download wkhtmltopdf](https://wkhtmltopdf.org/downloads.html)

## Setup
1. Clone this repo.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt

## Usage
1. Run this command: python Grab_Thread.py
2. **DO NOT** run this command: sudo rm -rf /