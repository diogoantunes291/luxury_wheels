from tkinter import *
from tkinter import ttk
import re
import sqlite3
from datetime import *
from app import *


class Gestao_Utilizadores:

    def __init__(self, janela_inicio, db_consulta, tabela_utilizadores_gerir, nome_user):
        self.janela_inicio = janela_inicio
        self.db_consulta = db_consulta
        self.tabela_utilizadores_gerir = tabela_utilizadores_gerir
        self.nome_user = nome_user

        self.janela_utilizadores = None

        self.mensagem_apagar = Label(self.janela_inicio, text='', fg='red', font=('Arial', 15))
        self.mensagem_apagar.place(x=850, y=20)

        self.mensagem_editar = Label(self.janela_inicio, text='', fg='red', font=('Arial', 15))
        self.mensagem_editar.place(x=850, y=20)
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

    def adicionar_utilizador(self):

        if self.janela_utilizadores is None or not self.janela_utilizadores.winfo_exists():
            self.janela_utilizadores = Toplevel()
            self.janela_utilizadores.title = 'Criar conta Luxury'
            self.janela_utilizadores.resizable(False, False)
            self.janela_utilizadores.wm_iconbitmap('recursos/luxury.ico')
            self.janela_utilizadores.geometry('500x350')

            # Criação da nova LabelFrame
            frame_cc = LabelFrame(self.janela_utilizadores, text='Novo Utilizador', font=('Nerko One', 20, 'bold'))
            frame_cc.place(x=100, y=60)

            self.mensagem = Label(self.janela_utilizadores, text='', fg='red')
            self.mensagem.place(x=100, y=20)

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

            admin_p = StringVar()
            admin_p.set('Não')
            opcoes_admin = ['Sim', 'Não']

            self.etiqueta_admin = Label(frame_cc, text='Admin: ')
            self.etiqueta_admin.grid(row=8, column=0)
            self.input_admin = ttk.OptionMenu(frame_cc, admin_p, admin_p.get(), *opcoes_admin)
            self.input_admin.grid(row=8, column=1)

            # Criação do botão Criar Conta

            botao_confirmar_criar = ttk.Button(frame_cc, text='CONFIRMAR', command=lambda: self.add_utilizador(
                self.input_nome.get().title(),
                self.input_user.get(),
                self.input_password.get(),
                self.input_telemovel.get(),
                self.input_email.get(),
                admin_p.get()))
            botao_confirmar_criar.grid(row=9, column=0, columnspan=3, sticky=W + E)

            frame_cc.grid_columnconfigure(0, weight=1)
            frame_cc.grid_columnconfigure(1, weight=1)
        else:
            self.janela_utilizadores.lift()

    def add_utilizador(self, nome_completo, nome_utilizador, password, telemovel, email, admin):

        query = 'INSERT INTO Utilizador VALUES(NULL, ?, ?, ?, ?, ?, ?)'
        parametros = (nome_completo, nome_utilizador, password, telemovel, email, admin)

        query_username = 'SELECT Username FROM Utilizador'
        registo_username = self.db_consulta(query_username)
        usernames = [username[0] for username in registo_username]
        for username in registo_username:
            username.append(username)

        if nome_utilizador in usernames:
            self.mensagem['text'] = 'Esse USERNAME já está associado a outra conta.'
            self.janela_utilizadores.after(1500, lambda: self.mensagem.config(text=''))
            return

        query_email = 'SELECT Email FROM Utilizador WHERE Email = ?'
        registo_email = self.db_consulta(query_email, (email,)).fetchone()
        if registo_email:
            self.mensagem['text'] = 'Esse email já está associado a outra conta.'
            self.janela_utilizadores.after(1500, lambda: self.mensagem.config(text=''))
            return

        if '' in (nome_completo, nome_utilizador, password, telemovel, email, admin):
            self.mensagem['text'] = 'TODOS OS CAMPOS TÊM DE SER PREENCHIDOS!'
            self.janela_utilizadores.after(1500, lambda: self.mensagem.config(text=''))
        elif not nome_completo.capitalize().replace(' ', '').isalpha():
            self.mensagem['text'] = 'O nome só pode conter letras!!'
            self.janela_utilizadores.after(1500, lambda: self.mensagem.config(text=''))
        elif self.input_password.get() != self.input_confirmar.get():
            self.mensagem['text'] = 'As palavras palavras pass têm de ser iguais!'
            self.janela_utilizadores.after(1500, lambda: self.mensagem.config(text=''))
        elif not self.validar_telemovel(telemovel):
            self.mensagem['text'] = 'Número de telemóvel inválido. (Números portugueses têm 9 numeros!)'
            self.janela_utilizadores.after(1500, lambda: self.mensagem.config(text=''))
        elif not telemovel.isdigit():
            self.mensagem['text'] = 'Número de telemóvel são apenas números!'
            self.janela_utilizadores.after(1500, lambda: self.mensagem.config(text=''))
        elif not self.validar_email(email):
            self.mensagem['text'] = 'Email inválido. Deve estar no formato: nome@email.com'
            self.janela_utilizadores.after(1500, lambda: self.mensagem.config(text=''))
        else:
            try:
                dt = datetime.now()
                data_agora = dt.strftime('%Y-%m-%d %H:%M:%S')
                query_movimentos = 'INSERT INTO Movimentos VALUES (NULL, ?)'
                movimentos = f'Utilizador {nome_completo} Adicionado no dia: {data_agora}  Utilizador: {self.nome_user.title()}'
                self.db_consulta(query_movimentos, (movimentos,))
                self.db_consulta(query, parametros)
                self.mensagem['text'] = 'Conta criada com sucesso!'
                self.janela_utilizadores.after(1000, self.janela_utilizadores.destroy)
            except Exception as e:
                self.mensagem['text'] = f'Erro de Base de Dados:\n{e}'

        self.get_utilizadores()

    def apagar_utilizador(self):
        if not hasattr(self, 'mensagem_apagar'):
            self.mensagem_apagar['text'] = ''
        try:
            nome = self.tabela_utilizadores_gerir.item(self.tabela_utilizadores_gerir.selection())['values'][0]
            id = self.tabela_utilizadores_gerir.item(self.tabela_utilizadores_gerir.selection())['text']
        except IndexError:
            self.mensagem_apagar['text'] = 'Selecione um Utilizador'
            self.janela_inicio.after(1500, lambda: self.mensagem_apagar.config(text=''))
            return

        self.mensagem_apagar['text'] = ''

        try:
            query = 'DELETE FROM Utilizador WHERE ID = ?'
            dt = datetime.now()
            data_agora = dt.strftime('%Y-%m-%d %H:%M:%S')
            query_movimentos = 'INSERT INTO Movimentos VALUES (NULL, ?)'
            movimentos = f'Utilizador {nome} Eliminado no dia: {data_agora}  Utilizador: {self.nome_user.title()}'
            self.db_consulta(query_movimentos, (movimentos,))
            self.db_consulta(query, (id,))
        except Exception as e:
            self.mensagem['text'] = f'Erro de Base de Dados: {e}'

        self.mensagem_apagar['text'] = f'Utilizador {nome} apagado com sucesso.'

        self.tabela_utilizadores_gerir.delete(self.tabela_utilizadores_gerir.selection())

        # esta linha faz com que desapareca a mensagem de cliente apagado com sucesso depois de 3 segundos.
        self.janela_inicio.after(3000, lambda: self.mensagem_apagar.config(text=''))

        self.get_utilizadores()

    def editar_utilizador(self):

        if not hasattr(self, 'mensagem_editar'):
            self.mensagem_editar = Label(self.janela_inicio, text='', fg='red', font=('Arial', 15))
            self.mensagem_editar.place(x=850, y=20)

        try:
            self.tabela_utilizadores_gerir.item(self.tabela_utilizadores_gerir.selection())['values'][0]
        except IndexError:
            self.mensagem_editar['text'] = 'Selecione um Utilizador'
            self.janela_inicio.after(1500, lambda: self.mensagem_editar.config(text=''))
            return

        self.mensagem_editar['text'] = ''

        nome = self.tabela_utilizadores_gerir.item(self.tabela_utilizadores_gerir.selection())['values'][0]
        username = self.tabela_utilizadores_gerir.item(self.tabela_utilizadores_gerir.selection())['values'][1]
        password = self.tabela_utilizadores_gerir.item(self.tabela_utilizadores_gerir.selection())['values'][2]
        telemovel = self.tabela_utilizadores_gerir.item(self.tabela_utilizadores_gerir.selection())['values'][3]
        email = self.tabela_utilizadores_gerir.item(self.tabela_utilizadores_gerir.selection())['values'][4]
        admin = self.tabela_utilizadores_gerir.item(self.tabela_utilizadores_gerir.selection())['values'][5]

        if self.janela_utilizadores is None or not self.janela_utilizadores.winfo_exists():
            self.janela_utilizadores = Toplevel()
            self.janela_utilizadores.title = 'Editar Utilizador'
            self.janela_utilizadores.resizable(False, False)
            self.janela_utilizadores.wm_iconbitmap('recursos/luxury.ico')
            self.janela_utilizadores.geometry('580x450')

            self.mensagem = Label(self.janela_utilizadores, text='', fg='red')
            self.mensagem.place(x=150, y=20)

            frame_editar_clientes = LabelFrame(self.janela_utilizadores, text='Editar Utilizador',
                                               font=('Nerko One', 20, 'bold'))
            frame_editar_clientes.place(x=150, y=60)

            self.etiqueta_nome_antigo = Label(frame_editar_clientes, text='Nome Antigo: ', font=('Arial', 10))
            self.etiqueta_nome_antigo.grid(row=1, column=0)
            self.input_nome_antigo = Entry(frame_editar_clientes,
                                           textvariable=StringVar(self.janela_utilizadores, value=nome), state='readonly',
                                           font=('Arial', 10))
            self.input_nome_antigo.grid(row=1, column=1)

            self.etiqueta_nome_novo = Label(frame_editar_clientes, text='Nome Novo: ', font=('Arial', 10))
            self.etiqueta_nome_novo.grid(row=2, column=0)
            self.input_nome_novo = Entry(frame_editar_clientes, font=('Arial', 10))
            self.input_nome_novo.grid(row=2, column=1)

            self.etiqueta_username_antigo = Label(frame_editar_clientes, text='Nome de Utilizador Antigo: ',
                                                  font=('Arial', 10))
            self.etiqueta_username_antigo.grid(row=3, column=0)
            self.input_username_antigo = Entry(frame_editar_clientes,
                                               textvariable=StringVar(self.janela_utilizadores, value=username),
                                               state='readonly',
                                               font=('Arial', 10))
            self.input_username_antigo.grid(row=3, column=1)

            self.etiqueta_username_novo = Label(frame_editar_clientes, text='Nome de Utilizador Novo: ', font=('Arial', 10))
            self.etiqueta_username_novo.grid(row=4, column=0)
            self.input_username_novo = Entry(frame_editar_clientes, font=('Arial', 10))
            self.input_username_novo.grid(row=4, column=1)

            self.etiqueta_password_antiga = Label(frame_editar_clientes, text='Palavra-Passe Antiga: ', font=('Arial', 10))
            self.etiqueta_password_antiga.grid(row=5, column=0)
            self.input_password_antiga = Entry(frame_editar_clientes,
                                               textvariable=StringVar(self.janela_utilizadores, value=password),
                                               state='readonly', font=('Arial', 10))
            self.input_password_antiga.grid(row=5, column=1)

            self.etiqueta_password_nova = Label(frame_editar_clientes, text='Palavra-Passe Nova: ', font=('Arial', 10))
            self.etiqueta_password_nova.grid(row=6, column=0)
            self.input_password_nova = Entry(frame_editar_clientes, font=('Arial', 10), show='•')
            self.input_password_nova.grid(row=6, column=1)

            self.etiqueta_email_antigo = Label(frame_editar_clientes, text='Email Antigo: ', font=('Arial', 10))
            self.etiqueta_email_antigo.grid(row=7, column=0)
            self.input_email_antigo = Entry(frame_editar_clientes,
                                            textvariable=StringVar(self.janela_utilizadores, value=email), state='readonly',
                                            font=('Arial', 10))
            self.input_email_antigo.grid(row=7, column=1)

            self.etiqueta_email_novo = Label(frame_editar_clientes, text='Email Novo: ', font=('Arial', 10))
            self.etiqueta_email_novo.grid(row=8, column=0)
            self.input_email_novo = Entry(frame_editar_clientes, font=('Arial', 10))
            self.input_email_novo.grid(row=8, column=1)

            self.etiqueta_telemovel_antigo = Label(frame_editar_clientes, text='Telemóvel Antigo: ', font=('Arial', 10))
            self.etiqueta_telemovel_antigo.grid(row=9, column=0)
            self.input_telemovel_antigo = Entry(frame_editar_clientes,
                                                textvariable=StringVar(self.janela_utilizadores, value=telemovel),
                                                state='readonly', font=('Arial', 10))
            self.input_telemovel_antigo.grid(row=9, column=1)

            self.etiqueta_telemovel_novo = Label(frame_editar_clientes, text='Telemóvel Novo: ', font=('Arial', 10))
            self.etiqueta_telemovel_novo.grid(row=10, column=0)
            self.input_telemovel_novo = Entry(frame_editar_clientes, font=('Arial', 10))
            self.input_telemovel_novo.grid(row=10, column=1)

            self.etiqueta_admin_antigo = Label(frame_editar_clientes, text='Admin Antigo: ', font=('Arial', 10))
            self.etiqueta_admin_antigo.grid(row=11, column=0)
            self.input_admin_antigo = Entry(frame_editar_clientes,
                                            textvariable=StringVar(self.janela_utilizadores, value=admin),
                                            state='readonly', font=('Arial', 10))
            self.input_admin_antigo.grid(row=11, column=1)

            admin_p = StringVar()
            admin_p.set('Não')
            opcoes_admin = ['Sim', 'Não']

            self.etiqueta_admin_novo = Label(frame_editar_clientes, text='Admin Novo: ', font=('Arial', 10))
            self.etiqueta_admin_novo.grid(row=12, column=0)
            self.input_admin_novo = ttk.OptionMenu(frame_editar_clientes, admin_p, admin_p.get(), *opcoes_admin)
            self.input_admin_novo.grid(row=12, column=1)

            botao_atualizar = Button(frame_editar_clientes, text='ATUALIZAR UTILIZADOR',
                                     command=lambda: self.atualizar_utilizador(
                                         self.input_nome_novo.get(),
                                         self.input_nome_antigo.get(),
                                         self.input_username_novo.get(),
                                         self.input_username_antigo.get(),
                                         self.input_password_nova.get(),
                                         self.input_password_antiga.get(),
                                         self.input_email_novo.get(),
                                         self.input_email_antigo.get(),
                                         self.input_telemovel_novo.get(),
                                         self.input_telemovel_antigo.get(),
                                         admin_p.get(),
                                         self.input_admin_antigo.get()))
            botao_atualizar.grid(row=13, column=0, columnspan=2, sticky=W + E)
        else:
            self.janela_utilizadores.lift()

    def atualizar_utilizador(self, novo_nome, antigo_nome, novo_username, antigo_username, nova_passe, antiga_passe,
                             novo_email, antigo_email, novo_telemovel, antigo_telemovel, novo_admin, antigo_admin):
        utilizador_modificado = False
        parametros = []

        query = ('UPDATE Utilizador SET Nome = ?, Username = ?, Password = ?, Email = ?, Telemóvel = ?, Admin = ?'
                 'WHERE Nome = ? AND Username = ? AND Password = ? AND Email = ? AND Telemóvel = ? AND Admin = ?')

        def adicionar_parametro(novo_valor, valor_antigo):
            nonlocal utilizador_modificado
            if novo_valor and novo_valor != valor_antigo:
                parametros.append(novo_valor)
                utilizador_modificado = True
                return True
            parametros.append(valor_antigo)
            return False

        if novo_nome != '':
            if not novo_nome.replace(' ', '').isalpha():
                self.mensagem['text'] = 'O nome só pode conter letras!!'
                self.janela_utilizadores.after(1500, lambda: self.mensagem.config(text=''))
                return  # sai da função se houver erro

        if nova_passe != '':
            if self.input_password_nova.get() == antiga_passe:
                self.mensagem['text'] = 'A nova palavra-passe não pode ser a mesma da antiga.'
                self.janela_utilizadores.after(1500, lambda: self.mensagem.config(text=''))
                return

        if novo_telemovel != '':
            if not novo_telemovel.isdigit() and not self.validar_telemovel(novo_telemovel):
                self.mensagem['text'] = 'Número de telemóvel inválido. (Números portugueses têm 9 numeros!)'
                self.janela_utilizadores.after(1500, lambda: self.mensagem.config(text=''))
                return

        if novo_email != '':
            query_email = 'SELECT Email FROM Utilizador'
            registo_email = self.db_consulta(query_email)
            emails = [email[0] for email in registo_email]  # esta forma é uma 'list comprehension no python
        # vai buscar cada linha na base de dados e transforma numa tupla '(email,)' assim para cada iteração do loop
        # extrai um email por tupla e se estivel algum email em alguma tupla for igual ao que foi inserido exibe a msg
            for email in registo_email:
                emails.append(email)

            if not self.validar_email(novo_email):
                self.mensagem['text'] = 'Email inválido. Deve estar no formato: nome@email.com'
                self.janela_utilizadores.after(1500, lambda: self.mensagem.config(text=''))
                return

            if novo_email in emails:
                self.mensagem['text'] = 'Esse email já está associado a outra conta.'
                self.janela_utilizadores.after(1500, lambda: self.mensagem.config(text=''))
                return

        adicionar_parametro(novo_nome, antigo_nome)
        adicionar_parametro(novo_username, antigo_username)
        adicionar_parametro(nova_passe, antiga_passe)
        adicionar_parametro(novo_email, antigo_email)
        adicionar_parametro(novo_telemovel, antigo_telemovel)
        adicionar_parametro(novo_admin, antigo_admin)

        parametros.extend([antigo_nome, antigo_username, antiga_passe, antigo_email, antigo_telemovel, antigo_admin])

        if utilizador_modificado:
            try:
                dt = datetime.now()
                data_agora = dt.strftime('%Y-%m-%d %H:%M:%S')
                query_movimentos = 'INSERT INTO Movimentos VALUES (NULL, ?)'
                movimentos = f'Utilizador {antigo_nome} Modificado no dia: {data_agora}  Utilizador: {self.nome_user.title()}'
                self.db_consulta(query_movimentos, (movimentos,))
                self.db_consulta(query, parametros)
                self.mensagem['text'] = f'Utilizador {antigo_nome} modificado com sucesso!'
                self.janela_utilizadores.after(1000, self.janela_utilizadores.destroy)
            except sqlite3.OperationalError:
                self.mensagem['text'] = 'Erro de Base de Dados'

        else:
            self.mensagem['text'] = f'Utilizador NÃO foi modificado!'
            self.janela_utilizadores.after(1000, self.janela_utilizadores.destroy)

        self.get_utilizadores()

    def get_utilizadores(self):

        try:
            query = 'SELECT * FROM Utilizador'
            registos_db = self.db_consulta(query)

            for item in self.tabela_utilizadores_gerir.get_children():
                self.tabela_utilizadores_gerir.delete(item)

            for linha in registos_db:
                self.tabela_utilizadores_gerir.insert('', 'end', text=linha[0], values=(linha[1], linha[2],
                                                                                        linha[3], linha[4],
                                                                                        linha[5],
                                                                                        linha[6]))
        except sqlite3.OperationalError:
            self.mensagem['text'] = 'Erro de Base de Dados'
