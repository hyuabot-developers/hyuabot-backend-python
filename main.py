# External Module
from sanic import Sanic, Blueprint
from sanic_openapi import swagger_blueprint

# Internal Module
from kakao.url import kakao_url

# Server Object
app = Sanic(__name__)

# NameSpace
app.blueprint(kakao_url)
app.blueprint(swagger_blueprint)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)