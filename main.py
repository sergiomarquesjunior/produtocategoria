import uuid


from sqlalchemy import create_engine, select
from sqlalchemy.orm import DeclarativeBase, relationship, Session
from sqlalchemy import Column, Uuid, String, DateTime, func, DECIMAL, INTEGER, Boolean, ForeignKey




motor = create_engine("sqlite+pysqlite:///banco_de_dados.sqlite", echo=True)



class Base(DeclarativeBase):
    pass


class DatasMixin():
    dta_cadastro = Column(DateTime,
                          server_default=func.now(),
                          nullable=False)
    dta_atualizacao = Column(DateTime,
                             onupdate=func.now(),
                             default=func.now(),
                             nullable=False)
class Categoria(Base, DatasMixin):
    __tablename__ = 'tbl_categorias'
    id = Column(Uuid(as_uuid=True),
                primary_key=True,
                default=uuid.uuid4)
    nome = Column(String(256),
                 nullable=False)

    listas_de_produtos = relationship("Produto",
                                      back_populates="categoria",
                                      cascade="all, delete-orphan",
                                      lazy="selectin")


class Produto(Base, DatasMixin):
    __tablename__ = 'tbl_produtos'

    id = Column(Uuid(as_uuid=True),
                primary_key=True,
                default=uuid.uuid4)
    nome = Column(String(256),
                  nullable=False)
    preco = Column(DECIMAL(10, 2),
            default=0.00)
    estoque = Column(INTEGER,
                     default=0)
    ativo = Column(Boolean,
                   default=True)
    categoria_id = Column(Uuid(as_uuid=True),
                          ForeignKey("tbl_categorias.id"))
    # propriedades de navegação
    categoria = relationship("Categoria",
                             back_populates="listas_de_produtos")

def seed_database():
    # iterar sobre as categorias e adicionar os produtos
   with Session(motor) as sessao:
       registro = sessao.execute(select(Categoria).limit(1)).scalar_one_or_none()
       if registro:
           return
       from seed import seed_data
       for categoria in seed_data:
            cat = Categoria()
            print(f"Semeando a categoria {categoria['categoria']}...")
            cat.nome = categoria["categoria"]
            for produto in categoria["produtos"]:
                p = Produto()
                p.nome = produto["nome"]
                p.preco = produto["preco"]
                p.estoque = 0
                p.ativo = True
                p.categoria = cat
                sessao.add(p)
            sessao.commit()

def incluir_categoria():
    print("Incluindo categoria")
    nome = input("Qual o nome da categoria que você que adicionar?")

if __name__ == "__main__":
    seed_database()





