import sqlite3

class BancoDeDados:
    def __init__(self):
        self.conexao = sqlite3.connect("sistema_escolar.sqlite3")
        self.cursor = self.conexao.cursor()
        self.inicializar_tabelas()

    def inicializar_tabelas(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS cursos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                duracao INTEGER NOT NULL
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS alunos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                idade INTEGER NOT NULL,
                curso_id INTEGER NOT NULL,
                FOREIGN KEY (curso_id) REFERENCES cursos (id)
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS notas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                aluno_id INTEGER NOT NULL,
                disciplina TEXT NOT NULL,
                nota REAL NOT NULL,
                FOREIGN KEY (aluno_id) REFERENCES alunos (id)
            )
        """)
        self.conexao.commit()

    def fechar_conexao(self):
        self.conexao.close()

class SistemaEscolar:
    def __init__(self):
        self.db = BancoDeDados()
        self.menu()

    def menu(self):
        while True:
            print("\n--- Sistema de Gestão Escolar ---")
            print("1. Gestão de Cursos")
            print("2. Gestão de Alunos")
            print("3. Lançamento de Notas")
            print("4. Sair")
            opcao = input("Escolha uma opção: ")

            if opcao == "1":
                self.gestao_cursos()
            elif opcao == "2":
                self.gestao_alunos()
            elif opcao == "3":
                self.gestao_notas()
            elif opcao == "4":
                print("Obrigado por usar o sistema! Até logo.")
                self.db.fechar_conexao()
                break
            else:
                print("Opção inválida. Tente novamente.")

    def gestao_cursos(self):
        while True:
            print("\n--- Gestão de Cursos ---")
            print("1. Cadastrar Curso")
            print("2. Atualizar Curso")
            print("3. Apagar Curso")
            print("4. Consultar Cursos")
            print("5. Voltar")
            opcao = input("Escolha uma opção: ")

            if opcao == "1":
                nome = input("Nome do curso: ")
                duracao = int(input("Tempo de duração (anos): "))
                self.db.cursor.execute("INSERT INTO cursos (nome, duracao) VALUES (?, ?)", (nome, duracao))
                self.db.conexao.commit()
                print("Curso cadastrado com sucesso!")

            elif opcao == "2":
                curso_id = int(input("ID do curso para atualizar: "))
                novo_nome = input("Novo nome: ")
                nova_duracao = int(input("Nova duração (anos): "))
                self.db.cursor.execute("UPDATE cursos SET nome = ?, duracao = ? WHERE id = ?", (novo_nome, nova_duracao, curso_id))
                self.db.conexao.commit()
                print("Curso atualizado com sucesso!")

            elif opcao == "3":
                curso_id = int(input("ID do curso para apagar: "))
                self.db.cursor.execute("DELETE FROM cursos WHERE id = ?", (curso_id,))
                self.db.conexao.commit()
                print("Curso apagado com sucesso!")

            elif opcao == "4":
                cursos = self.db.cursor.execute("SELECT * FROM cursos").fetchall()
                for curso in cursos:
                    print(f"ID: {curso[0]} | Nome: {curso[1]} | Duração: {curso[2]} anos")

            elif opcao == "5":
                break

    def gestao_alunos(self):
        while True:
            print("\n--- Gestão de Alunos ---")
            print("1. Cadastrar Aluno")
            print("2. Atualizar Aluno")
            print("3. Apagar Aluno")
            print("4. Consultar Alunos")
            print("5. Voltar")
            opcao = input("Escolha uma opção: ")

            if opcao == "1":
                nome = input("Nome do aluno: ")
                idade = int(input("Idade: "))
                cursos = self.db.cursor.execute("SELECT * FROM cursos").fetchall()
                for curso in cursos:
                    print(f"ID: {curso[0]} | Nome: {curso[1]}")
                curso_id = int(input("ID do curso escolhido: "))
                self.db.cursor.execute("INSERT INTO alunos (nome, idade, curso_id) VALUES (?, ?, ?)", (nome, idade, curso_id))
                self.db.conexao.commit()
                print("Aluno cadastrado com sucesso!")

            elif opcao == "2":
                aluno_id = int(input("ID do aluno para atualizar: "))
                novo_nome = input("Novo nome: ")
                nova_idade = int(input("Nova idade: "))
                self.db.cursor.execute("UPDATE alunos SET nome = ?, idade = ? WHERE id = ?", (novo_nome, nova_idade, aluno_id))
                self.db.conexao.commit()
                print("Aluno atualizado com sucesso!")

            elif opcao == "3":
                aluno_id = int(input("ID do aluno para apagar: "))
                self.db.cursor.execute("DELETE FROM alunos WHERE id = ?", (aluno_id,))
                self.db.conexao.commit()
                print("Aluno apagado com sucesso!")

            elif opcao == "4":
                alunos = self.db.cursor.execute("SELECT a.id, a.nome, a.idade, c.nome FROM alunos a INNER JOIN cursos c ON a.curso_id = c.id").fetchall()
                for aluno in alunos:
                    print(f"\nID: {aluno[0]} | Nome: {aluno[1]} | Idade: {aluno[2]} | Curso: {aluno[3]}")
                    notas = self.db.cursor.execute("SELECT disciplina, nota FROM notas WHERE aluno_id = ?", (aluno[0],)).fetchall()
                    disciplinas = {}
                    for disciplina, nota in notas:
                        if disciplina not in disciplinas:
                            disciplinas[disciplina] = []
                        disciplinas[disciplina].append(nota)
                    
                    media_total = 0
                    total_disciplinas = len(disciplinas)

                    if disciplinas:
                        print("  Notas:")
                        for disciplina, lista_notas in disciplinas.items():
                            lista_notas = lista_notas[:3]
                            media_disciplina = sum(lista_notas) / len(lista_notas)
                            media_total += media_disciplina
                            print(f"    Disciplina: {disciplina} | Notas: {lista_notas} | Média: {media_disciplina:.2f}")

                        media_final = media_total / total_disciplinas if total_disciplinas > 0 else 0
                        print(f"\n  Média Final: {media_final:.2f}")
                    else:
                        print("  Nenhuma nota cadastrada.")

            elif opcao == "5":
                break

    def gestao_notas(self):
        while True:
            print("\n--- Lançamento de Notas ---")
            print("1. Lançar Nota")
            print("2. Voltar")
            opcao = input("Escolha uma opção: ")

            if opcao == "1":
                aluno_id = int(input("ID do aluno: "))
                disciplina = input("Disciplina: ")
                nota = float(input("Nota: "))
                self.db.cursor.execute("INSERT INTO notas (aluno_id, disciplina, nota) VALUES (?, ?, ?)", (aluno_id, disciplina, nota))
                self.db.conexao.commit()
                print("Nota lançada com sucesso!")

            elif opcao == "2":
                break
            else:
                print("Opção inválida, tente novamente.")

SistemaEscolar()