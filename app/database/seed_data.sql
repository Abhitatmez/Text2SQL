-- Text2SQL Assistant E-commerce Database Seed Data
-- Sample data for testing complex queries with joins, filtering, and aggregation

-- Insert Customers (25 customers)
INSERT INTO customers (first_name, last_name, email, phone, city, state, country, registration_date, is_active) VALUES
('Rajesh', 'Kumar', 'rajesh.kumar@email.com', '+91-9876543210', 'Mumbai', 'Maharashtra', 'India', '2023-01-15', 1),
('Priya', 'Sharma', 'priya.sharma@email.com', '+91-9876543211', 'Delhi', 'Delhi', 'India', '2023-01-20', 1),
('Amit', 'Singh', 'amit.singh@email.com', '+91-9876543212', 'Bangalore', 'Karnataka', 'India', '2023-02-10', 1),
('Sneha', 'Patel', 'sneha.patel@email.com', '+91-9876543213', 'Ahmedabad', 'Gujarat', 'India', '2023-02-15', 1),
('Vikram', 'Gupta', 'vikram.gupta@email.com', '+91-9876543214', 'Pune', 'Maharashtra', 'India', '2023-03-01', 1),
('Anita', 'Rao', 'anita.rao@email.com', '+91-9876543215', 'Chennai', 'Tamil Nadu', 'India', '2023-03-05', 1),
('Rohit', 'Jain', 'rohit.jain@email.com', '+91-9876543216', 'Hyderabad', 'Telangana', 'India', '2023-03-20', 1),
('Kavya', 'Reddy', 'kavya.reddy@email.com', '+91-9876543217', 'Bangalore', 'Karnataka', 'India', '2023-04-01', 1),
('Suresh', 'Mishra', 'suresh.mishra@email.com', '+91-9876543218', 'Lucknow', 'Uttar Pradesh', 'India', '2023-04-10', 1),
('Deepika', 'Agarwal', 'deepika.agarwal@email.com', '+91-9876543219', 'Jaipur', 'Rajasthan', 'India', '2023-04-15', 1),
('Arjun', 'Nair', 'arjun.nair@email.com', '+91-9876543220', 'Kochi', 'Kerala', 'India', '2023-05-01', 1),
('Pooja', 'Sinha', 'pooja.sinha@email.com', '+91-9876543221', 'Kolkata', 'West Bengal', 'India', '2023-05-10', 1),
('Ravi', 'Iyer', 'ravi.iyer@email.com', '+91-9876543222', 'Chennai', 'Tamil Nadu', 'India', '2023-05-15', 1),
('Megha', 'Chopra', 'megha.chopra@email.com', '+91-9876543223', 'Mumbai', 'Maharashtra', 'India', '2023-06-01', 1),
('Karan', 'Malhotra', 'karan.malhotra@email.com', '+91-9876543224', 'Delhi', 'Delhi', 'India', '2023-06-10', 1),
('Sonal', 'Bhatt', 'sonal.bhatt@email.com', '+91-9876543225', 'Surat', 'Gujarat', 'India', '2023-06-15', 1),
('Manish', 'Verma', 'manish.verma@email.com', '+91-9876543226', 'Indore', 'Madhya Pradesh', 'India', '2023-07-01', 1),
('Richa', 'Saxena', 'richa.saxena@email.com', '+91-9876543227', 'Kanpur', 'Uttar Pradesh', 'India', '2023-07-10', 1),
('Nitin', 'Pandey', 'nitin.pandey@email.com', '+91-9876543228', 'Bhopal', 'Madhya Pradesh', 'India', '2023-07-20', 1),
('Shreya', 'Kulkarni', 'shreya.kulkarni@email.com', '+91-9876543229', 'Pune', 'Maharashtra', 'India', '2023-08-01', 1),
('Varun', 'Tiwari', 'varun.tiwari@email.com', '+91-9876543230', 'Varanasi', 'Uttar Pradesh', 'India', '2023-08-10', 1),
('Neha', 'Bansal', 'neha.bansal@email.com', '+91-9876543231', 'Gurgaon', 'Haryana', 'India', '2023-08-15', 1),
('Ajay', 'Mehta', 'ajay.mehta@email.com', '+91-9876543232', 'Rajkot', 'Gujarat', 'India', '2023-09-01', 1),
('Simran', 'Kaur', 'simran.kaur@email.com', '+91-9876543233', 'Chandigarh', 'Punjab', 'India', '2023-09-10', 1),
('Gaurav', 'Shah', 'gaurav.shah@email.com', '+91-9876543234', 'Nashik', 'Maharashtra', 'India', '2023-09-15', 1);

-- Insert Products (30 products across different categories)
INSERT INTO products (product_name, category, subcategory, brand, price_inr, cost_price_inr, stock_quantity, rating, description, created_date, is_active) VALUES
('iPhone 15 Pro', 'Electronics', 'Smartphones', 'Apple', 134900.00, 110000.00, 50, 4.8, 'Latest iPhone with A17 Pro chip', '2023-01-01', 1),
('Samsung Galaxy S24', 'Electronics', 'Smartphones', 'Samsung', 79999.00, 65000.00, 75, 4.6, 'Flagship Android smartphone', '2023-01-01', 1),
('MacBook Air M2', 'Electronics', 'Laptops', 'Apple', 114900.00, 95000.00, 30, 4.9, '13-inch laptop with M2 chip', '2023-01-01', 1),
('Dell XPS 13', 'Electronics', 'Laptops', 'Dell', 89990.00, 75000.00, 25, 4.5, 'Ultra-thin business laptop', '2023-01-01', 1),
('Sony WH-1000XM5', 'Electronics', 'Audio', 'Sony', 29990.00, 22000.00, 100, 4.7, 'Noise-canceling headphones', '2023-01-01', 1),
('AirPods Pro 2nd Gen', 'Electronics', 'Audio', 'Apple', 24900.00, 18000.00, 150, 4.6, 'Wireless earbuds with ANC', '2023-01-01', 1),
('Levis 501 Jeans', 'Clothing', 'Jeans', 'Levis', 3999.00, 2500.00, 200, 4.4, 'Classic straight-fit jeans', '2023-01-01', 1),
('Nike Air Force 1', 'Clothing', 'Shoes', 'Nike', 7999.00, 5500.00, 80, 4.5, 'Classic white sneakers', '2023-01-01', 1),
('Adidas Ultraboost 22', 'Clothing', 'Shoes', 'Adidas', 15999.00, 11000.00, 60, 4.6, 'Running shoes with boost technology', '2023-01-01', 1),
('Zara Cotton Shirt', 'Clothing', 'Shirts', 'Zara', 2999.00, 1800.00, 120, 4.2, 'Premium cotton formal shirt', '2023-01-01', 1),
('The Alchemist', 'Books', 'Fiction', 'HarperCollins', 399.00, 250.00, 500, 4.8, 'International bestseller by Paulo Coelho', '2023-01-01', 1),
('Atomic Habits', 'Books', 'Self-Help', 'Random House', 599.00, 350.00, 300, 4.9, 'Life-changing habits book by James Clear', '2023-01-01', 1),
('Rich Dad Poor Dad', 'Books', 'Finance', 'Plata Publishing', 499.00, 300.00, 250, 4.7, 'Personal finance classic', '2023-01-01', 1),
('Instant Pot Duo 7-in-1', 'Home & Kitchen', 'Appliances', 'Instant Pot', 8999.00, 6500.00, 40, 4.5, 'Multi-use pressure cooker', '2023-01-01', 1),
('Philips Air Fryer', 'Home & Kitchen', 'Appliances', 'Philips', 12999.00, 9500.00, 35, 4.6, 'Healthy cooking air fryer', '2023-01-01', 1),
('IKEA Study Table', 'Home & Kitchen', 'Furniture', 'IKEA', 4999.00, 3500.00, 25, 4.3, 'Modern wooden study table', '2023-01-01', 1),
('Whey Protein Powder', 'Health & Fitness', 'Supplements', 'Optimum Nutrition', 4999.00, 3500.00, 100, 4.7, '5lb whey protein isolate', '2023-01-01', 1),
('Yoga Mat Premium', 'Health & Fitness', 'Equipment', 'Reebok', 2499.00, 1500.00, 80, 4.4, 'Non-slip premium yoga mat', '2023-01-01', 1),
('Dumbbells Set 20kg', 'Health & Fitness', 'Equipment', 'Kore', 3999.00, 2800.00, 50, 4.5, 'Adjustable dumbbells set', '2023-01-01', 1),
('Lakme Foundation', 'Beauty & Personal Care', 'Makeup', 'Lakme', 899.00, 600.00, 200, 4.2, 'Long-lasting liquid foundation', '2023-01-01', 1),
('Himalaya Face Wash', 'Beauty & Personal Care', 'Skincare', 'Himalaya', 199.00, 120.00, 300, 4.3, 'Neem and turmeric face wash', '2023-01-01', 1),
('LOreal Shampoo', 'Beauty & Personal Care', 'Haircare', 'LOreal', 699.00, 450.00, 150, 4.4, 'Professional hair care shampoo', '2023-01-01', 1),
('Hot Wheels Car Set', 'Toys & Games', 'Toy Cars', 'Hot Wheels', 1999.00, 1200.00, 100, 4.5, '20-pack die-cast cars', '2023-01-01', 1),
('LEGO Creator Set', 'Toys & Games', 'Building Sets', 'LEGO', 5999.00, 4200.00, 30, 4.8, '3-in-1 creator building set', '2023-01-01', 1),
('Monopoly Board Game', 'Toys & Games', 'Board Games', 'Hasbro', 1299.00, 800.00, 75, 4.6, 'Classic family board game', '2023-01-01', 1),
('Samsung 55" 4K TV', 'Electronics', 'TVs', 'Samsung', 54999.00, 42000.00, 20, 4.5, '55-inch 4K Smart TV', '2023-01-01', 1),
('LG Washing Machine', 'Home & Kitchen', 'Appliances', 'LG', 34999.00, 28000.00, 15, 4.4, '7kg front load washing machine', '2023-01-01', 1),
('Godrej Refrigerator', 'Home & Kitchen', 'Appliances', 'Godrej', 24999.00, 20000.00, 12, 4.3, '265L double door refrigerator', '2023-01-01', 1),
('OnePlus 11 5G', 'Electronics', 'Smartphones', 'OnePlus', 56999.00, 45000.00, 65, 4.6, 'Flagship 5G smartphone', '2023-01-01', 1),
('Boat Smartwatch', 'Electronics', 'Wearables', 'Boat', 2999.00, 1800.00, 120, 4.2, 'Fitness tracking smartwatch', '2023-01-01', 1);

-- Insert Orders (35 orders with various statuses and dates)
INSERT INTO orders (customer_id, order_date, order_status, shipping_address, total_amount_inr, discount_amount_inr, shipping_fee_inr, payment_method, payment_status) VALUES
(1, '2023-06-15 10:30:00', 'delivered', 'Mumbai, Maharashtra', 139899.00, 5000.00, 99.00, 'credit_card', 'completed'),
(2, '2023-06-16 14:20:00', 'delivered', 'Delhi, Delhi', 84999.00, 1000.00, 150.00, 'upi', 'completed'),
(3, '2023-06-18 09:15:00', 'delivered', 'Bangalore, Karnataka', 29990.00, 0.00, 99.00, 'debit_card', 'completed'),
(4, '2023-06-20 16:45:00', 'shipped', 'Ahmedabad, Gujarat', 12998.00, 500.00, 99.00, 'cod', 'pending'),
(5, '2023-06-22 11:30:00', 'delivered', 'Pune, Maharashtra', 114900.00, 2000.00, 0.00, 'credit_card', 'completed'),
(6, '2023-06-25 13:40:00', 'delivered', 'Chennai, Tamil Nadu', 8999.00, 0.00, 99.00, 'upi', 'completed'),
(7, '2023-06-28 10:20:00', 'processing', 'Hyderabad, Telangana', 24900.00, 0.00, 99.00, 'wallet', 'completed'),
(8, '2023-07-02 15:15:00', 'delivered', 'Bangalore, Karnataka', 89990.00, 1500.00, 150.00, 'credit_card', 'completed'),
(9, '2023-07-05 12:30:00', 'delivered', 'Lucknow, Uttar Pradesh', 3999.00, 200.00, 50.00, 'cod', 'completed'),
(10, '2023-07-08 14:45:00', 'shipped', 'Jaipur, Rajasthan', 7999.00, 0.00, 99.00, 'upi', 'completed'),
(11, '2023-07-12 09:20:00', 'delivered', 'Kochi, Kerala', 15999.00, 1000.00, 99.00, 'debit_card', 'completed'),
(12, '2023-07-15 16:30:00', 'delivered', 'Kolkata, West Bengal', 1497.00, 100.00, 50.00, 'cod', 'completed'),
(13, '2023-07-18 11:40:00', 'delivered', 'Chennai, Tamil Nadu', 12999.00, 0.00, 99.00, 'credit_card', 'completed'),
(14, '2023-07-22 13:25:00', 'cancelled', 'Mumbai, Maharashtra', 4999.00, 0.00, 99.00, 'wallet', 'refunded'),
(15, '2023-07-25 10:15:00', 'delivered', 'Delhi, Delhi', 4999.00, 500.00, 50.00, 'upi', 'completed'),
(16, '2023-07-28 15:50:00', 'shipped', 'Surat, Gujarat', 2499.00, 0.00, 50.00, 'cod', 'pending'),
(17, '2023-08-02 12:35:00', 'delivered', 'Indore, Madhya Pradesh', 3999.00, 200.00, 50.00, 'debit_card', 'completed'),
(18, '2023-08-05 14:20:00', 'processing', 'Kanpur, Uttar Pradesh', 1098.00, 50.00, 50.00, 'upi', 'completed'),
(19, '2023-08-08 09:45:00', 'delivered', 'Bhopal, Madhya Pradesh', 699.00, 0.00, 50.00, 'cod', 'completed'),
(20, '2023-08-12 16:10:00', 'delivered', 'Pune, Maharashtra', 5999.00, 300.00, 99.00, 'credit_card', 'completed'),
(21, '2023-08-15 11:25:00', 'shipped', 'Varanasi, Uttar Pradesh', 1299.00, 0.00, 50.00, 'wallet', 'completed'),
(22, '2023-08-18 13:55:00', 'delivered', 'Gurgaon, Haryana', 54999.00, 2000.00, 200.00, 'credit_card', 'completed'),
(23, '2023-08-22 10:40:00', 'delivered', 'Rajkot, Gujarat', 34999.00, 1500.00, 150.00, 'debit_card', 'completed'),
(24, '2023-08-25 15:30:00', 'processing', 'Chandigarh, Punjab', 24999.00, 1000.00, 99.00, 'upi', 'completed'),
(25, '2023-08-28 12:20:00', 'delivered', 'Nashik, Maharashtra', 56999.00, 2500.00, 150.00, 'credit_card', 'completed'),
(1, '2023-09-02 14:15:00', 'shipped', 'Mumbai, Maharashtra', 2999.00, 0.00, 50.00, 'upi', 'completed'),
(3, '2023-09-05 09:30:00', 'delivered', 'Bangalore, Karnataka', 7999.00, 400.00, 50.00, 'wallet', 'completed'),
(5, '2023-09-08 16:25:00', 'delivered', 'Pune, Maharashtra', 15999.00, 800.00, 99.00, 'credit_card', 'completed'),
(7, '2023-09-12 11:45:00', 'processing', 'Hyderabad, Telangana', 899.00, 0.00, 50.00, 'cod', 'pending'),
(10, '2023-09-15 13:20:00', 'delivered', 'Jaipur, Rajasthan', 1697.00, 100.00, 50.00, 'upi', 'completed'),
(2, '2023-09-18 10:35:00', 'shipped', 'Delhi, Delhi', 1999.00, 0.00, 50.00, 'debit_card', 'completed'),
(4, '2023-09-22 15:40:00', 'delivered', 'Ahmedabad, Gujarat', 5999.00, 300.00, 99.00, 'credit_card', 'completed'),
(6, '2023-09-25 12:50:00', 'delivered', 'Chennai, Tamil Nadu', 24900.00, 1000.00, 99.00, 'wallet', 'completed'),
(8, '2023-09-28 14:05:00', 'pending', 'Bangalore, Karnataka', 29990.00, 1500.00, 99.00, 'credit_card', 'pending'),
(12, '2023-10-02 09:25:00', 'delivered', 'Kolkata, West Bengal', 134900.00, 5000.00, 200.00, 'credit_card', 'completed');

-- Insert Order Items (matching the orders above)
INSERT INTO order_items (order_id, product_id, quantity, unit_price_inr, total_price_inr) VALUES
-- Order 1: iPhone 15 Pro
(1, 1, 1, 134900.00, 134900.00),
-- Order 2: Samsung Galaxy S24
(2, 2, 1, 79999.00, 79999.00),
(2, 21, 1, 199.00, 199.00),
(2, 22, 1, 699.00, 699.00),
(2, 30, 1, 2999.00, 2999.00),
-- Order 3: Sony Headphones
(3, 5, 1, 29990.00, 29990.00),
-- Order 4: Jeans and Shoes
(4, 7, 2, 3999.00, 7998.00),
(4, 8, 1, 7999.00, 7999.00),
-- Order 5: MacBook Air M2
(5, 3, 1, 114900.00, 114900.00),
-- Order 6: Instant Pot
(6, 14, 1, 8999.00, 8999.00),
-- Order 7: AirPods Pro
(7, 6, 1, 24900.00, 24900.00),
-- Order 8: Dell XPS 13
(8, 4, 1, 89990.00, 89990.00),
-- Order 9: Levi's Jeans
(9, 7, 1, 3999.00, 3999.00),
-- Order 10: Nike Air Force 1
(10, 8, 1, 7999.00, 7999.00),
-- Order 11: Adidas Ultraboost
(11, 9, 1, 15999.00, 15999.00),
-- Order 12: Books bundle
(12, 11, 1, 399.00, 399.00),
(12, 12, 1, 599.00, 599.00),
(12, 13, 1, 499.00, 499.00),
-- Order 13: Philips Air Fryer
(13, 15, 1, 12999.00, 12999.00),
-- Order 14: IKEA Study Table (cancelled)
(14, 16, 1, 4999.00, 4999.00),
-- Order 15: Whey Protein
(15, 17, 1, 4999.00, 4999.00),
-- Order 16: Yoga Mat
(16, 18, 1, 2499.00, 2499.00),
-- Order 17: Dumbbells
(17, 19, 1, 3999.00, 3999.00),
-- Order 18: Beauty products
(18, 20, 1, 899.00, 899.00),
(18, 21, 1, 199.00, 199.00),
-- Order 19: L'Oreal Shampoo
(19, 22, 1, 699.00, 699.00),
-- Order 20: LEGO Creator Set
(20, 24, 1, 5999.00, 5999.00),
-- Order 21: Monopoly
(21, 25, 1, 1299.00, 1299.00),
-- Order 22: Samsung TV
(22, 26, 1, 54999.00, 54999.00),
-- Order 23: LG Washing Machine
(23, 27, 1, 34999.00, 34999.00),
-- Order 24: Godrej Refrigerator
(24, 28, 1, 24999.00, 24999.00),
-- Order 25: OnePlus 11 5G
(25, 29, 1, 56999.00, 56999.00),
-- Order 26: Boat Smartwatch
(26, 30, 1, 2999.00, 2999.00),
-- Order 27: Nike shoes
(27, 8, 1, 7999.00, 7999.00),
-- Order 28: Adidas shoes
(28, 9, 1, 15999.00, 15999.00),
-- Order 29: Lakme Foundation
(29, 20, 1, 899.00, 899.00),
-- Order 30: Beauty bundle
(30, 21, 2, 199.00, 398.00),
(30, 22, 2, 699.00, 1398.00),
-- Order 31: Hot Wheels
(31, 23, 1, 1999.00, 1999.00),
-- Order 32: LEGO Creator
(32, 24, 1, 5999.00, 5999.00),
-- Order 33: AirPods Pro
(33, 6, 1, 24900.00, 24900.00),
-- Order 34: Sony Headphones
(34, 5, 1, 29990.00, 29990.00),
-- Order 35: iPhone 15 Pro
(35, 1, 1, 134900.00, 134900.00); 