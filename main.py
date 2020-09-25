# External Module
from flask import Flask
from flask_caching import Cache

# Internal Module
from firebase.firebase_init import init
from kakao.url import kakao_url

# Server Object
app = Flask(__name__)

# Flask Config
config = {
    'DEBUG':True,
    'CACHE_TYPE':'simple',
    'CACHE_DEFAULT_TIMEOUT':300
}
# Blueprint
app.register_blueprint(kakao_url, url_prefix='/kakao')

# Execute Server
app.config.from_mapping(config)
cache = Cache(app)

if __name__ == '__main__':
    cache.init_app(app)
    init()
    with app.app_context():
        cache.clear()
    app.run(host='0.0.0.0', port=8080)