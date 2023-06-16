# -*- coding: utf-8 -*-

import json
import sys
import logging

class ConvertMjai():

    hand_dic = {
        '1z': 'E',
        '2z': 'S',
        '3z': 'W',
        '4z': 'N',
        '5z': 'P',
        '6z': 'F',
        '7z': 'C',
        '0m': '5mr',
        '0p': '5pr',
        '0s': '5sr',
        '' : '?',
    }

    action_dic = {
        'ActionNewRound': 'start_kyoku',
        'ActionDealTile': 'tsumo',
        'ActionDiscardTile': 'dahai',
        'ActionHule': 'hora',
        'ActionLiuJu':'ryukyoku',
        'ActionChiPengGang': 'a',
    }

    _mahjongsoul_json = {}

    _mjai_json = {}

    _player_number = 0

    _account_id = ''

    def __init__(self):
        pass

    def convert_to_mjai(self, data):
        #ConvertMjai._mahjongsoul_json = data
        ConvertMjai._mahjongsoul_json = eval(data)
        ConvertMjai._get_account_id(self)
        ConvertMjai._get_player_number(self)

        ConvertMjai._mjai_json = {}


        ConvertMjai._replace_action(self)
        ConvertMjai._replace_actor(self)
        ConvertMjai._replace_tile_noprama(self)
        ConvertMjai._replace_tsumogiri(self)

        #ConvertMjai._mjai_json = sorted(ConvertMjai._mjai_json.items())
        #logging.info('_mjai_json:'+str(ConvertMjai._mjai_json))
        json_data = json.dumps(ConvertMjai._mjai_json)

        return json_data


    def _get_account_id(self):
        if 'account_id' in ConvertMjai._mahjongsoul_json:
            ConvertMjai._account_id = ConvertMjai._mahjongsoul_json['account_id']
            print('account_id:', ConvertMjai._account_id)
        else:
            pass
        return None

    def _get_player_number(self):
        if 'ready_id_list' in ConvertMjai._mahjongsoul_json:
            for i in range(0,len(ConvertMjai._mahjongsoul_json['ready_id_list'])):
                if ConvertMjai._mahjongsoul_json['ready_id_list'][i] == ConvertMjai._account_id:
                    ConvertMjai._player_number = i
                    print(ConvertMjai._player_number)
                    return None

    def _replace_tile_noprama(self):
        if 'tiles' not in ConvertMjai._mahjongsoul_json:
            if 'tile' not in ConvertMjai._mahjongsoul_json:
                pass
            else:
                mjai_tile= ConvertMjai._mahjongsoul_json['tile']
                ConvertMjai._mjai_json['pai'] = ConvertMjai._replace_tile(self, mjai_tile)
        else:
            mjai_list = ConvertMjai._mahjongsoul_json['tiles']
            logging.info(mjai_list)
            i = 0
            for tile in mjai_list:
                logging.info(tile)
                ConvertMjai._mahjongsoul_json['tiles'][i] = ConvertMjai._replace_tile(self, tile)
                i = i+1
        return None

    def _replace_tile(self, tile):
        try:
            tile = ConvertMjai.hand_dic[tile]
        except KeyError:
            pass
        return tile

    def _replace_action(self):
        if 'action' not in ConvertMjai._mahjongsoul_json:
            pass
        else:
            match ConvertMjai._mahjongsoul_json['action']:
                case 'ActionNewRound':
                    ConvertMjai._mjai_json['type'] = 'start_kyoku'
                    ConvertMjai._mjai_json['bakaze'] = '' #风向
                    ConvertMjai._mjai_json['dora_marker'] = ConvertMjai._mahjongsoul_json['doras'][0] #宝牌
                    ConvertMjai._mjai_json['kyoku'] = '' #局数
                    ConvertMjai._mjai_json['honba'] = '' #本场
                    ConvertMjai._mjai_json['kyotaku'] = '' #余下的点棒
                    ConvertMjai._mjai_json['oya'] = '' #庄家
                    ConvertMjai._mjai_json['scores'] = ConvertMjai._mahjongsoul_json['scores'] #分数
                    ConvertMjai._mjai_json['tehais'] = [0,0,0,0]
                    #对局开始时每人手牌统计
                    for i in range(0, 4):
                        if i == ConvertMjai._player_number:
                            ConvertMjai._mjai_json['tehais'][i] = ConvertMjai._mahjongsoul_json['tiles']
                        else:
                            ConvertMjai._mjai_json['tehais'][i] = ['?', '?', '?', '?', '?', '?', '?', '?', '?', '?', '?',
                                                                   '?', '?']
                case 'ActionDealTile':
                    ConvertMjai._mjai_json['type'] = 'tsumo'
                case 'ActionDiscardTile':
                    ConvertMjai._mjai_json['type'] = 'dahai'
                case 'ActionHule':
                    ConvertMjai._mjai_json['type'] = 'hora'
                case 'ActionLiuJu':
                    ConvertMjai._mjai_json['type'] = 'ryukyoku'
                case 'ActionChiPengGang':
                    ConvertMjai._mjai_json['type'] = 'chi'
                    ConvertMjai._replace_actor(self)
                    ConvertMjai._mjai_json['target'] = ConvertMjai._mahjongsoul_json['froms'][2]
                    ConvertMjai._mjai_json['pai'] = ConvertMjai._replace_tile(self,ConvertMjai._mahjongsoul_json['tiles'][2])
                    ConvertMjai._mjai_json['consumed'] = [ConvertMjai._replace_tile(self,ConvertMjai._mahjongsoul_json['tiles'][0]),
                                                          ConvertMjai._replace_tile(self,ConvertMjai._mahjongsoul_json['tiles'][1])]
                    if ConvertMjai._mjai_json['pai'] == ConvertMjai._mjai_json['consumed'][0]:
                        ConvertMjai._mjai_json['type'] = 'pon'

                case _:
                    logging.error('unknown action')
                    sys.exit(1)
        return None

    def _replace_actor(self):
        if 'seat' not in ConvertMjai._mahjongsoul_json:
            pass
        else:
            ConvertMjai._mjai_json['actor'] = int(ConvertMjai._mahjongsoul_json['seat'])
        return None

    def _replace_tsumogiri(self):
        if 'moqie' not in ConvertMjai._mahjongsoul_json:
            pass
        else:
            ConvertMjai._mjai_json['tsumogiri'] = ConvertMjai._mahjongsoul_json['moqie']
        return None

if __name__ == '__main__':
    #for test
    Cm = ConvertMjai()
    while True:
        str = input()
        if str == '':
            pass
        else:
            print(Cm.convert_to_mjai(str))

