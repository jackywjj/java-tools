from werkzeug.middleware.proxy_fix import ProxyFix

from app import app

if __name__ == '__main__':
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.run(host="127.0.0.1", port=5000, debug=True)
