# Programa
from ContasBancos import CartaoCredito, ContaCorrente


conta_erik = ContaCorrente("Erik", "123.456.789-00", "0001", "123456")
conta_erik._saldo = 100

cartao_erik = CartaoCredito("Erik", conta_erik)
print(f"Titular: {cartao_erik.titular}")
print(f"Conta: {cartao_erik.conta_corrente.num_conta}")
print(f"Relação de cartões: {conta_erik.cartoes[0].numero}")
print(f"Validade: {conta_erik.cartoes[0].validade}")
print(f"Código Segurança: {conta_erik.cartoes[0].cod_seguranca}")
print(conta_erik.__dict__)
print(cartao_erik.__dict__)
