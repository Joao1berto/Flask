from database import db

class Agendamento(db.Model):
    __tablename__ = "usuario"
    id_agendamento = db.Column(db.Integer, primary_key = True)
    data = db.Column(db.Date)
    cliente = db.Column(db.String(100))
    servico = db.Column(db.String(100))

    def __init__(self, data, cliente, servico):
        self.data = data
        self.cliente = cliente
        self.servico = servico

    def __repr__(self):
        return "<Cliente {}>".format(self.cliente)