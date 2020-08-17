# Tennis SQL 

Tennis SQL attempts to move all of https://github.com/JeffSackmann/ .csv tennis datasets to an SQL database for easier querying.

## Todo 

1 - Ingestion
    ~~1.1 - Create 'players' table~~
    1.2 - Create 'games' table
    1.3 - Inherit from games to create seperate WTA, ITF tables 
    1.4 - Scrape data from github
    1.5 - Clean data
    1.6 - Flag potentially unreliable games
    1.7 - Bulk ingest to SQL
    1.8 - Web hook to ingestion data on git commit
    1.9 - Containerise
    1.10 - Deploy

2 - Wrapper