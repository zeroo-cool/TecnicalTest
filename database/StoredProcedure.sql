USE [ventas_db]
GO
/****** Objeto: StoredProcedure [dbo].[ventasTotalesCliente] Fecha de script: 10/06/2026 05:54:43 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
-- =============================================
-- Author:		Ernesto Bardales Hernández
-- Create date: 10-06-2026
-- Description:	Obtiene todos los totales por mes
-- =============================================
ALTER PROCEDURE [dbo].[ventasTotalesCliente]
AS
BEGIN

SELECT 
     [DT].[mes]            AS [Mes]
    ,[DC].[cliente_id]     AS [IdCliente]
    ,[DC].[nombre_cliente] AS [NombreCliente]
    ,SUM([FV].[total])     AS [ventasTotales]   
FROM [ventas_db].[dbo].[fact_ventas] AS [FV]
INNER JOIN [ventas_db].[dbo].[dim_tiempo] AS [DT] 
    ON [DT].[fecha_id] = [FV].[fecha_id]
INNER JOIN [ventas_db].[dbo].[dim_clientes] AS [DC] 
    ON [FV].[cliente_id] = [DC].[cliente_id]
WHERE [FV].[status] = 'Paid'
GROUP BY 
     [DT].[mes]           
    ,[DC].[nombre_cliente]
    ,[DC].[cliente_id]
ORDER BY 
     [DT].[mes] ASC, 
     [ventasTotales] DESC;  


END


--------------------------------------------------


USE [ventas_db]
GO
/****** Objeto: StoredProcedure [dbo].[rankigBestClient] Fecha de script: 10/06/2026 05:54:40 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
-- =============================================
-- Author:		Ernesto Bardales Hernández
-- Create date: 10-06-2026
-- Description:	Obtiene los mejores 5 ventas por cliente general
-- =============================================
ALTER PROCEDURE [dbo].[rankigBestClient]


AS
BEGIN

SELECT TOP 5
     [DC].[cliente_id]              AS [IdCliente]
    ,[DC].[nombre_cliente]          AS [NombreCliente]
    ,SUM([FV].[total])              AS [TotalFacturado] -- Suma toda la facturación histórica
FROM [ventas_db].[dbo].[fact_ventas] AS [FV]
INNER JOIN [ventas_db].[dbo].[dim_clientes] AS [DC] 
    ON [FV].[cliente_id] = [DC].[cliente_id]
-- WHERE [FV].[status] = 'Paid' 
GROUP BY 
     [DC].[cliente_id]
    ,[DC].[nombre_cliente]
ORDER BY [TotalFacturado] DESC;    

END


-------------------------------------------------

USE [ventas_db]
GO
/****** Objeto: StoredProcedure [dbo].[montoTotaldeudores] Fecha de script: 10/06/2026 05:54:38 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
-- =============================================
-- Author:		Ernesto Bardales Hernández
-- Create date: 10-06-2026
-- Description:	Monto Total de Deudores
-- =============================================
ALTER PROCEDURE [dbo].[montoTotaldeudores]

AS
BEGIN
     
     SELECT 
        [DC].[cliente_id]      AS [IdCliente],
        [DC].[nombre_cliente]  AS [NombreCliente],
        SUM([FV].[total])      AS [Total]
    FROM [ventas_db].[dbo].[fact_ventas] AS [FV]
    INNER JOIN [ventas_db].[dbo].[dim_clientes] AS [DC]
        ON [FV].[cliente_id] = [DC].[cliente_id]
    WHERE [FV].[status] IN ('Pending', 'Processing')
    GROUP BY 
        [DC].[cliente_id],
        [DC].[nombre_cliente]
    ORDER BY 
        SUM([FV].[total]) DESC; 


END
---------------------------------------------------

USE [ventas_db]
GO
/****** Objeto: StoredProcedure [dbo].[montoPendienteCobro] Fecha de script: 10/06/2026 05:54:35 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
-- =============================================
-- Author:		Ernesto Bardales Hernández
-- Create date: 10-06-2026
-- Description:	
-- =============================================
ALTER PROCEDURE [dbo].[montoPendienteCobro]

AS
BEGIN

     SELECT SUM(total) as total_pendiente
        FROM [ventas_db].[dbo].[fact_ventas]
        WHERE status IN ('Pending', 'Processing');

END

