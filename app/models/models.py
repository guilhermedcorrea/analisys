from ..extensions import db


class Usuario(db.Model):
    __tablename__ = 'usuario'
    __table_args__ = {"schema": "bigdata"}
    cod_usuario = db.Column(db.Integer, primary_key=True)
    senha = db.Column(db.String(100), unique=False, nullable=False)
    nome_usuario = db.Column(db.String(100), unique=False, nullable=False)
    email = db.Column(db.String(100), unique=False, nullable=False)
    data_alterado = db.Column(db.DateTime, unique=False, nullable=False)
    
    def __repr__(self):
      
        self.session.query(self.model)
        print(self.session.query(self.model))
        return '<Usuario %r>' % self.cod_usuario
    
  