CREATE TABLE [vpn].[Vpn_type] (
    [Vpnid]       INT            IDENTITY (1, 1) NOT NULL,
    [Vpnname]     VARCHAR (15)   NOT NULL,
    [Description] NVARCHAR (MAX) NOT NULL,
    [Rating]      DECIMAL (2, 1) NOT NULL,
    CONSTRAINT [PK_Vpn_type] PRIMARY KEY CLUSTERED ([Vpnid] ASC)
);


GO

