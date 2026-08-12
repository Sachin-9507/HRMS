from urllib.parse import quote_plus



encoded_password = quote_plus(getattr(Settings, 'database_password'))

from config import Settings
DATABASE_URL = (
      f"postgresql://{Settings.database_user};"
      f"{encoded_password}@"
      f"{Settings.database_host}:"
      f"{Settings.database_port}/" 
      f"{Settings.database_name}/"
   )   

print(DATABASE_URL)   