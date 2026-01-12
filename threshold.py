import requests

def init(args):
    if len(args) != 2:
        return "error"
    txid: str = args[1]
    if len(txid) != 64:
        return "tx len error"
    return get_destination_addresses(txid)

def get_destination_addresses(txid: str):
    mempool_tx_endpoint = 'https://mempool.space/api/tx/'
    url = f'{mempool_tx_endpoint}{txid}'
    response = requests.get(url) 

    if response.status_code > 200:
        return f"HTTP ERROR : {response.status_code}"
    data = response.json()

    witness_data: list =[{}]
    for vin in data['vin']:
        witness_bytes: list = []
        pushbytes_32: list = []
        if 'witness' in vin:
            if len(vin['witness']) == 3:
                b_data = bytes.fromhex(vin['witness'][2])
                for idx, b in enumerate(b_data):
                    witness_bytes.append(f'{hex(b)[2:]:02}')
                    if hex(b)[2:] == '20':
                        d32: str = b_data[idx+1:idx+1+32].hex()
                        if d32 != '':
                            pushbytes_32.append(d32)
        spk_address = vin['prevout']['scriptpubkey_address']
        if len(pushbytes_32) > 0:
            witness_data.append({"scriptpubkey_address": spk_address, "witness_bytes": witness_bytes, "pushbytes_32": pushbytes_32})
        else:
            witness_data.append({"scriptpubkey_address": spk_address, "witness_bytes": witness_bytes})
    for d in witness_data:
        if 'pushbytes_32' in d:
            poss_addr: str = d['pushbytes_32'][0]
            if poss_addr[0] == '0':
                print(f'threshold_deposit: {d['scriptpubkey_address']}\ndestination_address: 0x{poss_addr[-40:]}\n')
            elif poss_addr[-1] == '0':
                print(f'threshold_deposit: {d['scriptpubkey_address']}\ndestination_address: 0x{poss_addr[:40]}\n')
            else:
                continue
    return "SUCCESS -> EXITING..."