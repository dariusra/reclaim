from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__, template_folder='.')

# Function to fetch AWS IP ranges
def get_aws_ip_ranges():
    url = "https://ip-ranges.amazonaws.com/ip-ranges.json"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to fetch AWS IP ranges"}

# Function to filter IP ranges by service
def filter_ip_ranges(ip_ranges, services):
    filtered_ranges = []
    for ip_range in ip_ranges['prefixes']:
        if ip_range['service'] in services:
            filtered_ranges.append(ip_range)
    return filtered_ranges

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/aws_ip_ranges')
def aws_ip_ranges():
    ip_ranges = get_aws_ip_ranges()
    filtered_ranges = filter_ip_ranges(ip_ranges, ['ROUTE53_HEALTHCHECKS', 'S3'])
    return jsonify(filtered_ranges)

if __name__ == '__main__':
    app.run(port=1234)
