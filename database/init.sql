CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    user_name VARCHAR(100) NOT NULL,
    user_email VARCHAR(100) NOT NULL UNIQUE,
    user_password VARCHAR(255) NOT NULL
);

CREATE TABLE categories (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL
);

CREATE TABLE subscriptions (
    subscription_id SERIAL PRIMARY KEY,
    user_id INT,
    category_id INT,
    service_name VARCHAR(100) NOT NULL,
    plan_name VARCHAR(100) ,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
);

CREATE TABLE payments (
    payment_id SERIAL PRIMARY KEY,
    subscription_id INT,
    price INT NOT NULL,
    billing_cycle INT,
    payment_day date ,
    FOREIGN KEY (subscription_id) REFERENCES subscriptions(subscription_id)
);