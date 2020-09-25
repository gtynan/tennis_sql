# Tennis SQL 

## Overview

- FastAPI webserver for easier querying of [Jeff Sackman's](https://github.com/JeffSackmann/tennis_wta) women's tennis csv files.
- Data stored in MySQL database.
- Redis server ingests data on startup and 00:00 daily.  

## Setup

1. Git clone to local machine.
2. Configure constants depending on wants and needs (i.e. vary start date)
3. Create `.env` file (rename `.test.env` and configure variables, variables in current form will run successfully)
4. Docker build and run
```
docker-compose build
docker-compose up
```
5. Server live at: `0.0.0.0:5000` (docs found at `/docs`)


## Notes

- `Player ID` same as Jeff Sackman's `200000` column (see: https://github.com/JeffSackmann/tennis_wta/blob/master/wta_players.csv)
- `Tournament ID` same as Jeff Sackman's (see: `tourney_id` in any csv files)
- `Game ID` is equal to `tourney_id_match_num` (i.e. tourney_id: 2020-1049 and match_num: 300, Game ID: 2020-1049_300)

#### Todo
- DB schema file
- Additional routes (all games in a tournament, all games played by single player)
- Improve tests