/*This is used when you want to drop all the data from the tables*/
USE biazza;
DELETE FROM attachment WHERE 1=1;
DELETE FROM comment WHERE 1=1;
DELETE FROM question WHERE 1=1;
DELETE FROM message WHERE 1=1;
DELETE FROM conversation WHERE 1=1;
DELETE FROM user_tokens WHERE 1=1;
DELETE FROM accounts WHERE 1=1;
