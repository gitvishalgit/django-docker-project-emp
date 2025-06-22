```
docker compose exec db mysql -u root -p
```
# password root
```
USE mydb;
```
# create table 
```
CREATE TABLE register (
    id INT AUTO_INCREMENT PRIMARY KEY,
    First_Name VARCHAR(100),
    Last_Name VARCHAR(100),
    gender VARCHAR(10),
    emailid VARCHAR(100) UNIQUE,
    password VARCHAR(255)
);
```
```
CREATE TABLE Employee (
    id INT AUTO_INCREMENT PRIMARY KEY,
    First_Name VARCHAR(100),
    Last_Name VARCHAR(100),
    gender VARCHAR(10),
    emailid VARCHAR(100),
    password VARCHAR(100),
    DOB DATE,
    department VARCHAR(100),
    position VARCHAR(100),
    useremail VARCHAR(100)
);

```
```
exit
```
