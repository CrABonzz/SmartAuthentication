# Password
DEFAULT_SALT_SIZE = 32
HASH_ITERATIONS_AMOUNT = 100000
HASH_RESULT_SIZE = 64

DISTANCE_GRANUALITY = 45

ADMIN_MAIL = "smart.authentication.project@gmail.com"
ADMIN_PASSWORD = "Ss112233"

MAX_FAILED_LOGIN_ATTEMPTS = 7

# Password regexs
DIGIT_REGEX = r"\d", "Password should contain at least 1 digit.\n"
UPPERCASE_REGEX = r"[A-Z]", "Password should contain at least 1 uppercase.\n"
LOWERCASE_REGEX = r"[a-z]", "Password should contain at least 1 lowercase.\n"
SYMBOL_REGEX = r"[ !#$%&'()*+,-./[\\\]^_`{|}~" + r'"]', "Password should contain at least 1 symbol.\n"

AUTH_METHODS = ["text", "grid", "pixels", "lines"]

GRID_PHOTOS = {
    0: "penguin.png",
    1: "delicious.png",
    2: "digg.png",
    3: "furl.png",
    4: "flickr.png",
    5: "reddit.png",
    6: "rss.png",
    7: "stumbleupon.png",
    8: "yahoo.png",
    9: "youtube.png",
    10: "technorati.png",
    11: "fish.png",
}
