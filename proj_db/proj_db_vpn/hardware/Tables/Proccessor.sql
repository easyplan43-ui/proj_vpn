CREATE TABLE [hardware].[Proccessor] (
    [Procid]   INT            IDENTITY (1, 1) NOT NULL,
    [Procname] VARCHAR (15)   NOT NULL,
    [Price]    DECIMAL (2, 2) NOT NULL,
    CONSTRAINT [PK_Proccessor] PRIMARY KEY CLUSTERED ([Procid] ASC)
);


GO

