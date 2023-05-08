CREATE TABLE department (
id SERIAL PRIMARY KEY,
name varchar NOT NULL,
deanery varchar NOT NULL
);
 
CREATE TABLE student_group (
id SERIAL PRIMARY KEY,
name varchar NOT NULL,
department_id integer REFERENCES department(id)
);
 
CREATE TABLE student (
id SERIAL PRIMARY KEY,
full_name varchar NOT NULL,
passport varchar NOT NULL,
group_id integer REFERENCES student_group(id)
);
 
ALTER TABLE student_group ADD CONSTRAINT fk_department_id
FOREIGN KEY (department_id)
REFERENCES department(id);
 
ALTER TABLE student ADD CONSTRAINT fk_group_id
FOREIGN KEY (group_id)
REFERENCES student_group(id);
 
INSERT INTO department (name, deanery) VALUES ('Математики и информатики', 'Факультет математики и информатики');
INSERT INTO department (name, deanery) VALUES ('Физики', 'Факультет физики');
 
INSERT INTO student_group (name, department_id) VALUES ('БСТ-2205', 1);
INSERT INTO student_group (name, department_id) VALUES ('БСТ-2206', 1);
INSERT INTO student_group (name, department_id) VALUES ('БВТ-2207', 2);
INSERT INTO student_group (name, department_id) VALUES ('БВТ-2208', 2);
 
INSERT INTO student (full_name, passport, group_id) VALUES ('Мухин Игнатий Куприянович', '3452 346832', 1);
INSERT INTO student (full_name, passport, group_id) VALUES ('Афанасьев Альберт Валерьянович', '2356 352567', 1);
INSERT INTO student (full_name, passport, group_id) VALUES ('Фомичёв Аркадий Антонович', '5674 436732', 1);
INSERT INTO student (full_name, passport, group_id) VALUES ('Киселёв Ипполит Игнатьевич', '5325 352678', 1);
INSERT INTO student (full_name, passport, group_id) VALUES ('Фролов Роман Васильевич', '9754 463346', 1);
INSERT INTO student (full_name, passport, group_id) VALUES ('Новиков Иван Агафонович', '5784 453875', 2);
INSERT INTO student (full_name, passport, group_id) VALUES ('Козлов Исак Евгеньевич', '5327 273562', 2);
INSERT INTO student (full_name, passport, group_id) VALUES ('Носов Моисей Евгеньевич', '5239 385275', 2);
INSERT INTO student (full_name, passport, group_id) VALUES ('Гущин Герман Гордеевич', '2359 258275', 2);
INSERT INTO student (full_name, passport, group_id) VALUES ('Лыткин Вольдемар Геласьевич', '5326 235326', 2);
INSERT INTO student (full_name, passport, group_id) VALUES ('Мельников Ким Платонович', '3674 564346', 3);
INSERT INTO student (full_name, passport, group_id) VALUES ('Осипов Никифор Ефимович', '9657 475632', 3);
INSERT INTO student (full_name, passport, group_id) VALUES ('Козлов Модест Богданович', '5236 754353', 3);
INSERT INTO student (full_name, passport, group_id) VALUES ('Карпов Панкрат Платонович', '5236 657453', 3);
INSERT INTO student (full_name, passport, group_id) VALUES ('Осипов Мирон Федосеевич', '2367 463253', 3);
INSERT INTO student (full_name, passport, group_id) VALUES ('Туров Иннокентий Фролович', '2366 568907', 4);
INSERT INTO student (full_name, passport, group_id) VALUES ('Мухин Демьян Максович', '3526 632236', 4);
INSERT INTO student (full_name, passport, group_id) VALUES ('Комаров Антон Мэлорович', '3626 743453', 4);
INSERT INTO student (full_name, passport, group_id) VALUES ('Дьячков Леонтий Максимович', '5178 577232', 4);
INSERT INTO student (full_name, passport, group_id) VALUES ('Власов Юстиниан Семенович', '3252 523563', 4);