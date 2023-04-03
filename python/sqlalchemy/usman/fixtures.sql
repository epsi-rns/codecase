-- User table
CREATE TABLE User (
    id INT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL
);

INSERT INTO User (id, username, password, email)
VALUES
    (1, 'alice', '[hashed password]', 'alice@example.com'),
    (2, 'bob', '[hashed password]', 'bob@example.com'),
    (3, 'charlie', '[hashed password]', 'charlie@example.com');

-- Role table
CREATE TABLE Role (
    id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

INSERT INTO Role (id, name)
VALUES
    (1, 'admin'),
    (2, 'user');

-- Permission table
CREATE TABLE Permission (
    id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

INSERT INTO Permission (id, name)
VALUES
    (1, 'create_post'),
    (2, 'edit_post'),
    (3, 'delete_post'),
    (4, 'create_comment'),
    (5, 'delete_comment');

-- User_Role_Permission table
CREATE TABLE User_Role_Permission (
    user_id INT,
    role_id INT,
    permission_id INT,
    PRIMARY KEY (user_id, role_id, permission_id),
    FOREIGN KEY (user_id) REFERENCES User(id),
    FOREIGN KEY (role_id) REFERENCES Role(id),
    FOREIGN KEY (permission_id) REFERENCES Permission(id)
);

INSERT INTO User_Role_Permission (user_id, role_id, permission_id)
VALUES
    (1, 1, 1),
    (1, 1, 2),
    (1, 1, 3),
    (1, 2, 4),
    (2, 2, 1),
    (2, 2, 4),
    (3, 2, 4),
    (3, 2, 5);

-- Role_Permission table
CREATE TABLE Role_Permission (
    role_id INT,
    permission_id INT,
    PRIMARY KEY (role_id, permission_id),
    FOREIGN KEY (role_id) REFERENCES Role(id),
    FOREIGN KEY (permission_id) REFERENCES Permission(id)
);

INSERT INTO Role_Permission (role_id, permission_id)
VALUES
    (1, 1),
    (1, 2),
    (1, 3),
    (2, 1),
    (2, 4),
    (2, 5);

-- Add indexes to the User table
CREATE INDEX idx_user_username ON User (username);
CREATE INDEX idx_user_email ON User (email);

-- Add indexes to the Role table
CREATE INDEX idx_role_name ON Role (name);

-- Add indexes to the Permission table
CREATE INDEX idx_permission_name ON Permission (name);

-- Add indexes to the User_Role_Permission table
CREATE INDEX idx_urp_user_id ON User_Role_Permission (user_id);
CREATE INDEX idx_urp_role_id ON User_Role_Permission (role_id);
CREATE INDEX idx_urp_permission_id ON User_Role_Permission (permission_id);

-- Add indexes to the Role_Permission table
CREATE INDEX idx_rp_role_id ON Role_Permission (role_id);
CREATE INDEX idx_rp_permission_id ON Role_Permission (permission_id);
