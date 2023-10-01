from envparse import Env

env = Env()


SECRET_KEY = env.str("SECRET_KEY", default='secret_key')
ALGORITHM = env.str("ALGORITHM", default='HS256')
DATABASE_URL = env.str("REAL_DB_URL", default='postgresql+asyncpg://postgres:Weekend4532@localhost:5432/trms2')