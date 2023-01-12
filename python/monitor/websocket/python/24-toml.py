import tomli
import pprint

# test with https://www.toml-lint.com/

sheet_ident = 'sheetGlobal'

with open('config.toml', 'rb') as file_obj:
  config_root  = tomli.load(file_obj)
  env          = config_root['environment']
  config_env   = config_root[env]
  config_sheet = config_env[sheet_ident]

  pprint.pprint(config_sheet)
