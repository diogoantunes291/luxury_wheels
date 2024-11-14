from tkinter import ttk
from tkinter import *
import sqlite3
from datetime import datetime


class Gestao_Pagamentos:

    def __init__(self, janela_inicio, db_consulta, tabela_pagamentos, nome_utilizador):
        self.janela_inicio = janela_inicio
        self.db_consulta = db_consulta
        self.tabela_pagamentos = tabela_pagamentos
        self.nome_utilizador = nome_utilizador

        self.janela_pagamentos = None

        self.mensagem = Label(self.janela_inicio, text='', fg='red', font=('Arial', 15))
        self.mensagem.place(x=850, y=20)

    def adicionar_pagamento(self):

        if self.janela_pagamentos is None or not self.janela_pagamentos.winfo_exists():
            self.janela_pagamentos = Toplevel()
            self.janela_pagamentos.title('Pagamentos')
            self.janela_pagamentos.resizable(False, False)
            self.janela_pagamentos.wm_iconbitmap('recursos/luxury.ico')
            self.janela_pagamentos.geometry('500x200')

            frame_pagamentos = LabelFrame(self.janela_pagamentos, text='Pagamentos', font=('Nerko One', 20))
            frame_pagamentos.place(x=100, y=60)

            self.etiqueta_pagamento = Label(frame_pagamentos, text='Nova Forma de Pagamento:')
            self.etiqueta_pagamento.grid(row=1, column=0)

            self.input_pagamento = Entry(frame_pagamentos, font=('Arial', 10))
            self.input_pagamento.grid(row=1, column=1)

            botao_confirmar = ttk.Button(frame_pagamentos, text='CONFIRMAR', command=lambda: self.add_pagamento(
                self.input_pagamento.get()))
            botao_confirmar.grid(row=2, column=0, columnspan=2, sticky=W + E)
        else:
            self.janela_pagamentos.lift()

    def add_pagamento(self, pagamento):

        self.mensagem_janela = Label(self.janela_pagamentos, text='', fg='red')
        self.mensagem_janela.place(x=150, y=20)

        query_add = 'INSERT INTO Pagamentos VALUES (?)'

        query_repetido = 'SELECT [Formas Pagamento] FROM Pagamentos WHERE [Formas Pagamento] = ?'
        registo_repetido = self.db_consulta(query_repetido, (pagamento,)).fetchall()

        if not pagamento.replace(' ', '').isalpha():
            self.mensagem_janela['text'] = 'O Nome do método de pagamento só pode ter Letras.'
            self.janela_pagamentos.after(2000, lambda: self.mensagem_janela.config(text=''))
            return

        elif registo_repetido:
            self.mensagem_janela['text'] = 'Esse Método de Pagamento já existe!'
            self.janela_pagamentos.after(2000, lambda: self.mensagem_janela.config(text=''))
            return

        else:
            try:
                dt = datetime.now()
                data_agora = dt.strftime('%Y-%m-%d %H:%M:%S')
                query_movimentos = 'INSERT INTO Movimentos VALUES (NULL, ?)'
                movimentos = f'Pagamento {pagamento.title()} Adicionado no dia: {data_agora}  Utilizador: {self.nome_utilizador.title()}'
                self.db_consulta(query_movimentos, (movimentos,))
                self.db_consulta(query_add, (pagamento,))
                self.mensagem_janela['text'] = 'Pagamento adicionado com sucesso!'
                self.janela_pagamentos.after(1500, self.janela_pagamentos.destroy)
            except Exception as e:
                self.mensagem_janela['text'] = f'Erro de Base de Dados:\n{e}'

        self.get_pagamentos()

    def editar_pagamento(self):

        if not hasattr(self, 'mensagem'):
            self.mensagem = Label(self.janela_inicio, text='', fg='red', font=('Arial', 15))
            self.mensagem.place(x=850, y=20)

        selected_item = self.tabela_pagamentos.selection()
        if not selected_item:
            self.mensagem['text'] = 'Selecione um Pagamento'
            self.janela_inicio.after(1500, lambda: self.mensagem.config(text=''))
            return

        pagamento = self.tabela_pagamentos.item(self.tabela_pagamentos.selection())['text']

        if self.janela_pagamentos is None or not self.janela_pagamentos.winfo_exists():
            self.janela_pagamentos = Toplevel()
            self.janela_pagamentos.title('Pagamentos')
            self.janela_pagamentos.resizable(False, False)
            self.janela_pagamentos.wm_iconbitmap('recursos/luxury.ico')
            self.janela_pagamentos.geometry('500x200')

            self.mensagem = Label(self.janela_pagamentos, text='', fg='red')

            frame_pagamentos = LabelFrame(self.janela_pagamentos, text='Pagamentos', font=('Nerko One', 20))
            frame_pagamentos.place(x=100, y=60)

            self.etiqueta_pagamento_antigo = Label(frame_pagamentos, text='Antiga Forma de Pagamento:')
            self.etiqueta_pagamento_antigo.grid(row=1, column=0)
            self.input_pagamento_antigo = Entry(frame_pagamentos, textvariable=StringVar(self.janela_pagamentos,
                                                                                        value=pagamento),font=('Arial', 10))
            self.input_pagamento_antigo.grid(row=1, column=1)

            self.etiqueta_pagamento_novo = Label(frame_pagamentos, text='Nova Forma de Pagamento:')
            self.etiqueta_pagamento_novo.grid(row=2, column=0)
            self.input_pagamento_novo = Entry(frame_pagamentos, font=('Arial', 10))
            self.input_pagamento_novo.grid(row=2, column=1)

            botao_confirmar = ttk.Button(frame_pagamentos, text='CONFIRMAR', command=lambda: self.atualizar_pagamento(
                self.input_pagamento_antigo.get(),
                self.input_pagamento_novo.get()))
            botao_confirmar.grid(row=3, column=0, columnspan=2, sticky=W+E)
        else:
            self.janela_pagamentos.lift()

    def atualizar_pagamento(self, antigo_pagamento, novo_pagamento):

        self.mensagem_janela = Label(self.janela_pagamentos, text='', fg='red')
        self.mensagem_janela.place(x=150, y=20)

        pagamento_modificado = False

        parametros = []

        query = 'UPDATE Pagamentos SET [Formas Pagamento] = ? WHERE [Formas Pagamento] = ?'

        if novo_pagamento != antigo_pagamento:
            parametros = [novo_pagamento, antigo_pagamento]
            pagamento_modificado = True

        elif novo_pagamento == antigo_pagamento:
            self.mensagem_janela['text'] = 'A nova forma de pagamento não pode ser igual à antiga'
            self.janela_pagamentos.after(1500, lambda: self.mensagem_janela.config(text=''))
            return

        elif '' in novo_pagamento:
            parametros = [antigo_pagamento, antigo_pagamento]

        if pagamento_modificado:
            try:
                dt = datetime.now()
                data_agora = dt.strftime('%Y-%m-%d %H:%M:%S')
                query_movimentos = 'INSERT INTO Movimentos VALUES (NULL, ?)'
                movimentos = f'Pagamento {antigo_pagamento} Modificado no dia: {data_agora}  Utilizador: {self.nome_utilizador.title()}'
                self.db_consulta(query_movimentos, (movimentos,))
                self.db_consulta(query, parametros)
                self.mensagem_janela['text'] = f'Pagamento {antigo_pagamento}, modificado com sucesso!'
                self.janela_pagamentos.after(1500, self.janela_pagamentos.destroy)
            except sqlite3.OperationalError as e:
                self.mensagem_janela['text'] = f'Erro de Base de Dados: {e}'
        else:
            self.mensagem['text'] = f'Pagamento {antigo_pagamento} NÃO modificado!'
            self.janela_pagamentos.after(1500, lambda: self.janela_pagamentos.destroy)

        self.get_pagamentos()

    def apagar_pagamento(self):

        if not hasattr(self, 'mensagem'):
            self.mensagem = Label(self.janela_inicio, text='', fg='red', font=('Arial', 15))
            self.mensagem.place(x=850, y=20)

        selected_item = self.tabela_pagamentos.selection()
        if not selected_item:
            self.mensagem['text'] = 'Selecione um Pagamento'
            self.janela_inicio.after(1500, lambda: self.mensagem.config(text=''))
            return

        try:
            pagamento = self.tabela_pagamentos.item(selected_item)['text']
            dt = datetime.now()
            data_agora = dt.strftime('%Y-%m-%d %H:%M:%S')
            query_movimentos = 'INSERT INTO Movimentos VALUES (NULL, ?)'
            movimentos = f'Pagamento {pagamento.title()} Eliminado no dia: {data_agora}  Utilizador: {self.nome_utilizador.title()}'
            self.db_consulta(query_movimentos, (movimentos,))

            query = 'DELETE FROM Pagamentos WHERE [Formas Pagamento] = ?'
            self.db_consulta(query, (pagamento,))

            self.tabela_pagamentos.delete(selected_item)

            self.mensagem['text'] = f'Pagamento {pagamento.title()} apagado com sucesso!'
            self.janela_inicio.after(3000, lambda: self.mensagem.config(text=''))

            self.get_pagamentos()

        except sqlite3.OperationalError as e:
            self.mensagem['text'] = f'Erro de Base de Dados: {e}'

    def get_pagamentos(self):

        try:
            query = 'SELECT * FROM Pagamentos'
            registos_db = self.db_consulta(query)

            for item in self.tabela_pagamentos.get_children():
                self.tabela_pagamentos.delete(item)

            for linha in registos_db:
                self.tabela_pagamentos.insert('', 'end', text=linha[0])
        except Exception as e:
            self.mensagem['text'] = f'Erro de Base de Dados:\n{e}'
