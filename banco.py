import sqlite3
import threading
from conta_bancaria import Conta


class Banco:

  def __init__(self, arquivo_banco):
    self.arquivo_banco = arquivo_banco
    self.thread_local = threading.local()

  def get_conexao(self):
    if not hasattr(self.thread_local, "conexao"):
      self.thread_local.conexao = sqlite3.connect(self.arquivo_banco)
    return self.thread_local.conexao

  def criar_tabela(self):
    conexao = self.get_conexao()
    cursor = conexao.cursor()
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS contas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                saldo REAL NOT NULL
            )
        """)
    conexao.commit()

  def criar_conta(self, nome, saldo_inicial=0.0):
    conexao = self.get_conexao()
    cursor = conexao.cursor()
    cursor.execute(
      """
            INSERT INTO contas (nome, saldo) VALUES (?, ?)
        """, (nome, saldo_inicial))
    conexao.commit()
    return cursor.lastrowid

  def buscar_conta(self, id_conta):
    conexao = self.get_conexao()
    cursor = conexao.cursor()
    cursor.execute(
      """
            SELECT id, nome, saldo FROM contas WHERE id = ?
        """, (id_conta, ))
    dados = cursor.fetchone()
    if dados:
      id, nome, saldo = dados
      return Conta(id, nome, saldo)
    return None

  def depositar(self, id_conta, valor):
    conta = self.buscar_conta(id_conta)
    if conta:
      conta.depositar(valor)
      conexao = self.get_conexao()
      cursor = conexao.cursor()
      cursor.execute(
        """
                UPDATE contas SET saldo = ? WHERE id = ?
            """, (conta.saldo, conta.id))
      conexao.commit()

  def sacar(self, id_conta, valor):
    conta = self.buscar_conta(id_conta)
    if conta:
      conta.sacar(valor)
      conexao = self.get_conexao()
      cursor = conexao.cursor()
      cursor.execute(
        """
                UPDATE contas SET saldo = ? WHERE id = ?
            """, (conta.saldo, conta.id))
      conexao.commit()
