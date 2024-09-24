from sql_alchemy import banco

class ProductModel(banco.Model):
    __tablename__ = 'produtos'

    product_id = banco.Column(banco.Integer, primary_key=True)
    nome = banco.Column(banco.String(100), nullable=False)
    descricao = banco.Column(banco.String(255), nullable=True)
    preco = banco.Column(banco.Float, nullable=False)
    quantidade = banco.Column(banco.Integer, nullable=False)

    def __init__(self, nome, descricao, preco, quantidade):
        self.nome = nome
        self.descricao = descricao
        self.preco = preco
        self.quantidade = quantidade

    def json(self):
        return {
            'product_id': self.product_id,
            'nome': self.nome,
            'descricao': self.descricao,
            'preco': self.preco,
            'quantidade': self.quantidade 
            }

    @classmethod
    def find_product(cls, product_id):
        product = cls.query.filter_by(product_id=product_id).first()
        if product:
            return product
        return None

    @classmethod
    def delete_by_id(cls, product_id):
        try:
            product = cls.find_product(product_id)  
            if product:
                banco.session.delete(product)  
                banco.session.commit()  
                return True  
            return False  
        except Exception as e:
            banco.session.rollback()  
            print(f"Erro ao deletar o usuário: {e}")
            return False

    def save_product(self):
        banco.session.add(self)
        banco.session.commit()

    def delete_product(self):
        banco.session.delete(self)
        banco.session.commit()
        
    


