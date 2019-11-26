from Configure import Configure as conf

class Materials(object):

    # material_id - material_name
    list = None

    def get_list():
        if Materials.list == None:
            mls = conf.get('facilities').values()
            result = []
            for ml in mls:
                result.extend(ml)

            Materials.list = list(set(result))
            Materials.list.sort()
            
            Materials.list.insert(0,'none')
        return Materials.list

    def get_name(id):
        return Materials.get_list()[id]

    def get_id(name):
        return Materials.get_list().index(name)