create table ad
(
    id           serial        not null
        constraint ad_pk
            primary key,
    name         varchar(200)  not null,
    photo1       varchar       not null,
    photo2       varchar       not null,
    photo3       varchar       not null,
    price        integer       not null,
    description  varchar(1000) not null,
    created_date date default CURRENT_DATE
);
