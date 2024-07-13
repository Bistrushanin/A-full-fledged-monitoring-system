CREATE TABLE IF NOT EXISTS smartphones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    brand VARCHAR(255) NOT NULL,
    model VARCHAR(255) NOT NULL,
    storage_capacity INT,
    ram_capacity INT,
    battery_capacity INT
);

INSERT INTO smartphones (brand, model, storage_capacity, ram_capacity, battery_capacity) VALUES
('Apple', 'iPhone 13', 128, 4, 3095),
('Samsung', 'Galaxy S21', 256, 8, 4000),
('Google', 'Pixel 6', 128, 6, 4614),
('OnePlus', '9 Pro', 256, 12, 4500),
('Xiaomi', 'Mi 11', 256, 8, 4600);
