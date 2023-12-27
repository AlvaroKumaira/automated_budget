def client_name(client_code):
    return f"""
         SELECT DISTINCT 
         A1_NOME 
         FROM SA1010 
         WHERE A1_COD = '{client_code}'
        """


def item_info(item_code):
    return f"""
        SELECT
        P.B1_ZGRUPO,
        P.B1_DESC
        FROM
            SB1010 AS P
        WHERE
        P.D_E_L_E_T_ <> '*' AND
        P.B1_GRUPO NOT IN ('002', '001', '003') AND
        P.B1_TIPO IN ('ME', 'MI', 'KT', 'PA') AND
        P.B1_COD = '{item_code}'
"""


def sales_six_months_client(filial, client_code, group_code):
    return f"""
        SELECT TOP 1
        SD2.D2_TOTAL / NULLIF(SD2.D2_QUANT, 0) AS ValorUnitario
        FROM SD2010 AS SD2
        INNER JOIN SB1010 AS SB
        ON TRIM(SD2.D2_COD) = TRIM(SB.B1_COD)
        AND SB.D_E_L_E_T_ <> '*'
        WHERE SD2.D_E_L_E_T_  <> '*'
        AND SB.B1_GRUPO NOT IN ('002', '001', '003')
        AND SB.B1_TIPO IN ('ME', 'MI', 'KT', 'PA')
        AND SD2.D2_EMISSAO >= FORMAT(DATEADD(MONTH, -6, GETDATE()), 'yyyyMMdd')
        AND SD2.D2_FILIAL = '{filial}'
        AND SB.B1_ZGRUPO = '{group_code}'
        AND SD2.D2_CLIENTE = '{client_code}'
        ORDER BY SD2.D2_EMISSAO DESC
        """


def sales_six_months(filial, group_code):
    return f"""
        SELECT TOP 1
        SD2.D2_TOTAL / NULLIF(SD2.D2_QUANT, 0) AS ValorUnitario
        FROM SD2010 AS SD2
        INNER JOIN SB1010 AS SB
        ON TRIM(SD2.D2_COD) = TRIM(SB.B1_COD)
        AND SB.D_E_L_E_T_ <> '*'
        WHERE SD2.D_E_L_E_T_  <> '*'
        AND SB.B1_GRUPO NOT IN ('002', '001', '003')
        AND SB.B1_TIPO IN ('ME', 'MI', 'KT', 'PA')
        AND SD2.D2_EMISSAO >= FORMAT(DATEADD(MONTH, -6, GETDATE()), 'yyyyMMdd')
        AND SD2.D2_FILIAL = '{filial}'
        AND SB.B1_ZGRUPO = '{group_code}'
        ORDER BY SD2.D2_EMISSAO DESC
        """


def orders_six_months(group_code):
    return f"""
        SELECT
        AVG(SC7.C7_TOTAL / SC7.C7_QUANT) AS Average
        FROM SC7010 AS SC7
        INNER JOIN
            SB1010 AS SB ON TRIM(SC7.C7_PRODUTO) = TRIM(SB.B1_COD) AND SB.D_E_L_E_T_ <> '*'
        WHERE SC7.D_E_L_E_T_ <> '*' 
        AND SB.B1_GRUPO NOT IN ('002', '001', '003')
        AND SB.B1_TIPO IN ('ME', 'MI', 'KT', 'PA')
        AND SC7.C7_EMISSAO >= FORMAT(DATEADD(MONTH, -6, GETDATE()), 'yyyyMMdd')
        AND SB.B1_ZGRUPO = '{group_code}'
        AND SC7.C7_FILIAL = '0101'
        """


def cost_based_on_stock(group_code):
    return f"""
        SELECT
        MAX(S.B2_CM1) as Average
        FROM
        SB1010 AS P
        LEFT JOIN
        SB2010 AS S ON TRIM(P.B1_COD) = TRIM(S.B2_COD) AND S.B2_FILIAL = '0101' AND S.B2_LOCAL = 'A01' 
        AND S.D_E_L_E_T_ <> '*'
        WHERE
        P.D_E_L_E_T_ <> '*' AND
        P.B1_GRUPO NOT IN ('002', '001', '003') AND
        P.B1_TIPO IN ('ME', 'MI', 'KT', 'PA') AND
        P.B1_ZGRUPO = '{group_code}' AND
        S.B2_QATU > '0' AND
        S.B2_FILIAL IS NOT NULL AND
        S.B2_LOCAL IS NOT NULL
        """


def item_quantity(filial, group_code):
    return f"""
        SELECT
        SUM(S.B2_QATU) as quantidade
        FROM
        SB1010 AS P
        LEFT JOIN
        SB2010 AS S 
        ON
        TRIM(P.B1_COD) = TRIM(S.B2_COD)
        AND S.B2_FILIAL = '{filial}'
        AND (S.B2_LOCAL = 'A01' OR S.B2_LOCAL IS NULL)
        AND S.D_E_L_E_T_ <> '*'
        WHERE
        P.D_E_L_E_T_ <> '*'
        AND P.B1_GRUPO NOT IN ('002', '001', '003')
        AND P.B1_TIPO IN ('ME', 'MI', 'KT', 'PA')
        AND P.B1_ZGRUPO = '{group_code}'

        """
