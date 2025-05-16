from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST : str = 'localhost'
    DB_PORT : int = 5432
    DB_USER : str = 'postgres'
    DB_PASS : str = 'qwerty'
    DB_NAME : str = 'jira_like'

    @property
    def DATABASE_URL_psycopg(self):
        return f'postgresql+psycopg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    #model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
