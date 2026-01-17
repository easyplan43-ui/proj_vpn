CREATE TABLE [locat].[Location] (
    [Locid]  TINYINT        IDENTITY (1, 1) NOT NULL,
    [Place]  VARCHAR (25)   NOT NULL,
    [Rating] DECIMAL (1, 1) NULL,
    PRIMARY KEY CLUSTERED ([Locid] ASC)
);


GO

