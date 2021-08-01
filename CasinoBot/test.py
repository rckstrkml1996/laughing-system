from config import settings

print("allgood")
assert settings.key == "value"
settings.pipirka = "pipirka"
print(settings.key)
