drop table if exists emails;
create table emails (
  id integer primary key autoincrement,
  email text,
  emailed integer
);

create table visited(
	id integer primary key autoincrement,
	link text
);
