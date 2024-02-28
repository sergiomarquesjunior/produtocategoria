from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import Column, Uuid, uuid, String, DateTime, func, DECIMAL, INTEGER, Boolean, ForeignKey,




motor = create_engine("sqlite+pysqlite://banco_de_dados.sqlite", echo=True)



class base(DeclarativeBase):
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
    preco = Column(DECIMAL(precision: 10, scale:2),
            default=0.00)
    estoque = Column(INTEGER,
                     default=0)
    ativo = Column(Boolean,
                   default=True)
    categoria_id = Column(Uuid(as_uuid=True),
                          ForeignKey("tbl_categorias.id"))

    categoria = relationship("Categoria",
                             back_populates="listas_de_produtos")
