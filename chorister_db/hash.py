from werkzeug.security import check_password_hash, generate_password_hash

print (generate_password_hash("password"))

print(check_password_hash("scrypt:32768:8:1$xY1XQv5FiEHeLpF2$6d1d354dbad5e88e5761bdd4bed7a2348c511f3d2df65da04a3cf8ba28dcf2bd1e9894ec307c10fbee5e6e7ca28768a815eeb0729e9ea2c8c5a4e61bde05c7fe", "password"))