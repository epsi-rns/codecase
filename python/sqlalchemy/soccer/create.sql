-- Team Allstars table
CREATE TABLE People (
    id INT NOT NULL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL,
    age INT,
    gender VARCHAR(50)
);

-- Lookup table
CREATE TABLE Roles (
    id INT NOT NULL PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

-- Lookup table
CREATE TABLE Responsibilities (
    id INT NOT NULL PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

-- Lookup table
CREATE TABLE Seats (
    id INT NOT NULL PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

-- People_Role table
CREATE TABLE PeopleRoles (
    person_id INT NOT NULL,
    role_id INT NOT NULL,
    PRIMARY KEY (person_id, role_id),
    FOREIGN KEY (person_id) REFERENCES People(id),
    FOREIGN KEY (role_id) REFERENCES Roles(id)
);

-- People_Role_Seat table
CREATE TABLE PlayersSeats (
    person_id INT NOT NULL,
    role_id INT NOT NULL,
    seat_id INT NOT NULL,
    is_bench BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (person_id, role_id, seat_id),
    FOREIGN KEY (person_id) REFERENCES People(id),
    FOREIGN KEY (role_id) REFERENCES Roles(id),
    FOREIGN KEY (seat_id) REFERENCES Seats(id)
);

-- People_Role_Responsibility table
CREATE TABLE StaffResps (
    person_id INT NOT NULL,
    role_id INT NOT NULL,
    resp_id INT NOT NULL,
    PRIMARY KEY (person_id, role_id, resp_id),
    FOREIGN KEY (person_id) REFERENCES People(id),
    FOREIGN KEY (role_id) REFERENCES Roles(id),
    FOREIGN KEY (resp_id) REFERENCES Responsibilities(id)
);
