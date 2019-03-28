CREATE TABLE Guns (
gun INT UNSIGNED AUTO_INCREMENT,
wins INT UNSIGNED,
losses INT UNSIGNED,
shots_fired INT UNSIGNED,
PRIMARY KEY (gun)
);

CREATE TABLE Games (
id INT UNSIGNED AUTO_INCREMENT,
current_state INT UNSIGNED,
winner INT UNSIGNED,
game_date TIMESTAMP,
PRIMARY KEY (id),
FOREIGN KEY (winner) REFERENCES Guns(gun)
);

CREATE TABLE Game_Users (
game_id INT UNSIGNED,
gun_id INT UNSIGNED,
PRIMARY KEY (game_id, gun_id),
FOREIGN KEY (game_id) REFERENCES Games(id),
FOREIGN KEY (gun_id) REFERENCES Guns(gun)
);