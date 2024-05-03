import textwrap

def analisa_cpf(texto):
   barre_isso = ("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
   for char in texto:
      if char not in texto:
        return True
      return False

def menu():
 menu = '''
 [D]\t Depositar 
 [W]\t Sacar
 [BS]\t Extrato
 [NA]\t Nova conta
 [LA]\t Listar contas
 [NU]\t Novo usuário
 [Q]\t Sair

 => '''
 return input(textwrap.dedent(menu))

def depositar(saldo, valor, extrato, /):
    if valor > 0 :
        saldo += valor
        extrato += f"Depósito:\tR$ {valor : .2f}\n"
        print ("\n ==== Depósito realizado com sucesso ! ====")
    else:
        print ("ඞඞඞ Operação falhou! O valor informado é invalido. ඞඞඞ")

    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques > limite_saques

    if excedeu_saldo:
        print ("ඞඞඞ Operação falhou! Você não tem saldo suficiente ඞඞඞ")
    
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque:\t\tR$ {valor: .2f}\n"
        numero_saques += 1
        print("\n=== Saque realizado com sucesso! ===")
    
    else:
        print("\nඞඞඞ Operação falhou! O valor informado é invalido. ඞඞඞ")
    
    return saldo, extrato

def exibir_extrato(saldo, /, *, extrato):
   print("\n================== EXTRATO ==================")
   print("Não foram realizadas  movimentações." if not extrato else extrato)
   print(f"\nSaldo:\t\tR$ {saldo:.2f}")
   print("=============================================")

def criar_usuario (usuarios):
    cpf = input("Informe o CPF do Usuário: ")
    usuario = filtrar_usuarios(cpf, usuarios)

    if analisa_cpf(cpf):
      print("Erro forneça apenas números em seu CPF !")

    if usuario :
      print ("Erro Ja existe alguem com esse CPF !")
      return
   
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (DD--MM--AA): ")
    endereco = input("Informe o endereço (logradouro, nmro - bairro - cidade/sigla do estado)")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    print("=== Usuário criado com sucesso! ===")

def filtrar_usuarios(cpf, usuarios):
   usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
   return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, numero_conta, usuarios):
   cpf = input ("Informe o CPF do usuário: ")
   usuario = filtrar_usuarios(cpf, usuarios)

   if usuario:
      print("\n=== Conta criada com sucesso! ===")
      return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
   
   print("\n ඞඞඞ Usuário não encontrado, fluxo de criação de conta encerrado ! ඞඞඞ")

def listar_contas(contas):
   for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usario']['nome']}
        """
        print ("=" * 100)
        print (textwrap.dedent(linha))             

def main ():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500 
    extrato = ''
    numero_saques = 0
    usuarios = []
    contas = []

    while True :
        opcao = menu()

        if opcao == 'D':
            valor = float(input('Informe o valor do deposito: '))
                      
            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == 'W':
            valor = float(input('Informe o valor do saque: '))

            saldo, extrato = sacar (
                saldo = saldo,
                valor = valor,
                extrato = extrato,
                limite= limite,
                numero_saques = numero_saques,
                limite_saques = LIMITE_SAQUES,
            )

        elif opcao == 'BS':
            exibir_extrato(saldo, extrato=extrato)
    
        elif opcao == 'NU':
            criar_usuario(usuarios)
    
        elif opcao == 'NA':
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
               contas.append(contas)

        elif opcao == "LA":
           listar_contas(contas)

        elif opcao == 'Q':
         break

        else:
         print("Operação inválida, por favor selecione novamente a operação desejada.")

main()