import sqlite3
from tkinter import *
from tkinter import ttk
import re
import datetime
from datetime import *
from app import *


class Gestao_Reservas:

    def __init__(self, janela_inicio, db_consulta, tabela_reservas_gerir, nome_utilizador):
        self.janela_inicio = janela_inicio
        self.db_consulta = db_consulta
        self.tabela_reservas_gerir = tabela_reservas_gerir
        self.janela_reservas = None
        self.nome_utilizador = nome_utilizador

        self.user = ''

        self.escolha_modelo = None
        self.mensagem = Label(self.janela_inicio, text='', fg='red', font=('Arial', 15))
        self.mensagem.place(x=850, y=20)

        self.mensagem_apagar = Label(self.janela_inicio, text='', fg='red', font=('Arial', 15))
        self.mensagem_apagar.place(x=700, y=20)

    @staticmethod
    def validar_data(data):
        # Expressão regular para o formato YYYY-MM-DD
        padrao = r"^(19|20)\d{2}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$"

        if re.match(padrao, data):
            return True
        else:
            return False

    def criar_reserva(self):

        query_disponivel = 'UPDATE Veiculos SET Disponivel = "Não" WHERE Manutenção = "Sim"'
        self.db_consulta(query_disponivel)

        if self.janela_reservas is None or not self.janela_reservas.winfo_exists():
            self.janela_reservas = Toplevel()
            self.janela_reservas.title = 'Nova Reserva Luxury'
            self.janela_reservas.resizable(False, False)
            self.janela_reservas.wm_iconbitmap('recursos/luxury.ico')
            self.janela_reservas.geometry('500x350')

            frame_cr = LabelFrame(self.janela_reservas, text='Nova Reserva', font=('Nerko One', 20, 'bold'))
            frame_cr.place(x=100, y=60)

            query = 'SELECT * FROM Veiculos WHERE Disponivel = "Sim"'
            resultados_db = self.db_consulta(query)

            query_nome = 'SELECT Nome FROM Clientes'
            resultados_db_nome = self.db_consulta(query_nome)

            nomes = []
            marcas_modelos = {}

            # para obter as marcas e modelos sem ser repetidos crio um set
            # marcas_set = set()
            # modelos_set = set()

            # É criado um dicionário em cima agora defino que as marcas são as Keys e os Modelos são os Values
            for linha in resultados_db:
                marca = linha[1]
                modelo = linha[2]
                if marca not in marcas_modelos:  # Se a marca já existir não será adicionada evitando marcas repetidas
                    marcas_modelos[marca] = []  # Adiciona a Marca como KEY
                marcas_modelos[marca].append(modelo)  # Adiciona o Modelo como VALUE

            # for linha in resultados_db:
            #    marcas_set.add(linha[0])
            #    modelos_set.add(linha[1])

            # mas como um set é desordenado e sem INDEX todos os nomes apareciam no botão de escolha
            # então tenho de transformar novamente em lista e já fica ordenado e sem ser repetido!

            # marcas = list(marcas_set)
            # modelos = list(modelos_set)

            for linha_nomes in resultados_db_nome:
                nomes.append(linha_nomes[0])

            nomes_p = StringVar()
            nomes_p.set(nomes[0])

            marcas_p = StringVar()
            marcas = list(marcas_modelos.keys())
            marcas_p.set(marcas[0])

            modelos_p = StringVar()
            modelos_p.set(marcas_modelos[marcas_p.get()][0])

            self.etiqueta_nome = Label(frame_cr, text='Nome: ')
            self.etiqueta_nome.grid(row=2, column=0)
            self.input_nome = ttk.OptionMenu(frame_cr, nomes_p, nomes_p.get(), *nomes)
            self.input_nome.grid(row=2, column=1)

            self.etiqueta_marca = Label(frame_cr, text='Marca: ')
            self.etiqueta_marca.grid(row=3, column=0)
            self.input_marca = ttk.OptionMenu(frame_cr, marcas_p, marcas_p.get(), *marcas)
            self.input_marca.grid(row=3, column=1)

            self.etiqueta_modelo = Label(frame_cr, text='Modelo: ')
            self.etiqueta_modelo.grid(row=4, column=0)
            self.escolha_modelo = ttk.OptionMenu(frame_cr, modelos_p, modelos_p.get(), *marcas_modelos[marcas_p.get()])
            self.escolha_modelo.grid(row=4, column=1)

            def atualizar_modelos(*args):
                marca_selecionada = marcas_p.get()
                modelos = marcas_modelos[marca_selecionada]  # Obtem os modelos da marca escolhida
                modelos_p.set(modelos[0])  # Escreve o primeiro modelo da marca na barra de opções
                self.escolha_modelo['menu'].delete(0, 'end')  # Limpa a barra de escolha dos modelos a cada troca de marca
                for i in modelos:  # preenche novamente com os modelos
                    self.escolha_modelo['menu'].add_command(label=i, command=lambda value=i: modelos_p.set(value))
                    # ^ i= modelos da lista  ^=prencher com o modelo ^=mostra o primeiro modelo da lista

            marcas_p.trace('w', atualizar_modelos)

            self.etiqueta_data_inicio = Label(frame_cr, text='Data Inicio da Reserva: ')
            self.etiqueta_data_inicio.grid(row=5, column=0)
            self.input_data_inicio = Entry(frame_cr, font=('Arial', 10))
            self.input_data_inicio.grid(row=5, column=1)
            self.etiqueta_formato_inicio = Label(frame_cr, text='Formato Data --> YYYY-MM-DD', fg='grey')
            self.etiqueta_formato_inicio.grid(row=6, column=1)

            self.etiqueta_data_fim = Label(frame_cr, text='Data Fim da Reserva: ')
            self.etiqueta_data_fim.grid(row=7, column=0)
            self.input_data_fim = Entry(frame_cr, font=('Arial', 10))
            self.input_data_fim.grid(row=7, column=1)
            self.etiqueta_formato_fim = Label(frame_cr, text='Formato Data --> YYYY-MM-DD', fg='grey')
            self.etiqueta_formato_fim.grid(row=8, column=1)

            botao_confirmar = Button(frame_cr, text='CONFIRMAR', command=lambda: self.add_reserva(
                nomes_p.get(),
                marcas_p.get(),
                modelos_p.get(),
                self.input_data_inicio.get(),
                self.input_data_fim.get()))
            botao_confirmar.grid(row=9, column=0, columnspan=2, sticky=W + E)
        else:
            self.janela_reservas.lift()

    def add_reserva(self, nome, marca, modelo, data_inicio, data_fim):

        self.mensagem = Label(self.janela_reservas, text='', fg='red')
        self.mensagem.place(x=150, y=20)

        self.mensagem['text'] = ''

        reservas = []
        query_reservas = 'SELECT id_veiculo FROM Reservas'
        id_veiculos = self.db_consulta(query_reservas)
        for i in id_veiculos:
            reservas.append(i)

        query_preco = 'SELECT Preço FROM Veiculos WHERE Modelo = ?'
        parametros_preco = (modelo,)
        preco_resultado = self.db_consulta(query_preco, parametros_preco)

        for preco in preco_resultado:
            if preco:
                preco_dia = preco[0]
            else:
                self.mensagem['text'] = 'Modelo de veiculo não encontrado.'
                self.janela_reservas.after(1500, lambda: self.mensagem.config(text=''))
                return

        query_id_veiculo = """SELECT ID
                              FROM Veiculos
                              WHERE Marca = ? and Modelo = ?"""
        parametros_id = [marca, modelo]
        registo_id = self.db_consulta(query_id_veiculo, parametros_id)
        for i in registo_id:
            id_veiculo = i[0]

        query = ('INSERT INTO Reservas (Nome, Marca, Modelo, [Data Inicio], [Data Fim], [Preço Dia], id_veiculo) '
                 'VALUES (?, ?, ?, ?, ?, ?, ?)')
        parametros = (nome, marca, modelo, data_inicio, data_fim, preco_dia, id_veiculo)

        if '' in (nome, marca, modelo, data_inicio, data_fim):
            self.mensagem['text'] = 'TODOS OS CAMPOS DEVEM SER PREENCHIDOS!!!'

        elif not self.validar_data(data_inicio):
            self.mensagem['text'] = 'A data tem somente o formato de "YYYY-MM-DD"!!'

        elif not self.validar_data(data_fim):
            self.mensagem['text'] = 'A data tem somente o formato de "YYYY-MM-DD"!!'

        else:
            try:
                dt = datetime.now()
                data_agora = dt.strftime('%Y-%m-%d')

                if data_inicio > data_agora and data_fim > data_agora:
                    query_movimentos = 'INSERT INTO Movimentos VALUES (NULL, ?)'
                    movimentos = f'Reserva em nome de {nome} Adicionada no dia: {data_agora}  Utilizador: {self.nome_utilizador.title()}'
                    self.db_consulta(query_movimentos, (movimentos,))
                    self.db_consulta(query, parametros)

                    query_update_veiculo = 'UPDATE Veiculos SET Disponivel = "Não" WHERE ID = ?'
                    self.db_consulta(query_update_veiculo, (id_veiculo,))

                    self.mensagem['text'] = 'Reserva criada com sucesso!'
                    self.janela_reservas.after(1500, self.janela_reservas.destroy)

                else:
                    self.mensagem['text'] = 'Data Inválida'
                    self.janela_reservas.after(1500, lambda: self.mensagem.config(text=''))
            except sqlite3.OperationalError:
                self.mensagem['text'] = 'Erro de Base de Dados'

        self.get_reservas()

    def apagar_reserva(self):
        if not hasattr(self, 'mensagem_apagar'):
            self.mensagem_apagar = Label(self.janela_inicio, text='', fg='red', font=('Arial', 15))
            self.mensagem_apagar.place(x=850, y=20)

        try:
            id = self.tabela_reservas_gerir.item(self.tabela_reservas_gerir.selection())['text']
            nome = self.tabela_reservas_gerir.item(self.tabela_reservas_gerir.selection())['values'][0]
            marca = self.tabela_reservas_gerir.item(self.tabela_reservas_gerir.selection())['values'][1]
            modelo = self.tabela_reservas_gerir.item(self.tabela_reservas_gerir.selection())['values'][2]
        except IndexError:
            self.mensagem_apagar['text'] = 'Selecione uma Reserva'
            self.janela_inicio.after(1500, lambda: self.mensagem_apagar.config(text=''))
            return

        try:
            dt = datetime.now()
            data_agora = dt.strftime('%Y-%m-%d %H:%M:%S')
            query_movimentos = 'INSERT INTO Movimentos VALUES (NULL, ?)'
            movimentos = f'Reserva ID={id} em nome {nome} Eliminada no dia: {data_agora} Utilizador: {self.nome_utilizador.title()}'
            self.db_consulta(query_movimentos, (movimentos,))
            query = 'DELETE FROM Reservas WHERE ID = ?'
            self.db_consulta(query, (id,))

            self.tabela_reservas_gerir.delete(self.tabela_reservas_gerir.selection())

            self.mensagem_apagar[
                'text'] = f'Reserva em nome de {nome}\nCom o veiculo da marca {marca} e modelo {modelo}\nEliminada com sucesso!'
            self.janela_inicio.after(3000, lambda: self.mensagem_apagar.config(text=''))

            self.get_reservas()

        except sqlite3.OperationalError:
            self.mensagem['text'] = 'Erro de Base de Dados'

    def editar_reserva(self):

        if not hasattr(self, 'mensagem'):
            self.mensagem = Label(self.janela_inicio, text='', fg='red', font=('Arial', 15))
            self.mensagem.place(x=850, y=20)

        selected_item = self.tabela_reservas_gerir.selection()
        if not selected_item:
            self.mensagem['text'] = 'Selecione uma Reserva'
            self.janela_inicio.after(1500, lambda: self.mensagem.config(text=''))
            return

        # EXPERIMENTAR NOVA FUNÇÃO PARA REDUÇÃO DE CÓDIGO

        selecao = self.tabela_reservas_gerir.selection()

        item = self.tabela_reservas_gerir.item(selecao[0])

        id = item['text']
        nome = item['values'][0]
        veiculo = item['values'][1]
        data_inicio = item['values'][2]
        data_fim = item['values'][3]
        preco_dia = item['values'][5]

        if self.janela_reservas is None or not self.janela_reservas.winfo_exists():
            self.janela_reservas = Toplevel()
            self.janela_reservas.title = 'Editar Reserva'
            self.janela_reservas.resizable(False, False)
            self.janela_reservas.wm_iconbitmap('recursos/luxury.ico')
            self.janela_reservas.geometry('580x450')

            frame_editar_reservas = LabelFrame(self.janela_reservas, text='Editar Reserva',
                                               font=('Nerko One', 20, 'bold'))
            frame_editar_reservas.place(x=150, y=60)

            query = 'SELECT * FROM Veiculos WHERE Disponivel = "Sim"'
            resultados_db = self.db_consulta(query)

            query_nome = 'SELECT Nome FROM Clientes'
            resultados_db_nome = self.db_consulta(query_nome)

            nomes = []
            marcas_modelos = {}

            for linha in resultados_db:
                marca = linha[1]
                modelo = linha[2]
                if marca not in marcas_modelos:
                    marcas_modelos[marca] = []
                marcas_modelos[marca].append(modelo)

            for linha_nomes in resultados_db_nome:
                nomes.append(linha_nomes[0])

            nomes_p = StringVar()
            nomes_p.set(nome)

            marcas_p = StringVar()
            marcas = list(marcas_modelos.keys())
            marcas_p.set(marcas[0])

            modelos_p = StringVar()
            modelos_p.set(marcas_modelos[marcas_p.get()][0])

            self.etiqueta_id = Label(frame_editar_reservas, text='ID Reserva:')
            self.etiqueta_id.grid(row=2, column=0)
            self.input_id = Entry(frame_editar_reservas, textvariable=StringVar(self.janela_reservas, value=id),
                                  state='readonly', font=('Arial', 10))
            self.input_id.grid(row=2, column=1)

            self.etiqueta_antigo_nome = Label(frame_editar_reservas, text='Nome Antigo: ')
            self.etiqueta_antigo_nome.grid(row=3, column=0)
            self.input_antigo_nome = Entry(frame_editar_reservas, textvariable=StringVar(self.janela_reservas, value=nome),
                                           state='readonly', font=('Arial', 10))
            self.input_antigo_nome.grid(row=3, column=1)

            self.etiqueta_novo_nome = Label(frame_editar_reservas, text='Novo Nome: ')
            self.etiqueta_novo_nome.grid(row=4, column=0)
            self.input_novo_nome = ttk.OptionMenu(frame_editar_reservas, nomes_p, self.input_antigo_nome.get(), *nomes)
            self.input_novo_nome.grid(row=4, column=1)

            self.etiqueta_antiga_marca = Label(frame_editar_reservas, text='Veiculo Antigo: ')
            self.etiqueta_antiga_marca.grid(row=5, column=0)
            self.input_antiga_marca = Entry(frame_editar_reservas,
                                            textvariable=StringVar(self.janela_reservas, value=veiculo),
                                            state='readonly', font=('Arial', 10))
            self.input_antiga_marca.grid(row=5, column=1)

            self.etiqueta_nova_marca = Label(frame_editar_reservas, text='Novo Veiculo: ')
            self.etiqueta_nova_marca.grid(row=6, column=0)
            self.input_nova_marca = ttk.OptionMenu(frame_editar_reservas, marcas_p, marcas_p.get(), *marcas)
            self.input_nova_marca.grid(row=6, column=1)

            self.input_novo_modelo = ttk.OptionMenu(frame_editar_reservas, modelos_p, modelos_p.get(),
                                                    *marcas_modelos[marcas_p.get()])
            self.input_novo_modelo.grid(row=7, column=1)

            def atualizar_modelo(*args):
                marca_selecionada = marcas_p.get()
                modelos = marcas_modelos[marca_selecionada]
                modelos_p.set(modelos[0])
                self.input_novo_modelo['menu'].delete(0, 'end')
                for i in modelos:
                    self.input_novo_modelo['menu'].add_command(label=i, command=lambda value=i: modelos_p.set(value))

            marcas_p.trace('w', atualizar_modelo)

            self.etiqueta_antiga_data_inicio = Label(frame_editar_reservas, text='Data Inicio Anterior:')
            self.etiqueta_antiga_data_inicio.grid(row=11, column=0)
            self.input_antiga_data_inicio = Entry(frame_editar_reservas,
                                                  textvariable=StringVar(self.janela_reservas, value=data_inicio),
                                                  state='readonly', font=('Arial', 10))
            self.input_antiga_data_inicio.grid(row=11, column=1)

            self.etiqueta_nova_data_inicio = Label(frame_editar_reservas, text='Nova Data Inicio: ')
            self.etiqueta_nova_data_inicio.grid(row=12, column=0)
            self.input_nova_data_inicio = Entry(frame_editar_reservas, font=('Arial', 10))
            self.input_nova_data_inicio.grid(row=12, column=1)

            self.etiqueta_antiga_data_fim = Label(frame_editar_reservas, text='Data Fim Anterior:')
            self.etiqueta_antiga_data_fim.grid(row=13, column=0)
            self.input_antiga_data_fim = Entry(frame_editar_reservas,
                                               textvariable=StringVar(self.janela_reservas, value=data_fim),
                                               state='readonly', font=('Arial', 10))
            self.input_antiga_data_fim.grid(row=13, column=1)

            self.etiqueta_nova_data_fim = Label(frame_editar_reservas, text='Nova Data Fim: ')
            self.etiqueta_nova_data_fim.grid(row=14, column=0)
            self.input_nova_data_fim = Entry(frame_editar_reservas, font=('Arial', 10))
            self.input_nova_data_fim.grid(row=14, column=1)

            botao_atualizar = Button(frame_editar_reservas, text='CONFIRMAR', command=lambda: self.edit_reserva(
                nomes_p.get(),
                marcas_p.get(),
                modelos_p.get(),
                self.input_nova_data_inicio.get(),
                self.input_antiga_data_inicio.get(),
                self.input_nova_data_fim.get(),
                self.input_antiga_data_fim.get(),
                self.input_id.get()
            ))
            botao_atualizar.grid(row=15, column=0, columnspan=2, sticky=W + E)
        else:
            self.janela_reservas.lift()

    def edit_reserva(self, novo_nome, nova_marca, novo_modelo, nova_data_inicio, antiga_data_inicio, nova_data_fim,
                     antiga_data_fim, id):

        if not hasattr(self, 'mensagem_editar'):
            self.mensagem_editar = Label(self.janela_reservas, text='', fg='red', font=('Arial', 15))
            self.mensagem_editar.place(x=150, y=20)

        query_update_reserva = (
            'UPDATE Reservas SET Nome = ?, Marca = ?, Modelo = ?, [Data Inicio] = ?, [Data Fim] = ?, [Preço Dia] = ?, '
            'id_veiculo = ?'
            'WHERE ID = ?'
        )

        query_preco = 'SELECT Preço FROM Veiculos WHERE Modelo = ?'
        preco = self.db_consulta(query_preco, (novo_modelo,))

        query_id_veiculo = 'SELECT ID FROM Veiculos WHERE Marca = ? AND Modelo = ?'
        parametros_id_veiculo = [nova_marca, novo_modelo]
        consulta_id_veiculo = self.db_consulta(query_id_veiculo, parametros_id_veiculo)
        for i in consulta_id_veiculo:
            id_veiculo = i[0]

        resultado_preco = preco.fetchone()
        if resultado_preco:
            novo_preco = resultado_preco[0]

        data_inicio = nova_data_inicio if nova_data_inicio.strip() else antiga_data_inicio
        data_fim = nova_data_fim if nova_data_fim.strip() else antiga_data_fim

        if nova_data_inicio != '' and not self.validar_data(nova_data_inicio):
            self.mensagem_editar['text'] = 'Formato de data errada!'
            return

        if nova_data_fim != '' and not self.validar_data(nova_data_fim):
            self.mensagem_editar['text'] = 'Formato de data errada!'
            return

        parametros = [novo_nome, nova_marca, novo_modelo, data_inicio, data_fim, novo_preco, id_veiculo, id]

        if data_inicio > data_fim:
            self.mensagem_editar['text'] = 'Data inválida'
            self.janela_reservas.after(1500, lambda: self.mensagem_editar.config(text=''))
        else:
            try:
                dt = datetime.now()
                data_agora = dt.strftime('%Y-%m-%d %H:%M:%S')
                query_movimentos = 'INSERT INTO Movimentos VALUES (NULL, ?)'
                movimentos = f'Reserva ID={id} Modificada no dia: {data_agora}  Utilizador: {self.nome_utilizador.title()}'
                self.db_consulta(query_movimentos, (movimentos,))
                self.db_consulta(query_update_reserva, parametros)
                self.mensagem_editar['text'] = f'Reserva modificada com sucesso!'
                self.janela_reservas.after(1500, self.janela_reservas.destroy)

            except sqlite3.OperationalError:
                self.mensagem_editar['text'] = 'Erro de Base de Dados'

        self.get_reservas()

    def get_reservas(self):

        registos_tabela = self.tabela_reservas_gerir.get_children()

        for item in registos_tabela:
            self.tabela_reservas_gerir.delete(item)

        try:
            query_get = 'SELECT * FROM Reservas ORDER BY ID DESC'
            resultados_get = self.db_consulta(query_get)

            for linha in resultados_get:
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
        except sqlite3.OperationalError:
            self.mensagem['text'] = 'Erro de Base de Dados'
