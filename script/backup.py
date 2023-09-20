def searchFiles(rootUrl):
    urlList = []
    # php备份文件
    FILE_LIST = ['index.php', 'robots.txt', 'login.php', 'profile.php', 'source.php', 'phpinfo.php', 'test.php', 'register.php', '%3f']
    for file in FILE_LIST:
        urlList.append(f'{rootUrl}/{file}')
        urlList.append(f'{rootUrl}/{file}.bak')
        urlList.append(f'{rootUrl}/{file}~')
        urlList.append(f'{rootUrl}/{file}.swp')
        urlList.append(f'{rootUrl}/.{file}.swp')
        urlList.append(f'{rootUrl}/.{file}.un~')

    # 源代码检测
    SOURCE_LIST = [
        '.svn', '.svn/wc.db', '.svn/entries', # svn
        '.git/', '.git/HEAD', '.git/index', '.git/config', '.git/description', '.gitignore' # git
        '.hg/', # hg
        'CVS/', 'CVS/Root', 'CVS/Entries', # cvs
        '.bzr', # bzr
        'WEB-INF/web.xml', 'WEB-INF/src/', 'WEB-INF/classes', 'WEB-INF/lib', 'WEB-INF/database.propertie', # java
        '.DS_Store', # macos
        'README', 'README.md', 'README.MD', # readme
        '_viminfo', '.viminfo', # vim
        '.bash_history',
        '.htaccess'
    ]
    for source in SOURCE_LIST:
        urlList.append(f'{rootUrl}/{source}')

    # 压缩文件
    suffixList = ['.rar','.zip','.tar','.tar.gz', '.7z']
    keyList = ['www','wwwroot','site','web','website','backup','data','mdb','WWW','新建文件夹','ceshi','databak',
    'db','database','sql','bf','备份','1','2','11','111','a','123','test','admin','app','bbs','htdocs','wangzhan']
    num1 = rootUrl.find('.')
    num2 = rootUrl.find('.', num1 + 1)
    keyList.append(rootUrl[num1 + 1:num2])
    for key in keyList:
        for suff in suffixList:
            urlList.append(f'{rootUrl}/{key}{suff}')
    return urlList