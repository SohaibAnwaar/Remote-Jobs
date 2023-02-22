from scrappers.shared_attr import title_keywords

def get_title(title):
    title = title.lower()
    if 'intern' not in title and 'teacher' not in title \
            and 'lecturer' not in title and 'student' not in title \
            and 'professor' not in title:
        for keyword in title_keywords:
            # print(keyword)
            if keyword in title:
                # print(keyword)
                return True
        else:
            return False
    else:
        return False