class user(object):
    def __init__(self,id,name):
        self.__id = id
        self.__nickname = name

    def set_age(self,age):
        self.__age = age
    def get_age(self):
        if hasattr(self,'__age'):
            return self.__age
        else:
            return "<null>"

    def set_name(self,name):
        self.__nickname = name
    def get_name(self):
        return self.__nickname

    def set_intro(self,intro):
        self.__intro = intro
    def get_intro(self):
        if hasattr(self,'__intro'):
            return self.__intro
        else:
            return "<null>"

    def get_id(self):
        return self.__id
    def set_id(self,id):
        self.__id = id

    def set_head(self,headaddr):
        self.__head = headaddr
    def get_head(self):
        if hasattr(self, '__head'):
            return self.__head
        else:
            return None
