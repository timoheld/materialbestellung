create table if not exists tblUsers(
    id_users int auto_increment,
    scoutname varchar(50),
    surname varchar(50),
    lastname varchar(50),
    password char(60),
    role int,
    primary key(id_users),
    foreign key(role)
        references tblUserRoles(id_userRoles)
);