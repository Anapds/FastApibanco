import uvicorn
from fastapi import FastAPI
import threading
from banco import Banco

app = FastAPI()
banco = Banco("banco.db")

@app.post("/contas")
def criar_conta(nome: str, saldo: float):
  id_conta = banco.criar_conta(nome, saldo)
  return {"mensagem": f"Conta criada com sucesso. ID da conta: {id_conta}"}


@app.get("/contas/{id_conta}")
def consultar_saldo(id_conta: int):
  conta = banco.buscar_conta(id_conta)
  if conta:
    return {"saldo": conta.saldo}
  return {"mensagem": "Conta não encontrada."}


@app.put("/contas/{id_conta}/depositar")
def depositar(id_conta: int, valor: float):
  banco.depositar(id_conta, valor)
  return {"mensagem": "Depósito realizado com sucesso."}


@app.put("/contas/{id_conta}/sacar")
def sacar(id_conta: int, valor: float):
  try:
    banco.sacar(id_conta, valor)
    return {"mensagem": "Saque realizado com sucesso."}
  except ValueError as e:
    return {"mensagem": str(e)}


if __name__ == '__main__':
  banco.criar_tabela()
  uvicorn.run(app, port=8080, host="127.0.0.1", reload=True)
