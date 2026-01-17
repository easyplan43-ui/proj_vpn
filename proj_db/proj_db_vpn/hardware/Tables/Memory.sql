CREATE TABLE [hardware].[Memory] (
    [Memid]  INT            IDENTITY (1, 1) NOT NULL,
    [Manuf]  VARCHAR (15)   NOT NULL,
    [DDR]    VARCHAR (6)    NOT NULL,
    [Volume] TINYINT        NOT NULL,
    [Price]  DECIMAL (2, 2) NULL,
    PRIMARY KEY CLUSTERED ([Memid] ASC),
    CONSTRAINT [Uniq_comb] UNIQUE NONCLUSTERED ([Manuf] ASC, [DDR] ASC, [Volume] ASC)
);


GO

