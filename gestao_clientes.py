import re
from tkinter import *
from datetime import *
import sqlite3


class Gestao_Clientes:
    def __init__(self, janela_inicio, db_consulta, tabela_clientes_gerir, nome_utilizador):
        self.janela_inicio = janela_inicio
        self.db_consulta = db_consulta
        self.tabela_clientes_gerir = tabela_clientes_gerir
        self.janela_clientes = None
        self.nome_utilizador = nome_utilizador

        self.mensagem_editar = Label(self.janela_inicio, text='', fg='red', font=('Arial', 20))
        self.mensagem_editar.place(x=850, y=20)

        self.mensagem = Label(self.janela_clientes, text='', fg='red')
        self.mensagem.place(x=150, y=20)

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

    def apagar_cliente(self):
        if not hasattr(self, 'mensagem_apagar'):
            self.mensagem_apagar = Label(self.janela_inicio, text='', fg='red', font=('Arial', 20))
            self.mensagem_apagar.place(x=850, y=20)
        try:
            nome = self.tabela_clientes_gerir.item(self.tabela_clientes_gerir.selection())['values'][0]
            id = self.tabela_clientes_gerir.item(self.tabela_clientes_gerir.selection())['text']
        except IndexError:
            self.mensagem_apagar['text'] = 'Selecione um Cliente'
            self.janela_inicio.after(1500, lambda: self.mensagem_apagar.config(text=''))
            return

        self.mensagem_apagar['text'] = ''

        try:
            dt = datetime.now()
            data_agora = dt.strftime('%Y-%m-%d %H:%M:%S')
            query_movimentos = 'INSERT INTO Movimentos VALUES (NULL, ?)'
            movimentos = f'Cliente {nome.title()} Eliminado no dia: {data_agora}  Utilizador: {self.nome_utilizador.title()}'
            self.db_consulta(query_movimentos, (movimentos,))

            query = 'DELETE FROM Clientes WHERE ID = ?'
            self.db_consulta(query, (id,))

            self.mensagem_apagar['text'] = f'Cliente {nome.title()} apagado com sucesso.'

            self.tabela_clientes_gerir.delete(self.tabela_clientes_gerir.selection())

            # esta linha faz com que desapareca a mensagem de cliente apagado com sucesso depois de 3 segundos.
            self.janela_inicio.after(3000, lambda: self.mensagem_apagar.config(text=''))

            self.get_clientes()

        except sqlite3.OperationalError:
            self.mensagem['text'] = 'Erro de Base de Dados'

    def criar_cliente(self):

        if self.janela_clientes is None or not self.janela_clientes.winfo_exists():
            self.janela_clientes = Toplevel()
            self.janela_clientes.title = 'Novo Cliente Luxury'
            self.janela_clientes.resizable(False, False)
            self.janela_clientes.wm_iconbitmap('recursos/luxury.ico')
            self.janela_clientes.geometry('480x300')

            frame_criar_clientes = LabelFrame(self.janela_clientes, text='Novo Cliente', font=('Nerko One', 20, 'bold'))
            frame_criar_clientes.place(x=100, y=60)

            self.etiqueta_nome = Label(frame_criar_clientes, text='Nome Completo: ')
            self.etiqueta_nome.grid(row=2, column=0)
            self.input_nome = Entry(frame_criar_clientes, font=('Arial', 10))
            self.input_nome.grid(row=2, column=1)

            self.etiqueta_password = Label(frame_criar_clientes, text='Palavra-Passe: ')
            self.etiqueta_password.grid(row=3, column=0)
            self.input_password = Entry(frame_criar_clientes, font=('Arial', 10), show='•')
            self.input_password.grid(row=3, column=1)

            self.etiqueta_confirmar = Label(frame_criar_clientes, text='Confirmar Palavra-Passe: ')
            self.etiqueta_confirmar.grid(row=4, column=0)
            self.input_confirmar = Entry(frame_criar_clientes, font=('Arial', 10), show='•')
            self.input_confirmar.grid(row=4, column=1)

            self.etiqueta_email = Label(frame_criar_clientes, text='Email: ')
            self.etiqueta_email.grid(row=5, column=0)
            self.input_email = Entry(frame_criar_clientes, font=('Arial', 10))
            self.input_email.grid(row=5, column=1)

            self.etiqueta_telemovel = Label(frame_criar_clientes, text='Telemóvel: ')
            self.etiqueta_telemovel.grid(row=6, column=0)
            self.input_telemovel = Entry(frame_criar_clientes, font=('Arial', 10))
            self.input_telemovel.grid(row=6, column=1)

            self.mensagem_criar_conta = Label(self.janela_clientes, text='', fg='red')
            self.mensagem_criar_conta.place(x=100, y=270)

            botao_confirmar = Button(frame_criar_clientes, text='CONFIRMAR', command=lambda: self.add_cliente(
                self.input_nome.get(),
                self.input_password.get(),
                self.input_email.get(),
                self.input_telemovel.get()))
            botao_confirmar.grid(row=8, column=0, columnspan=3, sticky=W + E)

            frame_criar_clientes.columnconfigure(0, weight=1)
            frame_criar_clientes.columnconfigure(1, weight=1)
        else:
            self.janela_clientes.lift()

    def add_cliente(self, nome, password, email, telemovel):
        self.mensagem_criar_conta['text'] = ''

        if '' in (nome, password, email, telemovel):
            self.mensagem_criar_conta['text'] = 'TODOS OS CAMPOS TÊM DE SER PREENCHIDOS!!!'
            return

        if not nome.replace(' ', '').isalpha():
            self.mensagem_criar_conta['text'] = 'O Nome não pode conter números!!'
            return

        if self.input_password.get() != self.input_confirmar.get():
            self.mensagem_criar_conta['text'] = 'As palavras palavras pass têm de ser iguais!'
            return

        if not self.validar_telemovel(telemovel):
            self.mensagem_criar_conta['text'] = 'Número de telemóvel inválido. (Números portugueses têm 9 numeros!)'
            return

        if not telemovel.isdigit():
            self.mensagem_criar_conta['text'] = 'Número de telemóvel são apenas números!'
            return

        if not self.validar_email(email):
            self.mensagem_criar_conta['text'] = 'Email inválido. Deve estar no formato: nome@email.com'
            return

        query_email = 'SELECT Email FROM Clientes WHERE Email = ?'
        registo_email = self.db_consulta(query_email, (email,)).fetchone()
        if registo_email:
            self.mensagem_criar_conta['text'] = 'Esse email já está associado a outra conta.'
            self.janela_clientes.after(1500, lambda: self.mensagem_criar_conta.config(text=''))
            return

        query = 'INSERT INTO Clientes VALUES (NULL, ?, ?, ?, ?, DATE("now"))'
        parametros = (nome, password, email, telemovel)

        dt = datetime.now()
        data_agora = dt.strftime('%Y-%m-%d %H:%M:%S')
        query_movimentos = 'INSERT INTO Movimentos VALUES (NULL, ?)'
        movimentos = f'Cliente {nome.title()} Adicionado no dia: {data_agora}  Utilizador: {self.nome_utilizador.title()}'

        try:
            self.db_consulta(query_movimentos, (movimentos,))
            self.db_consulta(query, parametros)
            self.mensagem_criar_conta['text'] = 'Cliente adicionado com sucesso!'
            self.janela_clientes.after(1500, self.janela_clientes.destroy)
        except sqlite3.OperationalError:
            self.mensagem['text'] = 'Erro de Base de Dados'

        self.get_clientes()

    def editar_cliente(self):

        try:
            self.tabela_clientes_gerir.item(self.tabela_clientes_gerir.selection())['values'][0]
        except IndexError:
            self.mensagem_editar['text'] = 'Selecione um cliente'
            self.janela_inicio.after(3000, lambda: self.mensagem_editar.config(text=''))
            return

        self.mensagem_editar['text'] = ''

        nome = self.tabela_clientes_gerir.item(self.tabela_clientes_gerir.selection())['values'][0]
        password = self.tabela_clientes_gerir.item(self.tabela_clientes_gerir.selection())['values'][1]
        email = self.tabela_clientes_gerir.item(self.tabela_clientes_gerir.selection())['values'][2]
        telemovel = self.tabela_clientes_gerir.item(self.tabela_clientes_gerir.selection())['values'][3]

        if self.janela_clientes is None or not self.janela_clientes.winfo_exists():
            self.janela_clientes = Toplevel()
            self.janela_clientes.title = 'Editar Cliente'
            self.janela_clientes.resizable(False, False)
            self.janela_clientes.wm_iconbitmap('recursos/luxury.ico')
            self.janela_clientes.geometry('580x450')

            self.mensagem = Label(self.janela_clientes, text='', fg='red')
            self.mensagem.place(x=150, y=20)

            frame_editar_clientes = LabelFrame(self.janela_clientes, text='Editar Cliente', font=('Nerko One', 20, 'bold'))
            frame_editar_clientes.place(x=150, y=60)

            self.etiqueta_nome_antigo = Label(frame_editar_clientes, text='Nome Antigo: ', font=('Arial', 10))
            self.etiqueta_nome_antigo.grid(row=1, column=0)
            self.input_nome_antigo = Entry(frame_editar_clientes, textvariable=StringVar(self.janela_clientes, value=nome), state='readonly', font=('Arial', 10))
            self.input_nome_antigo.grid(row=1, column=1)

            self.etiqueta_nome_novo = Label(frame_editar_clientes, text='Nome Novo: ', font=('Arial', 10))
            self.etiqueta_nome_novo.grid(row=2, column=0)
            self.input_nome_novo = Entry(frame_editar_clientes, font=('Arial', 10))
            self.input_nome_novo.grid(row=2, column=1)

            self.etiqueta_password_antiga = Label(frame_editar_clientes, text='Palavra-Passe Antiga: ', font=('Arial', 10))
            self.etiqueta_password_antiga.grid(row=3, column=0)
            self.input_password_antiga = Entry(frame_editar_clientes, textvariable=StringVar(self.janela_clientes, value=password), state='readonly', font=('Arial', 10))
            self.input_password_antiga.grid(row=3, column=1)

            self.etiqueta_password_nova = Label(frame_editar_clientes, text='Palavra-Passe Nova: ', font=('Arial', 10))
            self.etiqueta_password_nova.grid(row=4, column=0)
            self.input_password_nova = Entry(frame_editar_clientes, font=('Arial', 10))
            self.input_password_nova.grid(row=4, column=1)

            self.etiqueta_email_antigo = Label(frame_editar_clientes, text='Email Antigo: ', font=('Arial', 10))
            self.etiqueta_email_antigo.grid(row=5, column=0)
            self.input_email_antigo = Entry(frame_editar_clientes, textvariable=StringVar(self.janela_clientes, value=email), state='readonly', font=('Arial', 10))
            self.input_email_antigo.grid(row=5, column=1)

            self.etiqueta_email_novo = Label(frame_editar_clientes, text='Email Novo: ', font=('Arial', 10))
            self.etiqueta_email_novo.grid(row=6, column=0)
            self.input_email_novo = Entry(frame_editar_clientes, font=('Arial', 10))
            self.input_email_novo.grid(row=6, column=1)

            self.etiqueta_telemovel_antigo = Label(frame_editar_clientes, text='Telemóvel Antigo: ', font=('Arial', 10))
            self.etiqueta_telemovel_antigo.grid(row=7, column=0)
            self.input_telemovel_antigo = Entry(frame_editar_clientes, textvariable=StringVar(self.janela_clientes, value=telemovel), state='readonly', font=('Arial', 10))
            self.input_telemovel_antigo.grid(row=7, column=1)

            self.etiqueta_telemovel_novo = Label(frame_editar_clientes, text='Telemóvel Novo: ', font=('Arial', 10))
            self.etiqueta_telemovel_novo.grid(row=8, column=0)
            self.input_telemovel_novo = Entry(frame_editar_clientes, font=('Arial', 10))
            self.input_telemovel_novo.grid(row=8, column=1)

            botao_atualizar = Button(frame_editar_clientes, text='ATUALIZAR CLIENTE', command=lambda: self.atualizar_cliente(
                self.input_nome_novo.get().title(),
                self.input_nome_antigo.get().title(),
                self.input_password_nova.get(),
                self.input_password_antiga.get(),
                self.input_email_novo.get(),
                self.input_email_antigo.get(),
                self.input_telemovel_novo.get(),
                self.input_telemovel_antigo.get()))
            botao_atualizar.grid(row=9, column=0, columnspan=2, sticky=W+E)
        else:
            self.janela_clientes.lift()

    def atualizar_cliente(self, novo_nome, antigo_nome, nova_passe, antiga_passe, novo_email, antigo_email,
                          novo_telemovel, antigo_telemovel):

        cliente_modificado = False
        parametros = []

        query = ('UPDATE Clientes SET Nome = ?, Password = ?, Email = ?, Telemóvel = ?'
                 'WHERE Nome = ? AND Password = ? AND Email = ? AND Telemóvel = ?')

        def adicionar_parametro(novo_valor, valor_antigo):
            nonlocal cliente_modificado
            if novo_valor and novo_valor != valor_antigo:
                parametros.append(novo_valor)
                cliente_modificado = True
                return True
            parametros.append(valor_antigo)
            return False

        if novo_nome != '':
            if not novo_nome.replace(' ', '').isalpha():
                self.mensagem['text'] = 'O nome só pode conter letras!!'
                self.janela_clientes.after(3000, lambda: self.mensagem.config(text=''))
                return

        if nova_passe != '':
            if self.input_password_nova.get() == antiga_passe:
                self.mensagem['text'] = 'A nova palavra-passe não pode ser a mesma da antiga.'
                self.janela_clientes.after(3000, lambda: self.mensagem.config(text=''))
                return

        if novo_telemovel != '':
            if not novo_telemovel.isdigit() and not self.validar_telemovel(novo_telemovel):
                self.mensagem['text'] = 'Número de telemóvel inválido. (Números portugueses têm 9 numeros!)'
                self.janela_clientes.after(3000, lambda: self.mensagem.config(text=''))
                return

        if novo_email != '':
            query_email = 'SELECT Email FROM Clientes WHERE Email = ?'
            registo_email = self.db_consulta(query_email, (novo_email,)).fetchone()
            if registo_email:
                self.mensagem_criar_conta['text'] = 'Esse email já está associado a outra conta.'
                self.janela_clientes.after(3000, lambda: self.mensagem_criar_conta.config(text=''))
                return

            if not self.validar_email(novo_email):
                self.mensagem['text'] = 'Email inválido. Deve estar no formato: nome@email.com'
                self.janela_clientes.after(3000, lambda: self.mensagem.config(text=''))
                return


        adicionar_parametro(novo_nome, antigo_nome)
        adicionar_parametro(nova_passe, antiga_passe)
        adicionar_parametro(novo_email, antigo_email)
        adicionar_parametro(novo_telemovel, antigo_telemovel)

        parametros.extend([antigo_nome, antiga_passe, antigo_email, antigo_telemovel])

        if cliente_modificado:
            try:
                dt = datetime.now()
                data_agora = dt.strftime('%Y-%m-%d %H:%M:%S')
                query_movimentos = 'INSERT INTO Movimentos VALUES (NULL, ?)'
                movimentos = f'Cliente {antigo_nome.title()} Modificado no dia: {data_agora}  Utilizador: {self.nome_utilizador.title()}'
                self.db_consulta(query_movimentos, (movimentos,))
                self.db_consulta(query, parametros)
                self.mensagem['text'] = f'Cliente {antigo_nome.title()} modificado com sucesso!'
                self.janela_clientes.after(1000, self.janela_clientes.destroy)

            except sqlite3.OperationalError:
                self.mensagem['text'] = 'Erro de Base de Dados'

        else:
            self.mensagem['text'] = f'Cliente NÃO foi modificado!'
            self.janela_clientes.after(1000, self.janela_clientes.destroy)

        self.get_clientes()

    def get_clientes(self):

        try:
            query = 'SELECT * FROM Clientes'
            registos_db = self.db_consulta(query)

            for item in self.tabela_clientes_gerir.get_children():
                self.tabela_clientes_gerir.delete(item)

            for linha in registos_db:
                self.tabela_clientes_gerir.insert('', 'end', text=linha[0],
                                                  values=(linha[1], linha[2], linha[3], linha[4],
                                                          linha[5]))
        except sqlite3.OperationalError:
            self.mensagem['text'] = 'Erro de Base de Dados'
