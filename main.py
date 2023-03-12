import users
import keys

#create users
# user1 = users.User.create("Sairam", users.UserType.BASIC, "sairam")
# key = keys.Key.create(keys.KeyType.PREMIUM)
# key2 = keys.Key.create(keys.KeyType.PREMIUM)
# key3 = keys.Key.create(keys.KeyType.PREMIUM)
# user1.add_key(key)
# user1.add_key(key2)
# user1.add_key(key3)
# print(user1)
# print(f"{user1!r}")

um = users.UserManager()

km = keys.KeysManager()
km1 = keys.KeysManager()

print(km.create_key(keys.KeyType.PREMIUM))
print(um.create_user("Sairam", users.UserType.BASIC, "sairam"))

if km == km1:
    print("INFO: new km is not created")
else:
    print("Warning: new km detected!")