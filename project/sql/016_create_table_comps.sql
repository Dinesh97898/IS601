CREATE TABLE
    IF NOT EXISTS IS601_S_Comps(
        -- Remember to refer to your proposal for your exact columns
        id int AUTO_INCREMENT PRIMARY KEY,
        title varchar(240) not null,
        min_participants int DEFAULT 3,
        current_participants int default 0,
        join_cost int default 1,
        payout_options varchar(10),
        -- going to store the data as a csv list
        starting_reward int DEFAULT 1,
        current_reward int DEFAULT (starting_reward),
        did_calc TINYINT(1) DEFAULT 0,
        did_payout tinyint(1) DEFAULT 0,
        duration int default 3,
        creator_id int,
        min_score int DEFAULT 1,
        expires TIMESTAMP DEFAULT (
            DATE_ADD(
                CURRENT_TIMESTAMP,
                INTERVAL duration DAY
            )
        ),
        created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
        FOREIGN KEY(creator_id) REFERENCES IS601_Users(id),
        check (min_score >= 1),
        check (starting_reward >= 1),
        check (
            current_reward >= starting_reward
        ),
        check (min_participants >= 3),
        check (current_participants >= 0),
        check(join_cost >= 0)
    )