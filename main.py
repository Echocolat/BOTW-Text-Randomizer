import oead
from bcml import util
from pymsyt import Msbt
import json
import os
import random

RULES = str('[Definition]\n' + 
'titleIds = 00050000101C9300,00050000101C9400,00050000101C9500\n' +
'name = Text randomizer\n' + 
'path = The Legend of Zelda: Breath of the Wild/Mods/Text randomizer\n' +
'description = Randomizes all the text you can found in the game. Provides a fun experience (I guess??). Has options (you can either randomize all of the texts together, or only type by type, like all of the actors stay actor names, just randomized INSIDE actor names).\n' +
'version = 7')

CONFIG = json.loads(open('config.json').read())

def get_names_and_randomize():

    text_list = {
        'actor_name': [],
        'actor_desc': [],
        'actor_picturename': [],
        'demo_text': [],
        'eventflow_text': [],
        'layout_text': [],
        'quest_name': [],
        'quest_step': [],
        'shout_text': [],
        'static_text': [],
        'tips_name': [],
        'tips_text': []
        }

    if not CONFIG['use_mod_file']:
        pack_data = util.get_game_file('Pack\\' + CONFIG['name_of_pack'], aoc = False).read_bytes()
    else:
        pack_data = open(CONFIG['file_path_only_for_mod_file'], 'rb').read()
    sarc = oead.Sarc(pack_data)
    sarc_writer = oead.SarcWriter(endian = oead.Endianness.Big)
    little_file = sarc.get_file(0)
    little_sarc = oead.Sarc(oead.yaz0.decompress(little_file.data))
    little_sarc_writer = oead.SarcWriter(endian = oead.Endianness.Big)
    for txtfile in little_sarc.get_files():
        if 'ActorType' in txtfile.name:
            txtdata = Msbt.from_binary(bytes(txtfile.data))
            txtdict = txtdata.to_dict()
            for entry in txtdict['entries']:
                if entry.endswith('_Name'):
                    for text in txtdict['entries'][entry]['contents']:
                        if 'text' in text:
                            text_list['actor_name'].append(text['text'])
                elif entry.endswith('_Desc'):
                    for text in txtdict['entries'][entry]['contents']:
                        if 'text' in text:
                            text_list['actor_desc'].append(text['text'])
                elif entry.endswith('_PictureBook'):
                    for text in txtdict['entries'][entry]['contents']:
                        if 'text' in text:
                            text_list['actor_picturename'].append(text['text'])
        elif 'DemoMsg' in txtfile.name:
            txtdata = Msbt.from_binary(bytes(txtfile.data))
            txtdict = txtdata.to_dict()
            for entry in txtdict['entries']:
                for text in txtdict['entries'][entry]['contents']:
                    if 'text' in text:
                        text_list['demo_text'].append(text['text'])
        elif 'EventFlowMsg' in txtfile.name:
            txtdata = Msbt.from_binary(bytes(txtfile.data))
            txtdict = txtdata.to_dict()
            for entry in txtdict['entries']:
                for text in txtdict['entries'][entry]['contents']:
                    if 'text' in text:
                        text_list['eventflow_text'].append(text['text'])
        elif 'LayoutMsg' in txtfile.name:
            txtdata = Msbt.from_binary(bytes(txtfile.data))
            txtdict = txtdata.to_dict()
            for entry in txtdict['entries']:
                for text in txtdict['entries'][entry]['contents']:
                    if 'text' in text:
                        text_list['layout_text'].append(text['text'])
        elif 'QuestMsg' in txtfile.name:
            txtdata = Msbt.from_binary(bytes(txtfile.data))
            txtdict = txtdata.to_dict()
            for entry in txtdict['entries']:
                if entry.endswith('_Name'):
                    for text in txtdict['entries'][entry]['contents']:
                        if 'text' in text:
                            text_list['quest_name'].append(text['text'])
                else:
                    for text in txtdict['entries'][entry]['contents']:
                        if 'text' in text:
                            text_list['quest_step'].append(text['text'])
        elif 'ShoutMsg' in txtfile.name:
            txtdata = Msbt.from_binary(bytes(txtfile.data))
            txtdict = txtdata.to_dict()
            for entry in txtdict['entries']:
                for text in txtdict['entries'][entry]['contents']:
                    if 'text' in text:
                        text_list['shout_text'].append(text['text'])
        elif 'StaticMsg' in txtfile.name:
            txtdata = Msbt.from_binary(bytes(txtfile.data))
            txtdict = txtdata.to_dict()
            for entry in txtdict['entries']:
                for text in txtdict['entries'][entry]['contents']:
                    if 'text' in text:
                        text_list['static_text'].append(text['text'])
        else:
            txtdata = Msbt.from_binary(bytes(txtfile.data))
            txtdict = txtdata.to_dict()
            for entry in txtdict['entries']:
                i = 0
                for text in txtdict['entries'][entry]['contents']:
                    if 'text' in text and i == 0:
                        text_list['tips_name'].append(text['text'])
                        i = 1
                    elif 'text' in text:
                        text_list['tips_text'].append(text['text'])

    if not CONFIG['randomize_all']:
        for key in text_list:
            random.shuffle(text_list[key])
    else:
        all_text = text_list['actor_name'] + text_list['actor_desc'] + text_list['actor_picturename'] + text_list['demo_text'] + text_list['eventflow_text'] + text_list['layout_text'] + text_list['quest_name'] + text_list['quest_step'] + text_list['shout_text'] + text_list['static_text'] + text_list['tips_name'] + text_list['tips_text']
        random.shuffle(all_text)

    for txtfile in little_sarc.get_files():
        if not CONFIG['randomize_all']:
            if 'ActorType' in txtfile.name and CONFIG['randomize_actor_text']:
                txtdata = Msbt.from_binary(bytes(txtfile.data))
                txtdict = txtdata.to_dict()
                for entry in txtdict['entries']:
                    if entry.endswith('_Name'):
                        for text in txtdict['entries'][entry]['contents']:
                            if 'text' in text:
                                text['text'] = text_list['actor_name'].pop()
                    elif entry.endswith('_Desc'):
                        for text in txtdict['entries'][entry]['contents']:
                            if 'text' in text:
                                text['text'] = text_list['actor_desc'].pop()
                    elif entry.endswith('_PictureBook'):
                        for text in txtdict['entries'][entry]['contents']:
                            if 'text' in text:
                                text['text'] = text_list['actor_picturename'].pop()
            elif 'DemoMsg' in txtfile.name and CONFIG['randomize_demo_text']:
                txtdata = Msbt.from_binary(bytes(txtfile.data))
                txtdict = txtdata.to_dict()
                for entry in txtdict['entries']:
                    for text in txtdict['entries'][entry]['contents']:
                        if 'text' in text:
                            text['text'] = text_list['demo_text'].pop()
            elif 'EventFlowMsg' in txtfile.name and CONFIG['randomize_event_text']:
                txtdata = Msbt.from_binary(bytes(txtfile.data))
                txtdict = txtdata.to_dict()
                for entry in txtdict['entries']:
                    for text in txtdict['entries'][entry]['contents']:
                        if 'text' in text:
                            text['text'] = text_list['eventflow_text'].pop()
            elif 'LayoutMsg' in txtfile.name and CONFIG['randomize_layout_text']:
                txtdata = Msbt.from_binary(bytes(txtfile.data))
                txtdict = txtdata.to_dict()
                for entry in txtdict['entries']:
                    for text in txtdict['entries'][entry]['contents']:
                        if 'text' in text:
                            text['text'] = text_list['layout_text'].pop()
            elif 'QuestMsg' in txtfile.name and CONFIG['randomize_quest_text']:
                txtdata = Msbt.from_binary(bytes(txtfile.data))
                txtdict = txtdata.to_dict()
                for entry in txtdict['entries']:
                    if entry.endswith('_Name'):
                        for text in txtdict['entries'][entry]['contents']:
                            if 'text' in text:
                                text['text'] = text_list['quest_name'].pop()
                    else:
                        for text in txtdict['entries'][entry]['contents']:
                            if 'text' in text:
                                text['text'] = text_list['quest_step'].pop()
            elif 'ShoutMsg' in txtfile.name and CONFIG['randomize_shout_text']:
                txtdata = Msbt.from_binary(bytes(txtfile.data))
                txtdict = txtdata.to_dict()
                for entry in txtdict['entries']:
                    for text in txtdict['entries'][entry]['contents']:
                        if 'text' in text:
                            text['text'] = text_list['shout_text'].pop()
            elif 'StaticMsg' in txtfile.name and CONFIG['randomize_static_text']:
                txtdata = Msbt.from_binary(bytes(txtfile.data))
                txtdict = txtdata.to_dict()
                for entry in txtdict['entries']:
                    for text in txtdict['entries'][entry]['contents']:
                        if 'text' in text:
                            text['text'] = text_list['static_text'].pop()
            elif CONFIG['randomize_tips_text']:
                txtdata = Msbt.from_binary(bytes(txtfile.data))
                txtdict = txtdata.to_dict()
                for entry in txtdict['entries']:
                    i = 0
                    for text in txtdict['entries'][entry]['contents']:
                        if 'text' in text and i == 0:
                            text['text'] = text_list['tips_name'].pop()
                            i = 1
                        elif 'text' in text:
                            text['text'] = text_list['tips_text'].pop()
        else:
            txtdata = Msbt.from_binary(bytes(txtfile.data))
            txtdict = txtdata.to_dict()
            for entry in txtdict['entries']:
                for text in txtdict['entries'][entry]['contents']:
                    if 'text' in text:
                        try:text['text'] = all_text.pop()
                        except:None

        little_sarc_writer.files[txtfile.name] = Msbt.from_dict(txtdict).to_binary(big_endian=True)
    _, little_sarc_bytes = little_sarc_writer.write()
    sarc_writer.files[little_file.name] = oead.yaz0.compress(little_sarc_bytes, True)
    _, sarc_bytes = sarc_writer.write()

    return sarc_bytes

def create_mod_structure():
    folder = os.path.join('Text randomizer\\content\\Pack')
    os.makedirs(folder, exist_ok=True)
    with open('Text randomizer\\rules.txt', 'w') as file:
        file.write(RULES)

def create_mod():
    create_mod_structure()
    bootup_data = get_names_and_randomize()
    with open('Text randomizer\\content\\Pack\\' + CONFIG['name_of_pack'], 'wb') as file:
        file.write(bootup_data)
    input('Press enter to exit...')

if __name__ == '__main__':
    create_mod()