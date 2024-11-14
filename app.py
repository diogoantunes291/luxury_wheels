import tkinter
import re  # Biblioteca REGEX ou Expressões regulares Validar / procurar / substituir e manipular strings!!!!
# IMPORTANTE
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
import sqlite3
from datetime import datetime, timedelta
from gestao_clientes import *
from gestao_veiculos import *
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from gestao_utilizadores import *
from gestao_reservas import *
from exportar import *
from gestao_pagamentos import *
from dashboard_grafico import *
# este import em cima não está a fazer nada sendo que só funciona se o invocar na função por algum erro
# porque no primeiro dia funcionu tudo perfeitamente então para ter a certeza faz o import na função também

# Se quiser posso substituir o self.mensagem por messagebox.showerror/showinfo/showwarning
# exemplo messagebox.showerror('Erro', '...')


class Empresa:
    db = 'database/LuxuryWheels.db'

    def __init__(self, root):
        self.janela = root  # criação da janela
        self.janela.title('Luxury Wheels')
        self.janela.resizable(1, 1)
        self.janela.wm_iconbitmap('recursos/luxury.ico')
        self.tabela_atual = None
        root.geometry('450x350')

        # Designar que todas as janelas são NONE para que antes de abrir possa criar uma verificação se estão abertas
        # para não criar segundas janelas iguais e possivelmente bloquear a base de dados

        self.janela_criar = None
        self.janela_inicio = None
        self.janela_detalhes = None
        self.janela_password = None
        self.janela_password = None
        self.janela_dashboard = None

        frame = LabelFrame(self.janela, text='Luxury Wheels', font=('Nerko One', 20, 'bold'))
        frame.place(x=100, y=60)

        # Criação das etiquetas de usuário e campo de texto
        self.etiqueta_user = Label(frame, text='Nome de Utilizador: ')
        self.etiqueta_user.grid(row=1, column=0)
        self.user = Entry(frame, font=('Arial', 10))
        self.user.focus()
        self.user.grid(row=1, column=1)

        # Criação da etiqueta de Password e o campo de texto
        self.etiqueta_passe = Label(frame, text='Palavra-passe: ')
        self.etiqueta_passe.grid(row=2, column=0)
        self.passe = Entry(frame, font=('Arial', 10), show='•')
        self.passe.grid(row=2, column=1)
        self.forgot_pass = Label(text='Não se lembra da sua palavra-passe?', fg="blue", cursor="hand2",
                                 font=('Arial', 8, 'underline'))
        self.forgot_pass.place(x=130, y=165)
        self.forgot_pass.bind('<Button-1>',
                              self.mudar_password)  # Criação e ligação da frase de alteração de palavra passe

        # Criação do Botão Iniciar Sessão
        botao_iniciarSessao = ttk.Button(frame, text='INICIAR SESSÃO', command=lambda: self.botao_inicio_sessao(
            self.user.get(),
            self.passe.get()))
        botao_iniciarSessao.grid(row=5, column=0, columnspan=2, sticky=W + E)

        self.mensagem = Label(text='', fg='red')
        self.mensagem.place(x=150, y=20)

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)

        # Criação do botão Criar Conta
        self.etiqueta_criar_conta = Label(text='Não tem uma conta?  ')
        self.etiqueta_criar_conta.place(x=170, y=240)
        botao_criar_conta = ttk.Button(text='CRIAR CONTA', command=self.criar_conta)
        botao_criar_conta.place(x=185, y=270)

    def db_consulta(self, consulta, parametros=()):
        with sqlite3.connect(self.db) as con:
            cursor = con.cursor()
            resultado = cursor.execute(consulta, parametros)
            con.commit()
            return resultado

    @staticmethod
    def validar_email(email):
        # Expressão regular para validar e-mail no formato correto!
        padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        if re.match(padrao, email):
            return True
        else:
            return False

    @staticmethod
    def validar_telemovel(telemovel):
        # Expressão regular para validar telemóvel com 9 números!
        padrao = r'^\d{9}$'

        if re.match(padrao, telemovel):
            return True
        else:
            return False

    def validacao_user(self):
        utilizador = self.user.get()
        query = 'SELECT Nome FROM Utilizador WHERE Username = ?'
        registo_nome = self.db_consulta(query, (utilizador,))
        for linha in registo_nome:
            nome = linha[0]
        return nome

    def validacao_password(self):
        password_introduzida = self.passe.get()
        return password_introduzida

    def fechar_tabela_atual(self):
        if self.tabela_atual:
            self.tabela_atual.destroy()
            self.tabela_atual = None

    def criar_conta(self):

        # Verificação se a janela já está aberta
        if self.janela_criar is None or not self.janela_criar.winfo_exists():
            # Criação da Nova janela para o botão Criar Conta
            self.janela_criar = Toplevel()
            self.janela_criar.title = 'Criar conta Luxury'
            self.janela_criar.resizable(False, False)
            self.janela_criar.wm_iconbitmap('recursos/luxury.ico')
            self.janela_criar.geometry('550x350')

            # Criação da nova LabelFrame
            frame_cc = LabelFrame(self.janela_criar, text='Crie uma conta Connosco', font=('Nerko One', 20, 'bold'))
            frame_cc.place(x=100, y=60)

            # Criação das etiquetas Nome, Novo User e Nova Password
            self.etiqueta_nome = Label(frame_cc, text='Nome Completo: ')
            self.etiqueta_nome.grid(row=2, column=0)
            self.input_nome = Entry(frame_cc, font=('Arial', 10))
            self.input_nome.grid(row=2, column=1)
            self.etiqueta_user = Label(frame_cc, text='Nome de Utilizador: ')
            self.etiqueta_user.grid(row=3, column=0)
            self.input_user = Entry(frame_cc, font=('Arial', 10))
            self.input_user.grid(row=3, column=1)

            self.etiqueta_password = Label(frame_cc, text='Palavra-passe: ')
            self.etiqueta_password.grid(row=4, column=0)
            self.input_password = Entry(frame_cc, font=('Arial', 10), show='•')
            self.input_password.grid(row=4, column=1)
            self.etiqueta_confirmar = Label(frame_cc, text='Confirmar Palavra-passe: ')
            self.etiqueta_confirmar.grid(row=5, column=0)
            self.input_confirmar = Entry(frame_cc, font=('Arial', 10), show='•')
            self.input_confirmar.grid(row=5, column=1)
            self.etiqueta_telemovel = Label(frame_cc, text='Telemóvel: ')
            self.etiqueta_telemovel.grid(row=6, column=0)
            self.input_telemovel = Entry(frame_cc, font=('Arial', 10))
            self.input_telemovel.grid(row=6, column=1)
            self.etiqueta_email = Label(frame_cc, text='Email: ')
            self.etiqueta_email.grid(row=7, column=0)
            self.input_email = Entry(frame_cc, font=('Arial', 10))
            self.input_email.grid(row=7, column=1)

            self.mensagem_criar_conta = Label(self.janela_criar, text='', fg='red')
            self.mensagem_criar_conta.place(x=100, y=270)

            # Criação do botão Criar Conta

            botao_confirmar_criar = ttk.Button(frame_cc, text='CONFIRMAR', command=lambda: self.add_utilizador(
                self.input_nome.get().title(),
                self.input_user.get(),
                self.input_password.get(),
                self.input_telemovel.get(),
                self.input_email.get()))
            botao_confirmar_criar.grid(row=8, column=0, columnspan=3, sticky=W + E)

            frame_cc.grid_columnconfigure(0, weight=1)
            frame_cc.grid_columnconfigure(1, weight=1)
        else:
            # se já existir trás a janela para "cima" das outras janelas
            self.janela_criar.lift()

    def add_utilizador(self, nome_completo, nome_utilizador, password, telemovel, email):

        query = 'INSERT INTO Utilizador VALUES(NULL, ?, ?, ?, ?, ?, "Não")'
        parametros = (nome_completo, nome_utilizador, password, telemovel, email)

        query_username = 'SELECT Username FROM Utilizador'
        registo_username = self.db_consulta(query_username)
        usernames = [username[0] for username in registo_username]
        for username in registo_username:
            username.append(username)

        if nome_utilizador in usernames:
            self.mensagem_criar_conta['text'] = 'Esse USERNAME já está associado a outra conta.'
            self.janela_criar.after(1500, lambda: self.mensagem_criar_conta.config(text=''))
            return

        query_email = 'SELECT Email FROM Utilizador'
        registo_email = self.db_consulta(query_email)
        emails = [email[0] for email in registo_email]
        for email in registo_email:
            emails.append(email)

        if email in emails:
            self.mensagem_criar_conta['text'] = 'Esse email já está associado a outra conta.'
            self.janela_criar.after(1500, lambda: self.mensagem_criar_conta.config(text=''))
            return

        if '' in (nome_completo, nome_utilizador, password, telemovel, email):
            self.mensagem_criar_conta['text'] = 'TODOS OS CAMPOS TÊM DE SER PREENCHIDOS!'
            self.janela_criar.after(1500, lambda: self.mensagem_criar_conta.config(text=''))
        elif not nome_completo.capitalize().replace(' ', '').isalpha():
            self.mensagem_criar_conta['text'] = 'O nome só pode conter letras!!'
            self.janela_criar.after(1500, lambda: self.mensagem_criar_conta.config(text=''))
        elif self.input_password.get() != self.input_confirmar.get():
            self.mensagem_criar_conta['text'] = 'As palavras palavras pass têm de ser iguais!'
            self.janela_criar.after(1500, lambda: self.mensagem_criar_conta.config(text=''))
        elif not self.validar_telemovel(telemovel):
            self.mensagem_criar_conta['text'] = 'Número de telemóvel inválido. (Números portugueses têm 9 numeros!)'
            self.janela_criar.after(1500, lambda: self.mensagem_criar_conta.config(text=''))
        elif not telemovel.isdigit():
            self.mensagem_criar_conta['text'] = 'Número de telemóvel são apenas números!'
            self.janela_criar.after(1500, lambda: self.mensagem_criar_conta.config(text=''))
        elif not self.validar_email(email):
            self.mensagem_criar_conta['text'] = 'Email inválido. Deve estar no formato: nome@email.com'
            self.janela_criar.after(1500, lambda: self.mensagem_criar_conta.config(text=''))
        else:
            dt = datetime.now()
            data_agora = dt.strftime('%Y-%m-%d %H:%M:%S')
            query_movimentos = 'INSERT INTO Movimentos VALUES (NULL, ?)'
            movimentos = f'Utilizador {nome_completo} Adicionado no dia: {data_agora}  Botão Criar Conta'
            self.db_consulta(query_movimentos, (movimentos,))

            self.db_consulta(query, parametros)
            self.mensagem['text'] = 'Conta criada com sucesso!'
            self.janela.after(4000, lambda: self.mensagem.config(text=''))
            self.janela_criar.destroy()

    def mudar_password(self, event):

        if self.janela_password is None or not self.janela_password.winfo_exists():
            # Criação da Nova janela para alterar palavra passe
            self.janela_password = Toplevel()
            self.janela_password.title = 'Alteração de palavra-passe.'
            self.janela_password.resizable(False, False)
            self.janela_password.wm_iconbitmap('recursos/luxury.ico')
            self.janela_password.geometry('550x300')

            # Criação da nova LabelFrame
            frame_mp = LabelFrame(self.janela_password, text='Alteração de Palavra-passe', font=('Nerko One', 20, 'bold'))
            frame_mp.place(x=100, y=60)

            frame_mp.grid_columnconfigure(0, weight=1)
            frame_mp.grid_columnconfigure(1, weight=1)

            # Criação das Etiquetas Email, Nova Palavra-passe e Confirmar nova palavra-passe
            self.etiqueta_nome_confirmar = Label(frame_mp, text='Nome Completo: ')
            self.etiqueta_nome_confirmar.grid(row=0, column=0)
            self.input_nome_confirmar = Entry(frame_mp, font=('Arial', 10))
            self.input_nome_confirmar.grid(row=0, column=1)
            self.etiqueta_email_mudar = Label(frame_mp, text='Email: ', font=('Arial', 10))
            self.etiqueta_email_mudar.grid(row=1, column=0)
            self.input_email_confirmar = Entry(frame_mp, font=('Arial', 10))
            self.input_email_confirmar.grid(row=1, column=1)
            self.etiqueta_passe_mudar = Label(frame_mp, text='Palavra-passe nova:', font=('Arial', 10))
            self.etiqueta_passe_mudar.grid(row=2, column=0)
            self.input_passe_mudar = Entry(frame_mp, font=('Arial', 10), show='•')
            self.input_passe_mudar.grid(row=2, column=1)
            self.etiqueta_passe_confirmar = Label(frame_mp, text='Confirmar Palavra-passe:', font=('Arial', 10))
            self.etiqueta_passe_confirmar.grid(row=3, column=0)
            self.input_passe_confirmar = Entry(frame_mp, font=('Arial', 10), show='•')
            self.input_passe_confirmar.grid(row=3, column=1)

            self.mensagem_password = Label(self.janela_password, text='', fg='red')
            self.mensagem_password.place(x=160, y=270)

            # Criação Botão CONFIRMAR MUDANÇAS

            botao_confirmar_mudar = ttk.Button(frame_mp, text='CONFIRMAR', command=lambda: self.confirmar_mudar(
                self.input_nome_confirmar.get(),
                self.input_email_confirmar.get(),
                self.input_passe_mudar.get()))
            botao_confirmar_mudar.grid(row=4, column=0, columnspan=2, sticky=W + E)
        else:
            # se já existir trás a janela para "cima" das outras janelas
            self.janela_password.lift()

    def confirmar_mudar(self, nome_completo_input, email_input, password_nova):

        query_nome_email = 'SELECT Password FROM Utilizador WHERE Nome = ? AND Email = ?'
        parametros_confirm = (nome_completo_input, email_input)

        resultado = self.db_consulta(query_nome_email, parametros_confirm).fetchone()

        if resultado is None:
            self.mensagem_password['text'] = 'Esse utilizador não existe ou o email está incorreto.'
            self.janela_password.after(1500, lambda: self.mensagem_password.config(text=''))

        password_antiga = resultado[0]

        if password_antiga == self.input_passe_mudar.get():
            self.mensagem_password['text'] = 'A palavra-passe nova não pode ser a mesma da anterior!'
            self.janela_password.after(1500, lambda: self.mensagem_password.config(text=''))
            return
        elif not self.validar_email(email_input):
            self.mensagem_password['text'] = 'Email inválido. Deve estar no formato: nome@email.com'
            self.janela_password.after(1500, lambda: self.mensagem_password.config(text=''))

        if '' in (password_nova, nome_completo_input, email_input):
            self.mensagem_password['text'] = 'TODOS OS CAMPOS TEM DE SER PREENCHIDOS!!!'
            self.janela_password.after(1500, lambda: self.mensagem_password.config(text=''))
            return

        if self.input_passe_mudar.get() != self.input_passe_confirmar.get():
            self.mensagem_password['text'] = 'As palavras-passe têm de ser iguais!'
            self.janela_password.after(1500, lambda: self.mensagem_password.config(text=''))
            return

        query_update = 'UPDATE Utilizador SET Password = ? WHERE Nome = ? AND Email = ?'
        parametros_update = (password_nova, nome_completo_input, email_input)
        self.db_consulta(query_update, parametros_update)
        self.janela_password.destroy()
        self.mensagem['text'] = 'Palavra-passe alterada com sucesso!'
        self.janela.after(1500, lambda: self.mensagem.config(text=''))

    def get_admin(self, admin):
        query_admin = 'SELECT admin FROM Utilizador WHERE Username = ?'
        resultado_admin = self.db_consulta(query_admin, (admin,)).fetchall()
        for i in resultado_admin[0]:
            if i == "Sim":
                return True
            else:
                return False

    def botao_inicio_sessao(self, username, password):

        if not username or not password:
            self.mensagem['text'] = 'TODOS OS CAMPOS DEVEM SER PREENCHIDOS'
            self.janela.after(1500, lambda: self.mensagem.config(text=''))
            return

        query = 'SELECT Username, Password FROM Utilizador WHERE Username = ? AND Password = ?'
        parametros = (username, password)

        resultado = self.db_consulta(query, parametros).fetchone()

        if resultado is None:
            self.mensagem['text'] = 'Nome de Utilizador ou palavra-passe incorretos!'
            self.janela.after(1500, lambda: self.mensagem.config(text=''))
            return

        if self.janela_inicio is None or not self.janela_inicio.winfo_exists():
            # Criação da Nova janela para iniciar sessão
            self.janela_inicio = Toplevel()
            self.janela_inicio.title = 'Bem-Vindo'
            self.janela_inicio.resizable(True, True)
            self.janela_inicio.wm_iconbitmap('recursos/luxury.ico')

            # Obtém o tamanho do ecrã
            largura_ecra = self.janela_inicio.winfo_screenwidth()
            altura_ecra = self.janela_inicio.winfo_screenheight()
            self.janela_inicio.geometry(f'{largura_ecra}x{altura_ecra}+0+0')

            frame_principal = LabelFrame(self.janela_inicio, text='Luxury Wheels', font=('Nerko One', 40), bg='white')
            frame_principal.grid(row=10, column=2, columnspan=4)

            frame_principal.grid_columnconfigure(0, weight=1)
            frame_principal.grid_columnconfigure(1, weight=1)

            self.nome_utilizador = Label(self.janela_inicio, text=f"Bem-Vindo, {self.validacao_user().title()}",
                                         font=('Arial', 13))
            self.nome_utilizador.place(x=20, y=20)

            if self.get_admin(self.user.get()):
                self.ver_movimentos = ttk.Button(self.janela_inicio, text='Ver Movimentos Utilizadores', width=40,
                                                 command=self.ver_movimentos)
                self.ver_movimentos.place(x=250, y=20)

            self.ver_graficos = ttk.Button(frame_principal, text='DASHBOARD | GRÁFICOS', width=40, command=self.dashboard())
            self.ver_graficos.grid(row=3, column=2, columnspan=4, pady=15, padx=35)

            self.todas_reservas = ttk.Button(frame_principal, text='VER RESERVAS', width=40,
                                             command=self.ver_reservas)
            self.todas_reservas.grid(row=5, column=2, columnspan=4, pady=15, padx=35)
            self.ver_detalhes = ttk.Button(frame_principal, text='VER DETALHES', width=40,
                                           command=self.ver_detalhes)
            self.ver_detalhes.grid(row=7, column=2, columnspan=4, pady=15, padx=35)
            self.veiculos_disponiveis = ttk.Button(frame_principal, text='VEICULOS DISPONIVEIS', width=40,
                                                   command=self.ver_veiculos)
            self.veiculos_disponiveis.grid(row=9, column=2, columnspan=4, pady=15, padx=35)
            self.info_mes = ttk.Button(frame_principal, text='INFORMAÇÕES MÊS', width=40,
                                       command=self.ver_info_mes)
            self.info_mes.grid(row=11, column=2, columnspan=4, pady=15, padx=35)
            self.ultimos_clientes = ttk.Button(frame_principal, text='CLIENTES REGISTADOS', width=40,
                                               command=self.ver_clientes)
            self.ultimos_clientes.grid(row=13, column=2, columnspan=4, pady=15, padx=35)
            self.revisao_expirar = ttk.Button(frame_principal, text='REVISÃO A EXPIRAR', width=40,
                                              command=self.ver_revisoes)
            self.revisao_expirar.grid(row=15, column=2, columnspan=4, pady=15, padx=35)
            self.legalizacao_expirar = ttk.Button(frame_principal, text='LEGALIZAÇÃO A EXPIRAR', width=40,
                                                  command=self.ver_legalizacao)
            self.legalizacao_expirar.grid(row=17, column=2, columnspan=4, pady=15, padx=35)
            self.gerir_clientes = ttk.Button(frame_principal, text='GERIR', width=40,
                                             command=self.gerir)
            self.gerir_clientes.grid(row=19, column=2, columnspan=4, pady=15, padx=35)

            self.logout = ttk.Button(self.janela_inicio, text='Terminar Sessão', width=40, command=self.terminar_sessao)
            self.logout.place(x=1200, y=750)

            self.exportar = Exportar_Info(self.janela_inicio, self.db_consulta)

            botao_confirmar = ttk.Button(self.janela_inicio, text='Exportar para EXCEL', width=30,
                                         command=self.exportar.exportar_excel)
            botao_confirmar.place(x=1300, y=50)

            # Criação das tabelas para o grid
            for i in range(20):
                self.janela_inicio.grid_columnconfigure(i, weight=1)
            for i in range(30):
                self.janela_inicio.grid_rowconfigure(i, weight=1)
        else:
            self.janela_inicio.lift()

    def terminar_sessao(self):
        if self.botao_inicio_sessao:
            self.user.delete(0, 'end')
            self.passe.delete(0, 'end')
        self.janela.destroy()
        turn_on()

    def dashboard(self):

        self.fechar_tabela_atual()

        self.dashboard = Dashboard(self.janela_inicio, self.db_consulta, self.janela_dashboard)

        self.dashboard.dashboard_completo()

        botao_grafico = ttk.Button(self.janela_inicio, text='Ver Gráficos Independentes', command=self.dashboard.criar_graficos, width=40)
        botao_grafico.place(x=800, y=150)

        botao_dashboard = ttk.Button(self.janela_inicio, text='Ver Dashboard', command=self.dashboard.dashboard_completo, width=40)
        botao_dashboard.place(x=800, y=200)

        def fechar():
            botao_dashboard.destroy()
            botao_grafico.destroy()
            botao_fechar.destroy()

        botao_fechar = ttk.Button(self.janela_inicio, text='FECHAR', command=fechar, width=40)
        botao_fechar.place(x=800, y=250)

    def ver_movimentos(self):

        self.fechar_tabela_atual()

        query_movimentos = 'SELECT * FROM Movimentos ORDER BY ID ASC'
        registos_movimentos = self.db_consulta(query_movimentos)

        frame_tabela = Frame(self.janela_inicio)
        frame_tabela.grid(row=10, column=10, sticky='nsew')
        frame_tabela.grid_propagate(False)
        frame_tabela.config(width=800, height=300)

        frame_tabela.grid_rowconfigure(0, weight=1)
        frame_tabela.grid_columnconfigure(0, weight=1)

        self.tabela_movimentos = ttk.Treeview(frame_tabela, height=15)
        self.tabela_movimentos.grid(row=10, column=10)
        self.tabela_movimentos.heading('#0', text='Movimentos', anchor=CENTER)

        self.tabela_movimentos.column('#0', width=700)

        def fechar():
            frame_tabela.destroy()

        barra_ajustavel = ttk.Scrollbar(frame_tabela, orient=VERTICAL, command=self.tabela_movimentos.yview)
        barra_ajustavel.grid(row=10, column=13, sticky='ns')

        for linha in registos_movimentos:
            movimentos = linha[1]
            self.tabela_movimentos.insert('', 'end', text=movimentos)

        botao_fechar = ttk.Button(frame_tabela, text='FECHAR', command=fechar)
        botao_fechar.grid(row=3, column=3)

        self.tabela_atual = frame_tabela

    def ver_reservas(self):
        self.fechar_tabela_atual()

        query_update_preco = ('UPDATE Reservas '
                              'SET [Preço Total] = [Preço Dia] * (julianday([Data Fim]) - julianday([Data Inicio]))')
        self.db_consulta(query_update_preco)

        frame_tabela = Frame(self.janela_inicio)
        frame_tabela.grid(row=10, column=12, sticky='nsew')
        frame_tabela.grid_propagate(False)
        frame_tabela.config(width=800, height=300)

        frame_tabela.grid_rowconfigure(0, weight=1)
        frame_tabela.grid_columnconfigure(0, weight=1)

        self.tabela_reservas = ttk.Treeview(frame_tabela, height=15, columns=("1", "2", "3", "4", "5", "6"))
        self.tabela_reservas.grid(row=10, column=12)
        self.tabela_reservas.heading('#0', text='ID', anchor=CENTER)
        self.tabela_reservas.heading('1', text='Nome', anchor=CENTER)
        self.tabela_reservas.heading('2', text='Veiculo', anchor=CENTER)
        self.tabela_reservas.heading('3', text='Data Inicio', anchor=CENTER)
        self.tabela_reservas.heading('4', text='Data Fim', anchor=CENTER)
        self.tabela_reservas.heading('5', text='Dias Restantes', anchor=CENTER)
        self.tabela_reservas.heading('6', text='Preço Total', anchor=CENTER)

        self.tabela_reservas.column('#0', width=40)
        self.tabela_reservas.column('1', width=125)
        self.tabela_reservas.column('2', width=125)
        self.tabela_reservas.column('3', width=90)
        self.tabela_reservas.column('4', width=90)
        self.tabela_reservas.column('5', width=40)
        self.tabela_reservas.column('6', width=70)

        def fechar():
            frame_tabela.destroy()

        barra_ajustavel = ttk.Scrollbar(frame_tabela, orient=VERTICAL, command=self.tabela_reservas.yview)
        barra_ajustavel.grid(row=10, column=13, sticky='ns')

        ver_reservas = StringVar()
        ver_reservas.set('Escolha uma opção:')
        opcoes = ['Ver todas as reservas', 'Ver reservas ativas', 'Ver ultimas 5 reservas', 'Ver reservas expiradas',
                  'Ver próximas reservas']

        barra_reservas = ttk.OptionMenu(frame_tabela, ver_reservas, ver_reservas.get(), *opcoes)
        barra_reservas.grid(row=2, column=1)

        self.tabela_reservas.configure(yscrollcommand=barra_ajustavel.set)

        dt = datetime.now()

        def filtrar():
            opcao_escolhida = ver_reservas.get()

            query_filtrada = 'SELECT * FROM Reservas ORDER BY ID ASC'
            registos_db = self.db_consulta(query_filtrada)

            if opcao_escolhida:
                for item in self.tabela_reservas.get_children():
                    self.tabela_reservas.delete(item)

                if opcao_escolhida == opcoes[0]:
                    for linha in registos_db:
                        data_inicio = datetime.strptime(linha[4], '%Y-%m-%d')
                        data_fim = datetime.strptime(linha[5], '%Y-%m-%d')
                        dias_aluguer = (datetime.strptime(linha[5], '%Y-%m-%d') - datetime.strptime(linha[4],
                                                                                                    '%Y-%m-%d')).days
                        preco_total = linha[6] * dias_aluguer
                        if data_inicio < dt:
                            dias_restantes = ((data_fim - dt) + timedelta(days=1)).days
                        elif data_inicio > dt:
                            dias_restantes = ((data_fim - data_inicio) + timedelta(days=1)).days
                        veiculo = f'{linha[2]} {linha[3]}'
                        if dias_restantes <= 0:
                            dias_restantes = 0
                        self.tabela_reservas.insert('', 'end', text=linha[0], values=(linha[1],
                                                                                      veiculo, linha[4], linha[5],
                                                                                      dias_restantes, preco_total))

                elif opcao_escolhida == opcoes[1]:
                    for linha in registos_db:
                        data_inicio = datetime.strptime(linha[4], '%Y-%m-%d')
                        data_fim = datetime.strptime(linha[5], '%Y-%m-%d')
                        dias_aluguer = (datetime.strptime(linha[5], '%Y-%m-%d') - datetime.strptime(linha[4],
                                                                                                    '%Y-%m-%d')).days
                        preco_total = linha[6] * dias_aluguer
                        if data_inicio < dt:
                            dias_restantes = ((data_fim - dt) + timedelta(days=1)).days
                        elif data_inicio > dt:
                            dias_restantes = ((data_fim - data_inicio) + timedelta(days=1)).days
                        veiculo = f'{linha[2]} {linha[3]}'
                        if data_fim >= dt and data_inicio <= dt:
                            self.tabela_reservas.insert('', 'end', text=linha[0], values=(linha[1],
                                                                                          veiculo, linha[4], linha[5],
                                                                                          dias_restantes, preco_total))

                elif opcao_escolhida == opcoes[2]:
                    query_filtrada_ultimas = 'SELECT * FROM Reservas ORDER BY ID DESC LIMIT 5'
                    registos_db_filtrada = self.db_consulta(query_filtrada_ultimas)
                    for linha in registos_db_filtrada:
                        data_inicio = datetime.strptime(linha[4], '%Y-%m-%d')
                        data_fim = datetime.strptime(linha[5], '%Y-%m-%d')
                        dias_aluguer = (datetime.strptime(linha[5], '%Y-%m-%d') - datetime.strptime(linha[4],
                                                                                                    '%Y-%m-%d')).days
                        preco_total = linha[6] * dias_aluguer
                        dias_restantes = (data_fim - data_inicio).days
                        veiculo = f'{linha[2]} {linha[3]}'
                        self.tabela_reservas.insert('', 'end', text=linha[0], values=(linha[1],
                                                                                      veiculo, linha[4], linha[5],
                                                                                      dias_restantes, preco_total))

                elif opcao_escolhida == opcoes[3]:
                    for linha in registos_db:
                        data_inicio = datetime.strptime(linha[4], '%Y-%m-%d')
                        data_fim = datetime.strptime(linha[5], '%Y-%m-%d')
                        dias_aluguer = (datetime.strptime(linha[5], '%Y-%m-%d') - datetime.strptime(linha[4],
                                                                                                    '%Y-%m-%d')).days
                        preco_total = linha[6] * dias_aluguer
                        if data_inicio < dt:
                            dias_restantes = ((data_fim - dt) + timedelta(days=1)).days
                        elif data_inicio > dt:
                            dias_restantes = ((data_fim - data_inicio) + timedelta(days=1)).days
                        veiculo = f'{linha[2]} {linha[3]}'
                        if dias_restantes <= 0:
                            dias_restantes = 0
                        if data_fim < dt and data_inicio < dt:
                            self.tabela_reservas.insert('', 'end', text=linha[0], values=(linha[1],
                                                                                          veiculo, linha[4], linha[5],
                                                                                          dias_restantes, preco_total))

                elif opcao_escolhida == opcoes[4]:
                    for linha in registos_db:
                        data_inicio = datetime.strptime(linha[4], '%Y-%m-%d')
                        data_fim = datetime.strptime(linha[5], '%Y-%m-%d')
                        dias_aluguer = (datetime.strptime(linha[5], '%Y-%m-%d') - datetime.strptime(linha[4],
                                                                                                    '%Y-%m-%d')).days
                        preco_total = linha[6] * dias_aluguer
                        if data_inicio < dt:
                            dias_restantes = ((data_fim - dt) + timedelta(days=1)).days
                        elif data_inicio > dt:
                            dias_restantes = ((data_fim - data_inicio) + timedelta(days=1)).days
                        veiculo = f'{linha[2]} {linha[3]}'
                        if data_fim >= dt and data_inicio >= dt:
                            self.tabela_reservas.insert('', 'end', text=linha[0], values=(linha[1],
                                                                                          veiculo, linha[4], linha[5],
                                                                                          dias_restantes, preco_total))

        botao_confirmar = Button(frame_tabela, text='CONFIRMAR', command=filtrar)
        botao_confirmar.grid(row=2, column=3)
        botao_fechar = Button(frame_tabela, text='FECHAR', command=fechar)
        botao_fechar.grid(row=3, column=3)

        self.tabela_atual = frame_tabela

    def ver_detalhes(self):

        self.fechar_tabela_atual()

        self.mensagem_detalhes = Label(self.janela_inicio, text='', fg='red')
        self.mensagem_detalhes.grid(row=5, column=0, columnspan=2, sticky=W + E)

        frame_tabela = Frame(self.janela_inicio)
        frame_tabela.grid(row=10, column=6, sticky='nsew')
        frame_tabela.grid_propagate(False)
        frame_tabela.config(width=800, height=300)

        frame_tabela.grid_rowconfigure(0, weight=1)
        frame_tabela.grid_columnconfigure(0, weight=1)

        self.tabela_detalhes = ttk.Treeview(frame_tabela, height=15,
                                            columns=("1", "2", "3", "4", "5", "6", "7", "8", "9",
                                                     "10", "11"))
        self.tabela_detalhes.grid(row=10, column=12)
        self.tabela_detalhes.heading('#0', text='ID', anchor=CENTER)
        self.tabela_detalhes.heading('1', text='Marca', anchor=CENTER)
        self.tabela_detalhes.heading('2', text='Modelo', anchor=CENTER)
        self.tabela_detalhes.heading('3', text='Categoria', anchor=CENTER)
        self.tabela_detalhes.heading('4', text='Tipo', anchor=CENTER)
        self.tabela_detalhes.heading('5', text='Qt Pessoas', anchor=CENTER)
        self.tabela_detalhes.heading('6', text='Imagem', anchor=CENTER)
        self.tabela_detalhes.heading('7', text='Preço', anchor=CENTER)
        self.tabela_detalhes.heading('8', text='Ultima Revisão', anchor=CENTER)
        self.tabela_detalhes.heading('9', text='Ultima Legalização', anchor=CENTER)
        self.tabela_detalhes.heading('10', text='Manutenção', anchor=CENTER)
        self.tabela_detalhes.heading('11', text='Disponivel', anchor=CENTER)

        self.tabela_detalhes.column('#0', width=50)
        self.tabela_detalhes.column('1', width=80)
        self.tabela_detalhes.column('2', width=80)
        self.tabela_detalhes.column('3', width=70)
        self.tabela_detalhes.column('4', width=70)
        self.tabela_detalhes.column('5', width=40)
        self.tabela_detalhes.column('6', width=40)
        self.tabela_detalhes.column('7', width=40)
        self.tabela_detalhes.column('8', width=80)
        self.tabela_detalhes.column('9', width=80)
        self.tabela_detalhes.column('10', width=50)
        self.tabela_detalhes.column('11', width=50)

        def fechar():
            frame_tabela.destroy()

        barra_ajustavel = ttk.Scrollbar(frame_tabela, orient=VERTICAL, command=self.tabela_detalhes.yview)
        barra_ajustavel.grid(row=10, column=13, sticky='ns')

        query = 'SELECT * FROM Veiculos ORDER BY ID'
        registos_db = self.db_consulta(query)

        for item in self.tabela_detalhes.get_children():
            self.tabela_detalhes.delete(item)

        for linha in registos_db:
            self.tabela_detalhes.insert('', 'end', text=linha[0], values=(linha[1], linha[2], linha[3], linha[4],
                                                                          linha[5], linha[6], linha[7], linha[8],
                                                                          linha[9],
                                                                          linha[10], linha[11]))

        botao_detalhes = Button(frame_tabela, text='VER DETALHES', command=self.get_detalhes)
        botao_detalhes.grid(row=11, column=12, columnspan=2, sticky=W + E)

        botao_fechar = Button(frame_tabela, text='FECHAR', command=fechar)
        botao_fechar.grid(row=3, column=3)

        self.tabela_atual = frame_tabela

    def get_detalhes(self):

        def carregar_imagem(janela, caminho_imagem):
            # Por alguma razão só funciona se o import estiver diretamente na função
            from PIL import Image, ImageTk
            # Carregar a imagem com a biblioteca Pillow
            img_pillow = Image.open(caminho_imagem)  # Caminho da imagem
            imagem_redimensionada = img_pillow.resize((300, 200))  # redimensiono a imagem
            img = ImageTk.PhotoImage(imagem_redimensionada)  # a imagem passa a ser a redimensionada e uma PhotoImage

            # Criar o Label com a imagem
            label_imagem = Label(janela, image=img)
            label_imagem.image = img
            label_imagem.place(x=185, y=350)

        if not hasattr(self, 'mensagem_detalhes'):
            self.mensagem_detalhes = Label(self.janela_inicio, text='', fg='red', font=('Arial', 15))
            self.mensagem_detalhes.place(x=850, y=20)

        try:
            self.tabela_detalhes.item(self.tabela_detalhes.selection())['values'][0]
        except IndexError:
            self.mensagem_detalhes['text'] = 'Selecione um Veiculo'
            self.janela_inicio.after(1500, lambda: self.mensagem_detalhes.config(text=''))
            return

        selecao = self.tabela_detalhes.selection()
        item = self.tabela_detalhes.item(selecao[0])

        id = item['text']
        marca = item['values'][0]
        modelo = item['values'][1]
        categoria = item['values'][2]
        tipo = item['values'][3]
        pessoas = item['values'][4]
        imagem = item['values'][5]
        preco = item['values'][6]
        revisao = item['values'][7]
        legalizacao = item['values'][8]
        manutencao = item['values'][9]
        disponivel = item['values'][10]

        self.janela_detalhes = Toplevel()
        self.janela_detalhes.title('Detalhes Veiculos')
        self.janela_detalhes.resizable(False, False)
        self.janela_detalhes.wm_iconbitmap('recursos/luxury.ico')
        self.janela_detalhes.geometry('680x600')

        frame_detalhes = LabelFrame(self.janela_detalhes, text='Detalhes', font=('Nerko One', 40))
        frame_detalhes.place(x=200, y=20)

        self.etiqueta_id = Label(frame_detalhes, text='ID:', font=('Arial', 10))
        self.etiqueta_id.grid(row=1, column=0)
        self.input_id = Entry(frame_detalhes, textvariable=StringVar(self.janela_detalhes, value=id), state='readonly',
                              font=('Arial', 10))
        self.input_id.grid(row=1, column=1)

        self.etiqueta_marca = Label(frame_detalhes, text='Marca:', font=('Arial', 10))
        self.etiqueta_marca.grid(row=2, column=0)
        self.input_marca = Entry(frame_detalhes, textvariable=StringVar(self.janela_detalhes, value=marca),
                                 state='readonly',
                                 font=('Arial', 10))
        self.input_marca.grid(row=2, column=1)

        self.etiqueta_modelo = Label(frame_detalhes, text='Modelo:', font=('Arial', 10))
        self.etiqueta_modelo.grid(row=3, column=0)
        self.input_modelo = Entry(frame_detalhes, textvariable=StringVar(self.janela_detalhes, value=modelo),
                                  state='readonly',
                                  font=('Arial', 10))
        self.input_modelo.grid(row=3, column=1)

        self.etiqueta_categoria = Label(frame_detalhes, text='Categoria:', font=('Arial', 10))
        self.etiqueta_categoria.grid(row=4, column=0)
        self.input_categoria = Entry(frame_detalhes, textvariable=StringVar(self.janela_detalhes, value=categoria),
                                     state='readonly',
                                     font=('Arial', 10))
        self.input_categoria.grid(row=4, column=1)

        self.etiqueta_tipo = Label(frame_detalhes, text='Tipo Veiculo:', font=('Arial', 10))
        self.etiqueta_tipo.grid(row=5, column=0)
        self.input_tipo = Entry(frame_detalhes, textvariable=StringVar(self.janela_detalhes, value=tipo),
                                state='readonly',
                                font=('Arial', 10))
        self.input_tipo.grid(row=5, column=1)

        self.etiqueta_pessoas = Label(frame_detalhes, text='Quantidade Pessoas:', font=('Arial', 10))
        self.etiqueta_pessoas.grid(row=6, column=0)
        self.input_pessoas = Entry(frame_detalhes, textvariable=StringVar(self.janela_detalhes, value=pessoas),
                                   state='readonly',
                                   font=('Arial', 10))
        self.input_pessoas.grid(row=6, column=1)

        self.etiqueta_preco = Label(frame_detalhes, text='Preco Dia:', font=('Arial', 10))
        self.etiqueta_preco.grid(row=7, column=0)
        self.input_preco = Entry(frame_detalhes, textvariable=StringVar(self.janela_detalhes, value=preco),
                                 state='readonly',
                                 font=('Arial', 10))
        self.input_preco.grid(row=7, column=1)

        self.etiqueta_revisao = Label(frame_detalhes, text='Ultima Revisão:', font=('Arial', 10))
        self.etiqueta_revisao.grid(row=8, column=0)
        self.input_revisao = Entry(frame_detalhes, textvariable=StringVar(self.janela_detalhes, value=revisao),
                                   state='readonly',
                                   font=('Arial', 10))
        self.input_revisao.grid(row=8, column=1)

        self.etiqueta_legalizacao = Label(frame_detalhes, text='Ultima Legalização:', font=('Arial', 10))
        self.etiqueta_legalizacao.grid(row=9, column=0)
        self.input_legalizacao = Entry(frame_detalhes, textvariable=StringVar(self.janela_detalhes, value=legalizacao),
                                       state='readonly',
                                       font=('Arial', 10))
        self.input_legalizacao.grid(row=9, column=1)

        self.etiqueta_manutencao = Label(frame_detalhes, text='Manutenção:', font=('Arial', 10))
        self.etiqueta_manutencao.grid(row=10, column=0)
        self.input_manutencao = Entry(frame_detalhes, textvariable=StringVar(self.janela_detalhes, value=manutencao),
                                      state='readonly',
                                      font=('Arial', 10))
        self.input_manutencao.grid(row=10, column=1)

        self.etiqueta_disponivel = Label(frame_detalhes, text='Disponível:', font=('Arial', 10))
        self.etiqueta_disponivel.grid(row=11, column=0)
        self.input_disponivel = Entry(frame_detalhes, textvariable=StringVar(self.janela_detalhes, value=disponivel),
                                      state='readonly',
                                      font=('Arial', 10))
        self.input_disponivel.grid(row=11, column=1)

        # janela em que tem de abrir e a "imagem" é o campo na tabela detalhes que eu chamei em cima
        carregar_imagem(self.janela_detalhes, imagem)

    def ver_veiculos(self):

        self.fechar_tabela_atual()

        query_manutencao = 'UPDATE Veiculos SET Disponivel = "Não" WHERE Manutenção = "Sim"'
        self.db_consulta(query_manutencao)

        query = '''UPDATE Veiculos
                   SET Disponivel = "Não"
                   WHERE ID IN (
                   SELECT id_veiculo
                   FROM Reservas
                   WHERE [Data Inicio] <= DATE("now")
                   AND [Data Fim] >= DATE("now") )'''
        self.db_consulta(query)

        frame_tabela = Frame(self.janela_inicio)
        frame_tabela.grid(row=10, column=6, sticky='nsew')
        frame_tabela.grid_propagate(False)
        frame_tabela.config(width=1000, height=300)

        frame_tabela.grid_rowconfigure(0, weight=1)
        frame_tabela.grid_columnconfigure(0, weight=1)

        self.tabela_veiculos = ttk.Treeview(frame_tabela, height=15, columns=("1", "2", "3", "4", "5", "6",
                                                                              "7", "8", "9", "10"))
        self.tabela_veiculos.grid(row=10, column=12)
        self.tabela_veiculos.heading('#0', text='ID', anchor=CENTER)
        self.tabela_veiculos.heading('1', text='Marca', anchor=CENTER)
        self.tabela_veiculos.heading('2', text='Modelo', anchor=CENTER)
        self.tabela_veiculos.heading('3', text='Tipo Veiculo', anchor=CENTER)
        self.tabela_veiculos.heading('4', text='Qt Pessoas', anchor=CENTER)
        self.tabela_veiculos.heading('5', text='Imagem', anchor=CENTER)
        self.tabela_veiculos.heading('6', text='Preço Dia', anchor=CENTER)
        self.tabela_veiculos.heading('7', text='Ultima Revisão', anchor=CENTER)
        self.tabela_veiculos.heading('8', text='Ultima Legalização', anchor=CENTER)
        self.tabela_veiculos.heading('9', text='Manutenção', anchor=CENTER)
        self.tabela_veiculos.heading('10', text='Disponivel', anchor=CENTER)

        self.tabela_veiculos.column('#0', width=50)
        self.tabela_veiculos.column('1', width=100)
        self.tabela_veiculos.column('2', width=100)
        self.tabela_veiculos.column('3', width=50)
        self.tabela_veiculos.column('4', width=50)
        self.tabela_veiculos.column('5', width=80)
        self.tabela_veiculos.column('6', width=80)
        self.tabela_veiculos.column('7', width=80)
        self.tabela_veiculos.column('8', width=60)
        self.tabela_veiculos.column('9', width=60)
        self.tabela_veiculos.column('10', width=60)

        query = 'SELECT * FROM Veiculos'
        registos_db = self.db_consulta(query)

        categorias_tipos = {}

        for linha in registos_db:
            categoria = linha[3]
            tipo = linha[4]
            if categoria not in categorias_tipos:
                categorias_tipos[categoria] = []
            if tipo not in categorias_tipos[categoria]:
                categorias_tipos[categoria].append(tipo)

        categoria = StringVar()
        categorias = list(categorias_tipos.keys())
        categoria.set(categorias[0])

        self.barra_categorias = ttk.OptionMenu(frame_tabela, categoria, categoria.get(), *categorias)
        self.barra_categorias.grid(row=2, column=1)

        selecionar_tipo = StringVar()
        selecionar_tipo.set('Selecione um tipo:')

        self.barra_tipos = ttk.OptionMenu(frame_tabela, selecionar_tipo, selecionar_tipo.get(),
                                          *categorias_tipos[categoria.get()])
        self.barra_tipos.grid(row=4, column=1)

        def atualizar_tipos(*args):
            categoria_selecionada = categoria.get()
            tipos = categorias_tipos[categoria_selecionada]
            selecionar_tipo.set(tipos[0])
            self.barra_tipos['menu'].delete(0, 'end')
            for i in tipos:
                self.barra_tipos['menu'].add_command(label=i, command=lambda value=i: selecionar_tipo.set(value))

        categoria.trace('w', atualizar_tipos)

        def fechar():
            frame_tabela.destroy()

        barra_ajustavel_vertical = ttk.Scrollbar(frame_tabela, orient=VERTICAL,
                                                 command=self.tabela_veiculos.yview)
        barra_ajustavel_vertical.grid(row=10, column=13, sticky='ns')

        def filtrar():

            # para o valor correto do dicionário uso categoria.get() e não categorias porque é a lista inteira
            categoria_selecionada = categoria.get()
            # o mesmo para o tipo tem de ser selecionar_tipo.get() e não categorias_tipos[categorias] por ser a lista
            tipo_selecionado = selecionar_tipo.get()

            for item in self.tabela_veiculos.get_children():
                self.tabela_veiculos.delete(item)

            query_filtrada = 'SELECT * FROM Veiculos WHERE Disponivel = "Sim" AND Manutenção = "Não"'
            parametros = []

            if categoria_selecionada in categorias_tipos:
                query_filtrada += ' AND Categoria = ?'
                parametros.append(categoria_selecionada)

            if tipo_selecionado in categorias_tipos[categoria_selecionada] and tipo != 'Selecione um tipo:':
                query_filtrada += ' AND [Tipo de Veiculo] = ?'
                parametros.append(tipo_selecionado)

            resultados_db_filtrado = self.db_consulta(query_filtrada, parametros)

            for linha in resultados_db_filtrado:
                self.tabela_veiculos.insert('', 'end', text=linha[0], values=(linha[1], linha[2],
                                                                              linha[4], linha[5], linha[6], linha[7],
                                                                              linha[8], linha[9], linha[10], linha[11]))

        botao_confirmar = Button(frame_tabela, text='CONFIRMAR', command=filtrar)
        botao_confirmar.grid(row=2, column=3)
        botao_fechar = Button(frame_tabela, text='FECHAR', command=fechar)
        botao_fechar.grid(row=3, column=3)

        self.tabela_atual = frame_tabela

    def ver_info_mes(self):

        self.fechar_tabela_atual()

        self.mensagem_info_mes = Label(self.janela_inicio, text='', fg='red')
        self.mensagem_info_mes.grid(row=5, column=0, columnspan=2, sticky=W + E)

        query = 'SELECT * FROM Reservas'
        resultados_db = self.db_consulta(query)

        frame_tabela = Frame(self.janela_inicio)
        frame_tabela.grid(row=10, column=12, sticky='nsew')
        frame_tabela.grid_propagate(False)
        frame_tabela.config(width=1000, height=300)

        selecionar_mes = StringVar()
        selecionar_mes.set('Escolha um mês:')
        meses = {'Janeiro': "01", 'Fevereiro': "02", 'Março': "03", 'Abril': "04", 'Maio': "05", 'Junho': "06",
                 'Julho': "07", 'Agosto': "08", 'Setembro': "09", 'Outubro': "10", 'Novembro': "11", 'Dezembro': "12"}

        selecionar_ano = StringVar()
        selecionar_ano.set('Escolha um ano:')
        anos = ['2022', '2023', '2024', '2025']

        barra_meses = ttk.OptionMenu(frame_tabela, selecionar_mes, selecionar_mes.get(), *meses)
        barra_meses.grid(row=0, column=1)

        barra_anos = ttk.OptionMenu(frame_tabela, selecionar_ano, selecionar_ano.get(), *anos)
        barra_anos.grid(row=1, column=1)

        self.tabela_info = ttk.Treeview(frame_tabela, height=15, columns=("1", "2", "3", "4", "5", "6"))
        self.tabela_info.grid(row=10, column=12)
        self.tabela_info.heading('#0', text='Nome', anchor=CENTER)
        self.tabela_info.heading('1', text='Veiculo', anchor=CENTER)
        self.tabela_info.heading('2', text='Data Inicio', anchor=CENTER)
        self.tabela_info.heading('3', text='Data Fim', anchor=CENTER)
        self.tabela_info.heading('4', text='Preço Dia', anchor=CENTER)
        self.tabela_info.heading('5', text='Preço Total', anchor=CENTER)
        self.tabela_info.heading('6', text='Total Mês/Ano', anchor=CENTER)

        self.tabela_info.column('#0', width=150)
        self.tabela_info.column('1', width=75)
        self.tabela_info.column('2', width=75)
        self.tabela_info.column('3', width=75)
        self.tabela_info.column('4', width=75)
        self.tabela_info.column('5', width=75)
        self.tabela_info.column('6', width=75)

        barra_ajustavel = ttk.Scrollbar(frame_tabela, orient=VERTICAL, command=self.tabela_info.yview)
        barra_ajustavel.grid(row=10, column=13, sticky='ns')

        def fechar():
            frame_tabela.destroy()

        def filtrar():
            mes_escolhido = selecionar_mes.get()
            ano_escolhido = selecionar_ano.get()

            query_filtrada = 'SELECT * FROM Reservas WHERE 1=1'
            parametros = []

            if mes_escolhido in meses:
                mes_numerico = meses[mes_escolhido]
                query_filtrada += ' AND substr([Data Inicio], 6, 2) = ?'
                parametros.append(mes_numerico)

            if ano_escolhido in anos:
                query_filtrada += ' AND substr([Data Inicio], 1, 4) = ?'
                parametros.append(ano_escolhido)

            if parametros:
                resultados_db_filtrado = self.db_consulta(query_filtrada, tuple(parametros))

                for item in self.tabela_info.get_children():
                    self.tabela_info.delete(item)

                total_mes = []

                for linha in resultados_db_filtrado:
                    dias_de_aluguer = (datetime.strptime(linha[5], '%Y-%m-%d') - datetime.strptime(linha[4],
                                                                                                   '%Y-%m-%d')).days
                    preco_total = linha[6] * dias_de_aluguer
                    total_mes.append(preco_total)
                    veiculo = f'{linha[2]} {linha[3]}'
                    self.tabela_info.insert('', 'end', text=linha[1],
                                            values=(veiculo, linha[4], linha[5], linha[6], preco_total))

                soma_total = sum(total_mes)

                self.tabela_info.insert('', 'end', text='',
                                        values=('', '', '', '', '', soma_total))

        botao = Button(frame_tabela, text='CONFIRMAR', command=filtrar)
        botao.grid(row=0, column=3)
        botao_fechar = Button(frame_tabela, text='FECHAR', command=fechar)
        botao_fechar.grid(row=0, column=5)

        self.tabela_atual = frame_tabela

        botao = Button(frame_tabela, text='CONFIRMAR', command=filtrar)
        botao.grid(row=0, column=3)
        botao_fechar = Button(frame_tabela, text='FECHAR', command=fechar)
        botao_fechar.grid(row=0, column=5)

        self.tabela_atual = frame_tabela

    def ver_clientes(self):

        self.fechar_tabela_atual()

        self.mensagem_clientes = Label(self.janela_inicio, text='', fg='red')

        query = 'SELECT * FROM Clientes'  # ORDER BY ID DESC LIMIT 5
        registos_db = self.db_consulta(query)

        frame_tabela = Frame(self.janela_inicio)
        frame_tabela.grid(row=10, column=15, sticky='nsew')
        frame_tabela.grid_propagate(False)
        frame_tabela.config(width=800, height=300)

        frame_tabela.rowconfigure(0, weight=1)
        frame_tabela.columnconfigure(0, weight=1)

        self.tabela_clientes_gerir = ttk.Treeview(frame_tabela, height=15, columns=('1', '2', '3', '4', '5'))
        self.tabela_clientes_gerir.grid(row=10, column=12)
        self.tabela_clientes_gerir.heading('#0', text='ID', anchor=CENTER)
        self.tabela_clientes_gerir.heading('1', text='Nome', anchor=CENTER)
        self.tabela_clientes_gerir.heading('2', text='Email', anchor=CENTER)
        self.tabela_clientes_gerir.heading('3', text='Telemóvel', anchor=CENTER)
        self.tabela_clientes_gerir.heading('4', text='Data Inscrição', anchor=CENTER)
        self.tabela_clientes_gerir.heading('5', text='Dias Inscrito', anchor=CENTER)

        self.tabela_clientes_gerir.column('#0', width=70)
        self.tabela_clientes_gerir.column('1', width=150)
        self.tabela_clientes_gerir.column('2', width=150)
        self.tabela_clientes_gerir.column('3', width=100)
        self.tabela_clientes_gerir.column('4', width=100)
        self.tabela_clientes_gerir.column('5', width=70)

        # Criação de uma Barra Ajustavel / ScrollBar caso os registos não cheguem nas 20 linhas de tabela

        barra_ajustavel = ttk.Scrollbar(frame_tabela, orient=VERTICAL, command=self.tabela_clientes_gerir.yview)
        barra_ajustavel.grid(row=10, column=16, sticky='ns')

        # Ligação de Scrollbar à tabela

        self.tabela_clientes_gerir.configure(yscrollcommand=barra_ajustavel.set)

        dt = datetime.now()

        ver_todos = StringVar()
        ver_todos.set('Escolha uma opção:')
        opcoes = ['Ver todos os clientes', 'Ver últimos 5 clientes']

        barra_clientes = ttk.OptionMenu(frame_tabela, ver_todos, ver_todos.get(), *opcoes)
        barra_clientes.grid(row=1, column=0)

        def fechar():
            frame_tabela.destroy()

        def filtrar():
            opcao_escolhida = ver_todos.get()
            query_filtrada = 'SELECT * FROM Clientes'

            if opcao_escolhida:
                for item in self.tabela_clientes_gerir.get_children():
                    self.tabela_clientes_gerir.delete(item)

                if opcao_escolhida == opcoes[0]:
                    query_filtrada += ' ORDER BY ID'
                    registos_db_filtrado = self.db_consulta(query_filtrada)

                    for linha in registos_db_filtrado:
                        data_inicio = datetime.strptime(linha[5], '%Y-%m-%d')
                        dias_inscrito = (dt - data_inicio).days
                        self.tabela_clientes_gerir.insert('', 'end', text=linha[0],
                                                          values=(linha[1], linha[3], linha[4],
                                                                  linha[5], dias_inscrito))
                elif opcao_escolhida == opcoes[1]:
                    query_filtrada += ' ORDER BY ID DESC LIMIT 5'
                    registos_db_filtrado = self.db_consulta(query_filtrada)
                    for linha in registos_db_filtrado:
                        data_inicio = datetime.strptime(linha[5], '%Y-%m-%d')
                        dias_inscrito = (dt - data_inicio).days
                        self.tabela_clientes_gerir.insert('', 'end', text=linha[0],
                                                          values=(linha[1], linha[3], linha[4],
                                                                  linha[5], dias_inscrito))
            else:
                self.mensagem_clientes['text'] = 'Escolha uma opção!'

        botao = Button(frame_tabela, text='CONFIRMAR', command=filtrar)
        botao.grid(row=2, column=0)
        botao_fechar = Button(frame_tabela, text='FECHAR', command=fechar)
        botao_fechar.grid(row=3, column=0)

        self.tabela_atual = frame_tabela

    def ver_revisoes(self):

        self.fechar_tabela_atual()

        query = 'SELECT * FROM Veiculos ORDER BY ID'
        registos_db = self.db_consulta(query)

        frame_tabela = Frame(self.janela_inicio)
        frame_tabela.grid(row=10, column=15, sticky='nsew')
        frame_tabela.grid_propagate(False)
        frame_tabela.config(width=800, height=300)

        frame_tabela.rowconfigure(0, weight=1)
        frame_tabela.columnconfigure(0, weight=1)

        def fechar():
            frame_tabela.destroy()

        self.tabela_revisao = ttk.Treeview(frame_tabela, height=15, columns=('1', '2', '3', '4', '5', '6'))
        self.tabela_revisao.grid(row=10, column=12)
        self.tabela_revisao.heading('#0', text='ID', anchor=CENTER)
        self.tabela_revisao.heading('1', text='Marca', anchor=CENTER)
        self.tabela_revisao.heading('2', text='Modelo', anchor=CENTER)
        self.tabela_revisao.heading('3', text='Categoria', anchor=CENTER)
        self.tabela_revisao.heading('4', text='Ultima Revisão', anchor=CENTER)
        self.tabela_revisao.heading('5', text='Próxima Revisão', anchor=CENTER)
        self.tabela_revisao.heading('6', text='Dias até Revisão', anchor=CENTER)

        self.tabela_revisao.column('#0', width=50)
        self.tabela_revisao.column('1', width=150)
        self.tabela_revisao.column('2', width=150)
        self.tabela_revisao.column('3', width=100)
        self.tabela_revisao.column('4', width=75)
        self.tabela_revisao.column('5', width=100)
        self.tabela_revisao.column('6', width=70)

        barra_ajustavel = ttk.Scrollbar(frame_tabela, orient=VERTICAL, command=self.tabela_revisao.yview)
        barra_ajustavel.grid(row=10, column=13, sticky='ns')

        botao_fechar = ttk.Button(frame_tabela, text='FECHAR', command=fechar)
        botao_fechar.grid(row=3, column=0)

        self.tabela_revisao.configure(yscrollcommand=barra_ajustavel.set)

        dt = datetime.now()

        def mostrar_aviso():
            aviso = False

            if not aviso:
                messagebox.showwarning('ATENÇÃO', 'REVISÃO A EXPIRAR')
            elif aviso:
                pass

        aviso = False

        for linha in registos_db:
            data_fim = datetime.strptime(linha[8], '%d-%m-%Y')
            data_proxima = data_fim + timedelta(days=365)
            data = datetime.strftime(data_proxima, '%d-%m-%Y')
            dias_restantes = (data_proxima - dt).days
            if dias_restantes <= 0:
                self.janela_inicio.after(100, lambda: messagebox.showwarning(
                    'ATENÇÃO', 'DATA DE REVISÃO ULTRAPASSADA '
                               '\nALTERAR DISPONIBILICADE DO VEICULO E FAZER MANUTENÇÃO'))
                aviso = True
                dias_restantes = 0
            elif dias_restantes <= 5 and not aviso:
                self.janela_inicio.after(100, mostrar_aviso)
                aviso = True
            if dias_restantes <= 15:
                self.tabela_revisao.insert('', 'end', text=linha[0], values=(linha[1], linha[2], linha[3],
                                                                             linha[8], data, dias_restantes))
        self.tabela_atual = frame_tabela

    def ver_legalizacao(self):

        self.fechar_tabela_atual()

        query = 'SELECT * FROM Veiculos ORDER BY Categoria ASC'
        registos_db = self.db_consulta(query)

        frame_tabela = Frame(self.janela_inicio)
        frame_tabela.grid(row=10, column=15, sticky='nsew')
        frame_tabela.grid_propagate(False)
        frame_tabela.config(width=800, height=300)

        frame_tabela.rowconfigure(0, weight=1)
        frame_tabela.columnconfigure(0, weight=1)

        self.tabela_legalizacao = ttk.Treeview(frame_tabela, height=15, columns=('1', '2', '3', '4', '5', '6'))
        self.tabela_legalizacao.grid(row=10, column=12)
        self.tabela_legalizacao.heading('#0', text='ID', anchor=CENTER)
        self.tabela_legalizacao.heading('1', text='Marca', anchor=CENTER)
        self.tabela_legalizacao.heading('2', text='Modelo', anchor=CENTER)
        self.tabela_legalizacao.heading('3', text='Categoria', anchor=CENTER)
        self.tabela_legalizacao.heading('4', text='Ultima legalização', anchor=CENTER)
        self.tabela_legalizacao.heading('5', text='Próxima legalização', anchor=CENTER)
        self.tabela_legalizacao.heading('6', text='Dias até legalização', anchor=CENTER)

        self.tabela_legalizacao.column('#0', width=70)
        self.tabela_legalizacao.column('1', width=120)
        self.tabela_legalizacao.column('2', width=120)
        self.tabela_legalizacao.column('3', width=120)
        self.tabela_legalizacao.column('4', width=100)
        self.tabela_legalizacao.column('5', width=100)
        self.tabela_legalizacao.column('6', width=100)

        dt = datetime.now()

        aviso = False

        def fechar():
            frame_tabela.destroy()

        botao_fechar = ttk.Button(frame_tabela, text='FECHAR', command=fechar)
        botao_fechar.grid(row=3, column=0)

        for linha in registos_db:
            id = linha[0]
            data_fim = datetime.strptime(linha[8], '%d-%m-%Y')
            data_proxima = data_fim + timedelta(days=365)
            data = datetime.strftime(data_proxima, '%d-%m-%Y')
            dias_restantes = (data_proxima - dt).days
            if dias_restantes <= 0:
                self.janela_inicio.after(100, lambda: messagebox.showwarning(
                    'ATENÇÃO', 'LEGALIZAÇÃO EXPIRADA\nALTERAR DISPONIBILICADE DO VEICULO'))
                dias_restantes = 0
                aviso = True
            elif dias_restantes <= 5 and not aviso:
                self.janela_inicio.after(100, lambda: messagebox.showwarning(
                    'ATENÇÃO', 'LEGALIZAÇÃO PROXIMA DE EXPIRAR'))
                aviso = True
            if dias_restantes <= 15:
                self.tabela_legalizacao.insert('', 'end', text=linha[0], values=(linha[1], linha[2], linha[3], linha[8],
                                                                                 data, dias_restantes))
        self.tabela_atual = frame_tabela

    def gerir(self):

        self.mensagem_inicio = Label(self.janela_inicio, text='', fg='red', font=('Arial', 15))
        self.mensagem_inicio.place(x=800, y=20)

        self.fechar_tabela_atual()

        frame_gerir = LabelFrame(self.janela_inicio, text='Luxury Wheels', font=('Nerko One', 40))
        frame_gerir.grid(row=10, column=12, columnspan=4)

        gerir = StringVar()
        gerir.set('Escolha uma opção:')
        opcoes = ['Gerir Clientes', 'Gerir Reservas', 'Gerir Veiculos', 'Gerir Pagamentos', 'Gerir Utilizadores']

        barra_gerir = ttk.OptionMenu(frame_gerir, gerir, gerir.get(), *opcoes)
        barra_gerir.grid(row=0, column=0)

        botao_fechar = Button(frame_gerir, text='FECHAR', command=frame_gerir.destroy)
        botao_fechar.grid(row=0, column=1, columnspan=3)

        frame_gerir.grid_columnconfigure(0, weight=1)
        frame_gerir.grid_columnconfigure(1, weight=1)

        def ao_selecionar_opcao(*args):

            self.fechar_tabela_atual()

            if gerir.get() == opcoes[0]:
                frame_tabela = Frame(frame_gerir)
                frame_tabela.grid(row=1, column=0, sticky='nsew')
                frame_tabela.grid_propagate(False)
                frame_tabela.config(width=800, height=300)

                frame_tabela.rowconfigure(0, weight=1)
                frame_tabela.columnconfigure(0, weight=1)

                self.tabela_clientes_gerir = ttk.Treeview(frame_tabela, height=15,
                                                          columns=('1', '2', '3', '4', '5'))
                self.tabela_clientes_gerir.grid(row=0, column=0)
                self.tabela_clientes_gerir.heading('#0', text='ID', anchor=CENTER)
                self.tabela_clientes_gerir.heading('1', text='Nome', anchor=CENTER)
                self.tabela_clientes_gerir.heading('2', text='Palavra-Passe', anchor=CENTER)
                self.tabela_clientes_gerir.heading('3', text='Email', anchor=CENTER)
                self.tabela_clientes_gerir.heading('4', text='Telemóvel', anchor=CENTER)
                self.tabela_clientes_gerir.heading('5', text='Data Inscrição', anchor=CENTER)

                self.tabela_clientes_gerir.column('#0', width=70)
                self.tabela_clientes_gerir.column('1', width=150)
                self.tabela_clientes_gerir.column('2', width=70)
                self.tabela_clientes_gerir.column('3', width=150)
                self.tabela_clientes_gerir.column('4', width=100)
                self.tabela_clientes_gerir.column('5', width=100)

                nome_utilizador = self.validacao_user()
                self.gestao_clientes = Gestao_Clientes(self.janela_inicio, self.db_consulta, self.tabela_clientes_gerir,
                                                       nome_utilizador)

                query = 'SELECT * FROM Clientes'
                registos_db = self.db_consulta(query)

                for item in self.tabela_clientes_gerir.get_children():
                    self.tabela_clientes_gerir.delete(item)

                for linha in registos_db:
                    self.tabela_clientes_gerir.insert('', 'end', text=linha[0],
                                                      values=(linha[1], linha[2], linha[3], linha[4],
                                                              linha[5]))

                barra_ajustavel = ttk.Scrollbar(frame_tabela, orient=VERTICAL, command=self.tabela_clientes_gerir.yview)
                barra_ajustavel.grid(row=0, column=1, sticky='ns')

                self.tabela_clientes_gerir.configure(yscrollcommand=barra_ajustavel.set)

                botao_adicionar = Button(frame_tabela, text='ADICIONAR CLIENTE',
                                         command=self.gestao_clientes.criar_cliente)
                botao_adicionar.grid(row=1, column=0, sticky=W + E)

                botao_editar = Button(frame_tabela, text='EDITAR', command=self.gestao_clientes.editar_cliente)
                botao_editar.grid(row=2, column=0, sticky=W + E)

                botao_eliminar = Button(frame_tabela, text='ELIMINAR', command=self.gestao_clientes.apagar_cliente)
                botao_eliminar.grid(row=3, column=0, sticky=W + E)

                self.tabela_atual = frame_tabela

            elif gerir.get() == opcoes[1]:

                self.fechar_tabela_atual()

                frame_tabela = Frame(frame_gerir)
                frame_tabela.grid(row=1, column=0, sticky='nsew')
                frame_tabela.grid_propagate(False)
                frame_tabela.config(width=800, height=300)

                frame_tabela.grid_rowconfigure(0, weight=1)
                frame_tabela.grid_columnconfigure(0, weight=1)

                self.tabela_reservas_gerir = ttk.Treeview(frame_tabela, height=15,
                                                          columns=("1", "2", "3", "4", "5", "6", "7"))
                self.tabela_reservas_gerir.grid(row=0, column=0)
                self.tabela_reservas_gerir.heading('#0', text='ID', anchor=CENTER)
                self.tabela_reservas_gerir.heading('1', text='Nome', anchor=CENTER)
                self.tabela_reservas_gerir.heading('2', text='Veiculo', anchor=CENTER)
                self.tabela_reservas_gerir.heading('3', text='Data Inicio', anchor=CENTER)
                self.tabela_reservas_gerir.heading('4', text='Data Fim', anchor=CENTER)
                self.tabela_reservas_gerir.heading('5', text='Dias Restantes', anchor=CENTER)
                self.tabela_reservas_gerir.heading('6', text='Preço Dia', anchor=CENTER)
                self.tabela_reservas_gerir.heading('7', text='Preço Total', anchor=CENTER)

                self.tabela_reservas_gerir.column('#0', width=40)
                self.tabela_reservas_gerir.column('1', width=125)
                self.tabela_reservas_gerir.column('2', width=125)
                self.tabela_reservas_gerir.column('3', width=100)
                self.tabela_reservas_gerir.column('4', width=100)
                self.tabela_reservas_gerir.column('5', width=70)
                self.tabela_reservas_gerir.column('6', width=70)
                self.tabela_reservas_gerir.column('7', width=90)

                query = 'SELECT * FROM Reservas ORDER BY ID DESC'
                registos_db = self.db_consulta(query)

                for item in self.tabela_reservas_gerir.get_children():
                    self.tabela_reservas_gerir.delete(item)

                for linha in registos_db:
                    dt = datetime.now()
                    data_inicio = datetime.strptime(linha[4], '%Y-%m-%d')
                    data_fim = datetime.strptime(linha[5], '%Y-%m-%d')
                    dias_aluguer = (datetime.strptime(linha[5], '%Y-%m-%d') - datetime.strptime(linha[4],
                                                                                                '%Y-%m-%d')).days
                    preco_total = linha[6] * dias_aluguer
                    if data_inicio < dt:
                        dias_restantes = ((data_fim - dt) + timedelta(days=1)).days
                    elif data_inicio > dt:
                        dias_restantes = ((data_fim - data_inicio) + timedelta(days=1)).days
                    veiculo = f'{linha[2]} {linha[3]}'
                    if dias_restantes <= 0:
                        dias_restantes = 0
                    self.tabela_reservas_gerir.insert('', 'end', text=linha[0], values=(linha[1],
                                                                                        veiculo, linha[4], linha[5],
                                                                                        dias_restantes, linha[6],
                                                                                        preco_total))

                barra_ajustavel = ttk.Scrollbar(frame_tabela, orient=VERTICAL, command=self.tabela_reservas_gerir.yview)
                barra_ajustavel.grid(row=0, column=1, sticky='ns')

                self.tabela_reservas_gerir.configure(yscrollcommand=barra_ajustavel.set)

                nome_utilizador = self.validacao_user()
                self.gestao_reservas = Gestao_Reservas(self.janela_inicio, self.db_consulta, self.tabela_reservas_gerir,
                                                       nome_utilizador)

                botao_adicionar = Button(frame_tabela, text='ADICIONAR RESERVA',
                                         command=self.gestao_reservas.criar_reserva)
                botao_adicionar.grid(row=1, column=0, sticky=W + E)

                botao_editar = Button(frame_tabela, text='EDITAR', command=self.gestao_reservas.editar_reserva)
                botao_editar.grid(row=2, column=0, sticky=W + E)

                botao_eliminar = Button(frame_tabela, text='ELIMINAR', command=self.gestao_reservas.apagar_reserva)
                botao_eliminar.grid(row=3, column=0, sticky=W + E)

                self.tabela_atual = frame_tabela

            elif gerir.get() == opcoes[2]:

                self.fechar_tabela_atual()

                frame_tabela = Frame(frame_gerir)
                frame_tabela.grid(row=1, column=0, sticky='nsew')
                frame_tabela.grid_propagate(False)
                frame_tabela.config(width=800, height=300)

                frame_tabela.grid_rowconfigure(0, weight=1)
                frame_tabela.grid_columnconfigure(0, weight=1)

                self.tabela_veiculos_gerir = ttk.Treeview(frame_tabela, height=15, columns=("1", "2", "3", "4", "5",
                                                                                            '6', '7', '8', '9', '10',
                                                                                            '11', '12'))
                self.tabela_veiculos_gerir.grid(row=0, column=0)
                self.tabela_veiculos_gerir.heading('#0', text='ID', anchor=CENTER)
                self.tabela_veiculos_gerir.heading('1', text='Marca', anchor=CENTER)
                self.tabela_veiculos_gerir.heading('2', text='Modelo', anchor=CENTER)
                self.tabela_veiculos_gerir.heading('3', text='Categoria', anchor=CENTER)
                self.tabela_veiculos_gerir.heading('4', text='Tipo', anchor=CENTER)
                self.tabela_veiculos_gerir.heading('5', text='QT Pessoas', anchor=CENTER)
                self.tabela_veiculos_gerir.heading('6', text='Imagem', anchor=CENTER)
                self.tabela_veiculos_gerir.heading('7', text='Preço Dia', anchor=CENTER)
                self.tabela_veiculos_gerir.heading('8', text='Ultima Revisão', anchor=CENTER)
                self.tabela_veiculos_gerir.heading('9', text='Ultima Legalização', anchor=CENTER)
                self.tabela_veiculos_gerir.heading('10', text='Manutenção', anchor=CENTER)
                self.tabela_veiculos_gerir.heading('11', text='Disponivel', anchor=CENTER)
                self.tabela_veiculos_gerir.heading('12', text='Matrícula', anchor=CENTER)

                self.tabela_veiculos_gerir.column('#0', width=50)
                self.tabela_veiculos_gerir.column('1', width=100)
                self.tabela_veiculos_gerir.column('2', width=90)
                self.tabela_veiculos_gerir.column('3', width=90)
                self.tabela_veiculos_gerir.column('4', width=90)
                self.tabela_veiculos_gerir.column('5', width=50)
                self.tabela_veiculos_gerir.column('6', width=90)
                self.tabela_veiculos_gerir.column('7', width=50)
                self.tabela_veiculos_gerir.column('8', width=90)
                self.tabela_veiculos_gerir.column('9', width=50)
                self.tabela_veiculos_gerir.column('10', width=50)
                self.tabela_veiculos_gerir.column('11', width=50)
                self.tabela_veiculos_gerir.column('12', width=90)

                nome_utilizador = self.validacao_user()
                self.gestao_veiculos = Gestao_Veiculos(self.janela_inicio, self.db_consulta, self.tabela_veiculos_gerir,
                                                       nome_utilizador)

                query = 'SELECT * FROM Veiculos ORDER BY ID ASC'
                registos_db = self.db_consulta(query)

                for item in self.tabela_veiculos_gerir.get_children():
                    self.tabela_veiculos_gerir.delete(item)

                for linha in registos_db:
                    self.tabela_veiculos_gerir.insert('', 'end', text=linha[0], values=(linha[1],
                                                                                        linha[2], linha[3], linha[4],
                                                                                        linha[5], linha[6], linha[7],
                                                                                        linha[8], linha[9], linha[10],
                                                                                        linha[11], linha[12]))

                barra_ajustavel = ttk.Scrollbar(frame_tabela, orient=VERTICAL,
                                                command=self.tabela_veiculos_gerir.yview)
                barra_ajustavel.grid(row=0, column=1, sticky='ns')

                barra_ajustavel_horizontal = ttk.Scrollbar(frame_tabela, orient=HORIZONTAL,
                                                           command=self.tabela_veiculos_gerir.xview)
                barra_ajustavel_horizontal.grid(row=1, column=0, sticky='we')

                self.tabela_veiculos_gerir.configure(yscrollcommand=barra_ajustavel.set)

                botao_adicionar = Button(frame_tabela, text='ADICIONAR VEICULO',
                                         command=self.gestao_veiculos.adicionar_veiculo)
                botao_adicionar.grid(row=2, column=0, sticky=W + E)

                botao_editar = Button(frame_tabela, text='EDITAR', command=self.gestao_veiculos.editar_veiculo)
                botao_editar.grid(row=3, column=0, sticky=W + E)

                botao_eliminar = Button(frame_tabela, text='ELIMINAR', command=self.gestao_veiculos.apagar_veiculo)
                botao_eliminar.grid(row=4, column=0, sticky=W + E)

                self.tabela_atual = frame_tabela

            elif gerir.get() == opcoes[3]:

                self.fechar_tabela_atual()

                frame_tabela = Frame(frame_gerir)
                frame_tabela.grid(row=1, column=0, sticky='nsew')
                frame_tabela.grid_propagate(False)
                frame_tabela.config(width=800, height=300)

                frame_tabela.grid_rowconfigure(0, weight=1)
                frame_tabela.grid_columnconfigure(0, weight=1)

                self.tabela_pagamentos = ttk.Treeview(frame_tabela, height=15)
                self.tabela_pagamentos.grid(row=0, column=0)
                self.tabela_pagamentos.heading('#0', text='Pagamentos', anchor=CENTER)

                self.tabela_pagamentos.column('#0', width=500)

                query = 'SELECT * FROM Pagamentos'
                resultados_db = self.db_consulta(query)

                for item in self.tabela_pagamentos.get_children():
                    self.tabela_pagamentos.delete(item)

                for linha in resultados_db:
                    self.tabela_pagamentos.insert('', 'end', text=linha)

                nome_utilizador = self.validacao_user()
                self.gestao_pagamentos = Gestao_Pagamentos(self.janela_inicio, self.db_consulta, self.tabela_pagamentos,
                                                           nome_utilizador)

                botao_adicionar = Button(frame_tabela, text='ADICIONAR FORMA DE PAGAMENTO',
                                         command=self.gestao_pagamentos.adicionar_pagamento)
                botao_adicionar.grid(row=1, column=0, sticky=W + E)

                botao_editar = Button(frame_tabela, text='EDITAR', command=self.gestao_pagamentos.editar_pagamento)
                botao_editar.grid(row=2, column=0, sticky=W + E)

                botao_eliminar = Button(frame_tabela, text='ELIMINAR', command=self.gestao_pagamentos.apagar_pagamento)
                botao_eliminar.grid(row=3, column=0, sticky=W + E)
                self.tabela_atual = frame_tabela

            elif gerir.get() == opcoes[4] and self.get_admin(self.user.get()):

                self.fechar_tabela_atual()

                frame_tabela = LabelFrame(frame_gerir)
                frame_tabela.grid(row=1, column=0, sticky='nsew')
                frame_tabela.grid_propagate(False)
                frame_tabela.config(width=800, height=300)

                frame_tabela.rowconfigure(0, weight=1)
                frame_tabela.columnconfigure(0, weight=1)

                self.tabela_utilizadores_gerir = ttk.Treeview(frame_tabela, height=15, columns=('1', '2', '3', '4', '5',
                                                                                                '6'))
                self.tabela_utilizadores_gerir.grid(row=0, column=0)
                self.tabela_utilizadores_gerir.heading('#0', text='ID', anchor=CENTER)
                self.tabela_utilizadores_gerir.heading('1', text='Nome Completo', anchor=CENTER)
                self.tabela_utilizadores_gerir.heading('2', text='Nome Utilizador', anchor=CENTER)
                self.tabela_utilizadores_gerir.heading('3', text='Palavra-Passe', anchor=CENTER)
                self.tabela_utilizadores_gerir.heading('4', text='Telemóvel', anchor=CENTER)
                self.tabela_utilizadores_gerir.heading('5', text='Email', anchor=CENTER)
                self.tabela_utilizadores_gerir.heading('6', text='Admin', anchor=CENTER)

                self.tabela_utilizadores_gerir.column('#0', width=40)
                self.tabela_utilizadores_gerir.column('1', width=150)
                self.tabela_utilizadores_gerir.column('2', width=100)
                self.tabela_utilizadores_gerir.column('3', width=75)
                self.tabela_utilizadores_gerir.column('4', width=75)
                self.tabela_utilizadores_gerir.column('5', width=100)
                self.tabela_utilizadores_gerir.column('6', width=40)

                query = 'SELECT * FROM Utilizador'
                registos_db = self.db_consulta(query)

                for item in self.tabela_utilizadores_gerir.get_children():
                    self.tabela_utilizadores_gerir.delete(item)

                for linha in registos_db:
                    self.tabela_utilizadores_gerir.insert('', 'end', text=linha[0], values=(linha[1], linha[2],
                                                                                            linha[3], linha[4],
                                                                                            linha[5],
                                                                                            linha[6]))

                barra_ajustavel = ttk.Scrollbar(frame_tabela, orient=VERTICAL,
                                                command=self.tabela_utilizadores_gerir.yview)
                barra_ajustavel.grid(row=0, column=1, sticky='ns')

                self.tabela_utilizadores_gerir.configure(yscrollcommand=barra_ajustavel.set)

                nome_user = self.validacao_user()
                self.gestao_utilizadores = Gestao_Utilizadores(self.janela_inicio, self.db_consulta,
                                                               self.tabela_utilizadores_gerir, nome_user)

                botao_adicionar = Button(frame_tabela, text='ADICIONAR UTILIZADOR',
                                         command=self.gestao_utilizadores.adicionar_utilizador)
                botao_adicionar.grid(row=1, column=0, sticky=W + E)

                botao_editar = Button(frame_tabela, text='EDITAR', command=self.gestao_utilizadores.editar_utilizador)
                botao_editar.grid(row=2, column=0, sticky=W + E)

                botao_eliminar = Button(frame_tabela, text='ELIMINAR',
                                        command=self.gestao_utilizadores.apagar_utilizador)
                botao_eliminar.grid(row=3, column=0, sticky=W + E)

                self.tabela_atual = frame_tabela

            else:
                self.mensagem_inicio['text'] = 'Não tem permissões para gerir Utilizadores.'
                self.janela_inicio.after(3000, lambda: self.mensagem_inicio.config(text=''))

        # esta linha de código faz com que ao selecionar a opção não precise de um botão de confirmar
        gerir.trace_add('write', ao_selecionar_opcao)


def turn_on():
    if __name__ == '__main__':
        root = Tk()
        app = Empresa(root)
        root.mainloop()


turn_on()
