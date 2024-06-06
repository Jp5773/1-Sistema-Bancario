from abc import ABC, abstractmethod
from datetime import datetime
from typing import List
import textwrap

class Cliente:  
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
    
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
    
    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = '0001'
        self._cliente = cliente
        self._historico = Historico()
    
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo
        
        if excedeu_saldo:
            print('\n ඞඞඞ Operação falhou! Você não tem saldo suficiente. ඞඞඞ')

        elif valor > 0:
            self._saldo -= valor
            print('\n === Operação realizada com sucesso! ===')
            return True

        else: 
            print('\n ඞඞඞ Operação falhou! Valor informado é invalido. ඞඞඞ')

        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print('\n === Deposito realizado com sucesso! ===')
            return True
        else:
            print('\n ඞඞඞ Operação falhou! O valor informado é invalido. ඞඞඞ')
            return False

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=1000, limite_saques=4):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques
  
    def sacar(self, valor):
        numero_saques = len([transacao for transacao in self.historico.transacoes if transacao['tipo'] == Saque.__name__])

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print('\n ඞඞඞ Operação falhou! Valor do saque excedo o limite. ඞඞඞ')

        elif excedeu_saques:
            print('\n ඞඞඞ Operação falhou! Número maximo de saques excedido. ඞඞඞ')
        
        else:
            return super().sacar(valor)
        
        return False
  
    def __str__(self):
      return f"""\
          Agência:\t{self.agencia}
          C/C:\t\t{self.numero}
          Titular:\t{self.cliente.nome}
        """
    
class Historico:
    def __init__(self):
        self._trasacoes = []
    
    @property
    def transacoes(self):
        return self._trasacoes
    
    def adicionar_transacao(self, transacao):
        self._trasacoes.append(
            {
                'tipo': transacao.__class__.__name__,
                'valor': transacao.valor,
                'data': datetime.now().strftime
                ('%d-%m-%Y %H:%M:%S')
            }
        )

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

def filtrar_cliente(cpf, clientes):
    for cliente in clientes:
        if cliente.cpf == cpf:
            return cliente
    return None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
            print("\n ඞඞඞ Cliente não possui conta")
            return
    return cliente.contas[0]

def depositar(clientes):
    cpf = input('Informe o CPF do cliente (apenas números): ')
    clientes = filtrar_cliente(cpf, clientes)

    if not clientes:
        print('\n ඞඞඞ Cliente não encontrado! ඞඞඞ')
        return
    
    valor = float(input('Informe o valor do depósito'))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(clientes)
    if not conta:
        return
    
    clientes.realizar_transacao(conta, transacao)

def sacar(clientes):
    cpf = input("Informe o CPF do cliente (somente números): ")
    clientes = filtrar_cliente(cpf, clientes)
    
    if not clientes:
        print('\n ඞඞඞ Cliente não encontrado! ඞඞඞ')
        return
    
    valor = float(input('Inforem o valor do saque:'))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(clientes)
    if not conta:
        return
    
    clientes.realizar_transacao(conta, transacao)

def exibir_extrato(clientes):
    cpf = input('Informe o CPF do cliente (somente números): ')
    cliente = filtrar_cliente(cpf, clientes )

    if not cliente:
        print('\n ඞඞඞ Cliente não encontrado! ඞඞඞ')
        return
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    print ('\n =============== Extrato ===============')
    transacaoes = conta.historico.transacoes

    extrato = ''
    if not transacaoes:
        extrato = 'Não foram realizadas movimentações.'
    else :
        for transacao in transacaoes:
            extrato += f'\n{transacao['tipo']}:\n\tR${transacao['valor']:.2f}'
    
    print(extrato)
    print(f'\nSaldo:\n\tR$ {conta.saldo:.2f}')
    print('======================================')

def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente números): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print('\n ඞඞඞ Ja existe cliente com esse CPF ඞඞඞ')
        return
    
    nome = input("Informe o nome completo: ")
    data_nascimento = input('Informe a data de nascimento (dd - mm - aaaa): ')
    endereco = input('Informe o endereço (logradouro, nmro - bairro - cidade/sigla do estado): ')

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    
    clientes.append(cliente)
    print ("\n === Cliente criado com sucesso! ===")

def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente (somente números): ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print('\n ඞඞඞ Cliente não encontrado, fluxo de criação de conta encerrado! ඞඞඞ')
        return
    
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.adicionar_conta(conta)

    print('\n=== Contra criada com sucesso ! ===')

def listar_contas(contas):
    for conta in contas:
        print('=' * 100)
        print(textwrap.dedent(str(conta)))

def menu():
 menu = '''\n
 ======================MENU======================
 [D]\t Depositar 
 [W]\t Sacar
 [BS]\t Extrato
 [NA]\t Nova conta
 [LA]\t Listar contas
 [NC]\t Novo usuário
 [Q]\t Sair

 => '''
 return input(textwrap.dedent(menu))

def main ():
    clientes = []
    contas = []


    while True:
        opcao = menu()

        if opcao == 'D':
            depositar(clientes)

        elif opcao == 'W':
            sacar(clientes)

        elif opcao == 'BS':
            exibir_extrato(clientes)
        
        elif opcao == 'NC':
            criar_cliente(clientes)
    
        elif opcao == 'NA':
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == "LA":
            listar_contas(contas)

        elif opcao == 'Q':
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

main()