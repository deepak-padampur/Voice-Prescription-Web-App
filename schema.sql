create table users(
  id integer primary key autoincrement,
  email text not null,
  password text not null
);


create table doctor(
  id integer primary key autoincrement,
  email text not null,
  password text not null,
  expert boolean not null,
  speciality string,
  image string,
  admin boolean not  null
);


-- create table questions(
-- 	id integer primary key autoincrement,
-- 	question_text text not null,
-- 	answer_text text,
-- 	image string,
-- 	asked_by_id integer not null,
-- 	expert_id  integer not null
-- );
  


create table problem(
  id integer primary key autoincrement,
  email text not null,
  problem_specification string,
  problem_department string
  );
  


create table consult_doctor(
  id integer primary key autoincrement,
  doc_email text,
  user_email  text,
  problem_specification string,
  problem_department string
  );
  
  
