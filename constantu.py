sql_server = 'sqlserv03'  # this is virtual WSFC name, consists from sqlserv03/04
database = 'vpn_serv01' 
connection_string = (
      f"DRIVER={{SQL Server}};"
      f"SERVER={sql_server};"
      f"DATABASE={database};"
      f"Trusted_Connection=yes;"
    )
DOMAIN_CONTROLLERS = ['cd01.videoservaillance.com']
kilk_cds = len(DOMAIN_CONTROLLERS)
AD_DOMAIN = 'videoservaillance.com'          
WHERE_SEARCH_USER = 'DC=videoservaillance,DC=com'
# WHERE_SEARCH_ALL_GROUPS = 'OU=for users,OU=Global publ group,DC=videoservaillance,DC=com' наразі не використ
current_user_groups = ['prodazi', 'zakypku', 'bychalt', 'ekobezpeka', 'fin_chief', 'sklad', 'operat_vpnobs', 'admin_vpnobs'] # in AD
gener_kilk_sprob_enter = 4
sproba_enter = 0