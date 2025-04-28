from flask import Flask, render_template, request
import whois
import socket

app = Flask(__name__)

def check_domain(domain):
    try:
        domain_info = whois.whois(domain)
        if domain_info.domain_name:
            return {
                'available': False,
                'domain': domain,
                'registrar': domain_info.registrar,
                'expiration_date': domain_info.expiration_date
            }
    except Exception:
        pass

    try:
        socket.gethostbyname(domain)
        return {
            'available': False,
            'domain': domain,
            'registrar': None,
            'expiration_date': None
        }
    except socket.gaierror:
        return {
            'available': True,
            'domain': domain
        }

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        domain = request.form['domain']
        result = check_domain(domain)
        return render_template('result.html', result=result)
    return render_template('index.html')

