.read create.sql
.read insert.sql
.mode table
.shell reset
.save soccer.db



❯ sqlite3
SQLite version 3.41.2 2023-03-22 11:56:21
Enter ".help" for usage hints.
Connected to a transient in-memory database.
Use ".open FILENAME" to reopen on a persistent database.
sqlite> .read create.sql
sqlite> .read insert.sql
sqlite> .mode table
sqlite> .shell reset

sqlite> SELECT * FROM People;
+----+----------------------+----------------------------------+-----+--------+
| id |         name         |              email               | age | gender |
+----+----------------------+----------------------------------+-----+--------+
| 1  | Takumi Sato          | takumi.sato@example.com          | 17  | Male   |
| 2  | Sakura Yamamoto      | sakura.yamamoto@example.com      | 18  | Female |
| 3  | Rajesh Patel         | rajesh.patel@example.com         | 16  | Male   |
| 4  | Komal Sharma         | komal.sharma@example.com         | 26  | Female |
| 5  | Jian Chen            | jian.chen@example.com            | 15  | Male   |
| 6  | Yan Liu              | yan.liu@example.com              | 17  | Female |
| 7  | Vladimir Ivanov      | vladimir.ivanov@example.com      | 15  | Male   |
| 8  | Ekaterina Kuznetsova | ekaterina.kuznetsova@example.com | 26  | Female |
| 9  | Yusuf Abdullah       | yusuf.abdullah@example.com       | 17  | Male   |
| 10 | Fatima Al-Khalifa    | fatima.alkhalifa@example.com     | 18  | Female |
| 11 | Andi Suharto         | andi.suharto@example.com         | 15  | Male   |
| 12 | Lia Wijaya           | lia.wijaya@example.com           | 16  | Female |
| 13 | Marco Rossi          | marco.rossi@example.com          | 17  | Male   |
| 14 | Alessia Bianchi      | alessia.bianchi@example.com      | 16  | Female |
| 15 | Gustav Andersen      | gustav.andersen@example.com      | 15  | Male   |
| 16 | Maria Svensson       | maria.svensson@example.com       | 18  | Female |
| 17 | Ahmad Rahman         | ahmad.rahman@example.com         | 17  | Male   |
| 18 | Nur Hidayah          | nur.hidayah@example.com          | 16  | Female |
| 19 | Joko Susilo          | joko.susilo@example.com          | 15  | Male   |
| 20 | Ratih Wijayanti      | ratih.wijayanti@example.com      | 17  | Female |
| 21 | Abdullah Al-Bakr     | abdullah.albakr@example.com      | 16  | Male   |
| 22 | Huda Al-Farsi        | huda.alfarsi@example.com         | 15  | Female |
| 23 | Tetsuya Suzuki       | tetsuya.suzuki@example.com       | 18  | Male   |
| 24 | Akira Kato           | akira.kato@example.com           | 16  | Male   |
| 25 | Ravi Singh           | ravi.singh@example.com           | 15  | Male   |
| 26 | Nikolai Ivanov       | nikolai.ivanov@example.com       | 15  | Male   |
| 27 | dr. Johnson Bun      | dr.johnson@example.com           | 50  | Male   |
| 28 | Wilson Weasley       | busdriver.wilson@example.com     | 37  | Male   |
| 29 | Smith Sonian         | coach.smith@example.com          | 40  | Male   |
| 30 | Kim Kwan             | physio.kim@example.com           | 35  | Male   |
+----+----------------------+----------------------------------+-----+--------+

sqlite> SELECT name, age, gender
FROM People
WHERE age > 20
ORDER by age;
+----------------------+-----+--------+
|         name         | age | gender |
+----------------------+-----+--------+
| Komal Sharma         | 26  | Female |
| Ekaterina Kuznetsova | 26  | Female |
| Kim Kwan             | 35  | Male   |
| Wilson Weasley       | 37  | Male   |
| Smith Sonian         | 40  | Male   |
| dr. Johnson Bun      | 50  | Male   |
+----------------------+-----+--------+

sqlite> SELECT * FROM Roles;
+----+---------+
| id |  name   |
+----+---------+
| 1  | Players |
| 2  | Coach   |
| 3  | Support |
+----+---------+

sqlite> SELECT * FROM Responsibilities;
+----+-----------------+
| id |      name       |
+----+-----------------+
| 1  | Head Coach      |
| 2  | Coach Assistant |
| 3  | Coach Trainee   |
| 11 | Doctor          |
| 12 | Physiotherapist |
| 21 | Bus Driver      |
| 22 | Cooking Chef    |
| 23 | Equipment       |
+----+-----------------+

sqlite> SELECT * FROM Seats;;
+----+------------+
| id |    name    |
+----+------------+
| 1  | Captain    |
| 2  | Goalkeeper |
| 3  | Back       |
| 4  | Striker    |
| 5  | Winger     |
| 6  | Midfielder |
| 7  | Defender   |
+----+------------+

sqlite> SELECT
    People.name, Roles.name as role 
  FROM People
  INNER JOIN PeopleRoles
    ON People.id = PeopleRoles.person_id
  INNER JOIN Roles
    ON PeopleRoles.role_id = Roles.id;
+----------------------+---------+
|         name         |  role   |
+----------------------+---------+
| Takumi Sato          | Players |
| Sakura Yamamoto      | Coach   |
| Komal Sharma         | Support |
| Jian Chen            | Players |
| Yan Liu              | Support |
| Vladimir Ivanov      | Players |
| Ekaterina Kuznetsova | Support |
| Yusuf Abdullah       | Players |
| Fatima Al-Khalifa    | Support |
| Andi Suharto         | Players |
| Lia Wijaya           | Coach   |
| Marco Rossi          | Players |
| Alessia Bianchi      | Support |
| Gustav Andersen      | Players |
| Maria Svensson       | Support |
| Ahmad Rahman         | Players |
| Nur Hidayah          | Players |
| Joko Susilo          | Players |
| Ratih Wijayanti      | Support |
| Abdullah Al-Bakr     | Support |
| Huda Al-Farsi        | Players |
| Tetsuya Suzuki       | Players |
| Akira Kato           | Players |
| Ravi Singh           | Players |
| Nikolai Ivanov       | Players |
| dr. Johnson Bun      | Support |
| Wilson Weasley       | Support |
| Smith Sonian         | Coach   |
| Kim Kwan             | Support |
+----------------------+---------+

sqlite> SELECT
    People.name,
    Roles.name as roles,
    Seats.name as seat
  FROM People
  INNER JOIN PlayersSeats
    ON People.id = PlayersSeats.person_id
  INNER JOIN Roles
    ON PlayersSeats.role_id = Roles.id
  INNER JOIN Seats
    ON PlayersSeats.seat_id = Seats.id;
+-----------------+---------+------------+
|      name       |  roles  |    seat    |
+-----------------+---------+------------+
| Takumi Sato     | Players | Captain    |
| Jian Chen       | Players | Striker    |
| Vladimir Ivanov | Players | Winger     |
| Yusuf Abdullah  | Players | Winger     |
| Andi Suharto    | Players | Midfielder |
| Marco Rossi     | Players | Midfielder |
| Gustav Andersen | Players | Defender   |
| Ahmad Rahman    | Players | Defender   |
| Nur Hidayah     | Players | Striker    |
| Joko Susilo     | Players | Goalkeeper |
| Huda Al-Farsi   | Players | Goalkeeper |
| Tetsuya Suzuki  | Players | Back       |
| Akira Kato      | Players | Back       |
| Ravi Singh      | Players | Striker    |
| Nikolai Ivanov  | Players | Winger     |
+-----------------+---------+------------+

sqlite> SELECT
    People.name,
    Roles.name as roles,
    Responsibilities.name as responsibility
  FROM People
  INNER JOIN StaffResps
    ON People.id = StaffResps.person_id
  INNER JOIN Roles
    ON StaffResps.role_id = Roles.id
  INNER JOIN Responsibilities
    ON StaffResps.resp_id = Responsibilities.id
  ORDER BY Roles.id;
+----------------------+---------+-----------------+
|         name         |  roles  | responsibility  |
+----------------------+---------+-----------------+
| Sakura Yamamoto      | Coach   | Coach Assistant |
| Lia Wijaya           | Coach   | Coach Trainee   |
| Smith Sonian         | Coach   | Head Coach      |
| Komal Sharma         | Support | Doctor          |
| Yan Liu              | Support | Equipment       |
| Ekaterina Kuznetsova | Support | Bus Driver      |
| Fatima Al-Khalifa    | Support | Cooking Chef    |
| Alessia Bianchi      | Support | Equipment       |
| Maria Svensson       | Support | Cooking Chef    |
| Ratih Wijayanti      | Support | Physiotherapist |
| Abdullah Al-Bakr     | Support | Cooking Chef    |
| dr. Johnson Bun      | Support | Doctor          |
| Wilson Weasley       | Support | Bus Driver      |
| Kim Kwan             | Support | Physiotherapist |
+----------------------+---------+-----------------+

sqlite> SELECT
    People.name,
    People.age,
    Seats.name as seat
  FROM People
  INNER JOIN PlayersSeats
    ON People.id = PlayersSeats.person_id
  INNER JOIN Seats
    ON PlayersSeats.seat_id = Seats.id
  ORDER BY People.name;
+-----------------+-----+------------+
|      name       | age |    seat    |
+-----------------+-----+------------+
| Ahmad Rahman    | 17  | Defender   |
| Akira Kato      | 16  | Back       |
| Andi Suharto    | 15  | Midfielder |
| Gustav Andersen | 15  | Defender   |
| Huda Al-Farsi   | 15  | Goalkeeper |
| Jian Chen       | 15  | Striker    |
| Joko Susilo     | 15  | Goalkeeper |
| Marco Rossi     | 17  | Midfielder |
| Nikolai Ivanov  | 15  | Winger     |
| Nur Hidayah     | 16  | Striker    |
| Ravi Singh      | 15  | Striker    |
| Takumi Sato     | 17  | Captain    |
| Tetsuya Suzuki  | 18  | Back       |
| Vladimir Ivanov | 15  | Winger     |
| Yusuf Abdullah  | 17  | Winger     |
+-----------------+-----+------------+

sqlite> SELECT
    age, COUNT(*)
  FROM People
  GROUP BY age;
+-----+----------+
| age | COUNT(*) |
+-----+----------+
| 15  | 8        |
| 16  | 6        |
| 17  | 6        |
| 18  | 4        |
| 26  | 2        |
| 35  | 1        |
| 37  | 1        |
| 40  | 1        |
| 50  | 1        |
+-----+----------+

sqlite> SELECT DISTINCT
    People.age, COUNT(*)
  FROM People
  INNER JOIN PeopleRoles
    ON People.id = PeopleRoles.person_id
  WHERE PeopleRoles.role_id = 1
  GROUP BY People.age;
+-----+----------+
| age | COUNT(*) |
+-----+----------+
| 15  | 8        |
| 16  | 2        |
| 17  | 4        |
| 18  | 1        |
+-----+----------+

sqlite> CREATE VIEW Players
AS
  SELECT
    People.*,
    Roles.name as roles,
    Seats.name as seat
  FROM People
  INNER JOIN PlayersSeats
    ON People.id = PlayersSeats.person_id
  INNER JOIN Roles
    ON PlayersSeats.role_id = Roles.id
  INNER JOIN Seats
    ON PlayersSeats.seat_id = Seats.id;

sqlite> SELECT
    name, age, gender, seat
  FROM Players;
+-----------------+-----+--------+------------+
|      name       | age | gender |    seat    |
+-----------------+-----+--------+------------+
| Takumi Sato     | 17  | Male   | Captain    |
| Jian Chen       | 15  | Male   | Striker    |
| Vladimir Ivanov | 15  | Male   | Winger     |
| Yusuf Abdullah  | 17  | Male   | Winger     |
| Andi Suharto    | 15  | Male   | Midfielder |
| Marco Rossi     | 17  | Male   | Midfielder |
| Gustav Andersen | 15  | Male   | Defender   |
| Ahmad Rahman    | 17  | Male   | Defender   |
| Nur Hidayah     | 16  | Male   | Striker    |
| Joko Susilo     | 15  | Male   | Goalkeeper |
| Huda Al-Farsi   | 15  | Male   | Goalkeeper |
| Tetsuya Suzuki  | 18  | Male   | Back       |
| Akira Kato      | 16  | Male   | Back       |
| Ravi Singh      | 15  | Male   | Striker    |
| Nikolai Ivanov  | 15  | Male   | Winger     |
+-----------------+-----+--------+------------+

sqlite> DROP VIEW Players;

sqlite> CREATE VIEW Players
AS
  SELECT
    People.*,
    Roles.name as roles,
    Seats.name as seat,
    PlayersSeats.is_bench
  FROM People
  INNER JOIN PlayersSeats
    ON People.id = PlayersSeats.person_id
  INNER JOIN Roles
    ON PlayersSeats.role_id = Roles.id
  INNER JOIN Seats
    ON PlayersSeats.seat_id = Seats.id;

sqlite> SELECT
    name, age, seat, 
    CASE
      WHEN is_bench = false then 'Playing'
      ELSE 'Bench Warmer'
    END AS status
  FROM Players;
+-----------------+-----+------------+--------------+
|      name       | age |    seat    |    status    |
+-----------------+-----+------------+--------------+
| Takumi Sato     | 17  | Captain    | Playing      |
| Jian Chen       | 15  | Striker    | Playing      |
| Vladimir Ivanov | 15  | Winger     | Playing      |
| Yusuf Abdullah  | 17  | Winger     | Playing      |
| Andi Suharto    | 15  | Midfielder | Playing      |
| Marco Rossi     | 17  | Midfielder | Playing      |
| Gustav Andersen | 15  | Defender   | Playing      |
| Ahmad Rahman    | 17  | Defender   | Playing      |
| Nur Hidayah     | 16  | Striker    | Playing      |
| Joko Susilo     | 15  | Goalkeeper | Playing      |
| Huda Al-Farsi   | 15  | Goalkeeper | Bench Warmer |
| Tetsuya Suzuki  | 18  | Back       | Bench Warmer |
| Akira Kato      | 16  | Back       | Playing      |
| Ravi Singh      | 15  | Striker    | Playing      |
| Nikolai Ivanov  | 15  | Winger     | Bench Warmer |
+-----------------+-----+------------+--------------+

sqlite> SELECT
    People.name, People.age,
    Roles.name as roles,
    Seats.name as 'job desc'
  FROM People
  INNER JOIN PlayersSeats
    ON People.id = PlayersSeats.person_id
  INNER JOIN Roles
    ON PlayersSeats.role_id = Roles.id
  INNER JOIN Seats
    ON PlayersSeats.seat_id = Seats.id
UNION
SELECT
    People.name, People.age,
    Roles.name as roles,
    Responsibilities.name as 'job desc'
  FROM People
  INNER JOIN StaffResps
    ON People.id = StaffResps.person_id
  INNER JOIN Roles
    ON StaffResps.role_id = Roles.id
  INNER JOIN Responsibilities
    ON StaffResps.resp_id = Responsibilities.id
ORDER BY People.name;
+----------------------+-----+---------+-----------------+
|         name         | age |  roles  |    job desc     |
+----------------------+-----+---------+-----------------+
| Abdullah Al-Bakr     | 16  | Support | Cooking Chef    |
| Ahmad Rahman         | 17  | Players | Defender        |
| Akira Kato           | 16  | Players | Back            |
| Alessia Bianchi      | 16  | Support | Equipment       |
| Andi Suharto         | 15  | Players | Midfielder      |
| Ekaterina Kuznetsova | 26  | Support | Bus Driver      |
| Fatima Al-Khalifa    | 18  | Support | Cooking Chef    |
| Gustav Andersen      | 15  | Players | Defender        |
| Huda Al-Farsi        | 15  | Players | Goalkeeper      |
| Jian Chen            | 15  | Players | Striker         |
| Joko Susilo          | 15  | Players | Goalkeeper      |
| Kim Kwan             | 35  | Support | Physiotherapist |
| Lia Wijaya           | 16  | Coach   | Coach Trainee   |
| Marco Rossi          | 17  | Players | Midfielder      |
| Maria Svensson       | 18  | Support | Cooking Chef    |
| Nikolai Ivanov       | 15  | Players | Winger          |
| Nur Hidayah          | 16  | Players | Striker         |
| Ratih Wijayanti      | 17  | Support | Physiotherapist |
| Ravi Singh           | 15  | Players | Striker         |
| Sakura Yamamoto      | 18  | Coach   | Coach Assistant |
| Smith Sonian         | 40  | Coach   | Head Coach      |
| Takumi Sato          | 17  | Players | Captain         |
| Tetsuya Suzuki       | 18  | Players | Back            |
| Vladimir Ivanov      | 15  | Players | Winger          |
| Wilson Weasley       | 37  | Support | Bus Driver      |
| Yan Liu              | 17  | Support | Equipment       |
| Yusuf Abdullah       | 17  | Players | Winger          |
| dr. Johnson Bun      | 50  | Support | Doctor          |
| dr. Komal Sharma     | 26  | Support | Doctor          |
+----------------------+-----+---------+-----------------+

sqlite> SELECT
    People.email,
    Responsibilities.name as responsibility
  FROM People
  INNER JOIN StaffResps
    ON People.id = StaffResps.person_id
  INNER JOIN Responsibilities
    ON StaffResps.resp_id = Responsibilities.id
  WHERE Responsibilities.name = 'Doctor';
+--------------------------+----------------+
|          email           | responsibility |
+--------------------------+----------------+
| komal.sharma@example.com | Doctor         |
| dr.johnson@example.com   | Doctor         |
+--------------------------+----------------+
