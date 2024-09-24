import traceback

from flask import redirect
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required
from flask_openapi3 import OpenAPI, Info, Tag
from flask_restful import Api, reqparse

from model.product import ProductModel
from schemas.error import ErrorAuthorizationSchema, ErrorSchema, ServerErrorSchema
from schemas.produto import DeleteSchema, ListagemProdutosApiSchema, NotFoundSchema
from schemas.produto import ProductBody, ProductPath, RegisterSchema 

import os
from dotenv import load_dotenv

load_dotenv()

info = Info(title="API Produto", version="1.0.0", description="API para gerenciar produtos\n\n Para obter o token use a API de TOKEN.")
app = OpenAPI(__name__, info=info)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

api = Api(app)
jwt = JWTManager(app)

CORS(app, resources={r"/api/*": {"origins": "http://127.0.0.1:5000"}})

security_scheme = {
    "Bearer Token": {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT"
    }
}
app.security_schemes = security_scheme

@app.before_request
def cria_banco():
    banco.create_all()

home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger")
produto_tag = Tag(name="Produto", description="Rotas para Produto")

@app.get('/', tags=[home_tag], doc_ui=False)
def home():
    """ Home da aplicação.

        Redireciona para /openapi/swagger, abrindo a documentação da API.
    """
    return redirect('/openapi/swagger')

@app.get('/api/produtos', 
        tags=[produto_tag],
        responses={
                    "200": ListagemProdutosApiSchema, 
                    "400": ErrorSchema, 
                    "401": ErrorAuthorizationSchema, 
                    "500": ServerErrorSchema}, 
        security=[{"Bearer Token": []}])
def products():
    """ Lista de usuários.

        Traz todos os usuários se tiver a chave de acesso.
    """
    try:
        products = [products.json() for products in ProductModel.query.all()]
        return {'products': products}, 200
    except Exception as e:
        print(f"Erro ao carregar produtos: {str(e)}")
        return {'error': 'Server error'}, 500

@app.post('/api/registrar', tags=[produto_tag],
           responses={
                    "200": RegisterSchema, 
                    "400": ErrorSchema, 
                    "500": ServerErrorSchema}, )
@jwt_required()
def produto_novo(body:RegisterSchema):
    """ Novo produto.

        Cria um produto.
    """
    atributos = reqparse.RequestParser()
    atributos.add_argument('nome', type=str, required=True)
    atributos.add_argument('descricao', type=str, required=True)
    atributos.add_argument('preco', type=float, required=True)
    atributos.add_argument('quantidade', type=int, required=True)
    dados = atributos.parse_args()

    product = ProductModel(**dados)
 
    try:
        product.save_product()
    except:
        product.delete_product()
        traceback.print_exc()
        return {"mesage": "Um erro aconteceu."}, 500 
    
    return {
            'nome': dados['nome'],
            'descricao': dados['descricao'],
            'preco':dados['preco'],
            'quantidade':dados['quantidade']
            }, 201

@app.put('/api/produto/<int:id>', tags=[produto_tag],
        responses={
                    "200": ProductBody, 
                    "400": ErrorSchema, 
                    "404": NotFoundSchema, 
                    "401": ErrorAuthorizationSchema, 
                    "500": ServerErrorSchema},
        security=[{"Bearer Token": []}])
@jwt_required()
def update_Product(path: ProductPath, body: ProductBody):
    """ Atualizar um produto
    
        Atualiza o nome, email, descricao, preco, quantidade de um produto existente.
    """
    product = ProductModel.find_product(path.id)

    if product:
        try:
            product.nome = body.nome if body.nome else product.nome
            product.descricao = body.descricao if body.descricao else product.descricao
            product.preco = body.preco if body.preco else product.preco
            product.quantidade = body.quantidade if body.quantidade else product.quantidade

            product.save_product()

            return product.json(), 200
        except Exception as e:
            banco.session.rollback()  
            return {'message': f'Erro ao atualizar o produto: {str(e)}'}, 500
    return {'message': 'Produto não encontrado'}, 404

@app.delete('/api/produto/<int:id>', tags=[produto_tag],
            responses={
                    "200": DeleteSchema, 
                    "400": ErrorSchema, 
                    "404": ErrorSchema, 
                    "401": ErrorAuthorizationSchema, 
                    "500": ServerErrorSchema},
            security=[{"Bearer Token": []}])
@jwt_required()
def delete_Product(path: ProductPath):
    """ Deleta um produto
    
        Remove um produto por um ID existente.
    """
    success = ProductModel.delete_by_id(path.id)  
    if success:
        return {"message": "Produto deletado com sucesso"}, 200
    return {"message": "Produto não encontrado"}, 404

if __name__ == '__main__':
    from sql_alchemy import banco
    banco.init_app(app)
    app.run(debug=True, host='0.0.0.0', port=5002)