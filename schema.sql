CREATE DATABASE recipedb;
USE recipedb;


CREATE TABLE Users 
( firstname VARCHAR(11) NOT NULL,
  lastname VARCHAR(11) NOT NULL,
  dateofbirth DATE NOT NULL,
  email varchar(255) UNIQUE NOT NULL,
  password varchar(255) NOT NULL,
  city varchar(255) NOT NULL, 
  state varchar(255) NOT NULL,
  user_id int4  AUTO_INCREMENT,
  CONSTRAINT users_pk PRIMARY KEY (user_id)
);

CREATE TABLE Follows
(
  user_id1 INT4 NOT NULL, 
  user_id2 INT4 NOT NULL,
  CONSTRAINT friends_pk PRIMARY KEY (user_id1, user_id2),
  CONSTRAINT friends_fk1 FOREIGN KEY (user_id1) REFERENCES Users(user_id) ON DELETE CASCADE,
  CONSTRAINT friends_fk2 FOREIGN KEY (user_id2) REFERENCES Users(user_id) ON DELETE CASCADE
);


CREATE TABLE Recipe
(
  recipe_id int4  AUTO_INCREMENT,
  user_id int4,
  imgdata LONGBLOB,
  name VARCHAR(255),
  description VARCHAR(255),
  CONSTRAINT recipe_pk PRIMARY KEY (recipe_id),
  CONSTRAINT recipe_fk1 FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
  
);

CREATE TABLE Ingredient
( ingredient_id int4 AUTO_INCREMENT,
  recipe_id int4 NOT NULL,
  text VARCHAR(30) NOT NULL,
  CONSTRAINT ingredient_pk PRIMARY KEY (ingredient_id),
  CONSTRAINT ingredient_fk FOREIGN KEY (recipe_id) REFERENCES Recipe (recipe_id) ON DELETE CASCADE
);

CREATE TABLE Comments
(
comment_id int4  AUTO_INCREMENT,
text VARCHAR(150) NOT NULL,
user_id INT NOT NULL,
recipe_id INT NOT NULL,
CONSTRAINT comments_pk PRIMARY KEY (comment_id),
CONSTRAINT comments_fk1 FOREIGN KEY (recipe_id) REFERENCES Recipe (recipe_id) ON DELETE CASCADE,
CONSTRAINT comments_fk2 FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);
