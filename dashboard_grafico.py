import textwrap
import tkinter
from tkinter import *
import datetime
from datetime import *
import matplotlib.pyplot as plt
from app import *


class Dashboard:

    def __init__(self, janela_incio, db_consulta, janela_dashboard):
        self.janela_inicio = janela_incio
        self.db_consulta = db_consulta
        self.janela_dashboard = janela_dashboard

        self.janela_dashboard = None

    def grafico_reservas(self, frame):
        query_reservas = 'SELECT * FROM Reservas'
        registos_db = self.db_consulta(query_reservas)

        veiculos = []
        dias_restantes = []
        dt = datetime.now()

        for linha in registos_db:
            marca_modelo = f"{linha[2]} {linha[3]}"
            data_inicio = datetime.strptime(linha[4], '%Y-%m-%d')
            data_fim = datetime.strptime(linha[5], '%Y-%m-%d')
            dias_restantes_reserva = (data_fim - dt).days
            if data_fim >= dt and data_inicio <= dt:
                veiculos.append(marca_modelo)
                dias_restantes.append(dias_restantes_reserva)

        # Criar a figura do gráfico de barras
        fig, ax = plt.subplots(figsize=(11, 5))
        ax.bar(veiculos, dias_restantes, color='blue')
        ax.set_xlabel('Veículos')
        ax.set_ylabel('Dias Restantes')
        ax.set_title('Dias Restantes para Reservas Ativas')

        # Adicionar o gráfico ao Tkinter usando o Canvas
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column=0, columnspan=2, sticky='nsew')

    def grafico_clientes(self, frame):

        query_clientes = 'SELECT ID, Nome, [Data Inscrição] FROM CLIENTES ORDER BY ID DESC LIMIT 7'
        resultados_clientes = self.db_consulta(query_clientes)

        clientes = []
        inscricao = []

        for linha in resultados_clientes:
            nomes = linha[1]
            data = linha[2]
            if nomes not in clientes:
                clientes.append(nomes)
                inscricao.append(data)

        fig, ax = plt.subplots(figsize=(11, 5))
        ax.bar(inscricao, clientes, color='purple')
        ax.set_ylabel('Clientes')
        ax.set_xlabel('Data de Inscrição')
        ax.set_title('Ultimos 7 Clientes registados')

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column=0, columnspan=2, sticky='nsew')

    def grafico_mes(self, frame):

        selecionar_mes = StringVar()
        selecionar_mes.set('Escolha um mês:')
        meses = {'Janeiro': "01", 'Fevereiro': "02", 'Março': "03", 'Abril': "04", 'Maio': "05", 'Junho': "06",
                 'Julho': "07", 'Agosto': "08", 'Setembro': "09", 'Outubro': "10", 'Novembro': "11",
                 'Dezembro': "12"}

        selecionar_ano = StringVar()
        selecionar_ano.set('Escolha um ano:')
        anos = ['2022', '2023', '2024', '2025']

        barra_meses = ttk.OptionMenu(frame, selecionar_mes, selecionar_mes.get(), *meses)
        barra_meses.grid(row=2, column=0)

        barra_anos = ttk.OptionMenu(frame, selecionar_ano, selecionar_ano.get(), *anos)
        barra_anos.grid(row=2, column=1)

        def filtrar():

            mes_escolhido = selecionar_mes.get()
            ano_escolhido = selecionar_ano.get()

            parametros = []

            query = 'SELECT * FROM RESERVAS WHERE 1=1'

            if mes_escolhido in meses:
                mes_numerico = meses[mes_escolhido]
                query += ' AND substr([Data Inicio], 6, 2) = ?'
                parametros.append(mes_numerico)

            if ano_escolhido in anos:
                query += ' AND substr([Data Inicio], 1, 4) = ?'
                parametros.append(ano_escolhido)

            total_reserva = []
            veiculos_mes = []

            if parametros:
                resultados_mes = self.db_consulta(query, tuple(parametros))

                for linha in resultados_mes:
                    dias_de_aluguer = (datetime.strptime(linha[5], '%Y-%m-%d') - datetime.strptime(linha[4],
                                                                                                   '%Y-%m-%d')).days
                    preco_total = linha[6] * dias_de_aluguer
                    total_reserva.append(preco_total)
                    veiculo = f'{linha[2]}\n{linha[3]}'
                    veiculos_mes.append(veiculo)

                total_mes = sum(total_reserva)

            fig, ax = plt.subplots(figsize=(11, 5))
            ax.bar(veiculos_mes, total_reserva, color='green')
            ax.set_ylabel('Preço Total Reserva')
            ax.set_xlabel('Veículos')
            ax.set_title('Total Mês Reservas/Financeiro')

            if total_reserva:
                ax.set_ylim(0, max(total_reserva) + 1000)
            else:
                self.janela_inicio.after(100, lambda: messagebox.showerror(
                    'ERRO', 'Não há reservas no Mês/Ano selecionado/s '))

            ax.text(1.10, 1.10, f'Total Financeiro: {total_mes:.2f}€',
                    transform=ax.transAxes, fontsize=12, color='black', ha='right', va='top',
                    bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))

            canvas = FigureCanvasTkAgg(fig, master=frame)
            canvas.draw()
            canvas.get_tk_widget().grid(row=1, column=0, columnspan=2, sticky='nsew')

        botao_confirmar = Button(frame, text='CONFIRMAR', command=filtrar)
        botao_confirmar.grid(row=3, column=1, columnspan=2)

    def grafico_veiculos(self, frame):

        query_veiculos = 'SELECT * FROM Veiculos'
        resultados_veiculos = self.db_consulta(query_veiculos)

        categorias_tipos = {}

        for linha in resultados_veiculos:
            categoria = linha[3]
            tipo = linha[4]
            if categoria not in categorias_tipos:
                categorias_tipos[categoria] = []
            if tipo not in categorias_tipos[categoria]:
                categorias_tipos[categoria].append(tipo)

        categoria = StringVar()
        categorias_opcoes = list(categorias_tipos.keys())
        categoria.set(categorias_opcoes[0])

        self.barra_categorias = ttk.OptionMenu(frame, categoria, categoria.get(), *categorias_opcoes)
        self.barra_categorias.grid(row=2, column=0)

        def filtrar():

            categoria_selecionada = categoria.get()

            query_filtrada = 'SELECT * FROM Veiculos WHERE Disponivel = "Sim" AND Manutenção = "Não"'
            parametros = []

            if categoria_selecionada in categorias_tipos:
                query_filtrada += ' AND Categoria = ?'
                parametros.append(categoria_selecionada)

            resultados_db_filtrado = self.db_consulta(query_filtrada, parametros)

            if resultados_db_filtrado:

                tipos_contagem = {}
                nomes_veiculos = {}

                for linha in resultados_db_filtrado:
                    tipo_db = linha[4]
                    nome_veiculo = f"{linha[1]} {linha[2]}"

                    # Contar quantos veículos de cada tipo existem
                    if tipo_db not in tipos_contagem:
                        tipos_contagem[tipo_db] = 0
                        nomes_veiculos[tipo_db] = []
                    tipos_contagem[tipo_db] += 1
                    nomes_veiculos[tipo_db].append(nome_veiculo)

                etiquetas = []
                sizes = []

                for tipo, count in tipos_contagem.items():
                    etiquetas.append(f"{count} {tipo}")
                    sizes.append(count)

                # Criar gráfico de pizza
                fig, ax = plt.subplots(figsize=(11, 5))
                wedges, texts, autotexts = ax.pie(
                    sizes, labels=etiquetas, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)

                ax.set_position([0.3, 0.1, 0.6, 0.8])

                legenda = []
                for tipo, veiculos in nomes_veiculos.items():
                    # Quebrar a lista de veículos em múltiplas linhas para evitar texto muito longo
                    # textwrap.fill() trata da quebra no width dando um máximo de 40 caracteres
                    legenda_texto = textwrap.fill(f"{tipo}: {', '.join(veiculos)}", width=40)
                    legenda.append(legenda_texto)

                # Adicionar legenda com quebra de linha automática
                ax.legend(wedges, legenda, title="Veículos", loc="center right", bbox_to_anchor=(0, 0.9, 0.1, 0))

                # Centrar o gráfico
                ax.axis('equal')

                canvas = FigureCanvasTkAgg(fig, master=frame)
                canvas.draw()
                canvas.get_tk_widget().grid(row=3, column=0, columnspan=2, sticky='nsew')

        # Botão para confirmar e gerar gráfico
        botao_confirmar = Button(frame, text='CONFIRMAR', command=filtrar)
        botao_confirmar.grid(row=2, column=1)

    def grafico_revisoes(self, frame):

        query_revisao = 'SELECT * FROM Veiculos ORDER BY ID'
        resultados_revisao = self.db_consulta(query_revisao)

        formato_data = '%d-%m-%Y'
        dt = datetime.now()

        veiculos = []
        revisoes = []

        for linha in resultados_revisao:
            veiculo = f'{linha[1]}\n{linha[2]}'
            data_fim = datetime.strptime(linha[8], formato_data)
            data_proxima = data_fim + timedelta(days=365)
            dias_restantes = (data_proxima - dt).days + 1
            if dias_restantes <= 0:
                dias_restantes = 0
                self.janela_inicio.after(100, lambda: messagebox.showwarning(
                    'ATENÇÃO', 'DATA DE REVISÃO ULTRAPASSADA '
                               '\nALTERAR DISPONIBILICADE DO VEICULO E FAZER MANUTENÇÃO'))
            if dias_restantes <= 5 and dias_restantes > 0:
                self.janela_inicio.after(100, lambda: messagebox.showwarning(
                    'ATENÇÃO', 'DATA DE REVISÃO PERTO DE SER ULTRAPASSADA '
                               '\nALTERAR DISPONIBILICADE DO VEICULO E FAZER MANUTENÇÃO'))
            if dias_restantes <= 15:
                veiculos.append(veiculo)
                revisoes.append(dias_restantes)

        fig, ax = plt.subplots(figsize=(11, 5))
        ax.bar(veiculos, revisoes, color='red')
        ax.set_title('Veículos perto de Revisão | máx. 15 dias')
        ax.set_ylabel('Dias até Revisão')
        ax.set_xlabel('Veículos')

        ax.set_ylim(0, max(revisoes) + 5)

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column=0, columnspan=2, sticky='nsew')

    def grafico_legalizacoes(self, frame):

        query_legalizacao = 'SELECT * FROM Veiculos ORDER BY ID'
        resultados_legalizacao = self.db_consulta(query_legalizacao)

        formato_data = '%d-%m-%Y'
        dt = datetime.now()

        veiculos = []
        legalizacoes = []

        for linha in resultados_legalizacao:
            veiculo = f'{linha[1]}\n{linha[2]}'
            data_fim = datetime.strptime(linha[9], formato_data)
            data_proxima = data_fim + timedelta(days=365)
            dias_restantes = (data_proxima - dt).days + 1
            if dias_restantes <= 0:
                dias_restantes = 0
            if dias_restantes <= 15:
                veiculos.append(veiculo)
                legalizacoes.append(dias_restantes)

        fig, ax = plt.subplots(figsize=(11, 5))
        ax.bar(veiculos, legalizacoes, color='red')
        ax.set_title('Veículos a expirar Legalização | máx. 15 dias')
        ax.set_ylabel('Dias até Legalização')
        ax.set_xlabel('Veículos')

        ax.set_ylim(0, max(legalizacoes) + 5)

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column=0, columnspan=2, sticky='nsew')

    def criar_graficos(self):

        frame_dashboard = LabelFrame(self.janela_inicio, text='Gráficos', font=('Nerko One', 40))
        frame_dashboard.grid(row=10, column=10)

        graficos = StringVar()
        graficos.set('Escolha um gráfico:')
        opcoes = ['Veículos Alugados e dias restantes da reserva', 'Ultimos Clientes Registados',
                  'Reservas do Mês', 'Veículos Disponíveis', 'Veículos próximos de expirar revisão',
                  'Veículos próximos de expirar legalização']

        barra_graficos = ttk.OptionMenu(frame_dashboard, graficos, graficos.get(), *opcoes)
        barra_graficos.grid(row=0, column=0)

        botao_fechar = Button(frame_dashboard, text='FECHAR', command=frame_dashboard.destroy)
        botao_fechar.grid(row=0, column=1, columnspan=3)

        def selecionar_grafico(*args):

            # Fechar tudo que está no frame_dashboard exceto o botão de fechar e o Option Menu que são necessários
            for widget in frame_dashboard.winfo_children():
                if widget not in (barra_graficos, botao_fechar):
                    widget.destroy()

            if graficos.get() == opcoes[0]:
                self.grafico_reservas(frame_dashboard)

            elif graficos.get() == opcoes[1]:
                self.grafico_clientes(frame_dashboard)

            elif graficos.get() == opcoes[2]:
                self.grafico_mes(frame_dashboard)

            elif graficos.get() == opcoes[3]:
                self.grafico_veiculos(frame_dashboard)

            elif graficos.get() == opcoes[4]:
                self.grafico_revisoes(frame_dashboard)

            elif graficos.get() == opcoes[5]:
                self.grafico_legalizacoes(frame_dashboard)

        graficos.trace_add('write', selecionar_grafico)

    def dashboard_completo(self):

        if self.janela_dashboard is None or not self.janela_dashboard.winfo_exists():
            self.janela_dashboard = Toplevel()
            self.janela_dashboard.title('DASHBOARD')
            self.janela_dashboard.resizable(1, 1)
            self.janela_dashboard.wm_iconbitmap('recursos/luxury.ico')
            self.janela_dashboard.geometry("1200x700")

            self.janela_dashboard.rowconfigure(0, weight=1)
            self.janela_dashboard.columnconfigure(0, weight=1)

            # Canvas é basicamente um programa de edição vetorial do TKINTER sendo ele que me vai ajudar a manipular a janela
            # do dashboard pois os gráficos são muito grandes e não consegui adicionar diretamente na TOPLEVEL
            # Criação do Canvas
            canvas = Canvas(self.janela_dashboard)
            canvas.grid(row=0, column=0, sticky="nsew")

            barra_ajustavel = ttk.Scrollbar(self.janela_dashboard, orient=VERTICAL, command=canvas.yview)
            barra_ajustavel.grid(row=0, column=1, sticky='ns')

            barra_ajustavel_h = ttk.Scrollbar(self.janela_dashboard, orient=HORIZONTAL, command=canvas.xview)
            barra_ajustavel_h.grid(row=1, column=0, sticky='we')

            # Configurar o Canvas para trabalhar com a Scrollbar
            canvas.configure(yscrollcommand=barra_ajustavel.set)
            canvas.configure(xscrollcommand=barra_ajustavel_h.set)

            # Frame que vai ter o conteúdo do dashboard
            frame_conteudo = Frame(canvas)

            # Criar a janela dentro do canvas para colocar o frame_conteudo
            canvas.create_window((1, 1), window=frame_conteudo, anchor='nw')

            # Criação dos frames para receber os gráficos
            frame_reservas = LabelFrame(frame_conteudo, text='Reservas Ativas', font=('Nerko One', 20, 'bold'))
            frame_reservas.grid(row=0, column=0)

            frame_clientes = LabelFrame(frame_conteudo, text='Ultimos Clientes', font=('Nerko One', 20, 'bold'))
            frame_clientes.grid(row=0, column=1)

            frame_veiculos = LabelFrame(frame_conteudo, text='Veiculos Disponíveis', font=('Nerko One', 20, 'bold'))
            frame_veiculos.grid(row=0, column=2)

            frame_mes = LabelFrame(frame_conteudo, text='Informações Mês/Ano', font=('Nerko One', 20, 'bold'))
            frame_mes.grid(row=1, column=0)

            frame_revisoes = LabelFrame(frame_conteudo, text='Revisões a Terminar', font=('Nerko One', 20, 'bold'))
            frame_revisoes.grid(row=1, column=1)

            frame_legalizacoes = LabelFrame(frame_conteudo, text='Legalizações a Expirar', font=('Nerko One', 20, 'bold'))
            frame_legalizacoes.grid(row=1, column=2)

            # Adicionar os gráficos nos frames corretos
            self.grafico_reservas(frame_reservas)
            self.grafico_clientes(frame_clientes)
            self.grafico_veiculos(frame_veiculos)
            self.grafico_mes(frame_mes)
            self.grafico_revisoes(frame_revisoes)
            self.grafico_legalizacoes(frame_legalizacoes)

            # Atualizar o Canvas com a área de scroll (depois de adicionar todos os widgets)
            frame_conteudo.update_idletasks()
            canvas.config(scrollregion=canvas.bbox("all"))
        else:
            self.janela_dashboard.lift()
