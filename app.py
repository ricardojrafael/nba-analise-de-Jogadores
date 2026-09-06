import streamlit as st

from services.nba_service import (
    obter_jogadores_ativos,
    obter_id_jogador,
    obter_historico_jogos,
    analisar_confronto
)


# CONFIGURAÇÃO DA PÁGINA

st.set_page_config(
    page_title="NBA Player Analytics",
    page_icon="🏀",
    layout="wide"
)


# TÍTULO

st.title("🏀 Análise de Estatísticas dos jogadores da NBA")

st.write(
    "Histórico de confrontos do jogador contra determinado time."
)

st.divider()


# LISTA DE JOGADORES

nomes_jogadores = obter_jogadores_ativos()


# ENTRADA DE DADOS

col_jogador, col_time = st.columns(2)


with col_jogador:

    nome = st.selectbox(
        "Selecione o jogador",
        nomes_jogadores,
        index=None,
        placeholder="Digite o nome do jogador..."
    )


with col_time:

    time_alvo = st.selectbox(
        "Selecione o adversário",
        [
            "ATL",
            "BOS",
            "BKN",
            "CHA",
            "CHI",
            "CLE",
            "DAL",
            "DEN",
            "DET",
            "GSW",
            "HOU",
            "IND",
            "LAC",
            "LAL",
            "MEM",
            "MIA",
            "MIL",
            "MIN",
            "NOP",
            "NYK",
            "OKC",
            "ORL",
            "PHI",
            "PHX",
            "POR",
            "SAC",
            "SAS",
            "TOR",
            "UTA",
            "WAS"
        ],
        index=None,
        placeholder="Selecione o adversário..."
    )


# BOTÃO

analisar = st.button(
    "🔎 Analisar jogador",
    type="primary",
    use_container_width=True
)

# ANÁLISE

if analisar:

    # Verifica se jogador foi selecionado
    if not nome:
        st.warning("Selecione um jogador.")

    # Verifica se adversário foi selecionado
    elif not time_alvo:
        st.warning("Selecione um adversário.")

    else:

        with st.spinner("Buscando dados da NBA..."):

            try:

                # BUSCAR ID DO JOGADOR

                id_atleta = obter_id_jogador(nome)


                if not id_atleta:

                    st.error(
                        "Não foi possível localizar o jogador."
                    )


                else:

                    # BUSCAR HISTÓRICO

                    df_completo = obter_historico_jogos(
                        id_atleta
                    )


                    # FILTRAR ADVERSÁRIO

                    df_vs = analisar_confronto(
                        df_completo,
                        time_alvo
                    )

                    # VERIFICAR RESULTADOS
            

                    if df_vs.empty:

                        st.warning(
                            f"Nenhum confronto de {nome} "
                            f"contra {time_alvo} foi encontrado."
                        )


                    else:

                        
                        # CALCULAR ESTATÍSTICAS


                        media_pts = df_vs["PTS"].mean()

                        media_reb = df_vs["REB"].mean()

                        media_ast = df_vs["AST"].mean()

                        media_min = df_vs["MIN"].mean()

                        media_blk = df_vs["BLK"].mean()

                        media_3pt = df_vs["FG3M"].mean()

                        total_jogos = len(df_vs)


                        # TÍTULO DO RESULTADO

                        st.divider()

                        st.subheader(
                        f"📊 {nome} vs {time_alvo}"
                        )

                        st.caption(
                        f"Baseado em {total_jogos} confronto(s)"
                        )

                        col_foto, col_info = st.columns(
                        [1, 3]
                        )

                        with col_foto:

                            url_foto = (
                            f"https://cdn.nba.com/headshots/nba/latest/1040x760/"
                            f"{id_atleta}.png"
                            )

                            st.image(
                                url_foto,
                                width=220
                            )


                            with col_info:

                                st.title(nome)

                                st.write(
                                    f"Desempenho contra **{time_alvo}**"
                            )

                            st.write(
                                f"Jogos analisados: **{total_jogos}**"
                            )



                        # MÉTRICAS PRINCIPAIS

                        col1, col2, col3, col4, col5, col6 = st.columns(6)


                        col1.metric(
                        "🏀 Pontos", 
                        f"{media_pts:.1f}"
                        )


                        col2.metric(
                        " 🎫 Rebotes",
                        f"{media_reb:.1f}"
                        )


                        col3.metric(
                        " 🔭 Assistências",
                        f"{media_ast:.1f}"
                        )


                        col4.metric(
                        " 🕐 Minutos",
                        f"{media_min:.1f}"
                        )

                        col5.metric(
                        " 👽 Bloqueios",
                        f"{media_blk:.1f}"
                        )

                        col6.metric(
                        "3️⃣ 3  pontos",
                        f"{media_3pt:.1f}"

                        )

                        col_ef1, col_ef2 = st.columns(2)

                        col_ef2.metric(
                        "Jogos analisados",
                        total_jogos
                        )

                        # GRÁFICO DE PONTOS

                        st.subheader(
                        "📈 Pontos por confronto"
                        )


                        df_grafico = (
                        df_vs[
                            [
                                "GAME_DATE",
                                "PTS"
                            ]
                        ]
                        .copy()
                        )


                        df_grafico = (
                        df_grafico
                        .sort_values(
                            "GAME_DATE"
                        )
                        )


                        df_grafico = (
                        df_grafico
                        .set_index(
                            "GAME_DATE"
                        )
                        )


                        st.line_chart(
                        df_grafico
                        )

                        # HISTÓRICO DOS JOGOS

                        st.subheader(
                        "📋 Histórico de confrontos"
                        )


                        colunas = [
                        "GAME_DATE",
                        "MATCHUP",
                        "MIN",
                        "PTS",
                        "REB",
                        "AST",
                        "BLK"
                        ]


                        st.dataframe(
                        df_vs[colunas],
                        use_container_width=True,
                        hide_index=True
                        )

                # TRATAMENTO DE ERROS
            except Exception as erro:

                st.error(
                "Ocorreu um erro ao buscar os dados da NBA."
                )

                st.exception(erro)