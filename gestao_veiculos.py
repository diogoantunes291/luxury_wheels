from tkinter import *
from tkinter import ttk
from datetime import datetime
import re
import sqlite3


class Gestao_Veiculos:
    def __init__(self, janela_inicio, db_consulta, tabela_veiculos_gerir, nome_utilizador):
        self.janela_inicio = janela_inicio
        self.db_consulta = db_consulta
        self.tabela_veiculos_gerir = tabela_veiculos_gerir
        self.janela_veiculos = None
        self.nome_utilizador = nome_utilizador
        self.mensagem = Label(self.janela_inicio, text='', fg='red')
        self.mensagem_editar = Label(self.janela_inicio, text='', fg='red', font=('Arial', 15))

    @staticmethod
    def validar_data(data):
        # Expressão regular para o formato DD-MM-YYYY
        padrao = r"^(0[1-9]|[12][0-9]|3[01])-(0[1-9]|1[0-2])-(\d{4})$"

        if re.match(padrao, data):
            return True
        else:
            return False

    @staticmethod
    def validar_matricula(matricula):
        # Expressão regular para verificar o modelo ANTIGO e NOVO das matrículas portuguêsas
        padrao = r"^([A-Z]{2}-\d{2}-\d{2}|\d{2}-[A-Z]{2}-\d{2}|\d{2}-\d{2}-[A-Z]{2}|[A-Z]{2}-\d{2}-[A-Z]{2})$"

        if re.match(padrao, matricula):
            return True
        else:
            return False

    @staticmethod
    def validar_pessoas(pessoas):

        padrao = r"^[1-9]$"

        if re.match(padrao, pessoas):
            return True
        else:
            return False

    def apagar_veiculo(self):
        if not hasattr(self, 'mensagem_apagar'):
            self.mensagem_apagar = Label(self.janela_inicio, text='', fg='red', font=('Arial', 15))
            self.mensagem_apagar.place(x=850, y=20)

        try:
            marca = self.tabela_veiculos_gerir.item(self.tabela_veiculos_gerir.selection())['values'][0]
            modelo = self.tabela_veiculos_gerir.item(self.tabela_veiculos_gerir.selection())['values'][1]
            id = self.tabela_veiculos_gerir.item(self.tabela_veiculos_gerir.selection())['text']
        except IndexError:
            self.mensagem_apagar['text'] = 'Selecione um Veiculo'
            self.janela_inicio.after(1500, lambda: self.mensagem_apagar.config(text=''))
            return

        self.mensagem_apagar['text'] = ''

        query_reservado = """SELECT ID
                             FROM Veiculos
                             WHERE ID IN 
                             (SELECT id_veiculo
                             FROM Reservas
                             WHERE id_veiculo = ?)"""
        parametro = [id]
        resultado_reservado = self.db_consulta(query_reservado, parametro)
        veiculos_reservados = resultado_reservado.fetchall()

        if not veiculos_reservados:
            try:
                query = 'DELETE FROM Veiculos WHERE ID = ?'
                self.db_consulta(query, (id,))

                dt = datetime.now()
                data_agora = dt.strftime('%Y-%m-%d %H:%M:%S')
                query_movimentos = 'INSERT INTO Movimentos VALUES (NULL, ?)'
                movimentos = f'Veiculo {marca} {modelo} Eliminado no dia: {data_agora}  Utilizador: {self.nome_utilizador.title()}'
                self.db_consulta(query_movimentos, (movimentos,))

                self.tabela_veiculos_gerir.delete(self.tabela_veiculos_gerir.selection())

                self.mensagem_apagar['text'] = f'Veiculo da marca {marca} e modelo {modelo} apagado com sucesso.'

                # esta linha faz com que desapareça depois de 3 segundos a mensagem de cliente apagado com sucesso.
                self.janela_inicio.after(3000, lambda: self.mensagem_apagar.config(text=''))
            except sqlite3.OperationalError as e:
                print(f'Erro de Base de Dados: {e}')
                self.mensagem_apagar['text'] = f'Erro ao apagar veículo: {e}'
        else:
            print(f'O Veiculo de ID={id} está reservado\nNão pode ser apagado durante a reserva')
            self.mensagem_apagar[
                'text'] = f'O Veiculo de ID={id} está reservado\nNão pode ser apagado durante a reserva.'
            self.janela_inicio.after(3000, lambda: self.mensagem_apagar.config(text=''))

        self.get_veiculos()

    def adicionar_veiculo(self):

        if self.janela_veiculos is None or not self.janela_veiculos.winfo_exists():
            self.janela_veiculos = Toplevel()
            self.janela_veiculos.title = 'Novo Cliente Luxury'
            self.janela_veiculos.resizable(False, False)
            self.janela_veiculos.wm_iconbitmap('recursos/luxury.ico')
            self.janela_veiculos.geometry('515x500')

            frame_adicionar_veiculos = LabelFrame(self.janela_veiculos, text='Novo Veiculos',
                                                  font=('Nerko One', 20, 'bold'))
            frame_adicionar_veiculos.place(x=100, y=60)

            self.etiqueta_marca = Label(frame_adicionar_veiculos, text='Marca: ')
            self.etiqueta_marca.grid(row=2, column=0)
            self.input_marca = Entry(frame_adicionar_veiculos, font=('Arial', 10))
            self.input_marca.grid(row=2, column=1)

            self.etiqueta_modelo = Label(frame_adicionar_veiculos, text='Modelo: ')
            self.etiqueta_modelo.grid(row=3, column=0)
            self.input_modelo = Entry(frame_adicionar_veiculos, font=('Arial', 10))
            self.input_modelo.grid(row=3, column=1)

            menu_c = StringVar()
            menu_c.set('Categorias:')
            menu_categoria = ['CARRO', 'MOTO']

            self.etiqueta_categoria = Label(frame_adicionar_veiculos, text='Categoria: ')
            self.etiqueta_categoria.grid(row=4, column=0)
            self.input_categoria = ttk.OptionMenu(frame_adicionar_veiculos, menu_c, menu_c.get(), *menu_categoria)
            self.input_categoria.grid(row=4, column=1)

            menu_t = StringVar()
            menu_t.set('Tipos:')
            menu_tipo = ['Luxo', 'Citadino', 'Familiar', 'SUV', 'Clássico', 'Conforto', 'Desportivo']

            self.etiqueta_tipo = Label(frame_adicionar_veiculos, text='Tipo de Veiculo: ')
            self.etiqueta_tipo.grid(row=5, column=0)
            self.input_tipo = ttk.OptionMenu(frame_adicionar_veiculos, menu_t, menu_t.get(), *menu_tipo)
            self.input_tipo.grid(row=5, column=1)

            self.etiqueta_pessoas = Label(frame_adicionar_veiculos, text='Número de Pessoas: ')
            self.etiqueta_pessoas.grid(row=6, column=0)
            self.input_pessoas = Entry(frame_adicionar_veiculos, font=('Arial', 10))
            self.input_pessoas.grid(row=6, column=1)

            self.etiqueta_preco = Label(frame_adicionar_veiculos, text='Preço Dia: ')
            self.etiqueta_preco.grid(row=7, column=0)
            self.input_preco = Entry(frame_adicionar_veiculos, font=('Arial', 10))
            self.input_preco.grid(row=7, column=1)

            self.etiqueta_revisao = Label(frame_adicionar_veiculos, text='Última Revisão: ')
            self.etiqueta_revisao.grid(row=8, column=0)
            self.input_revisao = Entry(frame_adicionar_veiculos, font=('Arial', 10))
            self.input_revisao.grid(row=8, column=1)
            self.etiqueta_exemplo = Label(frame_adicionar_veiculos, text='Formato data -> DD-MM-YYYY', fg='grey')
            self.etiqueta_exemplo.grid(row=9, column=1)

            self.etiqueta_legalizacao = Label(frame_adicionar_veiculos, text='Última Legalização: ')
            self.etiqueta_legalizacao.grid(row=10, column=0)
            self.input_legalizacao = Entry(frame_adicionar_veiculos, font=('Arial', 10))
            self.input_legalizacao.grid(row=10, column=1)
            self.etiqueta_exemplo_2 = Label(frame_adicionar_veiculos, text='Formato data -> DD-MM-YYYY', fg='grey')
            self.etiqueta_exemplo_2.grid(row=11, column=1)

            self.etiqueta_matricula = Label(frame_adicionar_veiculos, text='Matrícula: ')
            self.etiqueta_matricula.grid(row=12, column=0)
            self.input_matricula = Entry(frame_adicionar_veiculos, font=('Arial', 10))
            self.input_matricula.grid(row=12, column=1)
            self.etiqueta_exemplo_3 = Label(frame_adicionar_veiculos, text='Formato Matricula -> XX-XX-XX', fg='grey')
            self.etiqueta_exemplo_3.grid(row=13, column=1)

            self.etiqueta_imagem = Label(frame_adicionar_veiculos, text='Local Imagem:')
            self.etiqueta_imagem.grid(row=14, column=0)
            self.input_imagem = Entry(frame_adicionar_veiculos, font=('Arial', 10))
            self.input_imagem.grid(row=14, column=1)

            self.caminho_imagem = Label(frame_adicionar_veiculos, text='exemplo: recursos/golf.jpg', fg='grey')
            self.caminho_imagem.grid(row=15, column=1)

            self.mensagem_adicionar = Label(self.janela_veiculos, text='', fg='red')
            self.mensagem_adicionar.place(x=120, y=20)

            botao_confirmar = Button(frame_adicionar_veiculos, text='CONFIRMAR', command=lambda: self.add_veiculo(
                self.input_marca.get(),
                self.input_modelo.get(),
                menu_c.get(),
                menu_t.get(),
                self.input_pessoas.get(),
                self.input_imagem.get(),
                self.input_preco.get(),
                self.input_revisao.get(),
                self.input_legalizacao.get(),
                self.input_matricula.get()))
            botao_confirmar.grid(row=16, column=0, columnspan=2, sticky=W + E)

            frame_adicionar_veiculos.columnconfigure(0, weight=1)
            frame_adicionar_veiculos.columnconfigure(1, weight=1)
        else:
            self.janela_veiculos.lift()

    def add_veiculo(self, marca, modelo, categoria, tipo, pessoas, imagem, preco, revisao, legalizacao, matricula):

        self.mensagem_adicionar['text'] = ''

        query = ('INSERT INTO Veiculos (Marca, Modelo, Categoria, [Tipo de Veiculo], [Qt Pessoas],'
                 'Imagem, Preço, [Ultima Revisao], [Ultima Legalizacao], Manutenção, Disponivel, Matricula) '
                 'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, "Não", "Sim", ?)')
        parametros = (marca, modelo, categoria, tipo, pessoas, imagem, preco, revisao, legalizacao, matricula)

        query_matricula = 'SELECT Matricula FROM Veiculos WHERE Matricula = ?'
        resultado_matricula = self.db_consulta(query_matricula, (matricula,)).fetchone()

        if '' in (marca, modelo, categoria, tipo, pessoas, imagem, preco, revisao, legalizacao):
            self.mensagem_adicionar['text'] = 'TODOS OS CAMPOS DEVEM SER PREENCHIDOS!!!'
        elif not marca.capitalize().isalpha():
            self.mensagem_adicionar['text'] = 'A Marca não pode conter números!!'
        elif not self.validar_pessoas(pessoas):
            self.mensagem_adicionar['text'] = 'O número de pessoas SÓ pode ser UM DÍGITO!'
        elif not preco.isdigit():
            self.mensagem_adicionar['text'] = 'O preço é composto por NUMEROS.'
        elif not self.validar_data(revisao):
            self.mensagem_adicionar['text'] = 'A data tem somente o formato de "DD-MM-YYYY"!!'
        elif not self.validar_data(legalizacao):
            self.mensagem_adicionar['text'] = 'A data tem somente o formato de "DD-MM-YYYY"!!'
        elif not self.validar_matricula(matricula):
            self.mensagem_adicionar['text'] = 'A matrícula tem somente o formato de "XX-XX-XX"'
        elif resultado_matricula:
            self.mensagem_adicionar['text'] = 'Essa matrícula já está atribuida.'
        else:
            try:
                dt = datetime.now()
                data_agora = dt.strftime('%Y-%m-%d %H:%M:%S')
                query_movimentos = 'INSERT INTO Movimentos VALUES (NULL, ?)'
                movimentos = f'Veiculo {marca} {modelo} Adicionado no dia: {data_agora}  Utilizador: {self.nome_utilizador.title()}'
                self.db_consulta(query_movimentos, (movimentos,))
                self.db_consulta(query, parametros)
                self.mensagem_adicionar['text'] = 'Veiculo adicionado com sucesso!'
                self.janela_veiculos.after(1500, self.janela_veiculos.destroy)
            except sqlite3.OperationalError:
                self.mensagem['text'] = 'Erro de Base de Dados'

        self.get_veiculos()

    def editar_veiculo(self):

        if not hasattr(self, 'mensagem_apagar'):
            self.mensagem_editar = Label(self.janela_inicio, text='', fg='red', font=('Arial', 15))
            self.mensagem_editar.place(x=850, y=20)

        try:
            self.tabela_veiculos_gerir.item(self.tabela_veiculos_gerir.selection())['values'][0]
        except IndexError:
            self.mensagem_editar['text'] = 'Selecione um Veiculo'
            self.janela_inicio.after(1500, lambda: self.mensagem_editar.config(text=''))
            return

        id = self.tabela_veiculos_gerir.item(self.tabela_veiculos_gerir.selection())['text']
        marca = self.tabela_veiculos_gerir.item(self.tabela_veiculos_gerir.selection())['values'][0]
        modelo = self.tabela_veiculos_gerir.item(self.tabela_veiculos_gerir.selection())['values'][1]
        categoria = self.tabela_veiculos_gerir.item(self.tabela_veiculos_gerir.selection())['values'][2]
        tipo = self.tabela_veiculos_gerir.item(self.tabela_veiculos_gerir.selection())['values'][3]
        pessoas = self.tabela_veiculos_gerir.item(self.tabela_veiculos_gerir.selection())['values'][4]
        imagem = self.tabela_veiculos_gerir.item(self.tabela_veiculos_gerir.selection())['values'][5]
        preco = self.tabela_veiculos_gerir.item(self.tabela_veiculos_gerir.selection())['values'][6]
        revisao = self.tabela_veiculos_gerir.item(self.tabela_veiculos_gerir.selection())['values'][7]
        legalizacao = self.tabela_veiculos_gerir.item(self.tabela_veiculos_gerir.selection())['values'][8]
        manutencao = self.tabela_veiculos_gerir.item(self.tabela_veiculos_gerir.selection())['values'][9]
        disponivel = self.tabela_veiculos_gerir.item(self.tabela_veiculos_gerir.selection())['values'][10]
        matricula = self.tabela_veiculos_gerir.item(self.tabela_veiculos_gerir.selection())['values'][11]

        if self.janela_veiculos is None or not self.janela_veiculos.winfo_exists():
            self.janela_veiculos = Toplevel()
            self.janela_veiculos.title = 'Editar Veiculo'
            self.janela_veiculos.resizable(False, False)
            self.janela_veiculos.wm_iconbitmap('recursos/luxury.ico')
            self.janela_veiculos.geometry('630x750')

            frame_editar_veiculos = LabelFrame(self.janela_veiculos, text='Editar Veiculo', font=('Nerko One', 20, 'bold'))
            frame_editar_veiculos.place(x=150, y=60)

            self.mensagem_editar = Label(self.janela_veiculos, text='', fg='red')
            self.mensagem_editar.place(x=150, y=20)

            self.etiqueta_marca_antiga = Label(frame_editar_veiculos, text='Marca Antiga: ', font=('Arial', 10))
            self.etiqueta_marca_antiga.grid(row=1, column=0)
            self.input_marca_antiga = Entry(frame_editar_veiculos,
                                            textvariable=StringVar(self.janela_veiculos, value=marca),
                                            state='readonly', font=('Arial', 10))
            self.input_marca_antiga.grid(row=1, column=1)

            self.etiqueta_marca_nova = Label(frame_editar_veiculos, text='Marca Nova: ', font=('Arial', 10))
            self.etiqueta_marca_nova.grid(row=2, column=0)
            self.input_marca_nova = Entry(frame_editar_veiculos, font=('Arial', 10))
            self.input_marca_nova.grid(row=2, column=1)

            self.etiqueta_modelo_antigo = Label(frame_editar_veiculos, text='Modelo Antigo: ', font=('Arial', 10))
            self.etiqueta_modelo_antigo.grid(row=3, column=0)
            self.input_modelo_antigo = Entry(frame_editar_veiculos,
                                             textvariable=StringVar(self.janela_veiculos, value=modelo),
                                             state='readonly', font=('Arial', 10))
            self.input_modelo_antigo.grid(row=3, column=1)

            self.etiqueta_modelo_novo = Label(frame_editar_veiculos, text='Modelo Novo: ', font=('Arial', 10))
            self.etiqueta_modelo_novo.grid(row=4, column=0)
            self.input_modelo_novo = Entry(frame_editar_veiculos, font=('Arial', 10))
            self.input_modelo_novo.grid(row=4, column=1)

            self.etiqueta_categoria_antiga = Label(frame_editar_veiculos, text='Categoria Antiga: ', font=('Arial', 10))
            self.etiqueta_categoria_antiga.grid(row=5, column=0)
            self.input_categoria_antiga = Entry(frame_editar_veiculos,
                                                textvariable=StringVar(self.janela_veiculos, value=categoria),
                                                state='readonly',
                                                font=('Arial', 10))
            self.input_categoria_antiga.grid(row=5, column=1)

            menu_c = StringVar()
            menu_c.set('Categorias:')
            menu_categoria = ['CARRO', 'MOTO']

            self.etiqueta_categoria_nova = Label(frame_editar_veiculos, text='Categoria Nova: ', font=('Arial', 10))
            self.etiqueta_categoria_nova.grid(row=6, column=0)
            self.input_categoria_nova = ttk.OptionMenu(frame_editar_veiculos, menu_c, menu_c.get(), *menu_categoria)
            self.input_categoria_nova.grid(row=6, column=1)

            self.etiqueta_tipo_antigo = Label(frame_editar_veiculos, text='Tipo Antigo: ', font=('Arial', 10))
            self.etiqueta_tipo_antigo.grid(row=7, column=0)
            self.input_tipo_antigo = Entry(frame_editar_veiculos,
                                           textvariable=StringVar(self.janela_veiculos, value=tipo),
                                           state='readonly', font=('Arial', 10))
            self.input_tipo_antigo.grid(row=7, column=1)

            menu_t = StringVar()
            menu_t.set('Tipos:')
            menu_tipo = ['Luxo', 'Citadino', 'Familiar', 'SUV', 'Clássico', 'Conforto', 'Desportivo']

            self.etiqueta_tipo_novo = Label(frame_editar_veiculos, text='Tipo Novo: ', font=('Arial', 10))
            self.etiqueta_tipo_novo.grid(row=8, column=0)
            self.input_tipo_novo = ttk.OptionMenu(frame_editar_veiculos, menu_t, menu_t.get(), *menu_tipo)
            self.input_tipo_novo.grid(row=8, column=1)

            self.etiqueta_quantidade_antiga = Label(frame_editar_veiculos, text='Quantidade de Pessoas Antigo: ',
                                                    font=('Arial', 10))
            self.etiqueta_quantidade_antiga.grid(row=9, column=0)
            self.input_quantidade_antiga = Entry(frame_editar_veiculos,
                                                 textvariable=StringVar(self.janela_veiculos, value=pessoas),
                                                 state='readonly',
                                                 font=('Arial', 10))
            self.input_quantidade_antiga.grid(row=9, column=1)

            self.etiqueta_quantidade_nova = Label(frame_editar_veiculos, text='Quantidade de Pessoas Nova: ',
                                                  font=('Arial', 10))
            self.etiqueta_quantidade_nova.grid(row=10, column=0)
            self.input_quantidade_nova = Entry(frame_editar_veiculos, font=('Arial', 10))
            self.input_quantidade_nova.grid(row=10, column=1)

            self.etiqueta_imagem_antiga = Label(frame_editar_veiculos, text='Caminho Imagem Antigo:')
            self.etiqueta_imagem_antiga.grid(row=11, column=0)
            self.input_imagem_antiga = Entry(frame_editar_veiculos, textvariable=StringVar(self.janela_veiculos,
                                                                    value=imagem), state='readonly', font=('Arial', 10))
            self.input_imagem_antiga.grid(row=11, column=1)

            self.etiqueta_imagem_nova = Label(frame_editar_veiculos, text='Caminho Imagem Novo: ', font=('Arial', 10))
            self.etiqueta_imagem_nova.grid(row=12, column=0)
            self.input_imagem_nova = Entry(frame_editar_veiculos, font=('Arial', 10))
            self.input_imagem_nova.grid(row=12, column=1)

            self.etiqueta_preco_antigo = Label(frame_editar_veiculos, text='Preço Antigo: ', font=('Arial', 10))
            self.etiqueta_preco_antigo.grid(row=13, column=0)
            self.input_preco_antigo = Entry(frame_editar_veiculos,
                                            textvariable=StringVar(self.janela_veiculos, value=preco),
                                            state='readonly', font=('Arial', 10))
            self.input_preco_antigo.grid(row=13, column=1)

            self.etiqueta_preco_novo = Label(frame_editar_veiculos, text='Preço Novo: ', font=('Arial', 10))
            self.etiqueta_preco_novo.grid(row=14, column=0)
            self.input_preco_novo = Entry(frame_editar_veiculos, font=('Arial', 10))
            self.input_preco_novo.grid(row=14, column=1)

            self.etiqueta_revisao_antiga = Label(frame_editar_veiculos, text='Ultima Revisão: ', font=('Arial', 10))
            self.etiqueta_revisao_antiga.grid(row=15, column=0)
            self.input_revisao_antiga = Entry(frame_editar_veiculos, textvariable=StringVar(self.janela_veiculos,
                                                                                            value=revisao),
                                              state='readonly', font=('Arial', 10))
            self.input_revisao_antiga.grid(row=15, column=1)

            self.etiqueta_revisao_nova = Label(frame_editar_veiculos, text='Nova Data de revisão: ',
                                               font=('Arial', 10))
            self.etiqueta_revisao_nova.grid(row=16, column=0)
            self.input_revisao_nova = Entry(frame_editar_veiculos, font=('Arial', 10))
            self.input_revisao_nova.grid(row=16, column=1)

            self.etiqueta_legalizacao_antiga = Label(frame_editar_veiculos, text='Ultima Legalização: ')
            self.etiqueta_legalizacao_antiga.grid(row=17, column=0)
            self.input_legalizacao_antiga = Entry(frame_editar_veiculos, textvariable=StringVar(self.janela_veiculos,
                                                                                                value=legalizacao),
                                                  state='readonly', font=('Arial', 10))
            self.input_legalizacao_antiga.grid(row=17, column=1)

            self.etiqueta_legalizacao_nova = Label(frame_editar_veiculos, text='Nova Data de legalização:')
            self.etiqueta_legalizacao_nova.grid(row=18, column=0)
            self.input_legalizacao_nova = Entry(frame_editar_veiculos, font=('Arial', 10))
            self.input_legalizacao_nova.grid(row=18, column=1)

            manutencao_p = StringVar()
            manutencao_p.set('Escolha uma opção:')
            opcoes_manutencao = ['Sim', 'Não']

            self.etiqueta_manutencao_antiga = Label(frame_editar_veiculos, text='Manutenção Antes: ')
            self.etiqueta_manutencao_antiga.grid(row=19, column=0)
            self.input_manutencao_antiga = Entry(frame_editar_veiculos, textvariable=StringVar(self.janela_veiculos,
                                                                                               value=manutencao),
                                                 state='readonly', font=('Arial', 10))
            self.input_manutencao_antiga.grid(row=19, column=1)

            self.etiqueta_manutencao_nova = Label(frame_editar_veiculos, text='Em Manutenção?')
            self.etiqueta_manutencao_nova.grid(row=20, column=0)
            self.input_manutencao_nova = ttk.OptionMenu(frame_editar_veiculos, manutencao_p, manutencao_p.get(),
                                                        *opcoes_manutencao)
            self.input_manutencao_nova.grid(row=20, column=1)

            disponivel_p = StringVar()
            disponivel_p.set('Escolha uma opção:')
            opcoes_disponivel = ['Sim', 'Não']

            self.etiqueta_disponivel_antigo = Label(frame_editar_veiculos, text='Disponibilidade Antes: ')
            self.etiqueta_disponivel_antigo.grid(row=21, column=0)
            self.input_disponivel_antigo = Entry(frame_editar_veiculos, textvariable=StringVar(self.janela_veiculos,
                                                                                               value=disponivel),
                                                 state='readonly', font=('Arial', 10))
            self.input_disponivel_antigo.grid(row=21, column=1)

            self.etiqueta_disponivel_novo = Label(frame_editar_veiculos, text='Disponivel?')
            self.etiqueta_disponivel_novo.grid(row=22, column=0)
            self.input_disponivel_novo = ttk.OptionMenu(frame_editar_veiculos, disponivel_p, disponivel_p.get(),
                                                        *opcoes_disponivel)
            self.input_disponivel_novo.grid(row=22, column=1)

            self.etiqueta_matricula_antigo = Label(frame_editar_veiculos, text='Matricula Antiga: ')
            self.etiqueta_matricula_antigo.grid(row=23, column=0)
            self.input_matricula_antigo = Entry(frame_editar_veiculos, textvariable=StringVar(self.janela_veiculos,
                                                                                              value=matricula),
                                                state='readonly', font=('Arial', 10))
            self.input_matricula_antigo.grid(row=23, column=1)

            self.etiqueta_matricula_novo = Label(frame_editar_veiculos, text='Matricula Nova:')
            self.etiqueta_matricula_novo.grid(row=24, column=0)
            self.input_matricula_novo = Entry(frame_editar_veiculos, font=('Arial', 10))
            self.input_matricula_novo.grid(row=24, column=1)

            botao_atualizar = Button(frame_editar_veiculos, text='ATUALIZAR VEICULO',
                                     command=lambda: self.atualizar_veiculo(
                                         id,
                                         self.input_marca_nova.get(),
                                         self.input_marca_antiga.get(),
                                         self.input_modelo_novo.get(),
                                         self.input_modelo_antigo.get(),
                                         menu_c.get(),
                                         self.input_categoria_antiga.get(),
                                         menu_t.get(),
                                         self.input_tipo_antigo.get(),
                                         self.input_quantidade_nova.get(),
                                         self.input_quantidade_antiga.get(),
                                         self.input_imagem_nova.get(),
                                         self.input_imagem_antiga.get(),
                                         self.input_preco_novo.get(),
                                         self.input_preco_antigo.get(),
                                         self.input_revisao_nova.get(),
                                         self.input_revisao_antiga.get(),
                                         self.input_legalizacao_nova.get(),
                                         self.input_legalizacao_antiga.get(),
                                         manutencao_p.get(),
                                         self.input_manutencao_antiga.get(),
                                         disponivel_p.get(),
                                         self.input_disponivel_antigo.get(),
                                         self.input_matricula_novo.get(),
                                         self.input_matricula_antigo.get()))
            botao_atualizar.grid(row=25, column=0, columnspan=2, sticky=W + E)
        else:
            self.janela_veiculos.lift()

    def atualizar_veiculo(self, id, nova_marca, antiga_marca, novo_modelo, antigo_modelo, nova_categoria, antiga_categoria,
                          novo_tipo, antigo_tipo, pessoas_novo, pessoas_antigo,  imagem_nova, imagem_antiga, novo_preco,
                          antigo_preco, nova_revisao, antiga_revisao, nova_legalizacao, antiga_legalizacao,
                          manutencao_nova, manutencao_antiga, disponivel_nova, disponivel_antiga,
                          matricula_nova, matricula_antiga):

        veiculo_modificado = False
        parametros = []

        # Função auxiliar para adicionar parâmetro
        def adicionar_parametro(novo_valor, valor_antigo):
            nonlocal veiculo_modificado
            if novo_valor and novo_valor != valor_antigo:
                parametros.append(novo_valor)
                veiculo_modificado = True
                return True
            parametros.append(valor_antigo)
            return False

        if nova_revisao != '' and not self.validar_data(nova_revisao):
            self.mensagem_editar['text'] = 'Formato de data errado!'
            return

        if nova_legalizacao != '' and not self.validar_data(nova_legalizacao):
            self.mensagem_editar['text'] = 'Formato de data errado!'
            return

        if matricula_nova != '' and not self.validar_matricula(matricula_nova):
            self.mensagem_editar['text'] = 'Formato de matrícula inválido!'
        elif matricula_nova == '':
            matricula_nova = matricula_antiga

        # Verificar e adicionar cada campo
        adicionar_parametro(nova_marca, antiga_marca)
        adicionar_parametro(novo_modelo, antigo_modelo)
        adicionar_parametro(nova_categoria if nova_categoria != "Categorias:" else "", antiga_categoria)
        adicionar_parametro(novo_tipo if novo_tipo != "Tipos:" else "", antigo_tipo)
        adicionar_parametro(pessoas_novo, pessoas_antigo)
        adicionar_parametro(imagem_nova, imagem_antiga)
        adicionar_parametro(novo_preco, antigo_preco)
        adicionar_parametro(nova_revisao, antiga_revisao)
        adicionar_parametro(nova_legalizacao, antiga_legalizacao)
        adicionar_parametro(manutencao_nova if manutencao_nova != "Escolha uma opção:" else "", manutencao_antiga)
        adicionar_parametro(disponivel_nova if disponivel_nova != "Escolha uma opção:" else "", disponivel_antiga)
        adicionar_parametro(matricula_nova, matricula_antiga)

        parametros.extend([id])

        dt = datetime.now()
        data_agora = dt.strftime('%Y-%m-%d %H:%M:%S')
        query_movimentos = 'INSERT INTO Movimentos VALUES (NULL, ?)'
        movimentos = f'Veiculo {antiga_marca} {antigo_modelo} Atualizado no dia: {data_agora}  Utilizador: {self.nome_utilizador.title()}'

        if veiculo_modificado:
            try:
                query = (
                    'UPDATE Veiculos SET Marca = ?, Modelo = ?, Categoria = ?, [Tipo de Veiculo] = ?, [Qt Pessoas] = ?,'
                    'Imagem = ?, Preço = ?, [Ultima Revisao] = ?, [Ultima Legalizacao] = ?, Manutenção = ?,'
                    'Disponivel = ?, Matricula = ?'
                    'WHERE ID = ?')
                self.db_consulta(query, tuple(parametros))
                self.db_consulta(query_movimentos, (movimentos,))
                self.mensagem_editar[
                    'text'] = f'Veiculo da marca {antiga_marca} e modelo {antigo_modelo} modificado com sucesso!'
                self.janela_veiculos.after(1000, self.janela_veiculos.destroy)
            except sqlite3.OperationalError:
                self.mensagem['text'] = 'Erro de Base de Dados'
        else:
            self.mensagem_editar['text'] = f'Veiculo NÃO foi modificado.'
            self.janela_veiculos.after(1000, self.janela_veiculos.destroy)

        self.get_veiculos()

    def get_veiculos(self):

        try:
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
        except sqlite3.OperationalError:
            self.mensagem['text'] = 'Erro de Base de Dados'
