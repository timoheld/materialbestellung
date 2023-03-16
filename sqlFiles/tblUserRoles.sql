create table if not exists tblUserRoles(
    id_userRoles int auto_increment,
    name varchar(50),
    description varchar(250),
    permissions int,
    primary key(id_userRoles),
    foreign key(permissions)
        references tblPermissions(id_permissions)
); 