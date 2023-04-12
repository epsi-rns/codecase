-- Team Allstars table
INSERT INTO People (id, name, email, age, gender)
VALUES 
    (1, 'Takumi Sato', 'takumi.sato@example.com', 17, 'Male'),
    (2, 'Sakura Yamamoto', 'sakura.yamamoto@example.com', 18, 'Female'),
    (3, 'Rajesh Patel', 'rajesh.patel@example.com', 16, 'Male'),
    (4, 'dr. Komal Sharma', 'komal.sharma@example.com', 26, 'Female'),
    (5, 'Jian Chen', 'jian.chen@example.com', 15, 'Male'),
    (6, 'Yan Liu', 'yan.liu@example.com', 17, 'Female'),
    (7, 'Vladimir Ivanov', 'vladimir.ivanov@example.com', 15, 'Male'),
    (8, 'Ekaterina Petrova', 'ekaterina.petrova@example.com', 26, 'Female'),
    (9, 'Yusuf Abdullah', 'yusuf.abdullah@example.com', 17, 'Male'),
    (10, 'Fatima Al-Khalifa', 'fatima.alkhalifa@example.com', 18, 'Female'),
    (11, 'Andi Suharto', 'andi.suharto@example.com', 15, 'Male'),
    (12, 'Lia Wijaya', 'lia.wijaya@example.com', 16, 'Female'),
    (13, 'Marco Rossi', 'marco.rossi@example.com', 17, 'Male'),
    (14, 'Alessia Bianchi', 'alessia.bianchi@example.com', 16, 'Female'),
    (15, 'Gustav Andersen', 'gustav.andersen@example.com', 15, 'Male'),
    (16, 'Maria Svensson', 'maria.svensson@example.com', 18, 'Female'),
    (17, 'Ahmad Rahman', 'ahmad.rahman@example.com', 17, 'Male'),
    (18, 'Nur Hidayah', 'nur.hidayah@example.com', 16, 'Male'),
    (19, 'Joko Susilo', 'joko.susilo@example.com', 15, 'Male'),
    (20, 'Ratih Wijayanti', 'ratih.wijayanti@example.com', 17, 'Female'),
    (21, 'Abdullah Al-Bakr', 'abdullah.albakr@example.com', 16, 'Male'),
    (22, 'Huda Al-Farsi', 'huda.alfarsi@example.com', 15, 'Male'),
    (23, 'Tetsuya Suzuki', 'tetsuya.suzuki@example.com', 18, 'Male'),
    (24, 'Akira Kato', 'akira.kato@example.com', 16, 'Male'),
    (25, 'Ravi Singh', 'ravi.singh@example.com', 15, 'Male'),
    (26, 'Nikolai Ivanov', 'nikolai.ivanov@example.com', 15, 'Male'),
    (27, 'dr. Johnson Bun', 'dr.johnson@example.com', 50, 'Male'),
    (28, 'Wilson Weasley', 'busdriver.wilson@example.com', 37, 'Male'),
    (29, 'Smith Sonian', 'coach.smith@example.com', 40, 'Male'),
    (30, 'Kim Kwan', 'physio.kim@example.com', 35, 'Male')
;

-- Lookup table
INSERT INTO Roles (id, name)
VALUES
    (1, 'Players'),
    (2, 'Coach'),
    (3, 'Support')
;

-- Lookup table
INSERT INTO Seats (id, name)
VALUES 
    (1, 'Captain'),
    (2, 'Goalkeeper'),
    (3, 'Back'),
    (4, 'Striker'),
    (5, 'Winger'),
    (6, 'Midfielder'),
    (7, 'Defender')
;

-- Lookup table
INSERT INTO Responsibilities (id, name)
VALUES 
    (1, 'Head Coach'),
    (2, 'Coach Assistant'),
    (3, 'Coach Trainee'),
    (11, 'Doctor'),
    (12, 'Physiotherapist'),
    (21, 'Bus Driver'),
    (22, 'Cooking Chef'),
    (23, 'Equipment')
;

-- People_Role table
INSERT INTO PeopleRoles (person_id, role_id)
VALUES
    (1, 1),
    (2, 2),
    (4, 3),
    (5, 1),
    (6, 3),
    (7, 1),
    (8, 3),
    (9, 1),
    (10, 3),
    (11, 1),
    (12, 2),
    (13, 1),
    (14, 3),
    (15, 1),
    (16, 3),
    (17, 1),
    (18, 1),
    (19, 1),
    (20, 3),
    (21, 3),
    (22, 1),
    (23, 1),
    (24, 1),
    (25, 1),
    (26, 1),
    (27, 3),
    (28, 3),
    (29, 2),
    (30, 3)
;

-- People_Role_Seat table
INSERT INTO PlayersSeats (person_id, role_id, seat_id, is_bench)
VALUES
    (1, 1, 1, false),
    (5, 1, 4, false),
    (7, 1, 5, false),
    (9, 1, 5, false),
    (11, 1, 6, false),
    (13, 1, 6, false),
    (15, 1, 7, false),
    (17, 1, 7, false),
    (18, 1, 4, false),
    (19, 1, 2, false),
    (22, 1, 2, true),
    (23, 1, 3, true),
    (24, 1, 3, false),
    (25, 1, 4, false),
    (26, 1, 5, true)
;

-- People_Role_Responsibility table
INSERT INTO StaffResps (person_id, role_id, resp_id)
VALUES
    (2, 2, 2),
    (4, 3, 11),
    (6, 3, 23),
    (8, 3, 21),
    (10, 3, 22),
    (12, 2, 3),
    (14, 3, 23),
    (16, 3, 22),
    (20, 3, 12),
    (21, 3, 22),
    (27, 3, 11),
    (28, 3, 21),
    (29, 2, 1),
    (30, 3, 12)
;

