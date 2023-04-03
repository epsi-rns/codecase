SELECT User.*
  FROM User
  INNER JOIN User_Role_Permission ON User_Role_Permission.user_id = User.id
  INNER JOIN Role ON Role.id = User_Role_Permission.role_id
  WHERE Role.name = 'admin'
  GROUP BY User.id;


SELECT User.*
  FROM User
  INNER JOIN User_Role_Permission ON User_Role_Permission.user_id = User.id
  INNER JOIN Role_Permission ON Role_Permission.role_id = User_Role_Permission.role_id
  INNER JOIN Permission ON Permission.id = Role_Permission.permission_id
  WHERE Permission.name = 'create_post' OR Permission.name = 'edit_post' OR Permission.name = 'delete_post'
  GROUP BY User.id
  HAVING COUNT(DISTINCT Permission.id) = 3;


CREATE VIEW Admin
AS
  SELECT User.*
  FROM User
  INNER JOIN User_Role_Permission ON User_Role_Permission.user_id = User.id
  INNER JOIN Role ON Role.id = User_Role_Permission.role_id
  WHERE Role.name = 'admin'
  GROUP BY User.id;
