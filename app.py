from flask import Flask, render_template, request, jsonify, send_file
import os
import datetime
from web_scrpit import web_scraping_books as wb

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'downloads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape_books():
    try:
        # Get URL from request with a default value
        default_url = 'https://books.toscrape.com/catalogue/category/books/travel_2/index.html'
        url = default_url
        
        if request.is_json:
            data = request.get_json()
            if data and 'url' in data:
                url = data['url']
        
        # Create filename with current date
        try:
            domain = url.split('//')[-1].split('/')[0].replace('.', '_')
            filename = f"{domain}_{datetime.date.today().strftime('%Y-%m-%d')}.csv"
        except Exception as e:
            # Fallback filename if URL parsing fails
            filename = f"scraped_data_{datetime.date.today().strftime('%Y-%m-%d')}.csv"
            
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Run the web scraping function with URL parameter
        wb(save_path, url=url)
        
        # Return the file for download
        return send_file(
            save_path,
            as_attachment=True,
            download_name=filename,
            mimetype='text/csv'
        )
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
