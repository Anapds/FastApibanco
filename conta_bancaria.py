class Conta:

  def __init__(self, id, nome, saldo):
    self.id = id
    self.nome = nome
    self.saldo = saldo

  def depositar(self, valor):
    self.saldo += valor

  def sacar(self, valor):
    if self.saldo >= valor:
      self.saldo -= valor
    else:
      raise ValueError("Saldo insuficiente")
