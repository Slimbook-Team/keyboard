var language_resourcen = JSON.parse(window.language_data);

function get_language_string(language, stringname)
{
    if(language_resourcen[language][stringname] == "" 
        || language_resourcen[language][stringname] == "undefinded"
        || language_resourcen[language][stringname] == undefined)
    {
        if(language_resourcen["default"][stringname] == "" 
        || language_resourcen["default"][stringname] == "undefinded"
        || language_resourcen["default"][stringname] == undefined)
        {
            return "<string not found>";
        }
        
        return language_resourcen["default"][stringname];
    }
    
    return language_resourcen[language][stringname];
}
