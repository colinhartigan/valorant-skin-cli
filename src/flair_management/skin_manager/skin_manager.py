class Skin_Manager:

    @staticmethod
    def fetch_weapon_data(weapon_uuid,weapons_data):
        for i in weapons_data:
            if i['uuid'] == weapon_uuid:
                return i

    @staticmethod
    def fetch_skin_data(skin_uuid,skin_datas):
        for i in skin_datas:
            if i['uuid'] == skin_uuid:
                return i

    @staticmethod
    def modify_skin(client,weapon_uuid,skin_uuid,level_uuid,chroma_uuid):
        loadout = client.fetch_player_loadout()
        
        for weapon in loadout['Guns']:
            if weapon['ID'] == weapon_uuid:
                weapon['SkinID'] = skin_uuid 
                weapon['SkinLevelID'] = level_uuid 
                weapon['ChromaID'] = chroma_uuid     
                
        client.put_player_loadout(loadout=loadout)
        