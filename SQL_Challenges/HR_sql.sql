-- Refresh tables by using drop tables

drop table Department cascade;
drop table Salaries cascade;
drop table Titles cascade;
drop table dept_manager cascade;
drop table dept_emp cascade;
drop table Employees cascade;

-- Create tables & relationship between tables

CREATE TABLE Department (
    dept_no varchar,
    dept_name varchar,
    PRIMARY KEY (dept_no)
);

CREATE TABLE Employees (
    emp_no int   NOT NULL,
    emp_title varchar,
    birth_date date,
    first_name varchar,
    last_name varchar,
    sex varchar,
    hire_date date,
    PRIMARY KEY (emp_no)
);

CREATE TABLE Salaries (
    emp_no int   NOT NULL,
    salary int   NOT NULL,
    Primary key(emp_no),
	foreign key (emp_no) references Employees (emp_no)
);

CREATE TABLE Titles (
    title_id varchar,
    title varchar,
    PRIMARY KEY (title_id)
);

CREATE TABLE dept_manager (
    dept_no varchar,
	emp_no int   NOT NULL,
    primary key (emp_no,dept_no),
	foreign key (dept_no) references Department (dept_no),
	foreign key (emp_no) references Employees (emp_no)
);

CREATE TABLE dept_emp (
    emp_no int   NOT NULL,
    dept_no varchar,
    primary key (emp_no,dept_no),
	foreign key (dept_no) references Department (dept_no),
	foreign key (emp_no) references Employees (emp_no)
);

-- create table by filtering specific columns among tables

--List the following details of each employee: employee number, last name, first name, sex, and salary.
select e.emp_no, e.last_name, e.first_name, e.sex, s.salary
from Employees e
left join Salaries s
on e.emp_no = s.emp_no
order by e.last_name, e.first_name;

--List first name, last name, and hire date for employees who were hired in 1986.
select e.emp_no, e.last_name, e.first_name, e.hire_date
from Employees e
where (select date_part('year', (select e.hire_date))) = '1986'
order by e.hire_date, e.last_name, e.first_name;

--List the manager of each department with the following information: 
--department number, department name, the manager's employee number, last name, first name.
select m.emp_no, e.last_name, e.first_name, d.dept_name
from dept_manager m
left join Employees e
on m.emp_no = e.emp_no
left join Department d
on m.dept_no = d.dept_no
order by e.last_name, e.first_name;

--List the department of each employee with the following information: 
-- employee number, last name, first name, and department name.
select e.emp_no, e.last_name, e.first_name, d.dept_name
from employees e
right join dept_emp ed
on e.emp_no = ed.emp_no
left join Department d
on ed.dept_no = d.dept_no
order by e.emp_no, d.dept_name;

--List first name, last name, and sex for employees whose first name is "Hercules" and last names begin with "B."
select e.emp_no, e.last_name, e.first_name, e.sex
from Employees e
where e.first_name ='Hercules' and e.last_name like 'B%'
order by e.last_name, e.emp_no;

--List all employees in the Sales department, including their employee number, last name, first name, and department name.
select ed.emp_no, e.last_name, e.first_name, d.dept_name
from dept_emp ed
left join Employees e
on ed.emp_no = e.emp_no
left join Department d
on ed.dept_no = d.dept_no
where d.dept_name = 'Sales'
order by e.last_name, e.first_name, e.emp_no;

--List all employees in the Sales AND Development departments, 
-- including their employee number, last name, first name, and department name.
select ed.emp_no, e.last_name, e.first_name, d.dept_name
from dept_emp ed
left join Employees e
on ed.emp_no = e.emp_no
left join Department d
on ed.dept_no = d.dept_no
where d.dept_name = 'Sales'

	and ed.emp_no in 
	(
	select ed.emp_no
	from dept_emp ed
	left join Employees e
	on ed.emp_no = e.emp_no
	left join Department d
	on ed.dept_no = d.dept_no
	where d.dept_name = 'Development'
	)
order by e.last_name, e.first_name, e.emp_no
;

--List all employees in the Sales OR Development departments, 
-- including their employee number, last name, first name, and department name.
select  d.dept_name, ed.emp_no, e.last_name, e.first_name
from dept_emp ed
left join Employees e
on ed.emp_no = e.emp_no
left join Department d
on ed.dept_no = d.dept_no
where d.dept_name = 'Sales' OR d.dept_name = 'Development'
order by d.dept_name, e.last_name, e.first_name, e.emp_no;


-- In descending order, list the frequency count of employee last names, i.e., how many employees share each last name.
select e.last_name, count(e.last_name) 
from employees e
group by e.last_name 
order by e.last_name desc;


-- create the dataset file combined all columns in data tables above.
-- This file is used to build graphs in jupyter notebook

drop table dataset_HR;

create table dataset_HR (
	emp_no int,
	first_name varchar not null,
	last_name varchar not null,
	birth_date date,
	sex varchar,
	hire_date date,
	dept_no varchar,
	dept_name varchar,
	emp_title varchar,
	title_name varchar,
	salary int
);

select * from dataset_HR

insert into dataset_HR (emp_no, first_name, last_name, birth_date, sex, hire_date, 
						dept_no, dept_name, emp_title, title_name, salary)
	select ed.emp_no, e.first_name, e.last_name, e.birth_date, e.sex, 
		e.hire_date, d.dept_no, d.dept_name, e.emp_title, t.title, s.salary
	from dept_emp ed
	left join Employees e
	on ed.emp_no = e.emp_no
	left join Department d
	on ed.dept_no = d.dept_no
	left join Salaries s
	on e.emp_no = s.emp_no
	left join Titles t
	on e.emp_title = t.title_id;
	

