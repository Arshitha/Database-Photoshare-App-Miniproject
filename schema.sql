CREATE DATABASE photoshare;
USE photoshare;
-- DROP TABLE Pictures CASCADE;
-- DROP TABLE Users CASCADE;

CREATE TABLE Users (
    user_id INT4  AUTO_INCREMENT,
    email VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    sexes ENUM('F','M', ''), -- how to encode according to ISO 5218 
    -- standard ?
    DoB DATE,
    Bio TEXT,
    Hometown VARCHAR(255),
    Profile_Pic longblob,
    password varchar(255),
    CONSTRAINT users_pk PRIMARY KEY (user_id)
);

CREATE TABLE friends(
  user_id INT4,
  friend_id INT4,
  CONSTRAINT friends_fk FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE TABLE albums(
  album_id INT4 AUTO_INCREMENT NOT NULL,
  user_id INT4,
  album_title VARCHAR(255) NOT NULL,
  creation_date DATE NOT NULL,
  CONSTRAINT albums_pk PRIMARY KEY (album_id),
  CONSTRAINT album_fk FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE TABLE Pictures(
  picture_id INT4 AUTO_INCREMENT,
  user_id INT4,
  imgdata longblob,
  caption VARCHAR(255),
  album_id INT4,
  INDEX upid_idx (user_id),
  CONSTRAINT pictures_pk PRIMARY KEY (picture_id),
  CONSTRAINT pictures_fk FOREIGN KEY (album_id) REFERENCES albums(album_id)
);

CREATE TABLE tags(
  word CHAR(25),
  picture_id INT4,
  CONSTRAINT tags_fk FOREIGN KEY (picture_id) REFERENCES Pictures(picture_id)
);

CREATE TABLE comments(
  comment_id INT4 NOT NULL,
  user_id INT4 NOT NULL,
  comment TEXT,
  commented_date DATE NOT NULL,
  CONSTRAINT comments_fk FOREIGN KEY (user_id) REFERENCES Users(user_id)  
);

CREATE TABLE profile_pic(
  user_id INT4 NOT NULL,
  profile_pic_id INT4 AUTO_INCREMENT NOT NULL,
  profile_pic longblob, 
  CONSTRAINT profile_pic_pk PRIMARY KEY (profile_pic_id),
  CONSTRAINT profile_pic_fk FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

INSERT INTO Users (email, password, first_name, last_name, DoB) VALUES ('test@bu.edu', 'test', 'test', 'testsons', '1994-09-09');
INSERT INTO profile_pic (user_id, profile_pic) VALUES (1, LOAD_FILE('/Users/arshitha/Desktop/OneDesk/Boston University/Sem 3/Intro to DBS/progAssign1/Photoshare_Skeleton_Einstein/female_default.jpg'));

INSERT INTO Users (email, password, first_name, last_name, DoB) VALUES ('test1@bu.edu', 'test', 'test', 'testsonian', '2008-08-05');
INSERT INTO profile_pic (user_id, profile_pic) VALUES (2, LOAD_FILE('/Users/arshitha/Desktop/OneDesk/Boston University/Sem 3/Intro to DBS/progAssign1/Photoshare_Skeleton_Einstein/female_default.jpg'));

INSERT INTO Users (email, password, first_name, last_name, DoB) VALUES ('tanush@gmail.com', 'test','Tanush', 'S', '2006-08-30');
INSERT INTO profile_pic (user_id, profile_pic) VALUES (3, LOAD_FILE('/Users/arshitha/Desktop/OneDesk/Boston University/Sem 3/Intro to DBS/progAssign1/Photoshare_Skeleton_Einstein/female_default.jpg'));

INSERT INTO Users (email, password, first_name, last_name, DoB) VALUES ('arshy@gmail.com', 'test','Arshitha', 'Basavaraj','1994-09-27');
INSERT INTO profile_pic (user_id, profile_pic) VALUES (4, LOAD_FILE('/Users/arshitha/Desktop/OneDesk/Boston University/Sem 3/Intro to DBS/progAssign1/Photoshare_Skeleton_Einstein/female_default.jpg'));

INSERT INTO Users (email, password, first_name, last_name, DoB) VALUES ('ashish@gmail.com', 'test', 'Ashish', 'Srihari', '1998-04-20');
INSERT INTO profile_pic (user_id, profile_pic) VALUES (5, LOAD_FILE('/Users/arshitha/Desktop/OneDesk/Boston University/Sem 3/Intro to DBS/progAssign1/Photoshare_Skeleton_Einstein/female_default.jpg'));

INSERT INTO Users (email, password, first_name, last_name, DoB) VALUES ('shruthi@gmail.com', 'test','Shurthi','Siva', '1995-04-30');
INSERT INTO profile_pic (user_id, profile_pic) VALUES (6, LOAD_FILE('/Users/arshitha/Desktop/OneDesk/Boston University/Sem 3/Intro to DBS/progAssign1/Photoshare_Skeleton_Einstein/female_default.jpg'));

INSERT INTO Users (email, password, first_name, last_name, DoB) VALUES ('anna@gmail.com', 'test','Annapoorna', 'Shruthi', '1994-04-01');
INSERT INTO profile_pic (user_id, profile_pic) VALUES (7, LOAD_FILE('/Users/arshitha/Desktop/OneDesk/Boston University/Sem 3/Intro to DBS/progAssign1/Photoshare_Skeleton_Einstein/female_default.jpg'));

INSERT INTO Users (email, password, first_name, last_name, DoB) VALUES ('vidya@gmail.com', 'test', 'Vidya', 'R', '1994-06-21');
INSERT INTO profile_pic (user_id, profile_pic) VALUES (8, LOAD_FILE('/Users/arshitha/Desktop/OneDesk/Boston University/Sem 3/Intro to DBS/progAssign1/Photoshare_Skeleton_Einstein/female_default.jpg'));

INSERT INTO Users (email, password, first_name, last_name, DoB) VALUES ('rahul@gmail.com', 'test','Rahul', 'Madbhavi','1994-08-27');
INSERT INTO profile_pic (user_id, profile_pic) VALUES (9, LOAD_FILE('/Users/arshitha/Desktop/OneDesk/Boston University/Sem 3/Intro to DBS/progAssign1/Photoshare_Skeleton_Einstein/female_default.jpg'));
