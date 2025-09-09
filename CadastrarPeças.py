import sqlite3

DB_PATH = 'pecas_empilhadeira_pronto.db'

def escolher(texto, opcoes):
    print(f"\n{texto}")
    for i, opcao in enumerate(opcoes, 1):
        print(f"{i} - {opcao}")
    while True:
        try:
            escolha = int(input("Digite o número da opção: "))
            if 1 <= escolha <= len(opcoes):
                return opcoes[escolha - 1]
            else:
                print("❌ Opção inválida. Tente novamente.")
        except ValueError:
            print("❌ Por favor, digite um número válido.")

def cadastrar_peca():
    print("\n🔧 CADASTRO DE PEÇAS 🔧")

    marca = escolher("Qual a marca da empilhadeira?", ["Yale", "Hyster", "Hangcha"])
    tipo_energia = escolher("Qual o tipo de energia?", ["GLP", "Diesel", "Elétrica"])
    modelo = input("\nDigite o modelo da empilhadeira (Ex.: GDP50VX, 70VX...): ").strip()
    motor = input("\nDigite o motor (Ex.: Kubota 3.8L, GM, PSI...): ").strip()
    nome_peca = input("\nDigite o nome da peça (Ex.: Motor de Partida): ").strip()
    codigo_peca = input("\nDigite o código da peça (Ex.: 582018430): ").strip()
    observacoes = input("\nObservações (Opcional - pressione Enter para deixar vazio): ").strip()
    tipo_peca = input("\nDigite o tipo de peça (Ex.: Motor, sensores, filtros): ")
    versao_equipamento = input("\n Digite a versão do Equipamento (Ex: A975, B975...): ")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO pecas (
            marca_empilhadeira,
            tipo_energia,
            modelo,
            motor,
            nome_peca,
            codigo_peca,
            observacoes,
            tipo_peca,
            versao_equipamento       
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (marca, tipo_energia, modelo, motor, nome_peca, codigo_peca, observacoes, tipo_peca, versao_equipamento))

    conn.commit()
    conn.close()

    print("\n✅ Peça cadastrada com sucesso!\n")

if __name__ == '__main__':
    while True:
        cadastrar_peca()
        continuar = input("Deseja cadastrar outra peça? (s/n): ").strip().lower()
        if continuar != 's':
            print("\n🔧 Cadastro encerrado. Até mais!")
            break
