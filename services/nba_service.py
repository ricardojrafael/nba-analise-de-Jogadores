# %%
import pandas as pd

from nba_api.stats.static import players
import nba_api.stats.endpoints
from nba_api.stats.endpoints import playergamelog

#%%
# OBTER JOGADORES ATIVOS

def obter_jogadores_ativos():
    jogadores = players.get_active_players()

    nomes_jogadores = [
        jogador["full_name"]
        for jogador in jogadores
    ]

    return nomes_jogadores


# OBTER ID DO JOGADOR

def obter_id_jogador(nome_jogador):
    jogadores = players.get_players()

    for jogador in jogadores:

        if jogador["full_name"].lower() == nome_jogador.lower():
            return jogador["id"]

    return None


# OBTER HISTÓRICO DE JOGOS

def obter_historico_jogos(
    id_jogador,
    temporadas=("2025-26", "2025-24", "2024-23", "2023-22")
):

    if isinstance(temporadas, str):
        temporadas = (temporadas,)

    dfs = []

    for temporada in temporadas:

        log_jogos = playergamelog.PlayerGameLog(
            player_id=id_jogador,
            season=temporada
        )

        df_tmp = log_jogos.get_data_frames()[0]

        # Só adiciona se houver jogos
        if not df_tmp.empty:
            dfs.append(df_tmp)

    # Se não encontrou nenhum jogo
    if not dfs:
        return pd.DataFrame()

    # Junta as temporadas que possuem jogos
    df = pd.concat(
        dfs,
        ignore_index=True
    )

    # =====================================================
    # TRATAMENTO DA COLUNA MIN
    # =====================================================

    if "MIN" in df.columns:

        def converter_minutos(valor):

            # Valor ausente
            if pd.isna(valor):
                return 0.0

            # Se já for número
            if isinstance(valor, (int, float)):
                return float(valor)

            # Converte para string
            valor = str(valor)

            # Formato MM:SS
            if ":" in valor:
                partes = valor.split(":")

                minutos = float(partes[0])
                segundos = float(partes[1])

                return minutos + (segundos / 60)

            # Caso seja algo como "35.0"
            try:
                return float(valor)

            except ValueError:
                return 0.0

        df["MIN"] = df["MIN"].apply(
            converter_minutos
        )

    return df

# ANALISAR CONFRONTO

def analisar_confronto(
    df_jogos,
    sigla_adversario
):

    df_filtrado = df_jogos[
        df_jogos["MATCHUP"].str.contains(
            sigla_adversario,
            na=False
        )
    ].copy()

    return df_filtrado