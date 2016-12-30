drop table if exists emails;
create table emails (
  id integer primary key autoincrement,
  email text not null UNIQUE,
  emailed integer not null
);

create table visited(
	id integer primary key autoincrement,
	link text not null UNIQUE
);
