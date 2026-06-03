CREATE TABLE users(
    user_id int AUTO_INCREMENT PRIMARY KEY,
    user_name varchar(100) not null,
    user_email varchar(100)
);

CREATE TABLE categories(
    category_id int AUTO_INCREMENT PRIMARY KEY,
    category_name varchar(100) not null
);

CREATE TABLE subscriptions(
    subscription_id int AUTO_INCREMENT PRIMARY KEY,
    user_id int ,
    category_id int,
    service_name varchar(100) not null,
    plan_name varchar(100) not null,
    status varchar(100),--有付、沒付、已停止
    start_date date,
    foreign key (user_id) references users(user_id),
    foreign key (category_id) references categories(category_id),
);

CREATE TABLE payments(
    payment_id int AUTO_INCREMENT PRIMARY KEY,
    subscription_id int,
    price int not null,
    billing_cycle int ,
    payment_day int not null,
    foreign key (subscription_id) references subscriptions(subscription_id)

);
