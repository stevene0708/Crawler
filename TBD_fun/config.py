import configparser

CONFIG_FILE = "header.cfg"

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
cookie_1 = "X"
cookie_2 = "CC"
cookie_3 = "ZZ"

if __name__ == "__main__":
    conf = configparser.ConfigParser()
    
    cfgfile = open(CONFIG_FILE,'w')

    conf.add_section("HEADERS")
    conf.set("HEADERS", "User-Agent", "\"" + user_agent + "\"")
    
    conf.add_section("COOKIES")
    conf.set("COOKIES", "cf_chl_2", "\"" + cookie_1 + "\"")
    conf.set("COOKIES", "cf_clearance", "\"" + cookie_2 + "\"")
    conf.set("COOKIES", "csrftoken", "\"" + cookie_3 + "\"")
    
    
    conf.write(cfgfile)
    
    cfgfile.close()