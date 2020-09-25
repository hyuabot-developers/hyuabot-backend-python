# External Module
from flask import Flask
from flask_restx import Namespace, Api
from flask_caching import Cache

# Internal Module
from firebase.firebase_init import init
from kakao.url import kakao_url

# Server Object
app = Flask(__name__)
api = Api(
    app=app,
    version='0.1',
    title='API server working on GAE',
    terms_url='/',
    contact='jil8885@hanyang.ac.kr',
    license='MIT'
)

# Flask Config
config = {
    'DEBUG':True,
    'CACHE_TYPE':'simple',
    'CACHE_DEFAULT_TIMEOUT':300
}
# NameSpace
api.add_namespace(kakao_url, '/kakao')

# Execute Server
app.config.from_mapping(config)
app.config['JSON_AS_ASCII'] = False
cache = Cache(app)

if __name__ == '__main__':
    cache.init_app(app)
    init()
    with app.app_context():
        cache.clear()
    app.run(host='0.0.0.0', port=8080)